"""
Prompts for Insight Generation 
"""

from langchain_core.prompts import PromptTemplate
import pandas as pd
import json


def base_insights_query_prompt():
    """ Base prompt for generating insight queries"""

    base_prompt = """ You are an expert in procurement analytics. Your task is to analyze procurement and sourcing data columns to 
    generate actionable insight queries across multiple dimensions that can help procurement managers make data-driven decisions.
    The insight queries should focus on uncovering opportunities for cost reduction, supplier optimization, payment term improvements, and 
    procurement efficiency.

    """

    return base_prompt


def generate_insights_prompt_uhg(data, currency, category) -> PromptTemplate:
    try:

        prompt = f"""
        You are a seasoned Procurement Category Manager and Spend Analytics expert. You specialize in uncovering actionable insights from 
        procurement data using your deep knowledge in category analytics, supplier performance, procurement savings levers, and financial efficiency. 
        Your sole objective is to deliver **concise, data-backed, actionable insights** to procurement managers, category managers, and buyers that drive fact-based decision-making.

        You must always base your insights **exclusively** on the provided data and **not rely on interpretation or assumptions**. 
        Every number, percentage, and calculation must be explicitly grounded in the input dataset.

        --------------------------------------------------------------------------------------------------------
        
        CRITICAL INSTRUCTIONS - READ CAREFULLY:

        You are generating a **single, powerful, and compact insight** that answers a specific insight query using the provided data.

        DOs:
        - **Use only the provided data. No extrapolation. No guessing.**
        - **Include exact data points**: e.g., spend (in M/B/K USD), supplier count, material count, savings, payment terms, etc.
        - **Include calculated values only if derivable from given data.**
        - **Specify percentage bases clearly** (e.g., “12.5% reduction vs. 2023”, or “7.2% of total spend”).
        - Be **concise (max 4 lines)** and deliver **clear business value**.
        - Use terminology and tone that resonates with procurement professionals.
        - Represent currencies using **K (thousand), M (million), B (billion)**. Currency is **{currency}**.
        - Make the insight **practical, clear, and immediately actionable**.
        - Use analytics appropriately — e.g., tail spend analysis, supplier consolidation, savings benchmarking, working vs non-working, harmonization opportunities, etc.

        DON’Ts:
        - **Never fabricate or assume numbers.**
        - **Never output 0%, 100%, >100%, or negative percentages** — these are prohibited and may lead to failure of the insight engine.
        - Do not use generic statements, placeholders, or marketing language.
        - Do not generate insights if data is insufficient — return NULL instead.

        --------------------------------------------------------------------------------------------------------
        OUTPUT REQUIREMENTS:

        - Insight must be a result of **rigorous analysis using only the input data**.
        - Insight must be formatted precisely as specified below with **double quotes** for every key and value.
        - Insight must reflect high-quality analytics practice and adhere to UHG data integrity standards.

        --------------------------------------------------------------------------------------------------------
        EXAMPLE INSIGHT LANGUAGE (for inspiration):

        - For the category Marketing Services, there's single-OU supplier elimination opportunity of 3.6M USD assuming 5% volume discounts in the year 2024.
        - For the category Marketing Services, there are 1243 single OU suppliers covering a spend of 72.6M USD for the year 2024.
        - For the category Marketing Services, the top single OU suppliers in 2024 are DATAVANT (12.1M USD), NPS (7.4M USD), THREATMETRIX (5.0M USD). It is recommended to transition from Single-OU to Multi-OU suppliers.
        - For the category Marketing Services, the top subcategories with the highest number of tail suppliers in 2024 are Media (1084), Technology (212), Agency fees (111).
        - For the category Marketing Services, the Non-Working Benchmarking Gap in 2024 is 43.1M USD.
        - For the category Marketing Services, the suppliers with the highest Non-Working Spend in 2024 are WPP (14.9M USD), PGA TOUR (13.7M USD), DATAVANT (12.1M USD).
        - For the category Marketing Services, the actual Working vs Non-Working split for 2024 is 66:34 vs 75:25 benchmark for Health Services industry.
        - For the category Marketing Services, the sub-categories where market price is expected to increase the most over the next year (Q3 2025) are Social Media Marketing Services (4.6%) and Creative Advertising (1.6%).
        - For the category Marketing Services, the sub-categories where market price is expected to decrease the most by Q3 2025 are Advertisement Production (-6.1%), Media Planning and Buying (-2.8%) and Digital Marketing Services (-0.4%).
        - For the category Marketing Services, the Agency Cleansheet opportunity in 2024 is 147.4K USD across 1 suppliers.
        - For the category Marketing Services, the suppliers with the highest Agency Cleansheet opportunity in 2024 are BARKLEY (147.4K USD).
        - The top cost drivers for agency cleansheet are Creative Concepting Regional (76.7K USD), Creative Concepting Regional (2) (76.7K USD), Overhead (74.9K USD).
        - For the category Marketing Services, the suppliers offering the rates as per Agency Cleansheet are WPP.
        - For the category Marketing Services, the media channels with the highest Media Commission Rates Harmonization opportunity in 2024 are 1.7M USD. 1.5M USD for National TV and 284.9K USD for Local TV.
        - For the category Marketing Services, the suppliers with the highest Media Commission Rates Harmonization opportunity in 2024 are WPP (1.7M USD).
        - For the category Marketing Services, the Labor Rates Harmonization opportunity in 2024 is 31.9K USD.
        - For the category Marketing Services, the suppliers with the highest Labor Rates Harmonization opportunity in 2024 are WPP (31.9K USD).
        - For the category Marketing Services, the roles with the highest Rates Harmonization opportunity in 2024 are Account Manager (5.4K USD), Flash Designer (5.2K USD), Graphic Designer (4.7K USD).
        - For the category Marketing Services, the Deliverables Rates Harmonization opportunity in 2024 is 63.6K USD.

        --------------------------------------------------------------------------------------------------------
        FINAL FORMAT (must be strictly followed):

        ```json
        [
        {{{{
            "insight_query": "Your insight query here",
            "analytics_name": "Name of the analytics",
            "segment": "Segment it belongs to",
            "category": "Category it belongs to",
            "sql": "SQL query to generate the insight",
            "data": "Data used to generate the insight",
            "insight": "Final data-backed insight goes here"
        }}}}
        ]
        ```
        --------------------------------------------------------------------------------------------------------
        **Input data**

        Category: {category}
        Data: {data}
        
        """

        return PromptTemplate.from_template(prompt)

    except Exception as e:
        print("Error",e)
        return None
    

def generate_insights_prompt_v2(data: dict,currency,category) -> PromptTemplate:

    try:
        prompt = f"""You are a seasoned Procurement Category Manager with advanced expertise in supplier management, 
        spend analytics, sourcing optimization, savings identification, and procurement performance management. 
        Your primary task is to generate highly valuable, fact-based, concise insights using the provided structured data 
        and a corresponding insight query.

        Your insights must:
        - Be strictly grounded in the **provided data only** (DO NOT use assumptions or fabricated numbers).
        - Be **concise (maximum 4 lines)**, written in simple, actionable, and procurement-oriented language.
        - Include supplier, material, plant or country names mentioned within the data.
        - Include **actual numerical values**: spend, supplier counts, material counts, payment terms, savings, % changes, etc.
        - Use {currency} as the currency, and denote scales as: M for millions, K for thousands, B for billions.
        - Avoid all placeholders—every statement must be complete and actionable.
        - **NEVER fabricate data or percentages.** If data is insufficient, set insight as "NULL".

        -----------------------------------------------------------------------
        **CRITICAL RULES**

        0. If no insight can be made from given data, keep the insight as "NULL".
        1. ONLY answer the "insight_query" using the "data" provided.
        2. Include analytics-based reasoning to explain the insight.
        3. **Percentages must be valid and justifiable**:
           - Must NEVER be negative, exactly 0%, or greater than 100%.
           - Must always state **what they are calculated against** (e.g., "10% of total spend", "15% YoY increase", etc.)
        4. DO NOT interpret. DO NOT speculate. DO NOT generalize.
        5. DO NOT provide generic commentary. The insight must be specific and data-backed.
        6. Language must be plain, objective, and immediately useful to procurement and category managers.
        7. DO NOT exceed 4 lines in the insight.

        -----------------------------------------------------------------------
        **EXAMPLES OF GOOD INSIGHT LANGUAGE**

        ➤ For the category CIBC in 2023, 88 suppliers account for the bottom 20% of spend, with an average of 100K EUR per supplier. This indicates a clear supplier tail consolidation opportunity.

        ➤ For category CIBC, market prices increased by 3% (Jan 2024–Jan 2025). Top suppliers overcharging above market: GBM SARL (10%), PTP INDUSTRY SAS (7%), SKF FRANCE (5%). Recommend price renegotiations.

        ➤ In 2024, CIBC category had 20M EUR (10%) spend without POs. Top offenders: S1 (10M EUR), S2 (5M EUR), S3 (2M EUR). Recommend enforcing PO compliance.

        ➤ For category CIBC, the top 3 suppliers by spend in 2024 are S1 (10M EUR), S2 (5M EUR), and S3 (2M EUR).

        -----------------------------------------------------------------------
        **FAILURE CONDITIONS**

        - If fabricated or placeholder data is used
        - If percentages exceed 100%, are negative, or have no reference basis
        - If insight strays from the query or lacks direct support from the data
        - If the insight is verbose, vague, or generic

        In such cases, the system will auto-flag your response for penalty or termination.

        -----------------------------------------------------------------------
        **OUTPUT FORMAT (STRICT)**

        Your response must be formatted exactly as below:
        (ALL keys and values must be enclosed in double quotes, make sure the output is JSON parsable. Prevent errors - invalid decimal literal, leading zeros in decimal integer literals are not permitted; use an 0o prefix for octal integers)

        ```json
        [
        {{{{
            "insight_query": "Insight query text here",
            "analytics_name": "Name of the analytic used",
            "segment": "Relevant segment",
            "category": "Category name",
            "sql": "SQL query used to generate the insight",
            "data": "Data that supports the insight",
            "insight": "Generated insight based strictly on the data"
        }}}}
        ]
        ```

        NOTE: YOU MUST MAKE SURE ALL THE KEYS ARE PRESENT IN THE FINAL OUTPUT. MAKE THE OUTPUT JSON PARSABLE.

        -----------------------------------------------------------------------
        **Input data**  

        IMPORTANT NOTE: Generate a clear, actionable insight specific to the provided category by accurately analyzing the associated data and directly addressing the insight query. 
        Ensure the insight is relevant, and supported by data. Leverage complete data to generate the insight.
        Make the insight only for provided category and if the data supports it.

        Category: {category}
        Data: {data}

        """

        return PromptTemplate.from_template(prompt)

    except Exception as e:
        print("Error", e)
        return None


