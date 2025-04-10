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
    def business_alignment_task(self, agent, final_output_text):
        company_profile = """
        Q1: Do you have a published sustainability or ESG strategy? (If yes, please provide a link or key goals — e.g., net-zero targets, material focus areas.)
        1. Yes — Our 2030 strategy includes net-zero targets for Scopes 1 and 2 by 2030, and Scope 3 by 2045. Key focus areas include green logistics, renewable sourcing, and reducing water intensity.
        
        Q2: Do you measure and report your greenhouse gas (GHG) emissions? (Please indicate which scopes — 1, 2, or 3 — and share recent figures if available.)
        2. Yes — Scope 1 and 2 emissions are fully reported for 2022 and 2023. Scope 3 is not yet systematically measured but is identified as a priority for 2025.
        
        Q3: What actions have you taken to reduce your environmental footprint in the past year? (This could include energy efficiency, waste reduction, circular economy practices, etc.)
        3. Implemented building energy retrofits resulting in a 10% reduction in electricity use. Transitioned 40% of vehicle fleet to electric. Launched internal waste-reduction challenge across departments.
        
        Q4: Do you evaluate the sustainability practices of your suppliers or partners? (If so, how? For example, supplier audits, certifications, or sustainability clauses.)
        4. No — We currently do not evaluate supplier sustainability practices formally. There is no audit program or requirement for sustainability certifications, though we are exploring a framework for 2026.
        
        Q5: Who in your organization is responsible for sustainability efforts, and do you publish regular reports? (e.g., CSO, ESG committee, or external reporting like GRI/TCFD.)
        5. Sustainability is overseen by the Chief Strategy Officer. While no dedicated CSO exists, the company issues an integrated report aligned with GRI since 2021 and TCFD since 2023.
        """

        return Task(
            description=dedent(f"""
                You are a Corporate Sustainability Strategist. Your task is to evaluate how the following sustainability trends and insights (produced by another analyst) align with the current sustainability strategy of your company.

                ### Company Profile:
                {company_profile}

                ### Sustainability Summary to Analyze:
                {final_output_text}

                Please perform the following steps:

                1. **Identify Opportunities**: Highlight external trends that support or validate your company’s existing strategy or suggest new growth areas.

                2. **Identify Gaps or Risks**: Point out where your company may fall short or face risks based on external developments (e.g., new regulations, competitor actions).

                3. **Make Strategic Recommendations**: Provide 3–5 specific, actionable recommendations for improving alignment with sustainability trends. Consider reporting practices, supplier evaluation, technology investments, and employee engagement.

                Your output should be structured in these three sections: Opportunities, Gaps/Risks, Recommendations.
            """),
            expected_output="An analysis with sections: Opportunities, Gaps/Risks, and Recommendations tailored to the provided company profile.",
            agent=agent,
        )
