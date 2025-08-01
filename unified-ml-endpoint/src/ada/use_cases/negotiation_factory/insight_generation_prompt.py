from langchain_core.prompts import PromptTemplate
from numerize.numerize import numerize
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate
import json
from ada.utils.logs.logger import get_logger

log = get_logger("InsightGenerationPrompt")

def generate_insights_prompt_v2(name, info,currency_symbol) -> PromptTemplate:

    try:
        data = info[0]
        opportunity_column = info[1]
    except:
        data = info
        opportunity_column = 'N/A'

    try:
        prompt = f"""
        You are a senior procurement category manager preparing for a supplier negotiation. You have been given data for a **specific supplier and selected SKUs** across various analytics.

        Your task is to extract **only high-value, actionable insights** related to key negotiation levers. Every insight must be based **strictly on the provided data** — do not assume, fabricate, or generalize.

        If there is an opportunity, it means there is a potential for negotiation, it does not mean that supplier is the best supplier.

        -----------------------------------------------------------------------------------------------------

        **INCLUDE INSIGHTS ONLY IF THERE IS A NON-ZERO OPPORTUNITY.**

        **IF THERE IS SMALL OPPORTUNITY, YOU MUST NOT IGNORE IT, YOU MUST HAVE INSIGHTS FOR IT.**

        Your insights must fall within the following **negotiation lever categories**:

        NOTE: DO NOT INCLUDE ANY INFORMATION IN INSIGHT BASED ON YOUR INTERPRETATION. 
        
        NOTE:  REGION > PLANT > SUPPLIER > MATERIAL, THIS MEANS WHEN DATA CONTAINS PLANT COLUMN, OPPORTUNITY IS FOR THE SUPPLIER IN THAT SPECIFIC REGION/PLANT.

        1. **Price Arbitrage**:
        - Include opportunity amount not percentage 

        2. **PCM (Parametric Cost Modelling)**:
        - Include total opportunity amount not percentage

        3. **Payment Terms** – Identify potential working capital benefit:
        - Include current avg. payment term vs. standard (e.g., 90 days)
        - Include opportunity value not percentage

        4. **LPP (Linear Programming Price)** – Highlight misalignment with lowest available price:
        - Include opportunity value not percentage

        5. **Volume Discounts/ Early Payments** – Recommend leveraging volumes discounts/early payment discounts:
        - Include savings opportunity value/amount if available, not percentage.
        
        6. **General** – Make below three insights only. When calculating value for opportunity key here, YOU MUST give maximum value. 
        - For supplier [Supplier Name], top plants with opportunity are Plant1 (opportunity value), Plant2 (opportunity value) ...
        - For supplier [Supplier Name], top countries with opportunity are Country1 (opportunity value), Country2 (opportunity value) ...mention all countries.
        - For supplier [Supplier Name], top materials with opportunity are Material1 (opportunity value), Material2 (opportunity value) ...

        DO THE 6TH POINT INSTRUCTIONS ONLY WHEN ANALYTICS NAME IS 'GENERAL', FOR ALL OTHER ANALYTICS FOLLOW THE BASE GUIDELINES.

        -----------------------------------------------------------------------------------------------------

        **EXCLUDE** any insights related to (EXTREMELY IMPORTANT, DO NOT CREATE ANY INSIGHTS IF ANALYTICS IS ONE OF THE BELOW):
        - Supplier Consolidation
        - Low-Cost/High-Cost Country (LCC/HCC)
        - OEM vs. Non-OEM   

        -----------------------------------------------------------------------------------------------------

        **FORMATTING RULES**:

        - Output must be a Python dictionary:
        {{ 
        "insights": [ "Insight 1...", "Insight 2...", ... ],
        "opportunity": total_numeric_value 
        }}

        Opportunity Key Instruction:
            - It represents raw total numeric value
            - Do not apply any scaling here, always give the raw value.
            - If insight contains opportunity in K, do the translation by multiplying it to 1000 (similarly do the translation for B (billion) and M (million) also). 
            - Example: If insights has opportunity 2.5K and 3.2K, opportunity key would contain 57000, and not 5.7. 
            - Example: If the insight has opportunity of $47.8, the opportunity key would contain 47.8. 
            - Example: If the insight has an opportunity of 1.57M, the opportunity key would contain 1570000.
            - **Make sure both insight and opportunity value are in sync.**


        General Instructions:
            - Use {currency_symbol} as the currency and apply proper scaling: **K = thousand, M = million, B = billion**. Note: 1000K -> 1M, 1000M -> 1B
            - Currency symbol would always be placed in front.
            - Explicitly mention the supplier and material name in each insight. Extract the supplier and material name only from provided data.
            - **Insight would contain K,M andB represntation unlike opportunity key which contains raw value.**
            - Each insight should be 1–3 lines: precise, numeric, contextual, and immediately actionable
            - Use {opportunity_column} column to find opportunity values.
            - Do not fabrictate numbers or insights - rely strictly on the provided data
            - Do not make any assumptions or extrapolations beyond the data provided and do not make up any information
            - Do not repeat any insight - duplicates and redundant insights are strictly prohibited.
            - Each material with opportunity will have an insight, do not club them or summarize them in a single insight.
            - Mention complete information in the insight, do not misreprsent the data. 
            - **Do not leave any placeholders in insights, always mention supplier name and other.**
            - Do NOT include any insight with 0 or missing opportunity — if no opportunity exists, return:
            {{ "insights": [], "opportunity": 0 }}
            - Avoid vague language — insights should inform **what to negotiate, why it matters, and what value it unlocks**

        Tone & Style:
            - Practical and professional — suitable for procurement and category managers.
            - No generic phrases — be precise and contextual based on the data.
            - Avoid vague statements. Every insight should be data-backed and directly actionable.


        VERY VERY IMPORTANT: IF YOU MAKE UP ANY INFORMATION, YOU WILL BE TERMINATED IMMEDIATELY, DO NOT HALLUCINATE AND FOLLOW THE INSTRUCTIONS AT ALL COST.


        -----------------------------------------------------------------------------------------------------

        **INPUT DATA:**

        Analytics Name: {name}
        Opportunity Column (Except when analytics name is 'General', YOU MUST always pick opportunity value from this column): {opportunity_column} 
        Data: {data}

        -----------------------------------------------------------------------------------------------------

        ONLY return the dictionary — do not add commentary, headers, or any extra text. Close keys and values with double quotes, and ensure the output is valid JSON format.

        """
        return ChatPromptTemplate([SystemMessage(prompt)])
    
    except Exception as e:
        print("Error", e)
        return None

