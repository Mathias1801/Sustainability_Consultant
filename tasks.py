# tasks.py
from crewai import Task
from textwrap import dedent

class CustomTasks:
    def summarize_task(self, agent, serper_data_text):
        return Task(
            description=dedent(f"""
                You are provided with a collection of recent sustainability news and policy reports.

                Your job is to:
                1. Decide what articles are important for strategic sustainability concerns.
                2. Identify key points made in each article or document.
                3. Filter out irrelevant results (e.g. articles not related to environmental or policy relevance).
                4. Deliver a structured summary in the following format:

                **Legislative insight:**
                - [Summary of legislative relevant information on sustainability concerns]

                **Industry insight:**
                - [Relevant industry-defining news related to sustainability]

                **Strategic insight:**
                - [Strategic and competitive positioning in sustainability]

                **General insight:**
                - [Movements, awareness, or general knowledge about sustainability]

                ### Content for analysis:
                {serper_data_text}
            """),
            expected_output="A structured report on legislative, industry, strategic, and general sustainability news.",
            agent=agent,
        )
