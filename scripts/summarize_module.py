from textwrap import dedent
from llm_utils import generate_response

def summarize_articles(serper_data_text):
    prompt = dedent(f"""
        You are a Sustainability News Analyst. Your task is to review a collection of recent news articles and sustainability-related announcements and deliver a clear, relevant overview of developments from the past week.

        DO NOT REFERENCE SOURCES IN YOUR RESPONSE
        USE MARKDOWN FORMATTING IN YOUR RESPONSE

        Focus your efforts on:
        - Selecting only items related to environmental sustainability, climate policy, ESG frameworks, or industry-wide sustainability actions.
        - Ignoring news that is not directly relevant to the relevant subjects.

        Organize your findings into the following categories:

        **Legislative insight**
        - Summarize new policies, regulatory announcements, or international agreements with potential environmental or ESG impact.

        **Industry insight**
        - Report on major actions by companies or sectors (e.g., decarbonization commitments, green investments, product innovations).

        **General awareness**
        - Note public campaigns, global events, NGO actions, or cultural developments influencing sustainability discourse.

        Your summary should help a corporate strategist quickly understand the external sustainability context this week.

        ### Content to analyze:
        {serper_data_text}
    """)
    return generate_response(prompt)