# def generate_insights_prompt_v2(name,data:dict) -> PromptTemplate:

#     try:

#         prompt = f"""
#         You are a procurement category manager with deep knowledge of supplier management, spend analytics, procurement, 
#         category analytics, and savings and opportunity levers. Your task is to provide clear, descriptive, and fact-based insights that help buyers, 
#         procurement, and category managers make informed, data-driven decisions. The insights must be actionable and not generic.

#         -----------------------------------------------------------------------------------------------

#         Guidelines for Response:

#         - VERY IMPORTANT: INSIGHT MUST ONLY USE THE SUPPORTING DATA PASSED.
#         - Output a dictionary with the following structure:
#             - "insights": a list of short, descriptive insight strings which have detailed granular information extracted from the data to give procurement managers a clear understanding of the situation.
#             - "opportunity": a numeric value representing the **raw opportunity amount** (do not apply any scaling like K, M, or B here).
#         - The overall output must be a dictionary.

#         Formatting Rules:
#         - Format insight text with currency scaling (K = thousands, M = millions, B = billions), default to EUR.
#         - Ensure each insight is clear, descriptive (1–3 lines), and includes specific numeric evidence (amounts, percentages, rankings, counts). 
#         - Explain what the insight means and why it matters — e.g., describe the gap, the savings potential, or the supplier concentration.
#         - Do not make insights which do not bring any value to category managers, only high impact insights are required.
#         - Percentages must be reasonable (avoid >100%, 0%, or negative).
#         - Do not fabricate numbers — rely strictly on the provided data.
#         - If insufficient data exists for an analytic, output an empty "insights" list and opportunity as 0.

#         Tone & Style:
#         - Practical and professional — suitable for procurement and category managers.
#         - No generic phrases — be precise and contextual based on the data.
#         - Avoid vague statements. Every insight should be data-backed and directly actionable.

#         Input Data:

#         Analytics Name: {name}
#         {data}

#         Format your response strictly as a dictionary like this:

#         {{
#             "insights": ["Descriptive insight with value and context.",...],
#             "opportunity": 583
#         }}

#         Example Output:

#         {{
#             "insights": ["The average payment terms for LOWER BEARING 443 276 BEARING+SLEEVE and UPPER BEARING UCF 215 WITH GUARD range between 63 to 73 days, compared to the industry benchmark of 90 days.", "Aligning LOWER BEARING 443 276 BEARING+SLEEVE and UPPER BEARING UCF 215 WITH GUARD with the 90-day industry benchmark, an estimated 14.18K EUR in working capital could have been unlocked in 2025 YTD alone.","Current Avg. Payment Term for LOWER BEARING 443 276 BEARING+SLEEVE is 63 days resulting in unrealized Working Capital Benefit of 11.78K EUR in 2025 YTD.",...],
#             "opportunity": 14182
#         }}

#         Only output the dictionary — do not add any explanation or text outside this structure. Make sure you understand the analytic name properly and then make insights by interpreting the data provided.
#         """

#         return ChatPromptTemplate([SystemMessage(prompt)])

#     except Exception as e:
#         print("Error",e)
#         return None
    
# def generate_spend_insights_prompt_v2(spend_data: dict) -> ChatPromptTemplate:
#     """
#     Generates a prompt template for spend insights (without opportunity value).

#     Args:
#         spend_data (dict): Dictionary with key 'spend' containing list of spend records.

#     Returns:
#         ChatPromptTemplate: A LangChain chat prompt template ready for chaining.
#     """
#     log.info("Generating spend insights prompt with input data of %d records.", len(spend_data.get("spend", [])))
#     input_data = spend_data

#     prompt_template = """
# You are a senior procurement category manager with expertise in spend analysis and supplier performance evaluation. 
# Your role is to generate precise, fact-based, and decision-supportive insights that procurement and sourcing teams can act on.

# ------------------------------------------------------------------------------------------------

# Guidelines for Response:

# - Focus ONLY on the analytic name provided (e.g., "spend") and the data shown in the input dictionary.
# - Your output must be a JSON with:
#     - "insights": a list of 2 to 5 short, clear, and **descriptive** insights specific to the data.

# Insight Writing Rules:
# - Scale large amounts (K = thousands, M = millions).
# - Every insight must reference a concrete value, trend, or gap from the data (e.g., “Spend increased by 57% from EUR 3.1M to EUR 4.9M”).
# - Use human-friendly formatting: “EUR 3.06M” not “3062885.7”.
# - Prioritize key themes: sudden changes in spend, unit price shifts, PO bypassing, demand volume shifts, sourcing risks.
# - Avoid vague ratio phrases (like "1.3x category average") — instead explain what that means in practical terms.
# - Never invent metrics or percentages. If a percentage can't be calculated safely from given fields, skip it.
# - If no material insights exist, return an empty insights list.

