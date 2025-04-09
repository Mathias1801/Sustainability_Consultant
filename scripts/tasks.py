from crewai import Task
from textwrap import dedent

class CustomTasks:
    def summarize_task(self, agent, serper_data_text):
        return Task(
            description=dedent(f"""
                You are an expert sustainability analyst. Your task is to review the following collection of sustainability-related news articles and policy documents and produce a structured summary report for strategic decision-makers.

                Please follow these steps:

                1. **Determine relevance**:
                   - Only include content related to environmental sustainability, climate regulations, ESG frameworks, or major industry movements.
                   - Exclude irrelevant topics such as celebrity news, unrelated technology trends, or non-environmental financial updates.

                2. **Extract key insights**:
                   - For each relevant article, identify the most important point and its implications.
                   - Emphasize what the information means in terms of environmental policy, industry direction, or corporate strategy.

                3. **Organize your summary using the following four sections**:

                **Legislative insight**
                - Focus on government policy, environmental legislation, ESG reporting requirements, and international agreements.

                **Industry insight**
                - Highlight major actions taken by companies or industries, including investments, innovations, or sustainability goals.

                **Strategic insight**
                - Focus on competitive positioning, corporate strategy shifts, investment trends, and market opportunities related to sustainability.

                **General insight**
                - Summarize broader public sentiment, awareness campaigns, environmental movements, or high-level sustainability events.

                Example format:

                Legislative insight:
                - The European Commission proposed new emissions reporting guidelines affecting all companies with over 500 employees.

                Industry insight:
                - Toyota announced a $2B investment in hydrogen fuel technology to expand its clean energy fleet.

                Strategic insight:
                - Renewable energy firms are increasingly targeting emerging markets as governments introduce green stimulus packages.

                General insight:
                - A recent UN report highlighted rising global awareness of climate-driven migration and its socio-economic effects.

                ### Content to analyze:
                {serper_data_text}
            """),
            expected_output="A structured summary divided into legislative, industry, strategic, and general sustainability insights.",
            agent=agent,
        )
