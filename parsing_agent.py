import logging
from research_state import ResearchState

class ResearchParsingAgent:
    async def parse_research(self, state: ResearchState) -> ResearchState:
        """Extracts key points from research data."""
        logging.info("Extracting key insights from research data...")

        if not state.research_data or "Failed" in state.research_data:
            state.structured_research = "Error: No valid research data available."
            return state

        research_data_str = " ".join(state.research_data) if isinstance(state.research_data, list) else state.research_data
        key_points = "\n- " + "\n- ".join(research_data_str.split(". ")[:5])
        state.structured_research = f"Key Insights:\n{key_points}"
        
        return state