# Tone & Style:
# - Professional, concise, and factual — insights should sound like they came from a strategic sourcing manager.
# - Avoid fluffy or generic statements.
# - Be actionable: always hint at why the data point is important (e.g., non-PO risk, demand decline, volume drop, price escalation, etc.)

# Input Data Dictionary:

# {input_data_json}

# Expected Output Format:

# {{
#   "spend": {{
#     "insights": [
#       "Concrete, numeric-backed insight goes here.",
#       "Another insight describing a key change or risk."
#     ]
#   }}
# }}

# Only return the JSON structure — do not add any explanation or headings.
# """
#     prompt = prompt_template.replace("{input_data_json}", json.dumps(input_data, indent=2))
#     return ChatPromptTemplate.from_messages([SystemMessage(content=prompt)])

def generate_spend_insights_prompt_v2(spend_data: dict, currency_symbol) -> ChatPromptTemplate:
    """
    Generates a prompt template for negotiation-relevant spend insights.

    Args:
        spend_data (dict): Dictionary with key 'spend' containing list of spend records.

    Returns:
        ChatPromptTemplate: A LangChain chat prompt template ready for chaining.
    """
    log.info("Generating spend negotiation insights prompt with %d records.", len(spend_data.get("spend", [])))
    input_data = spend_data

    prompt_template = f"""
    You are a senior procurement category manager preparing for supplier negotiations. 
    Your task is to extract sharp, numeric-backed insights from spend data that give you leverage during negotiations.

    ------------------------------------------------------------------------------------------------

    Guidelines:

    - Focus only on the 'spend' analytic and the input data.
    - Output a JSON like:
    - "insights": Highly relevant negotiation-driving statements.
    - Note: Use associated data with each point only to make insights for that point.

    Negotiation Insight Rules:
    1. You MUST have an insight covering below points for each material:
        - Spend variance from past year to current year for each selected material
        - Price variance from past year to current year for each selected material
        - Quantity Variance from past year to current year for each selected material
        Example: From supplier [SUPPLIER NAME], spend on [MATERIAL/SKU NAME] decreased/increased YoY by €<spend_variance_absolute> (<spend_variance_percentage>%) with a quantity drop/increase of <quantity_variance_absolute> units (<quantity_variance_percentage>%) with change in unit price (€<price_variance_absolute>/unit, <price_variance_percentage>%).
        Note: You must decide 'decreased/increased' and 'drop/increase' in the insight based of provided data, you will be given with all the placeholders above. Do not make up any number. Refre below data only.

        spend_price_volume_variance_data: {input_data['spend_price_volume_variance']}

    2. You MUST have a separate insight for each material:
        - Stating whether material is single-sourced or multi-sourced, spend by the supplier on that material and if multi sourced what is the average price across different suppliers.
        MUST FOLLOW example language for single-sourced material(STRICTLY USE THIS IF MATERIAL IS SINGLE SOURCED): The spend on [MATERIAL/SKU NAME] (single-sourced) from supplier [SUPPLIER NAME] is €XYZ.
        MUST FOLLOW example language for multi-sourced material(STRICTLY USE THIS IF MATERIAL IS MULTI SOURCED): The spend on [MATERIAL/SKU NAME] (multi-sourced) from supplier [SUPPLIER NAME] is €ABC. The average price from supplier [SUPPLIER NAME] is €GHJ/unit while the average price across suppliers for the same material is €KLP/unit.
        Refer below data only.
        
        single_multi_source_data: {input_data['single_multi_source_data']}

    NOTE: DO NOT MIX INFORMATION FROM POINT 1 AND POINT 2.

    General Guidelines:
        - THERE SHOULD BE NO PLACEHOLDERS IN THE FINAL OUTPUT.
        - Always anchor insights in values, gaps, or trends (e.g., “Spend dropped 42% YoY” or “Unit price increased by 12%”).
        - Prioritize leverage points: price hikes, demand shifts, PO bypassing, low competition, volume consolidation potential.
        - Use scaled numbers (K = thousands, M = millions). Format like “EUR 2.4M”.
        - Ignore any patterns that are not negotiation-useful.
        - If no negotiation-worthy insight exists, return an empty list.
        - Avoid vague ratio phrases (like "1.3x category average") — instead explain what that means in practical terms.
        - Never invent metrics or percentages. If a percentage can't be calculated safely from given fields, skip it.
        - Use {currency_symbol} in the insights instead of hardcoding EUR.

    NOTE: DO NOT MISRERESENT INFROMATION/DATA, USE K(thousand), M (millions) and B (billions) to represent values. MAKE SURE YOU ARE USING THE CORRECT SCALING AT ALL COST.

    Tone & Style:
    - Strategic, analytical, negotiation-focused. Avoid fluff or raw reporting.
    - Never fabricate data or ratios.

    Input Data:
    {input_data}

    Expected Output:
    {{
    "spend": {{
        "insights": [
        "Insight with clear negotiation value here.",
        "Another leverage-point based insight."
        ]
    }}
    }}

    Only return the JSON. No other text or heading.
    """
    prompt = prompt_template.replace("{input_data_json}", json.dumps(input_data, indent=2))
    return ChatPromptTemplate.from_messages([SystemMessage(content=prompt)])


# def generate_supplier_insights_prompt_v2(supplier_data: dict) -> ChatPromptTemplate:
#     """
#     Generates a ChatPromptTemplate for supplier-level insights.

#     Args:
#         supplier_data (dict): Dictionary with key 'supplier' containing list of supplier records.

#     Returns:
#         ChatPromptTemplate: A LangChain chat prompt template ready for chaining.
#     """
#     log.info("Generating supplier insights prompt with input data of %d records.", len(supplier_data.get("supplier", [])))
#     input_data = supplier_data

