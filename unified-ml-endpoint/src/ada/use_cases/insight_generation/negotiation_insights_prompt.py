import json
import pandas as pd
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate


def classify_prompt(df_sample: pd.DataFrame) -> str:
    """
    Builds a prompt for the LLM that embeds a 2-row sample of the DataFrame,
    so it can infer for each column whether to use .sum() or .mean() when
    rolling up month-level data to year-level.
    """
    # Take exactly two rows (or fewer if df has [2)
    sample = df_sample
    # Convert to a JSON-serializable list of records
    sample_records = sample.to_dict(orient="records")
    
    prompt_template = f"""
        You are a data engineer. You need to decide, for each column in a monthly DataFrame sample, whether the correct pandas aggregation to roll up to yearly is `.sum()` or `.mean()`.

        Here is a 2-row snapshot of the data:

        {json.dumps(sample_records, indent=2)}

        Based on the values and common usage (for example, monetary/spend/savings fields should be summed, while rate or duration fields like days should be averaged), classify **each** column.

        **Output:** Return **only** a Python dict literal mapping column names to `"sum"` or `"mean"`, 
        
        for example:

        ```python
        {{
        "SPEND": "sum",
        "NUM_DAYS": "mean",
        "POTENTIALSAVINGS": "sum",
        "PAYMENT_COUNT": "sum",
        "PAYMENT_DAYS": "mean",
        "PRICE_ARBITRAGE": "sum"
        }}
        
        Do not include any other text or explanation.
        

        """
    return ChatPromptTemplate([SystemMessage(prompt_template)])


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
    - Step 1: Calculate if CHANGE_IN_SKU_PRICE_PERCENTAGE is less or more than CHANGE_IN_MARKET_PRICE_PERCENTAGE. The percentages will be in decimal but you are smart to find which is greater.
    - Step 2: Make the appropriate insight
        - If the SKU price increase is less than the market price increase, indicate that the supplier has outperformed the market — consider a favorable sourcing opportunity. (e.g., "Supplier [supplier name] increased unit price by X% vs market increase of Y% from past year for SKU [SKU name], indicating that the supplier offers favorable sourcing opportunities.") 
        - If the SKU price increase is greater than the market price increase, indicate that the supplier has overcharged relative to the market — this provides negotiation leverage. (e.g., “Supplier [supplier name] increased price by X% vs market increase of Y% from past year for SKU [SKU name] indicating that the supplier has overcharged relative to the market.”)

    Use this context to generate **insights**.

    Data: {data}
   
    Instructions:
    - Write insight for each material in data that support procurement negotiation with the supplier.
    - Always use percentage or numeric changes. Decimal values should be only two decimal places.
    - If the percentage is negatiive it means decreased, frame the insight such, without mentioning (-).
    - Do not fabricate data
    - Explicitly mention both percentage values in every insight (e.g., “Supplier [supplier name] increased unit price by X% vs market increase of Y% from past year for SKU [SKU name], indicating that the supplier offers favorable sourcing opportunities.”),(e.g., “Supplier [supplier name] increased price by X% vs market increase of Y% from past year for SKU ABC, which is more than the market increase indicating that the supplier has overcharged relative to the market.”), (e.g., “Supplier [supplier name] decreased price by X% vs market increase of Y% from past year for SKU ABC indicating that the supplier offers favourable sourcing opportunities.”), (e.g., “Supplier [supplier name] maintained price (do not mention percentage here, 0.0% doesn't make sense) vs market increase of Y% from past year for SKU ABC indicating that the supplier offers favourable sourcing opportunities.”).
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


def generate_spend_insights_prompt_v2(supplier, material,spend_data, currency_symbol,year) -> ChatPromptTemplate:
    """
    Generates a prompt template for negotiation-relevant spend insights.

    Args:
        spend_data (dict): Dictionary with key 'spend' containing list of spend records.

    Returns:
        ChatPromptTemplate: A LangChain chat prompt template ready for chaining.
    """
    
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
        Example: From supplier [SUPPLIER NAME], annual spend on [MATERIAL/SKU NAME] decreased/increased YoY between [PAST_YEAR] and [YEAR] by €<spend_variance_absolute> (<spend_variance_percentage>%) with a quantity drop/increase of <quantity_variance_absolute> units (<quantity_variance_percentage>%) and drop/increase in unit price (€<price_variance_absolute>/unit, <price_variance_percentage>%).
        Note: You must decide 'decreased/increased' and 'drop/increase' in the insight based of provided data, you will be given with all the placeholders above. Do not make up any number. Refre below data only.

        spend_price_volume_variance_data: {input_data['spend_price_volume_variance']}

    2. You MUST have a separate insight for each material:
        - Stating whether material is single-sourced or multi-sourced, spend by the supplier on that material and if multi sourced what is the average price across different suppliers.
        MUST FOLLOW example language for single-sourced material(STRICTLY USE THIS IF MATERIAL IS SINGLE SOURCED): The annual spend on [MATERIAL/SKU NAME] (which is single-sourced) from supplier [SUPPLIER NAME] is €XYZ.
        MUST FOLLOW example language for multi-sourced material(STRICTLY USE THIS IF MATERIAL IS MULTI SOURCED): The annual spend on [MATERIAL/SKU NAME] (which is multi-sourced) from supplier [SUPPLIER NAME] is €ABC. The average price from supplier [SUPPLIER NAME] is €GHJ/unit while the average price across suppliers for the same material is €KLP/unit.
        Refer below data only.
        
        single_multi_source_data: {input_data['single_multi_source_data']}

    NOTE: DO NOT MIX INFORMATION FROM POINT 1 AND POINT 2.

    General Guidelines:
        - YOU MUST TAKE THE EXACT PERIOD MENTIONED WITHIN THE DATA.
        - THERE SHOULD BE NO PLACEHOLDERS IN THE FINAL OUTPUT.
        - STRICT CONSTRAINT: DO NOT MENTION ANY VALUES FROM THE EXAMPLE
        - ALWAYS EXPLICITLY MENTION THE SUPPLIER AND MATERIAL NAME IN THE INSIGHT.
        - IF AN INSIGHT CAN'T BE MADE DUE TO NO DATA/ LACK OF DATA DO NOT MAKE IT. 
        - DO NOT INCLUDE NaN values in the insight at any cost. 
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
    SUPPLIER: {supplier}
    MATERIAL: {material}
    YEAR/PERIOD: {year}

    Expected Output:
    {{
    "spend": [
        "Insight with clear negotiation value here.",
        "Another leverage-point based insight."
        ]
    }}

    Only return the JSON. No other text or heading.
    """
    # prompt = prompt_template.replace("{input_data_json}", json.dumps(input_data, indent=2))
    return ChatPromptTemplate.from_messages([SystemMessage(content=prompt_template)])

def generate_additional_spend_insights_prompt(spend_without_po, supplier_ranking, top_business_units, top_materials, top_payment_terms, currency_symbol,supplier,category,year) -> ChatPromptTemplate:
    """
    Generates a prompt template for strategic supplier-level insights using business data.

    Args:
        summary_data (dict): Dictionary containing key supplier insights such as ranking, top materials, etc.

    Returns:
        ChatPromptTemplate: A LangChain chat prompt template ready for chaining.
    """

    prompt_template = f"""
    You are a senior procurement category manager preparing for strategic supplier reviews or negotiations. 
    Your task is to generate precise, numeric-backed insights from structured supplier data that highlight concentration, risk, and leverage opportunities.

    ------------------------------------------------------------------------------------------------

    Guidelines:

    - Use ONLY the structured input data to generate insights.
    - Output a JSON object like:
    {{
        "spend": [
            "Insight 1",
            "Insight 2",
            ...
        ]
    }}
    
    Insight Categories (each category must have its own separate insight — no mixing):

    1. **Supplier Ranking Insight**:
       - Clearly state the supplier’s rank in the category.
       - Include the supplier’s total spend, the total number of suppliers in that category, the percentage share of spend they represent, and the year.
       Example:
       "The supplier [SUPPLIER NAME] is ranked [X] out of [Y] suppliers in [PERIOD], contributing {currency_symbol}[TOTAL_SUPPLIER_SPEND] ([SUPPLIER_SPEND_PERCENTAGE]%) of the total annual spend for the category [CATEGORY NAME]."
       Use only the values from:
       supplier_ranking_data: {supplier_ranking}

    2. **Top SKUs Insight**:
       - State the top 3 SKUs by spend with their respective values.
       - Format: "The top SKUs procured from supplier [SUPPLIER NAME] in [PERIOD] are M1 ({currency_symbol}XM), M2 ({currency_symbol}YM) and M3 ({currency_symbol}ZM)."
       Use only the values from:
       top_SKU_data: {top_materials}

    3. **Top Business Units Insight**:
       - State the top 3 business units transacting with this supplier, along with their respective spend values.
       - Format: "The top business units procuring from supplier [SUPPLIER NAME] in [PERIOD] are BU1 ({currency_symbol}XM), BU2 ({currency_symbol}YM) and BU3 ({currency_symbol}ZM)."
       Use only the values from:
       top_business_units_data: {top_business_units}

    4. **Top Payment Terms Insight**:
       - Mention the top 3 payment terms and their associated spend and share.
       - Format: "The top payment terms for supplier [SUPPLIER NAME] in [PERIOD] are PT1 ({currency_symbol}XM: X%), PT2 ({currency_symbol}YM: Y%) and PT3 ({currency_symbol}ZM: Z%)."
       Use only the values from:
       top_payment_terms_data: {top_payment_terms}

    5. **Spend Without PO Insight**:
       - Clearly state the total value and share of spend that occurred without a PO.
       - Format: "The spend without purchase order for supplier [SUPPLIER NAME] in [PERIOD] is {currency_symbol}X (Y%)."
       Use only the values from:
       spend_without_po_data: {spend_without_po}

    GENERAL RULES:
    - YOU MUST TAKE THE EXACT PERIOD MENTIONED WITHIN THE DATA.
    - Each insight must be a separate point. NEVER COMBINE CATEGORIES INTO ONE INSIGHT.
    - DO NOT fabricate or infer missing information. Only generate insights for categories with complete data.
    - STRICTLY avoid placeholders like M1, BU1, PT1 unless those are present in the input data.
    - DO NOT use any sample numbers from these examples. Use the actual data only.
    - If no valid data is available for a given category, do not produce an insight for it.
    - Use scaled currency formatting: K (thousand), M (million), B (billion).
    - Always explicitly state the supplier name, year, and category.
    - Output must be pure JSON, with no additional commentary or headings.
    - Do not include NaN or null values in any insight.

    INPUT DATA:
    SUPPLIER: {supplier}
    CATEGORY: {category}
    YEAR/PERIOD: {year}

    Expected Output:
    {{
        "spend": [
            "Insight 1 here",
            "Insight 2 here",
            ...
        ]
    }}
    Only return the valid JSON structure shown above. Do not include explanations, commentary, or formatting.
    """
    return ChatPromptTemplate.from_messages([SystemMessage(content=prompt_template)])

def generate_additional_supplier_insights_prompt(top_single_sourced_materials,spend_increase_yoy_on_supplier,currency_symbol,supplier,category,year) -> ChatPromptTemplate:
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

    1. **Top Single-Sourced SKUs Insight**:
       - List the top 3 single-sourced SKUs with spend values.
       - Example: "The top single-sourced SKUs for supplier [SUPPLIER NAME] in [YEAR] are M1 ({currency_symbol}XM), M2 ({currency_symbol}YM), and M3 ({currency_symbol}ZM)."
       Use only the data from:
       top_single_sourced_materials_data: {top_single_sourced_materials}

    2. **Year-over-Year Spend Growth Insight**:
       - Capture supplier spend growth from the previous year to current year, both in absolute and percentage terms.
       - Example: "The spend for supplier [SUPPLIER NAME] has increased/decreased from {currency_symbol}X in [PAST_YEAR] to {currency_symbol}Y in [CURRENT_YEAR], a change of {currency_symbol}Z ([PERCENTAGE]% increase/decrease)."
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
    YEAR: {year}

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


def generate_supplier_insights_prompt_v2(supplier_data: dict, currency_symbol,supplier,year) -> ChatPromptTemplate:
    """
    Generates supplier-level insights focused on negotiation leverage using both KPI metrics and contextual opportunity/risk features.

    Args:
        supplier_data (dict): Dictionary with:
            - 'supplier': list of KPI records
            - 'features': dict of additional risk/opportunity indicators

    Returns:
        ChatPromptTemplate: LangChain-ready prompt template.
    """

    input_data_json = json.dumps(supplier_data, indent=2)

    prompt_template = f"""
    You are a senior procurement category manager preparing for a supplier negotiation or performance review.
    Your goal is to extract fact-based, numerically anchored insights that highlight negotiation leverage opportunities from structured KPI data.

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

    1. **Single-Source Spend Insight**:
       - Highlight the level of single-sourced spend and its potential impact on supply continuity or negotiation flexibility. If the single source spend is zero, do not make an insight.
       - Example: "Supplier [SUPPLIER NAME] has {currency_symbol}XM in single-source spend in [YEAR] which is XX% of its total annual spend OF {currency_symbol}Y, suggesting elevated supply dependency."
       Use only the data from:
       single_source_spend_data: {supplier_data['single_source_spend']}

    2. **Spend Per Invoice Insight**:
       - Identify high average spend per invoice and what it might imply for PO consolidation or transactional efficiency.
       - Example: "Supplier [SUPPLIER NAME] has an average spend per invoice of {currency_symbol}Y in [YEAR] compared to category average spend of {currency_symbol}YY, indicating a potential opportunity to reduce the number of invoice transactions through volume consolidation."
       Use only the data from:
       spend_per_invoice_data: {supplier_data['high_spend_low_invoice_risk']}

    3. **Multi-Source Spend Drop Insight**:
       - Capture reduction in multi-source spend and associated risk of increasing reliance on fewer suppliers.
       - Example: "Supplier [SUPPLIER NAME]'s multi-source spend dropped from {currency_symbol}X in [PAST_YEAR] to {currency_symbol}Y in [YEAR], a [PERCENTAGE]% decrease."
       Use only the data from:
       multi_source_drop_data: {supplier_data['multi_source_drop_risk']}

    GENERAL RULES:
    - You will make sure accurate K, M and B representations are captured. You will make sure data integrity is maintained and the numbers in the associated data is represented correctly in insights.
    - Each insight must be discrete and derived only from its respective dataset. DO NOT COMBINE categories or insights.
    - DO NOT fabricate data or fill missing values.
    - DO NOT include any placeholders in the final output.
    - Use scaled formatting: K (thousand), M (million), B (billion). e.g., {currency_symbol}1.4M.
    - Always explicitly mention the supplier name and year in each insight.
    - Omit insights for which required data is missing or not applicable.
    - Avoid subjective language (e.g., "significant", "high") unless backed by specific figures.
    - Format output strictly as valid JSON with no extra text or headings.

    INPUT DATA:
    SUPPLIER: {supplier}
    YEAR: {year}

    Expected Output:
    {{
        "supplier": [
            "Insight with negotiation relevance here.",
            "Another supplier-side insight here."
        ]
    }}
    Only return the valid JSON structure shown above. Do not include explanations, commentary, or formatting.
    """
    return ChatPromptTemplate.from_messages([SystemMessage(content=prompt_template)])


def generate_insights_prompt_v2(supplier,material,name, info,currency_symbol) -> ChatPromptTemplate:

    try:
        data = info[0]
        opportunity_column = info[1]
    except:
        data = info
        opportunity_column = 'N/A'

    try:
        prompt = f"""
        You are a senior procurement category manager preparing for a supplier negotiation. 
        You have been given {name} analytical data for supplier {supplier} and material {material}.

        Your task is to extract opportunity value from {opportunity_column} column in data and then 
        generate **only one high-value, actionable insight** that presents an opportunity for category manager
        to negotiate with the supplier {supplier}. 

        VERY IMPORTANT(MUST FOLLOW): NEVER MISS OUT ON OPPORTUNITY VALUE SPECIFIED IN {opportunity_column} column IN PROVIDED DATA, DO NOT MANIPULATE IT, PRESENT IT AS IT IS IN THE INSIGHT IN K,M AND B REPRESENTATION.
        MAKE INSIGHT EVEN IF THE OPPORTUNITY VALUE IS SMALL, DO NOT ROUND THEM OFF TO ZERO.

        **DO NOT PUT ZERO OPPORTUNITY ANYWHERE UNLESS IT IS MENTIONED IN {opportunity_column} column.**

        Insight must be based **strictly on the provided opportunity data** — do not assume, fabricate, or generalize 
        and should contain complete information.

        VERY IMPORTANT NOTE: AN INSIGHT WILL ALWAYS CONTAINS OPPORTUNITY VALUE from {opportunity_column} column in provided data ELSE IT WILL NOT BE CREATED.

        -----------------------------------------------------------------------------------------------------

        **INPUT DATA:**

        Analytics Name: {name}
        Opportunity Column: {opportunity_column}
        Supplier Name: {supplier}
        Material Name: {material}
        Data: {data}


        -----------------------------------------------------------------------------------------------------

        **NEGOTIATON LEVERS**:

            1. **Price Arbitrage**:
            - Include opportunity amount, no percentages allowed.
            - Example: Negotiate with [supplier name] for the material [SKU name] to leverage a price arbitrage opportunity of {currency_symbol}XYZ.

            2. **PCM (Parametric Cost Modelling)**:
            - Include total opportunity amount, no percentages allowed.
            - Example: Leverage Parametric Cost Modeling to negotiate a cost reduction with [supplier name] for the material [SKU name], unlocking an opportunity of {currency_symbol}XYZ.

            3. **Payment Terms** – Identify potential working capital benefit:
            - Include current avg. payment term vs. standard (e.g., 90 days)
            - Include opportunity value ,no percentages allowed.
            - Example: Negotiate with [supplier name] for the material [SKU name] to improve payment terms from 60 days to 90 days, unlocking a working capital opportunity of {currency_symbol}XYZ.

            4. **LPP (Linear Programming Price)** – Highlight misalignment with lowest available price:
            - Include opportunity value, no percentages allowed.
            - Example: For the material/SKU [SKU name] supplied by [supplier name], there is an opportunity to negotiate potential savings of {currency_symbol}XYZ based on LPP analysis.
            - Example: Leveraging the LPP misalignment with [supplier name] for the material [SKU name] can unlock potential savings of {currency_symbol}XYZ.
            - Example: Opportunity to negotiate with [supplier name] for the material [SKU name] to unlock potential savings of {currency_symbol}XYZ based on LPP analysis suggesting misalignment to the lowest available unit price.

            5. **Volume Discounts/ Early Payments** – Recommend leveraging volumes discounts/early payment discounts:
            - Include savings opportunity value/amount if available, not percentage.
            - Example: Negotiate with [supplier name] for the material [SKU name] to leverage volume discounts, unlocking a savings opportunity of {currency_symbol}XYZ.
            
            6. **Supplier Consolidation**
            - Include opportunity value, no percentages allowed.
            - Example: Negotiate with [supplier name] for the material [SKU name] to consolidate suppliers, unlocking a savings opportunity of {currency_symbol}XYZ.

            7. **HCC-LCC**
            - Include opportunity value, no percentages allowed.
            - Example: Negotiate with [supplier name] for the material [SKU name] to leverage HCC-LCC opportunity, unlocking a savings opportunity of {currency_symbol}XYZ.

            8. **OEM vs. Non-OEM**  
            - Include opportunity value, no percentages allowed.
            - Example: Negotiate with [supplier name] for the material [SKU name] to leverage OEM vs. Non-OEM opportunity, unlocking a savings opportunity of {currency_symbol}XYZ.

            9. **Web Price Benchmark**
            - Include opportunity value, no percentages allowed.
            - Example: Negotiate with [supplier name] for the material [SKU name] to leverage web price benchmark opportunity, unlocking a savings opportunity of {currency_symbol}XYZ.

        -----------------------------------------------------------------------------------------------------

        **FORMATTING RULES**:

        - Output must be a Python dictionary:
        {{ 
        "insights": [ "Insight which contains opportunity value"],
        "opportunity": total_numeric_value (extract raw value from {opportunity_column} column)
        }}

        Opportunity Key Instruction:
            - It represents raw total numeric value
            - Do not apply any scaling here, always give the raw value.
            - If insight contains opportunity in K, do the translation by multiplying it to 1000 (similarly do the translation for B (billion) and M (million) also). 
            - Example: If insights has opportunity 2.5K and 3.2K, opportunity key would contain 57000, and not 5.7. 
            - Example: If the insight has opportunity of $47.8, the opportunity key would contain 47.8. 
            - Example: If the insight has an opportunity of 1.57M, the opportunity key would contain 1570000.
            - **Make sure both insight and opportunity value are in sync.**


        **INSTRUCTIONS (MUST FOLLOW)**:
            - Do not create insights where opportunity is zero. Return an empty list in such case.
            - Never include percentages as opportunity in insight, include absolute value only from {opportunity_column} column.
            - Do not treat spend as opportunity ever.
            - Do not ignore small opportunities, they matter, do not round them off to zero.
            - Do not include any information in insight based on your interpretation.
            - Explicitly mention the supplier and material name in the insight.
            - Identify the negotiation lever based on analytics type - {name}
            - Make a single insight per analytic with the correct opportunity value.
            - Use {currency_symbol} as the currency and apply proper scaling: **K = thousand, M = million, B = billion**. Note: 1000K -> 1M, 1000M -> 1B
            - Currency symbol would always be placed in front.
            - **Insight would contain K,M and B represntation unlike opportunity key which contains raw value.**
            - Each insight should be 1–3 lines: precise, numeric, contextual, and immediately actionable
            - Do not fabrictate numbers or insights - rely strictly on the provided data.
            - Do not make any assumptions or extrapolations beyond the data provided and do not make up any information
            - Do not repeat any insight - duplicates and redundant insights are strictly prohibited.
            - Mention complete information in the insight, do not misreprsent the data. 
            - **Do not leave any placeholders in insights, always mention supplier name, material name and other details.**
            - Avoid vague language — insights should inform **what to negotiate, why it matters, and what value it unlocks**

        -----------------------------------------------------------------------------------------------------


        Tone & Style:
            - Practical and professional — suitable for procurement and category managers.
            - No generic phrases — be precise and contextual based on the data.
            - Avoid vague statements. Every insight should be data-backed and directly actionable.


        -----------------------------------------------------------------------------------------------------

        ONLY return the dictionary — do not add commentary, headers, or any extra text. Close keys and values with double quotes, and ensure the output is valid JSON format.

        """
        return ChatPromptTemplate([SystemMessage(prompt)])
    
    except Exception as e:
        print("Error", e)
        return None



