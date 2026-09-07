from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field
import operator

class SearchInput(BaseModel):
    query: str = Field(description="The stock ticker symbol to search for (e.g., AAPL, MSFT).")

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    route_action: str