#     prompt_template = """
# You are a procurement analyst tasked with deriving high-quality supplier-level insights from structured KPI data.

# ------------------------------------------------------------------------------------------------

# Guidelines for Response:

# - Focus exclusively on supplier-level KPIs in the input dictionary.
# - Output must be JSON with the following format:
#     - "insights": a list of 2 to 5 concise, data-backed, and actionable insights.

# Insight Writing Rules:
# - Use the currency mentioned in the data (usually found in a column like 'REPORTING_CURRENCY') instead of hardcoding EUR.
# - Use scaled values (K for thousands, M for millions).
# - Avoid vague wording. Every insight must cite a clear data point or trend (e.g., “Spend declined from EUR 4.1M to EUR 2.6M (-37%)”).
# - Emphasize themes like: PO bypass risk, spend concentration, sourcing risk, spend volatility, YoY contract/invoice/POnumber shifts, etc.
# - Don’t include raw data dump. Don’t invent ratios unless computable from given data.
# - Skip if no meaningful pattern or metric is identifiable.

# Tone:
# - Professional, precise, and suitable for senior procurement leadership.
# - Do NOT include any bullet points or headings outside JSON.

# Input Data:

# {input_data_json}

# Expected Output:

# {{
#   "supplier": {{
#     "insights": [
#       "Short, specific insight using numeric context.",
#       "Another fact-based insight with business relevance."
#     ]
#   }}
# }}

# Only return valid JSON. Do not add explanations or narrative outside the JSON structure.
# """
#     prompt = prompt_template.replace("{input_data_json}", json.dumps(input_data, indent=2))
#     return ChatPromptTemplate.from_messages([SystemMessage(content=prompt)])
# def generate_supplier_insights_prompt_v2(supplier_data: dict) -> ChatPromptTemplate:
#     """
#     Generates supplier-level insights focused on negotiation leverage.

#     Args:
#         supplier_data (dict): Dictionary with key 'supplier' containing list of supplier records.

#     Returns:
#         ChatPromptTemplate: A LangChain chat prompt template.
#     """
#     log.info("Generating negotiation-focused supplier insights from %d records.", len(supplier_data.get("supplier", [])))
#     input_data = supplier_data

#     prompt_template = """
# You are a procurement strategist preparing for supplier negotiation. 
# Use the structured KPI data to extract only those insights that help build leverage or negotiation pressure.

# ------------------------------------------------------------------------------------------------

# Guidelines:

# - Focus only on supplier-level KPIs.
# - Output must be:
#   - "insights": 2 to 5 focused, numeric-backed, negotiation-useful insights.

# Insight Writing Rules:
# - Include trends on spend concentration, PO policy violations, sourcing risk, or cost spikes.
# - Cite actual numbers. Use scaled values like “EUR 4.6M” or “27% drop”.
# - Emphasize facts that can justify a price challenge, reallocation, or contract revision.
# - Skip generic patterns with no negotiation impact.

# Tone:
# - Sharp, factual, and aligned to procurement negotiation mindset.
# - Never include narrative or raw data dump.

# Input:
# {input_data_json}

# Expected Output:
# {{
#   "supplier": {{
#     "insights": [
#       "Negotiation-relevant insight.",
#       "Another data-backed leverage point."
#     ]
#   }}
# }}

# Only output valid JSON. Do not include additional text.
# """
#     prompt = prompt_template.replace("{input_data_json}", json.dumps(input_data, indent=2))
#     return ChatPromptTemplate.from_messages([SystemMessage(content=prompt)])

# def generate_supplier_insights_prompt_v2(supplier_data: dict) -> ChatPromptTemplate:
#     """
#     Generates supplier-level insights focused on negotiation leverage using both KPI metrics and additional opportunity/risk features.

#     Args:
#         supplier_data (dict): Dictionary with keys:
#             - 'supplier': list of KPI records
#             - 'features': dict of supplementary negotiation signals

#     Returns:
#         ChatPromptTemplate: A LangChain chat prompt template.
#     """
#     log.info("Generating negotiation-focused supplier insights from %d supplier KPI records and %d feature blocks.",
#              len(supplier_data.get("supplier", [])), len(supplier_data.get("features", {})))

#     input_data_json = json.dumps(supplier_data, indent=2)
#     breakpoint()
#     prompt_template = f"""
# You are a procurement strategist preparing for supplier negotiation. 
# Your task is to generate actionable and numeric-backed insights that maximize leverage in the negotiation.

# ------------------------------------------------------------------------------------------------

# Data Provided:
# - "supplier": Structured KPI records such as spend, invoice count, PO coverage, sourcing mix.
# - "features": Contextual indicators that show savings potential or risk, such as:
#     - Top materials, plants, and regions by opportunity
#     - Single-source spend levels
#     - High spend per invoice (with low invoice volume)
#     - Drop in multi-source spend (dependency risk)

# Guidelines for Insight Generation:

# - Focus strictly on insights that support **negotiation leverage**.
# - Each insight must cite specific values or changes (e.g., “EUR 4.2M spend”, “35% drop in multi-source spend”).
# - Use scaled units: K (thousands), M (millions), and formatted numbers (e.g., EUR 2.1M).
# - Highlight facts that justify action: pricing challenge, contract renegotiation, sourcing shift, or performance concern.
# - Do not restate raw data. Derive insights from both KPIs and the contextual features.
# - If no meaningful leverage insight exists, return an empty list.

# Tone & Style:
# - Direct, professional, and negotiation-aligned — no fluff or generic comments.

# Input Data:
# {input_data_json}

