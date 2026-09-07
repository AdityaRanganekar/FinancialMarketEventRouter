import sys
from typing import Literal
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI

from src.entity.state_schema import AgentState
from src.config.configuration import ConfigurationManager
from src.tools.api_tools import financial_search_tool
from src.agents.core_nodes import AgentNodes
from src.exception.exception import MarketException
from src.logging.logger import logging

def create_workflow():
    """Initializes and compiles the LangGraph state machine."""
    try:
        logging.info("Initializing configuration and LLM for workflow")
        config_manager = ConfigurationManager()
        llm_config = config_manager.get_llm_config()

        llm = ChatOpenAI(
            base_url=llm_config.base_url,
            model=llm_config.model_name,
            temperature=llm_config.temperature,
            max_tokens=llm_config.max_tokens
        )
        
        tools = [financial_search_tool]
        llm_with_tools = llm.bind_tools(tools)
        nodes = AgentNodes(llm=llm, llm_with_tools=llm_with_tools)

        logging.info("Assembling StateGraph nodes and edges")

        workflow = StateGraph(AgentState)

        workflow.add_node("router", nodes.router_node)
        workflow.add_node("tool", ToolNode(tools))
        workflow.add_node("synthesize", nodes.synthesizer_node)

        workflow.add_edge(START, "router")

        def check_route(state: AgentState) -> Literal["tool", "synthesize"]:
            return "tool" if state["route_action"] == "tool" else "synthesize"

        workflow.add_conditional_edges(
            "router",
            check_route,
            {
                "tool": "tool",
                "synthesize": "synthesize"
            }
        )

        workflow.add_edge("tool", "synthesize")
        workflow.add_edge("synthesize", END)

        graph = workflow.compile()
        logging.info("Workflow graph compiled successfully")
        return graph

    except Exception as e:
        logging.error(f"Error assembling workflow: {str(e)}")
        raise MarketException(e, sys) from e