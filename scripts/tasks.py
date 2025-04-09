from crewai import Task
from textwrap import dedent

class CustomTasks:
    def summarize_task(self, agent, serper_data_text):
        return Task(
            description=dedent(f"""
                You are an expert sustainability analyst. Your job is to review the following collection of sustainability-related news and policy documents and deliver an insightful, structured summary for strategic decision-makers.

                Carefully follow these steps:
                1. **Scan for relevance**:
                   - Only include articles or sections that pertain to environmental sustainability, ESG policy, climate strategy, regulatory change, or green industry innovation.
                   - Disregard articles focused on unrelated technology, celebrity news, or unrelated business developments.

                2. **Extract key insights**:
                   - Identify the core message or implications of each relevant article.
                   - Focus on what this means for strategic planning, industry positioning, or upcoming regulations.

                3. **Categorize insights into four clearly labeled sections**:
                
                ---
                **🧾 Legislative insight**
                - Focus on laws, regulations, climate accords, compliance updates, or ESG mandates.

                **🏭 Industry insight**
                - Highlight developments within companies, sectors, or markets. Focus on innovation, leadership moves, or impactful projects.

                **📈 Strategic insight**
                - Focus on implications for competitive advantage, risk management, emerging trends, or strategic alignment with sustainability.

                **🌍 General insight**
                - Include public sentiment, awareness campaigns, social movements, and general sustainability milestones.

                ---

                📘 Example summary format:

                **🧾 Legislative insight**
                - The EU introduced new climate disclosure rules for large corporations starting 2026.

                **🏭 Industry insight**
                - Tesla announced a battery recycling initiative expected to reduce manufacturing waste by 40%.

                **📈 Strategic insight**
                - Companies investing in green supply chains are seeing stronger ESG ratings and long-term investor interest.

                **🌍 General insight**
                - Earth Hour 2025 saw record participation from over 200 countries.

                --- 

                ### Content to analyze:
                {serper_data_text}
            """),
            expected_output="An actionable, well-structured sustainability intelligence report divided into the four requested categories.",
            agent=agent,
        )