# Expected Output Format:
# {{
#   "supplier": {{
#     "insights": [
#       "Negotiation-relevant insight.",
#       "Another data-backed leverage point."
#     ]
#   }}
# }}

# Only return valid JSON. Do not include explanations, bullet points, or headings.
# """
#     return ChatPromptTemplate.from_messages([SystemMessage(content=prompt_template)])

# def generate_supplier_insights_prompt_v2(supplier_data: dict) -> ChatPromptTemplate:
#     """
#     Generates supplier-level insights focused on negotiation leverage using both KPI metrics and contextual opportunity/risk features.

#     Args:
#         supplier_data (dict): Dictionary with:
#             - 'supplier': list of KPI records
#             - 'features': dict of additional risk/opportunity indicators

#     Returns:
#         ChatPromptTemplate: LangChain-ready prompt template.
#     """
#     log.info("Generating negotiation-focused supplier insights from %d KPI records and %d feature groups.",
#              len(supplier_data.get("supplier", [])), len(supplier_data.get("features", {})))

#     input_data_json = json.dumps(supplier_data, indent=2)

#     prompt_template = f"""
# You are a senior procurement strategist preparing for negotiation with a supplier. 
# Your job is to extract negotiation-ready insights based on the supplier's KPIs and contextual leverage indicators.

# ------------------------------------------------------------------------------------------------

# Input Data:
# - "supplier": Structured KPI records (e.g., spend, invoice count, contract activity, PO compliance, single-source exposure).
# - "features": Aggregated indicators relevant for negotiation, such as:
#     - Top materials, plants, or regions by savings opportunity
#     - High spend per invoice (inefficient invoicing)
#     - Significant drop in multi-source spend (dependency risk)
#     - Large share of single-source spend (supply continuity risk)

# Your Objective:
# Write 3 to 6 concise, numeric-backed insights that directly support a negotiation stance — such as requesting a price reduction, consolidating volume, reducing supply risk, or challenging contract terms.

# Each insight must:
# - Clearly support negotiation.
# - Be backed by specific values from the input (EUR amounts, % changes, counts, etc.).
# - Use scaled, readable formatting: K = thousands, M = millions (e.g., EUR 2.7M, 37% drop).
# - Highlight a leverage point that procurement can act on.

# Strict Rules:
# - Do **not** invent, extrapolate, or assume any additional data points or metrics.
# - Use only the data explicitly provided in the input.
# - Do not repeat raw data or write vague summaries.
# - Every insight should imply a clear negotiation action.
# - If no meaningful leverage exists, return an empty list.

# Examples of correct tone and framing:
# - "Multi-source spend dropped by EUR 13.09M — risk of overreliance should be addressed through re-sourcing."
# - "Top material savings of EUR 588K provide clear justification to renegotiate pricing."
# - "Average spend per invoice is EUR 448K — volume consolidation or PO compliance enforcement recommended."

# Input:
# {input_data_json}

# Expected Output Format:
# {{
#   "supplier": {{
#     "insights": [
#       "Negotiation leverage insight here.",
#       "Another strong, data-backed negotiation point."
#     ]
#   }}
# }}

# Only return the valid JSON structure shown above. Do not include explanations, commentary, or formatting.
# """
#     return ChatPromptTemplate.from_messages([SystemMessage(content=prompt_template)])

# def generate_supplier_insights_prompt_v2(supplier_data: dict) -> ChatPromptTemplate:
#     """
#     Generates supplier-level insights focused on negotiation leverage using both KPI metrics and contextual opportunity/risk features.

#     Args:
#         supplier_data (dict): Dictionary with:
#             - 'supplier': list of KPI records
#             - 'features': dict of additional risk/opportunity indicators

#     Returns:
#         ChatPromptTemplate: LangChain-ready prompt template.
#     """
#     log.info("Generating negotiation-focused supplier insights from %d KPI records and %d feature groups.",
#              len(supplier_data.get("supplier", [])), len(supplier_data.get("features", {})))

#     input_data_json = json.dumps(supplier_data, indent=2)

#     prompt_template = f"""
# You are a senior procurement strategist preparing for negotiation with a supplier. 
# Your job is to extract negotiation-ready insights based on the supplier's KPIs and contextual leverage indicators.

# ------------------------------------------------------------------------------------------------

# Input Data:
# - "supplier": Structured KPI records (e.g., spend, invoice count, contract activity, PO compliance, single-source exposure).
# - "features": Aggregated indicators relevant for negotiation, such as:
#     - Top materials, plants, or regions by savings opportunity
#     - Create one insight each mentioning the top five materials, plants, and regions by savings opportunity.
#     - High spend per invoice (inefficient invoicing)
#     - Significant drop in multi-source spend (dependency risk)
#     - Large share of single-source spend (supply continuity risk)

# Your Objective:
# Write 3 to 6 concise, numeric-backed insights that directly support a negotiation stance — such as requesting a price reduction, consolidating volume, reducing supply risk, or challenging contract terms.

# Each insight must:
# - Clearly support negotiation.
# - Be backed by specific values from the input (EUR amounts, % changes, counts, etc.).
# - Use scaled, readable formatting: K = thousands, M = millions (e.g., EUR 2.7M, 37% drop).
# - Highlight a leverage point that procurement can act on.
# - If the insight pertains to materials, **include the material name** explicitly.

# Strict Rules:
# - Do **not** invent, extrapolate, or assume any additional data points or metrics.
# - Use only the data explicitly provided in the input.
# - Do not repeat raw data or write vague summaries.
# - Every insight should imply a clear negotiation action.
# - If no meaningful leverage exists, return an empty list.