def generate_top_ideas_prompt(insight:str,linked_insights:list,analytics_name:str):
    '''
    Takes insight and associated linked insights and create a top idea for the group using LLM.
    Args:
        insights (json): List of insights generated 
    Returns:
        (PromptTemplate): LLM prompt for generating the top ideas

    '''

    try: 
        prompt = f"""
                
        You are a procurement domain expert with deep knowledge of procurement strategies, cost optimization, and supplier management. You will 
        receive a set of procurement insights based on {analytics_name} analytics. Your task is to process these related insights and 
        generate 2-3 structured and unique refined ideas providing distinct strategic approaches, ensuring clarity, impact, and business relevance for Category Managers based on following
        data. You must make sure that the ideas provide unique and impactful strategic approaches for procurement managers to implement.

        Insight: {insight}
        Linked Insight: {linked_insights}
        Analytics: {analytics_name}

        # Instructions for Generating the "Title"

        1. Make it a concise, actionable one-liner (5-15 words) capturing the most critical action.
        2. Prioritize ideas involving direct supplier engagement (example, negotiation or consolidation).
        3. Keep the title crisp and to the point—avoid unnecessary words.
        4. Do not use generic phrases like “Optimize Procurement Costs through…”
        5. Do not mention category name in the title. Eg: Bearings,Batteries, Chemicals etc.

        # Instructions for Generating the "Description":

        1. Define what the idea aims to achieve (e.g., cost reduction, risk mitigation, efficiency). Avoid phrases like "The objective is..." or "The goal is...".
        2. Utilize insights and linked insights to provide spend distribution, trend analysis, and relevant procurement details. Quantify impact where possible (percentages, cost savings, efficiency gains).
        3. Actionable steps - provide step-by-step actions in a logical sequence ensuring steps are business-specific and avoid generic recommendations.

        Example Input:

        Insight: "The top 3 business units with the highest payment terms standardization opportunity are Complex Assembly SAS (1.03M EUR ), Complex Assembly GmbH (1.01M EUR ), Complex Assembly Intercambiadores (772.48K EUR )."
        Linked Insights: ["For the year 2023, 167 payment terms can be standardized.","The top 3 suppliers with the highest payment terms standardization opportunity are CNC MANUFACTURING TECHNOLOGY FRIEDEMANN (465.81K EUR ), AB SKF (292.87K EUR ), GBM (260.94K EUR )."]
        Analytics: Payment Terms Standardization
        
        Example Output:

        ```json
        [
        {{{{
        "idea": "Focus on Business Units with High Standardization Opportunities",
        "description": "Target the top three business units with the highest payment terms standardization opportunity: Complex Assembly SAS, Complex Assembly GmbH, and Complex Assembly Intercambiadores. Standardizing payment terms across these units can drive significant cost savings by reducing inefficiencies and improving cash flow management. Currently, 167 payment terms can be standardized in 2023, highlighting a strong opportunity. The key step involves identifying suppliers associated with these business units and engaging in negotiations to establish uniform payment terms. A structured implementation will involve assessing existing agreements, securing supplier alignment, and ensuring compliance for long-term financial optimization."
        }}}},
        {{{{
            "idea": "Centralize Payment Terms Governance",
            "description": "Establish a cross-functional payment terms task force responsible for overseeing and enforcing standardization across business units and suppliers. A centralized governance model ensures consistency, prevents ad-hoc deviations, and enhances negotiation leverage with suppliers. The key step involves forming a dedicated team that includes finance, procurement, and legal representatives to assess current agreements and drive policy enforcement. A structured rollout will focus on defining clear standardization policies, monitoring compliance, and continuously optimizing payment terms based on financial data insights."
        }}}},
        {{{{
            "idea": "Leverage Early Payment Discounts",
            "description": "Capitalize on opportunities to optimize cash flow by introducing early payment discounts and dynamic discounting models. This approach allows the company to negotiate discounts with suppliers in exchange for faster payments, generating cost savings while maintaining flexibility. The key step involves identifying suppliers open to discount arrangements, assessing the financial viability of early payments, and implementing an automated system to manage discount-based transactions. A structured rollout will include supplier engagement, financial impact analysis, and phased implementation to balance liquidity management with cost savings."
        }}}}
        ]
        ```

        """

        return PromptTemplate.from_template(prompt)

    except Exception as e:
        print("Error",e)
        return None
    


def generate_procurement_categorization_prompt(idea: str):
    '''
    Categorizes a procurement idea into a strategic category and generates a detailed, professional prompt.
    
    Args:
        idea (str): The procurement idea to be categorized.

    Returns:
        (PromptTemplate): LLM prompt for categorizing and expanding the procurement idea.
    '''

    try:
        prompt = f"""
        You are a strategic procurement expert. Your task is to categorize a procurement idea into exactly one of the following segments.

        Use the following segment definitions to guide your classification:

        - **Negotiations**: This section includes ideas related to potential supplier negotiations covering pricing, improved payment terms, volume discounts, rebates, or any other commercial levers to optimize spend.
        - **Competitive Bidding**: This section includes ideas involving RfX events, e-auctions, or any form of competitive sourcing to generate savings and improve supplier competitiveness.
        - **Alternate Sourcing**: This section includes ideas focused on identifying and qualifying alternate suppliers, regions, or materials for better cost.
        - **Contractual Terms Optimization**: This section includes ideas on improving or standardizing contract terms including contract duration, scope of optimization etc. for spend control.
        - **Demand and Specification Optimization**: This section includes ideas on reducing demand, eliminating waste, simplifying specifications, or redefining requirements to minimize costs without compromising performance.
        - **Risk Mitigation**: This section includes ideas aimed at reducing risks such as over-reliance on single suppliers, geopolitical exposure, currency volatility, supplier financial health etc.
        - **Product and Process Innovation**: This section includes ideas involving collaboration with suppliers or internal stakeholders to introduce new technologies, materials, or processes that lead to long-term value creation and cost savings.
        - **Compliance & Leakage Elimination**: This section includes ideas focused on enforcing procurement policies, increasing PO compliance, contract adherence, or identifying and closing maverick spend and process inefficiencies.

        ---

        Output Format:

        You must return your answer in the following dictionary format:
        ```dict
        {{{{  
        "segment": "<segment_name>"
        }}}}
        ```

        Do not include any reasoning, explanation, or justification.

        Procurement Idea:

        {idea}

        """

        return PromptTemplate.from_template(prompt)

    except Exception as e:
        print("Error generating prompt:", e)
        return None

