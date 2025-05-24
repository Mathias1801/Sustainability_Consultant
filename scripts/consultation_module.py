from textwrap import dedent
from llm_utils import get_gpt

def consult(summary_text, company_profile):
    prompt = dedent(f"""
        You are a Corporate Sustainability Strategist. Your task is to analyze how the following sustainability trends and developments align with the strategic sustainability profile of Maersk.

        DO NOT REFERENCE SOURCES IN YOUR RESPONSE
        USE MARKDOWN FORMATTING IN YOUR RESPONSE

        ### Company Profile:
        {company_profile}

        ### Sustainability Summary to Analyze:
        {summary_text}

        Please perform your analysis using the following three dimensions derived from academic research on corporate sustainability strategy:

        1. **Strategic Integration & Organizational Embedding**
        2. **Differentiation and Innovation Potential**
        3. **Implementation Readiness and Risk Alignment**

        Conclude your response with 3–5 specific strategic recommendations tailored to Maersk’s sustainability maturity.
    """)
    llm = get_gpt()
    message = llm.invoke(prompt)
    return message.content if hasattr(message, "content") else str(message)