# Examples of correct tone and framing:
# - "Multi-source spend dropped by EUR 13.09M — risk of overreliance should be addressed through re-sourcing."
# - "Top material savings for 'UPPER BEARING FY 2.15/16 TF/GHYVZ6A7' of EUR 588K provide clear justification to renegotiate pricing."
# - "Average spend per invoice for 'UPPER BEARING UCF 215 WITH GUARD' is EUR 448K — volume consolidation or PO compliance enforcement recommended."

# Input:
# {input_data_json}

# Expected Output Format:
# {{
#   "supplier": {{
#     "insights": [
#       "Negotiation leverage insight here.",
#       "Another strong, data-backed negotiation point."
#     ]
#   }}
# }}

# Only return the valid JSON structure shown above. Do not include explanations, commentary, or formatting.
# """
#     return ChatPromptTemplate.from_messages([SystemMessage(content=prompt_template)])

# def generate_supplier_insights_prompt_v2(supplier_data: dict) -> ChatPromptTemplate:
#     """
#     Generates supplier-level insights focused on negotiation leverage using both KPI metrics and contextual opportunity/risk features.

#     Args:
#         supplier_data (dict): Dictionary with:
#             - 'supplier': list of KPI records
#             - 'features': dict of additional risk/opportunity indicators

#     Returns:
#         ChatPromptTemplate: LangChain-ready prompt template.
#     """
#     log.info("Generating negotiation-focused supplier insights from %d KPI records and %d feature groups.",
#              len(supplier_data.get("supplier", [])), len(supplier_data.get("features", {})))

#     input_data_json = json.dumps(supplier_data, indent=2)

#     # Generate insights for all top materials
#     top_materials = supplier_data.get("top_materials", [])
#     material_insights = [
#         f"Savings of EUR {material['TOTAL_OPPORTUNITY'] / 1000:.1f}K for '{material['MATERIAL']}' provides clear justification to renegotiate pricing."
#         for material in top_materials
#     ]

#     # Generate insights for plants and regions by aggregating material savings and specifying involved materials
#     prompt_template = f"""
# You are a senior procurement strategist preparing for negotiation with a supplier. 
# Your job is to extract negotiation-ready insights based on the supplier's KPIs and contextual leverage indicators.

# ------------------------------------------------------------------------------------------------

# Input Data:
# - "supplier": Structured KPI records (e.g., spend, invoice count, contract activity, PO compliance, single-source exposure).
# - "features": Aggregated indicators relevant for negotiation, such as:
#     - Top materials, plants, or regions by savings opportunity
#     - High spend per invoice (inefficient invoicing)
#     - Significant drop in multi-source spend (dependency risk)
#     - Large share of single-source spend (supply continuity risk)

# Your Objective:
# Write 3 to 6 concise, numeric-backed insights that directly support a negotiation stance — such as requesting a price reduction, consolidating volume, reducing supply risk, or challenging contract terms.

# Each insight must:
# - Clearly support negotiation.
# - Be backed by specific values from the input (EUR amounts, % changes, counts, etc.).
# - Use scaled, readable formatting: K = thousands, M = millions (e.g., EUR 2.7M, 37% drop).
# - Highlight a leverage point that procurement can act on.
# - Aggregated insights for regions and plants should include all relevant materials under the respective region or plant, listing **all material names** involved.

# Strict Rules:
# - Do **not** invent, extrapolate, or assume any additional data points or metrics.
# - Use only the data explicitly provided in the input.
# - Do not repeat raw data or write vague summaries.
# - Every insight should imply a clear negotiation action.
# - If no meaningful leverage exists, return an empty list.

# Examples of correct tone and framing:
# - "Total material savings of EUR 13.09M across materials for region 'France' — renegotiate pricing for 'UPPER BEARING FY 2.15/16 TF/GHYVZ6A7', 'LOWER BEARING 443 276 BEARING+SLEEVE', etc."
# - "Savings of EUR 588K for 'UPPER BEARING FY 2.15/16 TF/GHYVZ6A7' provide clear justification to renegotiate pricing."
# - "Savings of EUR 1.2M across all plants — renegotiate pricing for materials including 'UPPER BEARING FY 2.15/16 TF/GHYVZ6A7', 'LOWER BEARING 443 276 BEARING+SLEEVE', etc."

# **Instructions**:
# 1. **For top regions**: Aggregate the savings for all materials within each region and provide a **single insight** for each region, **listing all materials** involved, along with the total material savings.
# 2. **For top plants**: Aggregate the savings for all materials within each plant and provide a **single insight** for each plant, **listing all materials** involved, along with the total material savings.
# 3. **For top materials**: Generate an insight for each material individually, as you have done for individual items.

# Input:
# {input_data_json}

# Expected Output Format:
# {{
#   "supplier": {{
#     "insights": [
#       {',\n      '.join([f'"{insight}"' for insight in material_insights])}
#     ]
#   }}
# }}

# Only return the valid JSON structure shown above. Do not include explanations, commentary, or formatting.
# """
#     return ChatPromptTemplate.from_messages([SystemMessage(content=prompt_template)])