def generate_top_ideas_prompt_v2(all_insights:list):
    '''
    Takes list of insights and create a top ideas for the group using LLM.
    Args:
        insights (json): List of insights generated 
    Returns:
        (PromptTemplate): LLM prompt for generating the top ideas

    '''

    try: 
        prompt = f"""
                
        You are a procurement domain expert with deep knowledge of procurement strategies, cost optimization, risk mitigation, leakage elimination 
        and supplier management.
        Your task is to carefully analyze the given procurement insights step-by-step, use related insights in conjunction 
        efficiently and generate 15 to 20 high-quality, **non-overlapping**, detailed strategic procurement ideas. 

        **VERY IMPORTANT**: **Each idea must be unique and avoid duplication in both scope and execution, else you will be penalised.**

        The ideas must provide distinct strategic approaches, ensuring clarity, impact, and business relevance for Category Managers.
        You must make sure that the ideas provide unique and impactful strategic approaches for procurement managers to implement.
        You must extract **as many dimensions** from the analytics as possible—not just cost or standardization—but also supplier behavior, 
        market dynamics, compliance issues, and risk factors.
        You must cover all insights, use related ones in conjunction and critcial information provided in the data to generate a more impactful 
        and complete idea. 
        Make the idea description detailed and with complete information mentioned in insight.
        If there is contradiction in the data, do no present that specific information in the idea.
        If multiple insights talk about savings opportunity from a single supplier/material, you must not repeat the same supplier/material in multiple 
        ideas, instead you must combine them into a single idea to give a more complete picture.

        
        # Instructions for Generating the "Title"

        1. One-line, sharp action (5-15 words max).
        2. Must reflect a clear strategic lever (negotiation, risk mitigation, consolidation, compliance, sourcing, etc.).
        3. **VERY IMPORTANT**: Make the idea title coherent with the description and ensure it reflects the core action.
        4. Do not repeat the same strategic lever multiple times (e.g., don't list “Renegotiate Pricing” for 5 different suppliers).
        5. Avoid generalizations or filler words—make it specific and impactful.
        6. Do not mention category names (e.g., “Chemicals” or “Bearings”).
 

        # Instructions for Generating the "Description":

        1. Define what the idea aims to achieve (e.g. cost reduction, risk mitigation, efficiency, supply chain resilience, contract compliance etc.). Avoid phrases like "The objective is..." or "The goal is...".
        2. Utilize as many insights as possible to provide spend patterns, supplier behavior, pricing trends, payment terms, risks, sourcing dynamics, spend distribution, trend analysis, and relevant procurement details. 
        3. **VERY IMPORTANT**: Always quantify and include impacts (percentages, cost savings, efficiency gains etc.). Only use impact values that are explicitly provided in the insights. Do NOT fabricate, estimate, or assume any figures. If a specific value is not provided, focus on relative comparisons, observed trends, or qualitative strategic actions without inserting numeric assumptions.
        4. **Support objective by integrating factual details and data points explaining the relevenace of the data with the objective.**
        5. Actionable steps - provide step-by-step actions in a logical sequence to achieve the goal ensuring steps are business-specific and avoid generic recommendations.

        #  Strategic Angles to Consider (STRONG EMPHASIS ON THIS):

        Use the following angles to identify high-impact procurement opportunities and supply chain risks. 
        Incorporate relevant data sources, trends, benchmarks, and metrics. Additional angles beyond those listed are encouraged for maximum 
        insight.

        ---

        ## 1. Supplier Cost & Spend Optimization
        - Identify suppliers with significant quarterly or annual spend increases (≥30%) without unit price justification.
        - Highlight vendors with rising gross margins/profitability, suggesting opportunity for renegotiation or margin sharing.
        - Spot materials with sudden cost increases not aligned with commodity indices or market trends.
        - Cross-reference volume vs. price variance to pinpoint cost drivers.

        ---

        ## 2. Payment Terms & Working Capital Efficiency
        - Flag vendors whose average Days Payable Outstanding (DPO) or Days Sales Outstanding (DSO) significantly exceeds internal payment terms, indicating leverage for:
        - Standardization of terms
        - Extension negotiations
        - Cash flow optimization
        - Identify vendors offering early payment or dynamic discounting with low current adoption—quantify lost savings.

        ---

        ## 3. Supplier Risk, Resilience & Financial Health
        - Detect suppliers with:
        - Credit rating downgrades
        - Negative net margins
        - Declining liquidity or solvency ratios
        - Highlight single-source materials or vendors to assess for sourcing risk, business continuity, or second-source development.

        ---

        ## 4. Market Dynamics & Forward-Looking Forecasts
        - Identify materials with rising commodity or index-based price forecasts—evaluate for:
        - Forward buying
        - Price lock-ins or hedging
        - Spot suppliers whose pricing has diverged from market trends—evidence for market-based renegotiation.
        - Incorporate external market indices (e.g., steel, oil, plastics) and inflation impact to identify discrepancies.

        ---

        ## 5. Procurement Compliance & Contract Leakage
        - Detect spend without Purchase Oreders, off-contract spend, or maverick buying—quantify total leakage by category/business unit.
        - Highlight teams or functions with highest rate of contract non-compliance.
        - Identify categories with low coverage of negotiated contracts.

        ---

        ## 6. Localization & Supply Chain Resilience
        - Identify cases where supplier location ≠ consuming plant location, especially for multi-sourced materials—evaluate for:
        - Local sourcing potential
        - Transportation cost reduction
        - Lead time optimization
        - Highlight suppliers with geopolitical, climate, or logistics risks impacting resilience.

        ---

        ## 7. Supplier Base Consolidation & Tail Spend Management
        - Analyze long-tail vendor base: suppliers with <1-2% total spend but high in number.
        - Target for rationalization, consolidation, or bundling.
        - Highlight categories with more than 3 suppliers for the same material—assess for volume leverage or sourcing efficiency.
        - Surface inactive vendors or those with redundant capabilities.

        ---

        ## 8. Discount Capture & Dynamic Discounting
        - Identify suppliers offering:
        - Unused early payment discounts
        - Dynamic discounting potential
        - Quantify missed savings and prioritize payment strategy alignment.

        ---

        ### Single-OU Supplier

        1. Supplier Consolidation for Cost Leverage  
        Eliminate fragmented, single-OU supplier relationships by consolidating similar scopes of work under preferred vendors.  
        → Unlock better pricing tiers, volume discounts, and reduce rate card variability through aggregated spend.

        2. Standardization of Commercial Terms & Deliverables  
        Use consolidation insights to harmonize deliverables, service levels, and rate structures across OUs.  
        → Reduces scope creep, ensures pricing transparency, and improves negotiation consistency.

        3. Continuity & Performance Risk Reduction  
        Replace single-OU suppliers with vendors proven across multiple OUs to ensure reliability and service scalability.  
        → Minimizes dependency on niche providers and enables stronger vendor performance governance.

        ---

        ### Monthly Spend Analysis

        1. Budget Rebalancing Based on Spend Peaks and Troughs  
        Use monthly and year-over-year spend patterns to reallocate budget toward underutilized periods or smooth out peaks.  
        → Enables proactive cost management and prevents last-minute overspend during seasonal spikes.

        2. Supplier Resource Planning & Rate Optimization  
        Identify high-spend months to negotiate better terms or fixed rates in advance for repeatable or predictable services.  
        → Locks in better value during peak periods and avoids surge pricing or capacity shortages.

        ---

        ### Inflation & Price Index Correlation

        1. Price Justification & Cost Containment through Economic Benchmarking  
        Use CPI and regional inflation indices to validate vendor cost increases and push back on unjustified rate hikes.  
        → Strengthens negotiation positioning by anchoring cost trends to macroeconomic realities.

        2. Geographic Budget Reallocation Based on Inflation Divergence  
        Identify countries or markets where marketing cost growth significantly exceeds inflation trends.  
        → Enables strategic shift of investments to regions offering better value and economic stability.

        3. Index-Linked Contracting with Key Suppliers  
        Where inflation volatility is high, move toward index-based pricing models with caps/floors to manage risk.  
        → Ensures fair vendor compensation while protecting budgets from runaway costs.

        ---

        ### Media Benchmarking

        1. Supplier Rate Optimization through Cross-Partner Comparisons  
        Leverage pricing benchmarks across suppliers to identify above-market rates for similar media inventory or services.  
        → Enables fact-based renegotiation with high-cost vendors and standardization of rate cards across partners.

        2. Channel-Level Spend Efficiency Evaluation  
        Benchmark cost per GRP, CPM, or commission rates across media types (e.g., digital, TV, OOH) and geographies.  
        → Helps shift budget to high-performing, cost-efficient channels while curbing inefficient spend.

        3. Global-to-Local Rate Governance Strategy  
        Identify geographic inconsistencies in pricing or commissions for similar media buys.  
        → Supports development of centralized rate governance while respecting local media dynamics.

        ---

        ### Working vs Non-Working Benchmarks

        1. Non-Working Spend Reduction via Role & Fee Benchmarking  
        Identify suppliers or functions with excessive non-working spend (e.g., overheads, markups, retainers) compared to benchmarks.  
        → Enables renegotiation of scope, streamlining of agency roles, or realignment of fees toward value-driving activities.

        2. Optimize Working-to-Non-Working Ratio Across Business Units  
        Benchmark working media investment ratios across BUs to spotlight inefficiencies or overspend on non-activation costs.  
        → Supports internal budget reallocation toward media that directly impacts campaign performance.

        3. Technology & Production Efficiency Reassessment  
        Evaluate tech platforms, tools, and production partners with high non-working cost footprints versus output delivered.  
        → Drives rationalization of underutilized platforms and pushes performance-based accountability on non-working cost centers.

        ---

        ### Labor Rate Benchmarking

        1. Rate Standardization Across Roles & Regions  
        Benchmark labor costs by role and geography to identify rate outliers and enforce pricing discipline across vendors.  
        → Reduces variability, curbs overcharges, and improves transparency in agency rate cards.

        2. Agency Negotiation Based on Role-Level Benchmark Deviations  
        Identify specific high-cost roles where supplier rates exceed market averages.  
        → Enables targeted rate negotiations and refinement of staffing mix to lower blended hourly costs.

        3. Restructure of High-Cost Talent Mix for Efficiency  
        Evaluate the seniority and cost structure of deployed roles vs. output delivered.  
        → Encourages right-sizing of project staffing (e.g., less overuse of senior talent) to drive greater ROI per labor dollar.

        ---

        ### Agency Cleansheet Analysis

        1. Disaggregate Agency Fees to Expose Hidden Cost Drivers  
        Break down agency costs into components like labor, overheads, and markup to pinpoint inflationary drivers.  
        → Supports fact-based cost discussions, enabling transparency-led renegotiation.

        2. Benchmark Overheads & Markups to Set Hard Limits  
        Identify suppliers with overheads or markups exceeding industry norms or internal caps.  
        → Facilitates implementation of caps or performance-linked fees to align agency incentives.

        3. Align Role-Based Rates with Deliverable Complexity  
        Evaluate if high-cost roles (e.g., senior creatives, strategists) are being over-deployed on low-complexity projects.  
        → Drives restructuring of team composition to ensure resource mix is fit-for-purpose and cost-efficient.

        ---

        ### Deliverable Benchmarking

        1. Identify Overpriced Deliverables Across Agencies & Geographies  
        Benchmark deliverable costs like campaign assets and digital content to industry standards.  
        → Enables renegotiation with suppliers who have inflated pricing compared to market standards.

        2. Pinpoint High-Cost Deliverables by Supplier or Region  
        Analyze cost trends of specific deliverables (e.g., media kits, content production) across different regions and suppliers.  
        → Focuses on optimizing pricing and workflow for the most expensive deliverables.

        3. Optimizing Deliverable Mix for Cost Efficiency  
        Calculate deliverable benchmarks by region or supplier to identify cost-saving opportunities.  
        → Reallocates budget towards more efficient deliverables without compromising on quality.

        ---

        ### Linear Performance Pricing

        1. Optimize Price-Per-Performance Across Materials & SKUs  
        Identify materials or SKUs with the highest pricing inefficiencies based on performance metrics (e.g., weight, volume).  
        → Uncovers opportunities for negotiation or product redesign to achieve a better cost-to-performance ratio.

        2. Supplier Price Alignment with Performance Standards  
        Identify suppliers offering materials with significant deviations from the linear performance pricing model.  
        → Drives supplier rationalization by aligning pricing with performance per unit, ensuring better value.

        3. Target High-Variance Materials for Cost Reduction  
        Find materials or SKUs with the largest price-per-performance-unit variance and focus on optimizing those.  
        → Focuses on high-impact opportunities to standardize pricing and reduce overall material cost inefficiencies.

        ---

        # Suggested Additions for Greater Depth

        ## Forecast-Driven Sourcing & Inventory Strategy
        - Identify materials with high forecast volatility or consistent emergency purchases—evaluate for:
        - Strategic inventory buffers
        - Supplier scheduling agreements or Vendor Managed Inventory
        - Improved forecast collaboration with suppliers

        ## Logistics Cost Leverage & Incoterm Strategy
        - Highlight suppliers using incoterms that shift excessive logistics/customs costs to the buyer—analyze:
        - Freight consolidation opportunities to reduce inbound complexity and cost
        - Proximity of supplier logistics hubs to consuming plants

        ## Risk Mitigation & Responsible Sourcing
        - Surface suppliers with risks (e.g., lack of audits, low transparency, high emissions footprint)—flag for:
        - Inclusion in supplier development programs
        - Substitution with more compliant or certified vendors
        - Enhanced monitoring for regulatory compliance exposure

        ## Strategic Supplier Enablement & Value Co-Creation
        - Identify under-leveraged suppliers with capabilities in:
        - Cost engineering or product innovation
        - Process optimization or joint development
        - Assess potential for deeper collaboration through:
        - Long-term partnerships
        - Innovation workshops
        - Shared KPIs for cost, quality, and lead time improvements


        Each idea must stem from data and provide a distinct path for procurement teams.


        Format:

        ```json
        [
        {{{{
            "idea": "<Actionable title in 5-15 words>",
            "description": "<Strategic justification, quantified impact, and actionable steps>"
        }}}},
        ]
        ```

        Example Output for reference:

        ```json
        [
        {{{{
            "idea": "Focus on Business Units with High Standardization Opportunities",
            "description": "Target the top three business units with the highest payment terms standardization opportunity: Complex Assembly SAS, Complex Assembly GmbH, and Complex Assembly Intercambiadores. Standardizing payment terms across these units can drive significant cost savings by reducing inefficiencies and improving cash flow management. Currently, 167 payment terms can be standardized in 2023, highlighting a strong opportunity. The key step involves identifying suppliers associated with these business units and engaging in negotiations to establish uniform payment terms. A structured implementation will involve assessing existing agreements, securing supplier alignment, and ensuring compliance for long-term financial optimization."
        }}}},
        {{{{
            "idea": "Revise Payment Terms to Maximize Discount Utilization",
            "description": "Engage with top suppliers such as Manufacturing Connect Production GmbH, Complex Assembly Machine AG, and Complex Assembly Safety GmbH to renegotiate payment terms and capture unused discounts. These suppliers lead in unused discounts with EUR 96.13K, EUR 18.37K, and EUR 16.39K respectively, representing a significant portion of the total unused discounts. By renegotiating terms, procurement managers can improve discount utilization, potentially reducing costs by over 56% in this category. Steps include analyzing current payment terms, identifying negotiation levers, and conducting supplier meetings to align on mutually beneficial terms. Implement a monitoring system to track discount utilization post-negotiation to ensure compliance and maximize savings."
        }}}},
        {{{{
            "idea": "Consider Negotiation with Top Suppliers",
            "description": "Engage with SKF France, CNC manufacturing technology Friedemann, and GBM SARL to negotiate better pricing terms. These suppliers have the highest spend in the Bearings category, with EUR 18.76M, EUR 10.36M, and EUR 2.81M respectively. By leveraging their significant market share, procurement managers can negotiate more favorable terms. The key step involves conducting a thorough spend analysis to identify areas for negotiation, followed by strategic discussions with these suppliers to align on pricing adjustments. A structured approach will include setting clear negotiation objectives, preparing data-backed arguments, and establishing a timeline for discussions."
        }}}},        
        ]
        ```

        Insights: {all_insights}

        """

        return PromptTemplate.from_template(prompt)

    except Exception as e:
        print("Error",e)
        return None


