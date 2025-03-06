import logging
import asyncio
from transformers import pipeline
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from research_state import ResearchState

class AnswerDraftingAgent:
    def __init__(self):
        self.memory = ConversationBufferMemory()
        model_list = [
            "mistralai/Mistral-7B-Instruct-v0.2",
            "HuggingFaceH4/zephyr-7b-beta",
        ]
        self.generator = None
        for model in model_list:
            try:
                logging.info(f"Trying to load model: {model}")
                self.generator = pipeline("text-generation", model=model)
                logging.info(f"Successfully loaded {model}")
                break
            except Exception as e:
                logging.warning(f"Failed to load {model}. Error: {e}")
        if not self.generator:
            raise RuntimeError("Failed to load any model.")

    async def generate_answer(self, state: ResearchState) -> ResearchState:
        """Generates a structured response from summarized research."""
        logging.info("Generating AI-powered answer...")

        if not state.summarized_data:
            state.final_answer = "Error: No valid summarized data available."
            return state
        
        prompt = PromptTemplate(
            template="""
            You are an expert research assistant. Based on the summarized insights, provide a detailed, well-structured response:

            **Query:** {query}
            
            **Summarized Research Data:**
            {summarized_data}

            Format the answer using clear paragraphs, bullet points, and markdown for readability.
            """,
            input_variables=["query", "summarized_data"]
        )

        formatted_prompt = prompt.format(query=state.query, summarized_data=state.summarized_data)
        response = await asyncio.to_thread(self.generator, formatted_prompt, max_length=1024, do_sample=True)
        state.final_answer = response[0]["generated_text"]
        
        return state
