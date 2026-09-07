import sys
import yfinance as yf
from langchain_core.tools import tool
from src.entity.state_schema import SearchInput
from src.exception.exception import MarketException
from src.logging.logger import logging

@tool("financial_search", args_schema=SearchInput)
def financial_search_tool(query: str) -> str:
    """Fetches real-time financial headlines for a given stock ticker."""
    try:
        logging.info(f"Entered financial_search_tool with query: {query}")
        
        ticker = yf.Ticker(query)
        news = ticker.news
        
        if not news:
            logging.warning(f"No recent news found for query: {query}")
            return f"No recent news found for {query}."
        
        formatted_news = []
        for article in news[:3]:
            title = article.get('title') or article.get('content', {}).get('title', 'Headline Unavailable')
            publisher = article.get('publisher') or article.get('content', {}).get('provider', {}).get('displayName', 'Unknown Publisher')
            formatted_news.append(f"- {title} ({publisher})")

        result = f"Latest headlines for {query}:\n" + "\n".join(formatted_news)
        logging.info(f"Exited financial_search_tool successfully for query: {query}")
        return result

    except Exception as e:
        logging.error(f"Error occurred in financial_search_tool: {str(e)}")
        raise MarketException(e, sys) from e