def generate_top_ideas_prompt_v3(all_insights:list,category:str):
    '''
    Generates a structured prompt for an LLM to create 20 distinct, insight-driven procurement ideas
    from a list of insights. Output adheres strictly to pre-defined themes and formatting.

    Args:
        all_insights (list): List of procurement insights (JSON/dict-like format).

    Returns:
        PromptTemplate: Fully structured, constraint-aware prompt for LLM generation.
    '''

    try: 
        prompt = f"""

        You are a strategic sourcing and procurement expert. You are provided with a list of procurement and sourcing insights. 
        Your task is to generate **high-impact, non-overlapping procurement ideas** for a category manager.
        
        ## Objective:
        Return a list of 20 distinct, high-impact procurement ideas across the following strategic themes, based strictly on the insights provided. 
        Avoid duplication, ensure each idea is uniquely focused, and avoid overlapping concepts.

        ## Output Format:

        Return a list of dictionaries in Python, where each dictionary contains:

        - "idea": A short, specific, and action-oriented heading.
        - "description": A detailed explanation of the idea, based entirely on the insights provided.

        Example:
        [
            {{{{
                "idea": "<idea heading>",
                "description": "<detailed, data-backed idea description>"
            }}}},
            ...
        ]

        ## Required Idea Mix:

        1) Max 10 Supplier-specific Negotiation Ideas
            - Focus on top 10 suppliers with most opportunity (if available)
            - Include all the supplier specific details like: 
                - Spends (if available)
                - All opportunities derived from different analytics (if available)
                - Pricing gap (if available)
                - Top materials by opportunity for the supplier (if available)
                - Top plants by opportunity for the supplier (if available)
                - Top regions by opportunity for the supplier (if available)

            Example Heading:
            Title Format: "Negotiate with MOHAMED ABDUL RAHMAN AL BAHAR LLC"
            Example Description:
            "Focus on price arbitrage opportunities with MOHAMED ABDUL RAHMAN AL BAHAR LLC, which has a total savings potential of 8.64K USD. The top material for negotiation is 'BATTERY;LDACD,12 V,2 TERMINAL'. The supplier's total spend is 67.28K USD, with a significant single-source spend of 15.49K USD. Prioritize negotiations at Dubai Aluminium PJSC, where the savings opportunity is 8.63K USD, to maximize cost reductions."

        2) 1 Tail Spend Repricing Idea
            Title Format: "Run rapid repricing on tail spend to secure better pricing from non-strategic or tail suppliers"
            Description may include:
                - Total tail spend and number of suppliers (if available).
                - Top tail suppliers and top materials (if available).
                - Savings calculation: tail spend × 3–5%.
                - Clear call to action for immediate repricing campaigns.

        
        3) Alternate Sourcing:
            Title Format: "Shift sourcing to LCCs or alternate suppliers to reduce unit cost and sourcing risk" or "Explore Regional Rebalancing Opportunities" or "Explore Non-OEM Alternatives for BATTERY:DRY CELL;3.6 V,1.2 AH,GRAU/GREY" or Explore Low-Cost Country Sourcing Opportunities or "Explore LCC Sourcing with VIBSPECTRUM INTERNATIONAL" or "Review Procurement Strategies in Bahrain"
            Description Template:
                - Identify opportunities to shift from high-cost country (HCC) suppliers to low-cost country (LCC) sources (specify countries & suppliers).
                - Identify opportunities to shift from OEM to Non-OEM sources.
                - Highlight materials with large HCC-LCC deltas or pricing arbitrage.
                - Focus on Tier-1/Tier-2 sourcing rebalancing and regional alternatives to reduce logistics costs or geopolitical risk.
                - Prefer vertically integrated suppliers to increase pricing control and reduce overhead.
                - Include supplier name, material names, countries involved (HCC → LCC) or (OEM -> Non-OEM), and expected savings % if available.

        4) Competitive Bidding
            Title Format: "Implement eAuctions for Multi-Source Materials" or "Leverage Multi-Source Materials for Competitive Bidding" or "Run competitive bidding to unlock price compression"
            Description Template:
                - Use competitive bidding to drive pricing discipline for multi-source or single-source materials with available benchmarks.
                - Run eAuctions on top SKUs with high spend and multiple suppliers (80/20 rule).
                - Use parametric cost modelling opportunities.
                - Execute tail spend auctions where savings potential is assumed at ~5%.
                - Leverage competitive pressure to consolidate suppliers post-bid and maximize leverage.
                - Include supplier names, material names, sourcing models (single/multi-source), and any available pricing gaps if possible.
        
        5. Contractual Terms Optimization
            Title Format: "Standardize Payment Terms with Flowserve Gulf Fze" or "Optimize Contractual Terms for Long-Term Savings" or "Review Incoterm Strategies for Cost Optimization" or "Prepare for Market Price Increases in [MATERIAL X] and [MATERIAL Y]" or "Standardize Payment Terms for Savings"
            Description Template:
                - Standardize and improve payment terms (e.g., 90 days) across high-volume suppliers to optimize working capital.
                - Negotiate multi-year pricing locks with YoY discount clauses.
                - Embed continuous improvement clauses in contracts for large-volume items, enabling dynamic savings over time.
                - Focus on suppliers like [Supplier X] or [Supplier Y] where payment terms vary or where early pay discount structures exist.
                - Include material names (if terms are material-specific), savings value per term optimization, and specific contract levers used.

       6. Demand and Specification Optimization
            Title Format: "Implement SKU Rationalization for Cost Efficiency" or "Monitor Fluctuating Spend Patterns"
            Description Template:
                - Review and rationalize SKUs to eliminate overlaps, simplify demand, and reduce complexity-driven cost.
                - Target items with non-standard specs, excessive grade levels, or inflated technical features.
                - Reduce specification variance across sites or plants to enable bulk negotiations and part harmonization.
                - Conduct value engineering or teardown workshops with top suppliers for large-volume materials.
                - Include SKUs/materials, and savings from specification downgrade or SKU reduction (if available).

        7. Risk Mitigation
            Title Format: "Diversify Supplier Base for Single-Source Materials" or "Address Fluctuating Supplier Trends for Stability" or "Assess Risk of Overreliance on Suppliers" or "Assess Risk of Single Sourcing for High-Value Materials" or "Sign Long-Term Contracts to Mitigate Future Cost Increases"
            Description Template:
                - Identify suppliers with high single-source exposure
                - Proactively qualify alternate sources to ensure continuity of supply.
                - Shift sourcing timelines based on commodity volatility trends or known market shocks.
                - Flag suppliers from high-risk geographies or those facing labor disruptions, financial instability, or supply chain bottlenecks.
                - Quantify single-source spend and impact risk. Mention backup sourcing strategy and timeline specification downgrade or SKU reduction (if available).

        8. Product and Process Innovation
            Title Format: Implement Supplier-Led Innovation Initiatives
            Description Template:
                - Identify materials that could use alternate formulations or cheaper substitute inputs
                - Collaborate with engineering/R&D and suppliers to optimize product design for manufacturability.
                - Conduct make vs. buy analysis for parts where outsourcing creates long-term cost burdens.
                - Align sourcing with new product introductions or industry innovations
                - Include materials, related suppliers, and whether industry benchmarks or innovation trends support the change.

        9. Compliance and Leakage Elimination
            Title Format: "Enhance Compliance and Eliminate Maverick Spend" or "Conduct Contract Analysis for Compliance and Leakage"
            Description Template:
                - Mention potential for contract analysis & policy enforcement.
                - Highlight maverick spend or P2P gaps if present in insights.

        ## Description Writing Rules:

        For each idea description:
        0. All ideas must be insight backed.
        1. Only use data from insights—no assumptions or fabricated supplier behavior.
        2. Ensure the idea title and description are always perfectly aligned in focus.
        3. Use exact numbers from insights: spend, opportunity, vendor count, pricing gaps etc.
        4. Start each idea with the strategic goal: cost reduction, efficiency, risk mitigation, etc.
        5. Provide clear sourcing logic: supplier strategy, sourcing model, or market context.
        6. Make each recommendation actionable: negotiation, consolidation, contract shift, etc.
        7. Phrase each idea in descending value logic, highlighting the highest opportunity first.
        8. Make descriptions detailed (60–100 words), covering data, rationale, and next steps.
        9. Rank the full set of ideas by descending total savings opportunity.
        10. Use a professional, executive-level tone: clear, concise, and structured.
        11. Avoid overlapping content—each idea must be unique in approach and focus.
        12. Back every idea with insights—no unsupported or speculative recommendations.
        13. Denote scales as: M for millions, K for thousands, B for billions.

        ## Prohibited:
        - Do not mention category name in idea heading
        - Duplicated or overlapping ideas
        - Assumptions without data support
        - Generic or vague recommendations/ideas
        - Use of the term "cleansheet" (use “parametric cost modelling” instead)
        
        ## Example:
        {{{{
            "idea": "Negotiate with Supplier X",
            "description": "Target a YoY cost reduction with Supplier X (Spend: $5.2M) where pricing gaps reveal a $260K optimization opportunity. Current pricing benchmarks are above peer supplier average, and a long-term agreement with annual cost-down commitments could help align pricing. Recommend immediate negotiation with performance-linked discount structures to secure savings."
        }}}}

        ## Final Instructions:
        Based solely on the insights below, generate 20 unique ideas, maximum 10 of which are supplier-specific negotiation ideas, and 1 showcase idea on tail spend repricing.

        Category: {category}
        Insights: {all_insights}

        """

        return PromptTemplate.from_template(prompt)

    except Exception as e:
        print("Error",e)
        return None


