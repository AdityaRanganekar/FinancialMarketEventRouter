import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage

from src.graph.workflow import create_workflow
from src.exception.exception import MarketException
from src.logging.logger import logging

from dotenv import load_dotenv
load_dotenv()

app = FastAPI(
    title="Financial Market Event Router",
    description="Agentic API routing financial queries to real-time market data and synthesis.",
    version="1.0.0"
)

try:
    graph = create_workflow()
    logging.info("Graph workflow loaded successfully into FastAPI app.")
except Exception as e:
    logging.critical(f"Failed to initialize graph workflow: {str(e)}")
    raise MarketException(e, sys) from e


class QueryRequest(BaseModel):
    query: str = Field(..., example="What is the latest news regarding NVDA?")


class QueryResponse(BaseModel):
    query: str
    response: str


@app.get("/health")
def health_check():
    """Health check endpoint to verify service availability."""
    return {"status": "healthy"}


@app.post("/analyze", response_model=QueryResponse)
def analyze_market_event(request: QueryRequest):
    """Executes the agentic state machine on the incoming query."""
    try:
        logging.info(f"Received request query: {request.query}")
        
        initial_state = {
            "messages": [HumanMessage(content=request.query)],
            "route_action": ""
        }

        final_state = graph.invoke(initial_state)
        final_message = final_state["messages"][-1].content

        logging.info("Successfully generated synthesis response.")
        return QueryResponse(query=request.query, response=final_message)

    except Exception as e:
        logging.error(f"Error during graph execution: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))