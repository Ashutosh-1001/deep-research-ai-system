import asyncio
from workflow import ResearchAI

if __name__ == "__main__":
    ai_system = ResearchAI()
    query = "Latest advancements in Cognitive Antenna Arrays"
    response = asyncio.run(ai_system.run(query))
    print("\nFinal Answer:\n", response)