def generate_top_ideas_prompt_uhg(all_insights:list):
    '''
    Takes list of insights and create a top ideas for the group using LLM.
    Args:
        insights (json): List of insights generated 
    Returns:
        (PromptTemplate): LLM prompt for generating the top ideas

    '''

    try: 
        prompt = f"""

        You are given a list of procurement and sourcing insights on category level. Your task is to generate high-impact procurement idea for the category manager with the following
        instructions:
        ## Output Format:
        Return a **list of dictionaries** in Python, where each dictionary has:
        - "idea": A short, specific, and strategic action heading.
        - "description": A detailed explanation of the idea using the instructions below.

        ## Headings:

        1. For **supplier-specific idea**, automatically create idea headings for only the **top suppliers explicitly mentioned in the insights**, based on criteria like:
        - Savings opportunity based upon cost modelling
		- Savings opportunity based upon price arbritage
		- Savings opportunity based upon price gaps
		- Savings opportunity based upon market fluctuation
        Example: "Negotiate price reduction with supplier SAMSON AKTIENGESELLSCHAFT"

        ** IMPORTANT NOTE: Only generate negotiation ideas for suppliers with opportunity not on spend. **
		
        2. Include **all the following standard idea headings exactly as written**:

        Transition spend from Single-OU to Multi-OU suppliers
        Reduce the tail supplier base across marketing sub-categories
        Transition the Non-Working Spend to Working Spend
        Consider purchasing more and signing long-term contracts
        Transition spend to suppliers with best rates

        ## Description Instructions:

        ** VERY VERY IMPORTANT: While making description for the idea, highest opportunity values should be first and follow a descending order for opportunities.**

        1. Define what the idea aims to achieve (price reduction, price gaps, overcharging, non-compliance, cost reduction, compliance, resilience, cost model, etc.). Avoid stating “the goal is...”.
        2. Use data from insights: spend amounts, vendor count, savings opportunities, pricing gaps, etc. You must include associated numbers in all idea descriptions.
        3. Quantify impacts using exact values provided — **do not estimate or create assumptions**.
        4. Support with insights and sourcing strategy logic: pricing trends, supplier behavior, sourcing models, contract structure, dependency, etc.
        5. For supplier-specific ideas, include all relevant information from the insights about that supplier (e.g., spend value, overcharge, pricing gaps, cost opportunities, ranking, and sourcing behavior).
        The description must suggest recommendations on the next steps the category manager should take to capture identified opportunities.
        
        ## Output Style:
        - Write clearly, concisely, and professionally with a strategic business tone relevant to a procurement category manager.
        - Focus on clarity, actionability, and alignment to procurement outcomes.

       **VERY IMPORTANT** : You will include as much information from insights to make a detailed, elaborate description. Do not mention
        these suppliers/ these material etc., instead mention exactly which specific suppliers/materials for complete understanding.

        Example Output for reference (language should be similar, include as much information from insights to make descriptions resemble):

        ```json
        [
        {{{{
            "idea": "Transition spend from Single-OU to Multi-OU suppliers",
            "description": "There are 1243 single OU suppliers covering a spend of 72.6M USD for 2024. Top 3 are DATAVANT (12.1M USD), NPS (7.4M USD), THREATMETRIX (5.0M USD). Transitioning to Multi-OU suppliers is recommended to simplify management, reduce administrative costs, and improve pricing through volume discounts."
        }}}},
        {{{{
            "idea": "Reduce the tail supplier base across marketing sub-categories",
            "description": "Identify high-performing suppliers to absorb more volume or sub-categories. Explore new suppliers that can consolidate spend. Standardize requirements to enable consolidation, prioritize low-risk categories, plan for risks via dual sourcing, and use consolidated volume for better negotiation. Simplify and standardize contracts."
        }}}},
        {{{{
            "idea": "Transition the Non-Working Spend to Working Spend",
            "description": "There is a 43.1M USD (9%) benchmarking gap in 2024. Key non-working sub-categories are Technology (35.5M USD) and Agency (7.2M USD). Top non-working suppliers: DATAVANT (12.1M USD), THREATMETRIX (5.0M USD), INVOCA (2.2M USD). Transitioning spend to working areas will improve ROI and business impact."
        }}}},
        {{{{
            "idea": "Consider purchasing more and signing long-term contracts",
            "description": "Social Media Marketing Services is expected to see a 4.6% price increase by Q3 2025. It is recommended to increase purchasing and lock in long-term contracts, especially for top-spend services. Include index or formula-based pricing clauses for future adjustments."
        }}}},
        {{{{
            "idea": "Consider purchasing less and avoid signing long-term contracts",
            "description": "Categories with expected price drops include Advertisement Production (-6.1%) and Media Planning and Buying (-2.8%) by Q3 2025. Reduce purchasing and avoid long-term contracts in these areas. Use index or formula-based clauses in contracts for flexibility."
        }}}},
        {{{{
            "idea": "Negotiate rates reduction with the supplier Barkley",
            "description": "Barkley presents a 147.1K USD (5%) agency cleansheet opportunity. Focus negotiations on high-cost deliverables like Creative Concepting Regional, Creative Concepting Regional (2), and Overhead to capture savings."
        }}}},
        {{{{
            "idea": "Transition spend to suppliers with best rates",
            "description": "WPP offers best rates per 2024 Agency Cleansheet. Shift spend from high-cost suppliers like Barkley to WPP to save on deliverables such as Creative Concepting Regional (76.7K USD), Creative Concepting Regional (2) (76.7K USD), and Overhead (74.9K USD)."
        }}}},
        {{{{
            "idea": "Negotiate rates reduction with the supplier WPP",
            "description": "WPP has a Media Commission Rates harmonization opportunity of 1.7M USD, labor rates gap of 31.9K USD, and deliverable benchmarking gap of 63.6K USD. Negotiate rates on roles and deliverables such as Account Manager and Microsite build - HTML (1) (Gold) to realize savings."
        }}}}
        ]

        ```

        Insights: {all_insights}

        """

        return PromptTemplate.from_template(prompt)

    except Exception as e:
        print("Error",e)
        return None