def generate_supplier_insights_prompt_v2(supplier_data: dict, currency_symbol) -> ChatPromptTemplate:
    """
    Generates supplier-level insights focused on negotiation leverage using both KPI metrics and contextual opportunity/risk features.

    Args:
        supplier_data (dict): Dictionary with:
            - 'supplier': list of KPI records
            - 'features': dict of additional risk/opportunity indicators

    Returns:
        ChatPromptTemplate: LangChain-ready prompt template.
    """
    log.info("Generating negotiation-focused supplier insights from %d KPI records and %d feature groups.",
             len(supplier_data.get("supplier", [])), len(supplier_data.get("features", {})))

    input_data_json = json.dumps(supplier_data, indent=2)

    prompt_template = f"""
    You are a senior procurement strategist preparing for negotiation with a supplier. 
    Your job is to extract negotiation-ready insights based on the supplier's KPIs and contextual leverage indicators.

    ------------------------------------------------------------------------------------------------

    Input Data:
    - "supplier": Structured KPI records (e.g., spend, invoice count, contract activity, PO compliance, single-source exposure).
    - "features": Aggregated indicators relevant for negotiation, such as:
        - Spend per invoice (if it is high, might indicate inefficient invoicing)
        - Significant drop in multi-source spend (dependency risk)
        - Large share of single-source spend (supply continuity risk)

    Your Objective:
    Write 3 to 5 concise, numeric-backed insights for the supplier that directly support a negotiation stance. Each insight should focus on one of the following aspects:
    - **Single-source spend** (e.g., amount and its potential risk)
    - **Spend per invoice** (e.g., amount per invoice and suggestions for volume consolidation or PO compliance)
    - **Multi-source spend drop risk** (e.g., the drop in multi-source spend and recommendations to reduce supplier dependence)

    Each insight must:
    - Be **clear** and **direct**, highlighting the negotiation leverage.
    - Include **numeric values** from the input data (EUR amounts, % changes, counts, etc.).
    - Use **scaled** formatting: K = thousands, M = millions (e.g., EUR 2.7M, 37% drop).
    - Focus on actionable points that can guide procurement decisions.
    
    For example:
    - "For supplier [Supplier Name], the **single-source spend** of EUR [Amount] is relatively high and should be monitored for future dependency risks."

    Strict Rules:
    - Make sure the numbers are consistent across insights and do not mismatch with each other. 
    - Do **not** invent, extrapolate, or assume any additional data points or metrics.
    - Use **only the data explicitly provided** in the input.
    - Do not **repeat raw data** or write vague summaries.
    - Every insight should imply a **clear negotiation action**.
    - If no meaningful leverage exists, return an empty list.
    - use currency symbol {currency_symbol} in the insights in displaying any figures.
    - Make sure you are doing the scaling correctly, 1,000 -> K, 1,000,000 -> M and so on. It is very important to do this correctly, else wromg information would be presented.
    - 1000K -> 1M.


    Input:
    {input_data_json}

    Expected Output Format:
    {{
    "supplier": {{
        "insights": [
        "Negotiation leverage insight here.",
        "Another strong, data-backed negotiation point."
        ]
    }}
    }}

    Only return the valid JSON structure shown above. Do not include explanations, commentary, or formatting.
    """
    return ChatPromptTemplate.from_messages([SystemMessage(content=prompt_template)])


def generate_market_insight_summary_prompt_v1(data: dict) -> ChatPromptTemplate:
    """
    Generates negotiation-relevant market insights for a supplier based on market trends and full supplier features.

    Args:
        data (dict): Includes:
            - market_insights: List[str]
            - supplier_name: str
            - category_name: str
            - supplier_features: dict (materials, regions, invoice risk, etc.)

    Returns:
        ChatPromptTemplate
    """
    insights = "\n".join([f"- {i}" for i in data.get("market_insights", [])])
    supplier = data.get("supplier_name", "")
    category = data.get("category_name", "")
    features = data.get("supplier_features", {})

    material_list = [m["MATERIAL"] for m in features.get("top_materials", []) if "MATERIAL" in m]
    region_list = [r["COUNTRY"] for r in features.get("top_regions", []) if "COUNTRY" in r]
    plant_list = [p["PLANT"] for p in features.get("top_plants", []) if "PLANT" in p]

    context_lines = []
    if material_list:
        context_lines.append(f"Top materials used: {', '.join(material_list)}.")
    if region_list:
        context_lines.append(f"Top regions: {', '.join(region_list)}.")
    if plant_list:
        context_lines.append(f"Top plants: {', '.join(plant_list)}.")

    supplier_context = " ".join(context_lines) if context_lines else "No material, plant, or region context available."

    prompt_template = f"""
You are a procurement strategist preparing for negotiation with supplier "{supplier}" in the "{category}" category.

You are given:
- Market trends related to cost drivers like metals or commodities.
- Supplier-level context including materials used, regions/plants involved, and risk signals.

Use this context to generate **negotiation-ready insights** by linking market trends to supplier exposure.

Supplier Context:
{supplier_context}

Market Insights:
{insights}

Instructions:
- Write 2 to 5 market-based insights that support procurement negotiation with the supplier.
- Clearly connect market trends (e.g., raw material movement) to supplier's known cost structure or regional footprint.
- Use percentage or numeric changes where available.
- Do not fabricate links — only use materials/regions explicitly mentioned.
- Avoid raw restatement. Each insight must justify a negotiation angle (e.g., price challenge, timing advantage, re-sourcing leverage).

Output format:
{{
  "market": [
    "Negotiation leverage from market trend 1.",
    "Negotiation leverage from market trend 2."
  ]
}}

Return only this JSON structure — no explanations or formatting.
"""
    return ChatPromptTemplate.from_messages([SystemMessage(content=prompt_template)])



