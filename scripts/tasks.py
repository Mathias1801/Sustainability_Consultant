# tasks.py
from crewai import Task
from textwrap import dedent

class CustomTasks:
    def summarize_task(self, agent, serper_data_text):
        return Task(
            description=dedent(f"""
                You are a Sustainability News Analyst. Your task is to review a collection of recent news articles and sustainability-related announcements and deliver a clear, relevant overview of developments from the past week.

                DO NOT REFERENCE SOURCES IN YOUR RESPONSE

                USE MARKDOWN FORMATTING IN YOUR RESPONSE

                Focus your efforts on:
                - Selecting only items related to environmental sustainability, climate policy, ESG frameworks, or industry-wide sustainability actions.
                - Ignoring news that is not directly relevant (e.g. unrelated finance, celebrity, or general tech news).

                Organize your findings into the following categories:

                **Legislative insight**
                - Summarize new policies, regulatory announcements, or international agreements with potential environmental or ESG impact.

                **Industry insight**
                - Report on major actions by companies or sectors (e.g., decarbonization commitments, green investments, product innovations).

                **General awareness**
                - Note public campaigns, global events, NGO actions, or cultural developments influencing sustainability discourse.

                For each point, write 1–2 sentences explaining what happened and why it might matter to organizations concerned with sustainability.

                Your summary should help a corporate strategist quickly understand the external sustainability context this week — but leave interpretation and alignment to other experts.

                USE MARKDOWN FORMATTING IN YOUR RESPONSE

                DO NOT REFERENCE SOURCES IN YOUR RESPONSE

                ### Content to analyze:
                {serper_data_text}
            """),
            expected_output="A structured summary divided into legislative, industry, and general insights.",
            agent=agent,
        )

    def business_alignment_task(self, agent, final_output_text):
        company_profile = """..."""  # Insert your latest version of the Maersk profile here.

        return Task(
            description=dedent(f"""
                You are a Corporate Sustainability Strategist. Your task is to analyze how the following sustainability trends and developments align with the strategic sustainability profile of Maersk.

                DO NOT REFERENCE SOURCES IN YOUR RESPONSE

                USE MARKDOWN FORMATTING IN YOUR RESPONSE

                ### Company Profile:
                {company_profile}

                ### Sustainability Summary to Analyze:
                {final_output_text}

                Please perform your analysis using the following three dimensions derived from academic research on corporate sustainability strategy:

                1. **Strategic Integration & Organizational Embedding**
                2. **Differentiation and Innovation Potential**
                3. **Implementation Readiness and Risk Alignment**

                Conclude your response with 3–5 specific strategic recommendations tailored to Maersk’s sustainability maturity.

                USE MARKDOWN FORMATTING IN YOUR RESPONSE

                DO NOT REFERENCE SOURCES IN YOUR RESPONSE
            """),
            expected_output="An analysis with sections: Strategic Integration, Differentiation, Implementation Readiness, and Recommendations.",
            agent=agent,
        )

    def attribution_task(self, agent, summary_text, consultation_text, source_data_text):
        return Task(
            description=dedent(f"""
                You are an Attribution Analyst. Your goal is to evaluate which claims from the following AI-generated outputs can be directly supported by the original source material provided.

                DO NOT MAKE UP SOURCES. Only reference source content that explicitly supports the claims.

                USE MARKDOWN FORMATTING IN YOUR RESPONSE

                ### AI-Generated Summary:
                {summary_text}

                ### AI-Generated Business Consultation:
                {consultation_text}

                ### Source Material:
                {source_data_text}

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
            """),
            expected_output="Markdown-formatted report linking claims to sources or flagging unsupported ones.",
            agent=agent,
        )
