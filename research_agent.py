import logging
import asyncio
import os
from langchain.tools import TavilySearchResults
from dotenv import load_dotenv
from research_state import ResearchState

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
if not TAVILY_API_KEY:
    raise EnvironmentError("TAVILY_API_KEY is missing! Set it in your .env file.")

class ResearchAgent:
    def __init__(self):
        self.search_tool = TavilySearchResults(api_key=TAVILY_API_KEY)

    async def search_web(self, state: ResearchState) -> ResearchState:
        logging.info(f"Searching web for: {state.query}")
        try:
            results = await asyncio.to_thread(self.search_tool.run, state.query)
            state.research_data = results if results else ["No relevant data found."]
        except Exception as e:
            logging.error(f"Error in Tavily search: {e}")
            state.research_data = ["Failed to retrieve data."]
        return state
