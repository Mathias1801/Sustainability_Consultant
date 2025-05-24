from textwrap import dedent
from llm_utils import generate_response

def run_attribution(summary, consultation, sources):
    prompt = dedent(f"""
        You are an Attribution Analyst. Your goal is to evaluate which claims from the following AI-generated outputs can be directly supported by the original source material provided.

        DO NOT MAKE UP SOURCES. Only reference source content that explicitly supports the claims.
        USE MARKDOWN FORMATTING IN YOUR RESPONSE

        ### AI-Generated Summary:
        {summary}

        ### AI-Generated Business Consultation:
        {consultation}

        ### Source Material:
        {sources}

        Your task is to:
        - Extract major claims from the summary and consultation outputs.
        - For each claim, search the source material to find supporting evidence.
        - If supported, quote the relevant part and identify which article it came from.
        - If no support is found, clearly flag the claim as unsupported.

        Format:

        ### Summary Attribution:
        - **Claim:** ...
          - **Supported by:** "[Quoted source text]"
          - **From article:** "Title of article"
          - **Confidence:** High / Medium / Low

        ### Consultation Attribution:
        - **Claim:** ...
          - **Supported by:** "[Quoted source text]"
          - **From article:** "Title of article"
          - **Confidence:** High / Medium / Low

        Flag any hallucinated claims or unverifiable statements. Be rigorous.
        DO NOT ADD CLAIMS — only evaluate what's present.
    """)
    return generate_response(prompt)
