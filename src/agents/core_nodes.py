import sys
from langchain_core.messages import SystemMessage, HumanMessage
from src.entity.state_schema import AgentState
from src.exception.exception import MarketException
from src.logging.logger import logging

class AgentNodes:
    def __init__(self, llm, llm_with_tools):
        self.llm = llm
        self.llm_with_tools = llm_with_tools

    def router_node(self, state: AgentState) -> dict:
        """Evaluates the user query and routes to the tool or synthesizer."""
        try:
            logging.info("Executing router_node")
            response = self.llm_with_tools.invoke(state["messages"])
            action = "tool" if response.tool_calls else "synthesize"
            logging.info(f"Router decided action: {action}")
            return {"messages": [response], "route_action": action}
        except Exception as e:
            logging.error(f"Error in router_node: {str(e)}")
            raise MarketException(e, sys) from e

    def synthesizer_node(self, state: AgentState) -> dict:
        """Synthesizes the extracted tool context into a final response."""
        try:
            logging.info("Executing synthesizer_node")
            messages = state["messages"]
            user_query = messages[0].content
            
            tool_content = ""
            for msg in messages:
                if msg.type == "tool":
                    tool_content = msg.content
                    break
                    
            system_prompt = SystemMessage(
                content="You are a financial market analyst. Synthesize the provided context and news into a concise, accurate market update."
            )
            
            synthesis_messages = [
                system_prompt,
                HumanMessage(content=f"Query: {user_query}\n\nContext from Tool:\n{tool_content}")
            ]
            
            response = self.llm.invoke(synthesis_messages)
            logging.info("Synthesis complete")
            return {"messages": [response]}
        except Exception as e:
            logging.error(f"Error in synthesizer_node: {str(e)}")
            raise MarketException(e, sys) from e