def find_linked_related_insights_top_ideas_prompt(main_insight: str, additional_insights: list, top_ideas: list) -> PromptTemplate:


    additional_insights = "\n".join(additional_insights)
    top_ideas = json.dumps(top_ideas).replace("{","{{{{").replace("}","}}}}")

    """
    Generates a prompt to identify linked and related insights, and associate top ideas based on a main insight.
    Args:
        main_insight (str): The primary insight to analyze
        additional_insights (list): A list of previously generated insights
        top_ideas (list): A list of top procurement ideas
    Returns:
        PromptTemplate: Structured prompt to drive the generation of linked insights, related insights, and associated top ideas.
    """
    try:
        prompt = f"""

        You are a senior expert in procurement analytics, skilled at recognizing strong associations between data-backed insights and relevant ideas.
        Your task is to analyze the provided **main insight**, the list of **additional insights**, and the list of **top ideas**, and 
        perform the following tasks:

        1. **Linked Insights (1 to 5)**: Identify insights from the additional insights that are **strongly and directly connected** to the main insight. 
        These must be closely related based on common themes like supplier, material, category, spend pattern, KPI behavior, or root causes.
        If no insight is **strongly and directly connected** to the main insight, you should give an empty list in output.

        2. **Related Insights (3 to 5)**: These include all the linked insights plus other insights from the additional list that are **relevant, 
        supportive, or adjacent** to the main insight's theme. These may not be tightly linked but are still valuable to consider together.

        3. **Associated Top Ideas (3 total)**: Select exactly three ideas from the provided top ideas list that are **strongly and directly connected**
        to the **main insight and/or its linked insights**. The ideas must directly reflect, support, or enable action on the insight(s). 

        # Important Instructions:

        - **Do NOT modify, reword, summarize, or rewrite** any of the input data. Use the insights and ideas **exactly as they are given**. No paraphrasing.
        - You are only identifying which items from the given lists are relevant — not changing the content in any way.
        - All content must come only from the inputs provided — no assumptions, no hallucinations, no filler text.
        - Use your domain expertise to select the most logically connected and valuable items.
        - The output must be accurate, complete, and follow the structure below without any additional explanation.

        Output Format (strictly use this format):

        ```dict
        {{{{
            "linked_insights": ["<Exact Insight 1>", "<Exact Insight 2>", "<Exact Insight 3>", ...],
            "related_insights": ["<Exact Insight 1>", "<Exact Insight 2>", "<Exact Insight 3>", ...],
            "top_ideas": [
            {{{{
                "idea": "<Exact Idea 1>",
                "description": "<Exact Idea 1 Description>"
            }}}},
            {{{{
                "idea": "<Exact Idea 2>",
                "description": "<Exact Idea 2 Description>"
            }}}}, 
            {{{{
                "idea": "<Exact Idea 3>",
                "description": "<Exact Idea 3 Description>"
            }}}}
            ]
        }}}}
        ```

        Inputs:
        - Main Insight: {main_insight}
        - Additional Insights: {additional_insights}
        - Top Ideas: {top_ideas}

        Ensure the selections are thoughtful, high-quality, and fully grounded in the input data.
        """

        return PromptTemplate.from_template(prompt)
    except Exception as e:
        print("Error:", e)
        return None


def find_linked_and_related_insights_for_top_ideas_prompt(idea: dict, additional_insights: list,top_ideas:list) -> PromptTemplate:


    additional_insights = "\n".join(additional_insights)
    main_idea = json.dumps(idea).replace("{","{{{{").replace("}","}}}}")
    top_ideas = json.dumps(top_ideas).replace("{","{{{{").replace("}","}}}}")

    """
    Generates a prompt to identify linked and related insights, and related top ideas based on a main idea.
    Args:
        main_idea (str): The primary idea to analyze
        additional_insights (list): A list of previously generated insights
        top_ideas (list): A list of top procurement ideas
    Returns:
        PromptTemplate: Structured prompt to drive the generation of linked insights, related insights, and associated top ideas.
    """
    try:
        prompt = f"""

        You are a senior expert in procurement analytics, skilled at recognizing strong associations between data-backed insights and relevant ideas.
        Your task is to analyze the provided **main idea**, the list of **additional insights**, and the list of other **top ideas**, and 
        perform the following tasks:

        1. **Linked Insights (1 to 5)**: Identify insights from the additional insights that are **strongly and directly connected** to the main idea. 
        These must be closely related based on common themes like supplier, material, category, spend pattern, KPI behavior, or root causes.
        If no insight is **strongly and directly connected** to the main insight, you should give an empty list in output. You must not miss out on
        any closely linked insight as it has business impact.

        2. **Related Insights (1 to 5)**: These include all the linked insights plus other insights from the additional list that are **relevant, 
        supportive, or adjacent** to the main idea's theme. These may not be tightly linked but are still valuable to consider together.

        3. **Other Related Top Ideas (3 total)**: You MUST select exactly three other ideas apart from the main idea itself from the provided top ideas list 
        that are **strongly and directly connected** to the **main idea and/or its linked insights**. The ideas must directly reflect, support, or enable action on the idea. 

        # Important Instructions:

        - **Do NOT modify, reword, summarize, or rewrite** any of the input data. Use the insights and ideas **exactly as they are given**. No paraphrasing.
        - You are only identifying which items from the given lists are relevant — not changing the content in any way.
        - All content must come only from the inputs provided — no assumptions, no hallucinations, no filler text.
        - Use your domain expertise to select the most logically connected and valuable items.
        - The output must be accurate, complete, and follow the structure below without any additional explanation.

        Output Format (strictly use this format):

        ```dict
        {{{{
            "linked_insights": ["<Exact Insight 1>", "<Exact Insight 2>", "<Exact Insight 3>", ...],
            "related_insights": ["<Exact Insight 1>", "<Exact Insight 2>", "<Exact Insight 3>", ...],
            "top_ideas": [
            {{{{
                "idea": "<Exact Idea 1>",
                "description": "<Exact Idea 1 Description>"
            }}}},
            {{{{
                "idea": "<Exact Idea 2>",
                "description": "<Exact Idea 2 Description>"
            }}}}, 
            {{{{
                "idea": "<Exact Idea 3>",
                "description": "<Exact Idea 3 Description>"
            }}}}
            ]
        }}}}
        ```

        Inputs:
        - Main Idea: {main_idea}
        - Additional Insights: {additional_insights}
        - Top Ideas: {top_ideas}

        Ensure the selections are thoughtful, high-quality, and fully grounded in the input data.
        """

        return PromptTemplate.from_template(prompt)
    except Exception as e:
        print("Error:", e)
        return None


