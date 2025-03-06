from dataclasses import dataclass

@dataclass
class ResearchState:
    query: str
    research_data: list = None
    structured_research: str = ""
    summarized_data: str = ""
    final_answer: str = ""
