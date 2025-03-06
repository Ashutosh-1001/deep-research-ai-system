import logging
import asyncio
from transformers import pipeline
from research_state import ResearchState

class SummarizationAgent:
    def __init__(self):
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    async def summarize_data(self, state: ResearchState) -> ResearchState:
        logging.info("Summarizing research data...")

        if not state.structured_research:
            state.summarized_data = "Error: No structured research data available."
            return state

        try:
            summary = await asyncio.to_thread(
                self.summarizer, state.structured_research, max_length=300, min_length=100, do_sample=False
            )
            state.summarized_data = summary[0]["summary_text"]
        except Exception as e:
            logging.error(f"Error summarizing research data: {e}")
            state.summarized_data = state.structured_research  # Fallback
        
        return state