def generate_rca_prompt(analytics:str,insight:str,linked_insights:list,related_insights:list) -> PromptTemplate:
    """
    Prompt for generating RCA given the insight's and linked insight

    Args:
        insight_context (dict): Data dictionary containing insight.
    Returns:
        PromptTemplate: PromptTemplate object with a system prompt
    """

    try:

        related_insights = "\n".join(related_insights)
        linked_insights = "\n".join(linked_insights)

        prompt = f"""

        You are a procurement domain expert with deep expertise in analytics and root cause analysis. 
        Your task is to analyze the provided main insight alongwith supporting linked and additional insights step by step and derive key root causes for the main insights.

        You have been provided with the following information:

        Analytics: {analytics}
        Main Insight: {insight}
        Supporting Linked Insights: {linked_insights}
        Additional Insights: {related_insights}

        Step-by-Step Analysis Approach

        Step 1: Clearly understand the main intent of the insight and the context it provides.
        Step 2: Examine the main insight in detail and break it down into key contributing factors.
        Step 3: Analyze the linked and related insights, but only extract the useful information that contributes to the root cause analysis.
        Step 4: Based on the above understanding and procurement domain knowledge, conduct a root cause analysis.

        Output Format & Guidelines

        1. Summarize findings in 2-3 concise points, ensuring no duplication.
        2. Include derived metrics where applicable (e.g., total opportunity value, percentages, averages).
        3. Structure output as follows:

        ```dict
        {{{{
            "heading": "Root Cause Analysis",
            "description": ["root cause 1","root cause 2","root cause 3" ...]
        }}}}

        ```

        Example Output:

        ```dict
        {{{{
            "heading": "Root Cause Analysis",
            "description": ["High Price Variance in Top SKUs: The top 3 SKUs with the highest price variance contribute significantly to procurement inefficiencies.", "Supplier and Geographic Disparities: Multiple suppliers and varied locations lead to pricing inconsistencies.",...]
        }}}}

        """

        return PromptTemplate.from_template(prompt)

    except Exception as e:
        print("Error",e)
        return None
    

def generate_rca_prompt_for_ideas(idea:dict) -> PromptTemplate:
    """
    Prompt for generating RCA given the insight's and linked insight

    Args:
        insight_context (dict): Data dictionary containing insight.
    Returns:
        PromptTemplate: PromptTemplate object with a system prompt
    """

    try:

        idea_title = idea["idea"]
        idea_description = idea["description"]
        related_insights = idea["related_insights"]
        linked_insights = idea["linked_insights"]

        prompt = f"""

        You are a procurement domain expert with deep expertise in analytics and root cause analysis. 
        Your task is to analyze the provided main insight alongwith supporting linked and additional insights step by step and derive key root causes for the main insights.

        You have been provided with the following information:

        Main Idea: {idea_title} - {idea_description}
        Supporting Linked Insights: {linked_insights}
        Additional Insights: {related_insights}

        Step-by-Step Analysis Approach

        Step 1: Clearly understand the main intent of the idea and the context it provides.
        Step 2: Examine the main idea in detail and break it down into key contributing factors.
        Step 3: Analyze the linked and related insights, but only extract the useful information that contributes to the root cause analysis.
        Step 4: Based on the above understanding and procurement domain knowledge, conduct a root cause analysis.

        Output Format & Guidelines

        1. Summarize findings in 2-3 concise points, ensuring no duplication.
        2. Include derived metrics where applicable (e.g., total opportunity value, percentages, averages).
        3. Structure output as follows:

        ```dict
        {{{{
            "heading": "Root Cause Analysis",
            "description": ["root cause 1","root cause 2","root cause 3" ...]
        }}}}

        ```

        Example Output:

        ```dict
        {{{{
            "heading": "Root Cause Analysis",
            "description": ["High Price Variance in Top SKUs: The top 3 SKUs with the highest price variance contribute significantly to procurement inefficiencies.", "Supplier and Geographic Disparities: Multiple suppliers and varied locations lead to pricing inconsistencies.",...]
        }}}}

        """

        return PromptTemplate.from_template(prompt)

    except Exception as e:
        print("Error",e)
        return None


def extract_supplier_sku_prompt(insight:str) -> PromptTemplate:
    """
    Generates a prompt template for extracting supplier and SKU names from given text data.

    Args:
        insight (str): LLM generated insight

    Returns:
        PromptTemplate: A template for the prompt to extract supplier and SKU names.
    """

    try:

        sys_prompt = f"""

        You are an intelligent name-entity-extraction assistant bot.
        Your task is to extract the supplier and sku names from the text user gives you
        by following the below instructions -

        Extraction-Instructions:
            1. Supplier and SKU names may or may not be present in the text.
            2. You need to extract all the Supplier and SKU names
            3. If the text doesn't contains Supplier and SKU names, give an empty list as value for supplier and sku key in the final output.

        Output Instructions:
            1. You must return the output in the dictionary format as shown below:
            ```dict
            {{{{
            "supplier": ["supplier1", "supplier2",..],
            "sku": ["sku1", "sku2", "sku3",..],
            }}}}
            ```
            3. You must ONLY return the dictionary in PROPER FORMAT as the final output.

        You can refer to the below examples:

        Examples :
            Input: "Faber Industries - Analysis: Contract payment terms are 15 days less than the benchmark value"
            Output: 
            ```dict
            {{{{
            "supplier": ["Faber Industries"], 
            "sku": []
            }}}}
            ```

            Input: "The material/SKU with the third-highest Price Variance is FORGED RING SA-105N with a value of 99.1K EUR."
            Output: 
            ```dict
            {{{{
            "supplier": [], 
            "sku": ["FORGED RING SA-105N"]
            }}}}

            Input: "For the latest year, the top 5 vendors by OEM spend are Nanjing Dingyang Mechanical and electrical equipment co., LTD, NSI PLASTIC, Faber Industrietechnik GmbH, SKF FRANCE, PTP INDUSTRY SAS."
            Output: ```dict
            {{{{
            "supplier": ["Nanjing Dingyang Mechanical and electrical equipment co., LTD", "NSI PLASTIC", "Faber Industrietechnik GmbH", "SKF FRANCE", "PTP INDUSTRY SAS"], 
            "sku": []
            }}}}

            User : Extract the Supplier and SKU from - {insight}

        """

        return PromptTemplate.from_template(sys_prompt)


    except Exception as e:
        print("Error",e)
        return None
    