def generate_market_insight_summary_prompt_v2(data: dict) -> ChatPromptTemplate:
    """
    Generates negotiation-relevant market insights for a supplier based on market trends and full supplier features.

    Args:
        data (dict): Includes:
            - market_insights: List[str]
            - supplier_name: str
            - category_name: str
            - supplier_features: dict (materials, regions, invoice risk, etc.)

    Returns:
        ChatPromptTemplate
    """
    
    prompt_template = f"""
    You are a procurement strategist preparing for negotiation and you are tasked to generate one market insight per material
    which shows market vs actual price variance of material year-on-year (YoY).

    You are provided with data containing the following fields:
    - supplier
    - category
    - sku or material
    - CHANGE_IN_SKU_PRICE_PERCENTAGE
    - CHANGE_IN_MARKET_PRICE_PERCENTAGE

    **VERY IMPORTANT NOTE**:
    - Step 1: Calculate if CHANGE_IN_SKU_PRICE_PERCENTAGE is less or more than CHANGE_IN_MARKET_PRICE_PERCENTAGE. The percentages will be in decimal but you are smart ton fimnd which is greater.
    - Step 2: Make the appropriate insight
        - If the SKU price increase is less than the market price increase, indicate that the supplier has outperformed the market — consider a favorable sourcing opportunity. (e.g., “Supplier [supplier name] increased price by X% vs market Y% for SKU ABC, indicating that the supplier offers favorable sourcing opportunities.”) 
        - If the SKU price increase is greater than the market price increase, indicate that the supplier has overcharged relative to the market — this provides negotiation leverage. (e.g., “Supplier [supplier name] increased price by X% vs market Y% for SKU ABC indicating that the supplier has overcharged relative to the market.”)

    Use this context to generate **insights**.

    Data: {data}
   
    Instructions:
    - Write insight for each material in data that support procurement negotiation with the supplier.
    - Always use percentage or numeric changes.
    - If the percentage is negatiive it means decreased, frame the insight such, without mentioning (-).
    - Do not fabricate data
    - Explicitly mention both percentage values in every insight (e.g., “Supplier [supplier name] increased price by X% vs market Y% for SKU ABC, which is less than the market increase indicating that the supplier offers favorable sourcing opportunities.”),(e.g., “Supplier [supplier name] increased price by X% vs market Y% for SKU ABC, which is more than the market increase indicating that the supplier has overcharged relative to the market.”), (e.g., “Supplier [supplier name] decreased price by X% vs market Y% for SKU ABC indicating that the supplier offers favourable sourcing opportunities.”), (e.g., “Supplier [supplier name] maintained price (do not mention percentage here, 0.0% doesn't make sense) vs market Y% for SKU ABC indicating that the supplier offers favourable sourcing opportunities.”).
    - Use only the actual data provided — do not fabricate or estimate any values.
    - Never leave any placeholders.
    - If no data is passed, give an empty list.
    - Write each insight in a clear, professional tone, focused on procurement strategy (e.g., negotiation opportunity, supplier efficiency, potential volume increase).
    - Provide only one actionable insight per material.

    Output format:
    {{
    "market": [
        "insight1",
        "insight2"
    ]
    }}

    Return only this JSON structure — no explanations or formatting.
    """
    return ChatPromptTemplate.from_messages([SystemMessage(content=prompt_template)])


def generate_additional_supplier_insights_prompt(top_single_sourced_materials,spend_increase_yoy_on_supplier,currency_symbol,supplier,category) -> ChatPromptTemplate:
    """
    Generates a prompt template for risk- and leverage-focused supplier insights.

    Args:
        risk_data (dict): Dictionary with keys covering sourcing concentration, risk exposure, revenue and profit change.

    Returns:
        ChatPromptTemplate: A LangChain chat prompt template ready for chaining.
    """

    prompt_template = f"""
    You are a senior procurement category manager preparing for a supplier negotiation or strategic review.  
    Your goal is to extract fact-based, numerically anchored insights that highlight supplier-side risk, concentration, and leverage opportunities.

    ------------------------------------------------------------------------------------------------

    Guidelines:

    - Focus ONLY on the provided structured data to derive insights.
    - Output a JSON object like:
    {{
        "supplier": [
            "Insight 1",
            "Insight 2",
            ...
        ]
    }}
    Only return the valid JSON structure shown above. Do not include explanations, commentary, or formatting.

    Insight Categories (Each must be a separate insight):

    1. **Top Single-Sourced Materials Insight**:
       - List the top 3 single-sourced materials with spend values.
       - Example: "The top single-sourced materials for supplier [SUPPLIER NAME] in [YEAR] are M1 ({currency_symbol}XM), M2 ({currency_symbol}YM), and M3 ({currency_symbol}ZM)."
       Use only the data from:
       top_single_sourced_materials_data: {top_single_sourced_materials}

    2. **Year-over-Year Spend Growth Insight**:
       - Capture supplier spend growth from the previous year to current year, both in absolute and percentage terms.
       - Example: "The spend for supplier [SUPPLIER NAME] has increased from {currency_symbol}X in [PAST_YEAR] to {currency_symbol}Y in [CURRENT_YEAR], a change of {currency_symbol}Z ([PERCENTAGE]% increase)."
       Use only the data from:
       spend_increase_yoy_on_supplier_data: {spend_increase_yoy_on_supplier}

    GENERAL RULES:
    - Each insight must be discrete and derived only from its respective dataset. DO NOT COMBINE categories or insights.
    - DO NOT fabricate data or fill missing values.
    - DO NOT include any placeholders in the final output.
    - Avoid use of terms like "significant" or "high" without quantitative backing.
    - DO NOT copy sample values — use only the data provided.
    - Use scaled formatting: K (thousand), M (million), B (billion). e.g., {currency_symbol}78.5M.
    - Always explicitly mention supplier name and year in each insight.
    - Omit insights for which required data is missing or not applicable.
    - Format output strictly as valid JSON with no extra text or headings.

    INPUT DATA:
    SUPPLIER: {supplier}
    CATEGORY: {category}

    Expected Output:
    {{
        "supplier": [
            "Insight with negotiation relevance here.",
            "Another supplier-side risk insight here."
        ]
    }}
    Only return the valid JSON structure shown above. Do not include explanations, commentary, or formatting.
    """
    return ChatPromptTemplate.from_messages([SystemMessage(content=prompt_template)])
