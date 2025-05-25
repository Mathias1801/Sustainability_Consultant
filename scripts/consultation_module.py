import json
from textwrap import dedent
from llm_utils import generate_response

def consult(summary_text, company_profile, perm_sources):
    prompt = dedent(f"""
        You are a Corporate Sustainability Strategist. Your task is to analyze how the following recent sustainability developments align with the strategic sustainability profile of Maersk.

        Your analysis should:
        - Contextualize the weekly trends using established sustainability tendencies, best practices, and long-term frameworks from the permanent source material.
        - Identify consistencies, gaps, and novel opportunities by comparing this week's developments to known standards and norms.
        - Provide actionable and insightful strategic guidance without artificial constraints on length or number of suggestions.

        DO NOT REFERENCE SOURCES IN YOUR RESPONSE  
        USE MARKDOWN FORMATTING IN YOUR RESPONSE

        ### Company Profile:
        {company_profile}

        ### Weekly Sustainability Summary:
        {summary_text}

        ### Permanent Sustainability Context (Established Tendencies):
        {perm_sources}

        Please perform your analysis using the following three dimensions derived from academic research on corporate sustainability strategy:

        1. **Strategic Integration & Organizational Embedding**
        2. **Differentiation and Innovation Potential**
        3. **Implementation Readiness and Risk Alignment**

        Conclude with a comprehensive list of strategic recommendations for Maersk that reflect both current developments and broader, long-term sustainability trajectories explained in the company_profile.
    """)

    return generate_response(prompt)