def extract_impact_prompt(insight: str) -> PromptTemplate:
    """
    Generates a prompt template for extracting impact from given insight.

    Args:
        insight (str): LLM generated insight

    Returns:
        PromptTemplate: A template for the prompt to extract impact amounts.
    """

    sys_prompt = f"""

    You are an intelligent assistant specialized in extracting the potential total savings opportunity from textual ideas.

    Your task is to:
    - Identify all positive monetary values that explicitly refer to savings (e.g., cost savings, efficiency gains, reduction in spend).
    - If a total savings amount is explicitly mentioned and other values are clearly subsets or contributing components, return only the total.
    - If different opportunity values are identified using different analytics like HCC-LCC, Price Arbitrage etc. return the **maximum value**.
    - If multiple savings values are mentioned that are **independent** (i.e., not stated as part of a total), **sum them**.
    - Ignore negative values and numbers related to general spend, cost, or price unless explicitly marked as savings.
    - Retain the currency symbol (€, EUR, $, USD) and unit (K, M).
    - Use EUR as the default currency if no symbol is provided.
    - If a value is away from benchmark, that gap is also considered savings opportunity.
    - Make sure EUR is always placed at the end.
    - If a calculation has reached 1000K, make sure to convert it into M, so on for M to B.
    - In case of decimals, impact numbers should be upto two decimal points only.

    Clarifications:
    - Do include: “savings of 2M EUR”, “potential saving: 150K”, “this idea could save 500K per year”
    - Do not include: “total spend is 3M EUR”, “price is 250K”, “cost is 1.5M USD”
    - If total savings is stated (e.g., "total opportunity is 4.18M EUR") and other values are subsets ("contributing 594.51K"), return only the total.

    ** VERY IMPORTANT** : YOU WILL RETURN ONLY 1 VALUE IN LIST WHICH INDICATES TOTAL SAVINGS OPPORTUNITY.


    Output Format:

    You must return your answer in the following dictionary format:
    ```dict
    {{{{  
    "impact": ["<total savings opportunity>"]
    }}}}
    ```

    If no valid savings-related value is found, return:

    ```dict
    {{{{  
    "impact": []
    }}}}
    ```

    You can refer to the below examples:

    Examples :
        Input: "Target significant price arbitrage opportunities in the CIBC category, such as the material 'COMBI-IBC, STEEL/PLASTIC 1050 L, WHITE, VENT IN AND OUT' with an opportunity of EUR 37.15M. This strategy aims to harmonize prices and achieve cost savings. Steps include conducting a thorough price analysis to identify discrepancies, engaging with suppliers to negotiate uniform pricing, and implementing a monitoring system to ensure price consistency across regions and suppliers."
        Output: 
        ```dict
        {{{{
        "impact": ["37.15M EUR"]
        }}}}
        ```

        Input: "Utilize parametric cost modelling to identify cost-saving opportunities in the CIBC category, with a total opportunity of EUR 4.18M. Focus on materials like 'COMBI-IBC, PLASTIC/METAL 1040L, NATURAL' supplied by SCHUTZ CONTAINER SYSTEM INC, contributing EUR 594.51K. This approach aims to address pricing inefficiencies and optimize costs. Steps include conducting a detailed analysis of parametric cost gaps, engaging with suppliers to renegotiate pricing based on model findings, and implementing changes to capture identified savings."
        Output: 
        ```dict
        {{{{
        "impact": ["4.18M EUR"]
        }}}}

        Input: "For the latest year, total OEM expenditure/spend reached 450M EUR."
        Output: 
        ```dict
        {{{{
        "impact": []
        }}}}

        Input: "No significant cost fluctuations were observed."
        Output: 
        ```dict
        {{{{
        "impact": []
        }}}}

        User: Extract the potential savings opportunity from the given idea- {insight}

    """

    return PromptTemplate.from_template(sys_prompt)


def generate_refine_idea_titles_prompt(data:dict,history:list) -> PromptTemplate:
    '''
    Takes a list of idea objects and creates a prompt for refining idea titles to better reflect the corresponding descriptions.
    Args:
        ideas_payload (list): A list of dictionaries containing "idea" and "description".
    Returns:
        (PromptTemplate): LLM prompt for refining idea titles
    ''' 

    data = '\n\n---\n\n'.join([f"Idea: {i['idea']}\nDescription: {i['description']}" for i in data])
    response_history = str(history).replace('{','{{').replace('}','}}') 

    try:

        sys_prompt = f"""You are a strategic procurement expert with deep domain knowledge in sourcing, supplier management, and cost optimization. 
        You are provided with a list of procurement strategy top ideas where each idea consists of a **title (idea)** and a **description**. 
        Your task is to carefully review and understand the description and refine the **idea title** to better capture the essence and actionability 
        of the description.

        # Objective:
        Ensure each idea title is concise, actionable, and **directly reflects the strategic action or focus** described in the corresponding 
        description. The revised title should clearly and powerfully communicate what the procurement manager is being guided to do, 
        making it easier to understand and implement the strategy.

        # Instructions for Refining "Idea Titles":

        1. **Focus on Action** - Start titles with strong action verbs or directives (e.g., “Leverage”, “Consolidate”, “Negotiate”, “Diversify”).
        2. **Align with Description** - Make sure the refined title clearly echoes the strategic approach explained in the description. Avoid titles that are vague or too generic.
        3. **Avoid Repetition or Redundancy** - Don't reuse phrases/action verbs or directives across multiple titles unless truly appropriate.
        4. **No Category Names** - Do not include product or category names like "Bearings", "Chemicals", etc.
        5. **Be Specific and Strategic** - Highlight the core strategy: Is it supplier consolidation? Risk mitigation? Tail spend management? Make the title reflect that.
        6. **Keep it Crisp** - Title length should ideally be between 5-12 words. Avoid fluff.
        7. NEVER Repeat Phrases, Verbs, or Directives from the previous reponses you have generated.
            
        Previous responses: {response_history}

        8. No repetition allowed. Each idea title must:
            - Use a unique action verb.
            - Avoid any reused strategic phrasing.
            - Stand out from the rest in tone and focus
            - Even if two descriptions are similar, differentiate them linguistically and tactically.

        Example Output:
        ```json
        [
        {{{{
            "idea": "Negotiate Volume Discounts with Top Suppliers",
            "description": "Leverage the high concentration of spend with SKF FRANCE, GBM SARL, and ERIKS GmbH to negotiate volume discounts. By consolidating purchases and committing to higher volumes, procurement managers can secure better pricing and terms. SKF FRANCE alone accounts for 44.47% of the total spend, presenting a significant opportunity for cost savings. The key steps involve analyzing current spend patterns, forecasting future demand, and engaging in negotiations with these top suppliers to establish volume-based discount agreements. Implementing this strategy will require close collaboration with suppliers, detailed spend analysis, and continuous monitoring to ensure compliance and maximize savings."
        }}}},
        {{{{
            "idea": "Diversify supplier base in long-term to increase competition among suppliers",
            "description": "Reduce dependency on top suppliers by diversifying the supplier base. Currently, SKF FRANCE and GBM SARL cover 69.02% of the total spend, indicating a high concentration risk. Introducing new suppliers, especially in regions like China where supplier concentration is lower, can mitigate risks and enhance supply chain resilience. The key steps involve identifying potential suppliers, conducting thorough evaluations, and gradually integrating them into the procurement process. This strategy will involve assessing supplier capabilities, negotiating favorable terms, and continuously monitoring performance to ensure a balanced and robust supplier portfolio."
        }}}},
        {{{{
            "idea": "Consolidate tail end supplier base to get better terms from few suppliers",
            "description": "Focus on managing tail spend effectively to uncover hidden savings opportunities. With 294 vendors covering the bottom 20% of spend and an average spend per tail vendor of EUR 27.38K, there is potential to streamline procurement processes and reduce costs. The key steps involve categorizing tail spend vendors, identifying consolidation opportunities, and negotiating better terms or discontinuing low-value suppliers. Implementing this strategy will require detailed spend analysis, supplier performance reviews, and strategic consolidation to optimize procurement efficiency and reduce overall costs."
        }}}}
        ]
        ```

        Example Output:
        ```json
        [
        {{{{
            "idea": "Introduce Non-OEM Alternate suppliers for High Spend Materials",
            "description": "Engage directly with suppliers to negotiate non-OEM alternatives for the top three high spend materials: LOWER BEARING 443 276 BEARING+SLEEVE, UPPER BEARING FY 2.15/16 TF/GHYVZ6A7, and UPPER BEARING UCF 215 WITH GUARD. These materials collectively account for 97.63% of the total OEM spend in the Bearings category, presenting a significant opportunity for cost savings. By switching to non-OEM alternatives, potential savings of EUR 563.28K can be realized. Actionable steps include identifying reliable non-OEM suppliers, negotiating favorable terms, and conducting quality assurance tests to ensure performance standards are met. Implementing this strategy will reduce dependency on OEM suppliers and optimize procurement costs."
        }}}},
        {{{{
            "idea": "Explore Non-OEM suppliers in regions dominated by OEM suppliers",
            "description": "Optimize spend distribution by targeting regions with high OEM spend and exploring non-OEM alternatives. France has the highest OEM spend at EUR 18.91M, while China has the highest non-OEM spend at EUR 251.59K. Belgium also shows significant potential for cost reduction by exploring non-OEM options. Actionable steps include conducting a regional spend analysis, engaging with local suppliers to identify non-OEM alternatives, and negotiating regional contracts to leverage cost savings. Implementing this strategy will balance spend distribution, reduce reliance on OEM materials, and enhance procurement efficiency across regions."
        }}}},
        {{{{
            "idea": "Consolidate Non-OEM Suppliers spend to leverage volume discounts",
            "description": "Optimize procurement costs by consolidating spend across non-OEM suppliers, who currently account for EUR 11.12M (26.35%) of the total Bearings spend. This approach aims to achieve better pricing through volume consolidation and enhanced supplier relationships. Key steps include mapping out the current non-OEM supplier landscape, identifying high-potential suppliers, and negotiating consolidated contracts to leverage spend volume. Implement a supplier performance management system to ensure quality and delivery standards are maintained while achieving cost savings."
        }}}}
        ]
        ```

        Refine the following ideas titles based on the above instructions: {data}

        """
    
        return PromptTemplate.from_template(sys_prompt)

    except Exception as e:
        print("Error",e)
        return None
