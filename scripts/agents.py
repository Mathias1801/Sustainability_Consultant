# agents.py
from crewai import Agent
from langchain_openai import ChatOpenAI

class CustomAgents:
    def __init__(self):
        self.OpenAIGPT35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)

    def summarize_agent(self):
        return Agent(
            role="Sustainability Summary Analyst",
            backstory="Expert in identifying trends and summarizing industry impact in sustainability news and policy.",
            goal="Analyze provided sustainability data and provide an actionable report.",
            llm=self.OpenAIGPT35,
        )
