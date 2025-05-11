from crewai import Task
from textwrap import dedent

class CustomTasks:
    def summarize_task(self, agent, serper_data_text):
        return Task(
            description=dedent(f"""
                You are an expert sustainability analyst. Your task is to review the following collection of sustainability-related news articles and policy documents and produce a structured summary report for strategic decision-makers.

                DO NOT REFERENCE SOURCES IN YOUR RESPONSE

                USE MARKDOWN FORMATTING IN YOUR RESPONSE
                
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

                USE MARKDOWN FORMATTING IN YOUR RESPONSE

                DO NOT REFERENCE SOURCES IN YOUR RESPONSE

            """),
            expected_output="A structured summary divided into legislative, industry, strategic, and general sustainability insights.",
            agent=agent,
        )
    def business_alignment_task(self, agent, final_output_text):
        company_profile = """
        Q1: What is your company’s sustainability strategy?
        1. Maersk embeds sustainability into its core corporate strategy, treating it not as an initiative but as a fundamental lens for decision-making. The company’s mission is to decarbonize global supply chains while creating long-term value for customers and society. Recent efforts include a $1.4 billion investment in green methanol-powered vessels and the introduction of an internal carbon pricing model to guide capital allocation.
        
        Q2: How do you measure and manage greenhouse gas emissions?
        2. Maersk tracks emissions using key performance indicators focused on fuel efficiency and sustainability metrics across its logistics chain. Scope 1 and 2 emissions are consistently measured, and systems for Scope 3 monitoring are being scaled. Emission data plays a key role in operational planning and strategic evaluation.
        
        Q3: What steps has your company taken to reduce its environmental footprint?
        3. Emission-reducing technologies have been prioritized, including a large-scale transition to green fuels. Maersk empowers its workforce through programs like the ‘sustainability champions’ initiative, which generated over 3000 ideas for operational improvements in a single year. Sustainability is also embedded into procurement, facility design, and innovation workflows.
        
        Q4: How do you approach sustainability across your value chain?
        4. Supplier sustainability is evaluated through scoring systems that are progressively integrated into sourcing and partnership decisions. While formal audit mechanisms are still expanding, the emphasis is on aligning upstream practices with long-term decarbonization goals.
        
        Q5: Who is responsible for sustainability and how is it governed?
        5. Maersk uses a distributed model of sustainability responsibility, with accountability shared across departments. An ESG-focused governance structure oversees risks and opportunities, while executive compensation is partly tied to sustainability performance. The company issues integrated reports aligned with international frameworks and engages in multi-stakeholder initiatives like SBTi.
        
        Q6: How is sustainability embedded in your company culture?
        6. Sustainability at Maersk is not managed top-down but through a blend of planned and emergent strategies. Employee involvement is central — cross-functional working groups, feedback loops, and internal storytelling campaigns foster engagement. The company emphasizes adaptability in the face of geopolitical volatility, regulatory shifts, and technological change.
        
        Q7: How do you differentiate from competitors through sustainability?
        7. Maersk views sustainability not as a compliance measure, but as a strategic differentiator. Its competitive edge lies in the ability to scale sustainable solutions across a global network, while leveraging policy influence and deep infrastructure. By aligning environmental goals with customer needs, Maersk positions sustainability as a premium service offering that supports long-term value creation.
        """

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
                   - Assess whether the identified trends can be structurally integrated into Maersk’s governance, operational frameworks, or culture.
                   - Consider alignment with established internal systems like leadership structures, cross-functional processes, internal communication practices, and management control mechanisms.
            
                2. **Differentiation and Innovation Potential**
                   - Identify any unique sustainability trends in the summary that could enable Maersk to maintain or enhance its strategic advantage over competitors.
                   - Highlight cases where Maersk could go beyond common ESG practices and invest in hard-to-imitate innovations, infrastructure, or policies.
            
                3. **Implementation Readiness and Risk Alignment**
                   - Evaluate how Maersk’s existing capabilities, employee involvement models, and stakeholder engagement mechanisms position it to adopt or respond to the identified trends.
                   - Call attention to any gaps or barriers in motivation, training, communication, or supplier practices that may hinder successful integration.
            
                Based on your evaluation, conclude your response with **3–5 specific strategic recommendations**. These should be actionable, connected to the summary insights, and tailored to Maersk’s current sustainability maturity.
            
                USE MARKDOWN FORMATTING IN YOUR RESPONSE
            
                DO NOT REFERENCE SOURCES IN YOUR RESPONSE
            """)
