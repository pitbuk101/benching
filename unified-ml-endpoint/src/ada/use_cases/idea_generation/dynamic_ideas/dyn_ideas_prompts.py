"""Prompts for Dynamic Ideas"""

from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.messages import SystemMessage
import json
import pandas as pd


def classify_prompt(df_sample: pd.DataFrame) -> str:
    """
    Builds a prompt for the LLM that embeds a 2-row sample of the DataFrame,
    so it can infer for each column whether to use .sum() or .mean() when
    rolling up month-level data to year-level.
    """
    # Take exactly two rows (or fewer if df has <2)
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
        "PAYMENT_DAYS": "mean"
        }}
        ```
        Do not include any other text or explanation.
        

        """
    return ChatPromptTemplate([SystemMessage(prompt_template)])


def get_question_classifier_prompt() -> PromptTemplate:
    """
    Creates a prompt template for classifying user input as ideas, opportunity or others
    """
    prompt_template = """
    You are a Procurement domain assistant to a Category Manager (the user).
    Your task is to classify the given input from the user into one of four labels:
    "ideas", "opportunity", "objectives" or "others".

    Carefully read the instructions below to understand the scope of each label:

    - "ideas":
      Questions specifically requesting next best actions, recommendations, or strategies for suppliers, SKUs, analytics.
      Few examples -
      1. What are the recommendations for Supplier X?
      2. Suggest some strategies from LCC analytics?

      User inputs like - how do I implement this idea? is not in "ideas" scope, classify it as "others"
      Also, user inputs like "What strategies can we use to improve supplier performance?" which do not have reference
      to any suppliers, SKUs, analytics  are not in "ideas" scope

    - "objectives":
      Questions specifically requesting objectives for suppliers, SKUs, analytics. If any user query has "objectives" keyword, it is 
      an indicator to classify the given input from the user as "objectives".
      Few examples -
        1. What are the objectives for supplier X?
        2. Tell me about the objectives for supplier abc where sku is 123?

    - "opportunity":
      Questions specifically requesting savings opportunities , cost reduction, optimization potential for suppliers,
      SKUs, analytics.
      Few examples -  What is the savings potential for Supplier Z?
      Tell the optimizations for SKU 123?

      User inputs like "How do I act upon this opportunity?" is not in "opportunity" scope, classify it as "others".

    - "others":
      Captures all other types of questions or inputs that do not fit into the "ideas", "objectives" or "opportunity" categories.

    Here is the chat history for context:
    {chat_history}

    Here is the user's input:
    {question}

    Based on the chat history and the instructions provided, classify the user input by returning only one label: "ideas",
    "opportunity", "objectives", or "others". Do not classify as anything other than these four labels else you will be penalised and terminated.
    
    """
    return PromptTemplate(input_variables=["user_q", "chat_history"], template=prompt_template)    

def create_objectives_prompt() -> PromptTemplate:

    prompt_template = """

    You are a procurement strategy expert for category {category}, advising on negotiations with {supplier}.  
    Using the analytics and data provided below, generate 3 clear and concise negotiation objectives that focus on optimizing commercial 
    terms such as payment terms, pricing, volume leverage, discounts, and any other strategic levers surfaced in the data.

    Instructions for Output:

    - Structure the response strictly in the JSON format provided below.
    - Each objective must be unique and based on specific insights or opportunities derived from the available analytics.
    - Do not repeat objectives or use generic advice.
    - Each objective must contain:
    - A Summary: Brief and factual overview of the current supplier/SKU terms, benchmarks, or inefficiencies that signal opportunity.
    - Saving Opportunities: List 2-3 key SKUs, categories, or levers. Use available data to indicate current vs. target terms, and quantify value (e.g., € savings, DPO improvement, % optimization).
    - Actions: Recommend 1-2 strategic procurement actions. Focus on what should be changed and why, with measurable outcomes.
    - Use a professional tone appropriate for internal procurement strategy documents.
    - Ensure the JSON is valid, parsable, and does not include any explanations or markdown.

    Input Data:

    Supplier: {supplier}
    Category: {category}
    Analytics: {additional_data}
    Currency: {currency}

    ** VERY IMPORTANT: Retain the currency symbol (EUR,USD) and unit (K, M).**

    NOTE: **You must structure/frame your response in a top-down approach, starting with the highest opportunity and then going down to the next best opportunities in terms of impact and value.**

    Output JSON Format (Strict):

    {{{{
    "objectives": [
        {{{{
        "id": 0,
        "objective": "Summary:\\n[...current state and benchmarks...]\\n\\nSaving opportunities:\\n[...SKU-based details with metrics...]\\n\\nActions:\\n[...specific, results-driven changes...]",
        "objective_type": "[e.g., Payment Terms, Price Reduction, Volume Leverage, etc.]",
        "objective_reinforcements": [],
        "list_of_skus": [
            "[SKU 1]",
            "[SKU 2]",
            "[...]"
        ]
        }}}},
        {{{{
        "id": 1,
        "objective": "Summary:\\n[...]\\n\\nSaving opportunities:\\n[...]\\n\\nActions:\\n[...]",
        "objective_type": "[...]",
        "objective_reinforcements": [],
        "list_of_skus": [
            "[SKU 1]",
            "[SKU 2]",
            "[...]"
        ]
        }}}},
        {{{{
        "id": 2,
        "objective": "Summary:\\n[...]\\n\\nSaving opportunities:\\n[...]\\n\\nActions:\\n[...]",
        "objective_type": "[...]",
        "objective_reinforcements": [],
        "list_of_skus": [
            "[SKU 1]",
            "[SKU 2]",
            "[...]"
        ]
        }}}}
    ]
    }}}}

    """

    return PromptTemplate(template=prompt_template,input_variables={"supplier","category","additional_data"})

def get_history_based_ner_prompt(query) -> PromptTemplate:

    """
    Generates a prompt template for extracting supplier, analytics, plant, region and SKU names from given text data.

    Args:
        analytics_list (list): List of analytics names to be used in the prompt

    Returns:
        PromptTemplate: A template for the prompt to extract supplier and SKU names.
    """

    try:

        sys_prompt = f"""

        You are an intelligent name-entity-extraction assistant bot.
        Your task is to extract the region, plant, supplier, and sku names from the user query by following the below instructions -

        Extraction-Instructions:
            1. Entity Types:
                - region: Refers to the name of the region or location.
                - plant: Refers to the name of the plant or facility.
                - supplier: Refers to the name of the supplier or vendor.
                - sku: Refers to the name of the SKU or material.
            2. Region, Plant, Supplier and SKU names may or may not be present in the text.
            3. If the text doesn't contains Region, Plant, Supplier or SKU names, do not include that respective entity in the final output.

        RESPONSE FORMAT :

        Must be valid JSON (list of dicts) response in the below format -

        [
            {{{{
                "entity": "region",
                "value": ["region1","region2","region3"...], 
                "type": "name" //can only be a name
            }}}},
            {{{{
                "entity": "plant",
                "value": ["plant1","plant2","plant3"...], 
                "type": "name" //can only be a name
            }}}},
            {{{{
                "entity": "supplier",
                "value": ["supplier1","supplier2","supplier3"...], 
                "type": "name" //can only be a name
            }}}},
            {{{{
                "entity": "sku",
                "value": ["sku1","sku2","sku3",...], 
                "type": "name" //can only be a name
            }}}}
        ]

        NOTE:
            1. The comments are only for reference, dont use them in output.
            2. IMPORTANT: ONLY RETURN JSON object in response without any additional text or explanations or any
            formatting like markdown or backticks.

        You can refer to the below examples:

        Examples :

            Input: "What are the payment terms for Faber Industries ? "
            Output: 
            [
                {{{{
                    "entity": "supplier",
                    "value": ["Faber Industries"], 
                    "type": "name"
                }}}}
            ]

            Input: "Does FORGED RING SA-105N has the highest price variance ?"
            Output: 
            [
                {{{{
                    "entity": "sku",
                    "value": ["FORGED RING SA-105N"], 
                    "type": "name"
                }}}}
            ]

            Input: "What is the total opportunity for plant Complex Alloy Solutions(PTY) in region South Africa?"
            Output: 
            [
                {{{{
                    "entity": "plant",
                    "value": ["Complex Alloy Solutions(PTY)"], 
                    "type": "name"
                }}}},
                {{{{
                    "entity": "region",
                    "value": ["South Africa"], 
                    "type": "name"

                }}}}
            ]

            User : Extract region, plant, supplier and sku for - {query}

        """

        return PromptTemplate.from_template(sys_prompt)


    except Exception as e:
        print("Error",e)
        return None
    

def question_rephraser_prompt() -> ChatPromptTemplate:
    """
    Rephrases a user's question based on relevant chat history.

    Returns:
        ChatPromptTemplate: A template for rephrasing questions based on chat history.
    """
    system_prompt = """You are an intelligent assistant designed to rephrase questions based on \
    relevant chat history.
    Your task is to rephrase the user's question only if the chat history provides
    additional context that is directly relevant to the question.
    If the chat history is irrelevant to the user's question, return the original question unmodified.
    """
    user_prompt = """
    Instructions:
    1. Rephrase Condition: Rephrase the user's question only if the chat history provides \
    relevant context to clarify or expand on the question.
    2. Return Condition: If the chat history does not provide relevant context, \
    return the question exactly as it is.
    3. Output Format: Response must be only a JSON object with the key "rephrased_question" \
    without any markdown formatting
    or enclosing backticks. DO NOT return any additional text or explanations.

    Input:
    - User Question: {question}
    - Chat History: {chat_history}

    Example 1 (Relevant Chat History):
    - User Question: What are the recommendations for this SKU?
    - Chat History: [
        ("What is source ai?", "SourceAI is a platform that offers various \
        features to assist procurement professionals."),
        ("Which SKUs am I overpaying the most on in category X?",
            "The calculation is done for category Bearings for the current year.
            The SKUs you are overpaying the most is PDR BEARING 438155 DWG 272460 \
            with overpaid amount of EUR 2,787.83 and grouped spend of EUR 2,820,280.32.")
    ]
    Output:
    {{
        "rephrased_question": "What are the recommendations for SKU PDR BEARING 438155 DWG 272460 which has
        overpaid amount of EUR 2,787.83 and grouped spend of EUR 2,820,280.32.?"
    }}
    Example 2 (Irrelevant Chat History):
    - User Question: What are the recommendations for Supplier X?
    - Chat History: [
        ("Hi, How are you?", "Hello! I'm doing well. How can I assist you with your \
        Bearings category today?"),
        ("What is source ai?", "SourceAI is a platform that offers various features to \
        assist procurement professionals."),
    ]
    Output:
    {{
        "rephrased_question": "What are the recommendations for Supplier X?"
    }}
    """
    return ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", user_prompt),
        ],
    )


# def create_dynamic_qna_prompt() -> ChatPromptTemplate:
#     """
#     Creates a prompt template for generating dynamic QnA responses.

#     Returns:
#         ChatPromptTemplate: A template for generating dynamic QnA responses.
#     """
#     # TODO: add to sys prompt - analytics glossary, high level meaning
#     #  and the kind of problems it solves
#     # TODO: Add meta info of the key cols for each entity
#     # TODO: Ques - does the chat history holds the info of the
#     #  prompt as msgs or only Q and A? If it does, then context len may be huge?

#     system_prompt = """
#     You are an intelligent analyst working in the Procurement domain assisting the Category manager.
#     You are given a user question and your task is to generate a response well grounded in facts and domain knowledge.
#     You have access to the chat history of the conversation and the relevant data and domain knowledge to generate a
#     well informed and analytical answer.

#     Some key terms and their meaning -
#     Ideas: refers to the strategies, the next best actions etc that can help in cost savings
#     Opportunities: Refers to the savings value based on the procurement analytics.

#     """

#     user_prompt = """
#     Give a concise answer for the below question
#     - User Question: {question}
#     - Chat History: {chat_history}
#     - Data and Domain knowledge: {data_context}

#     Note :
#     - Response with deeper analysis including domain context and citing facts and data is very well appreciated by the
#     Category Manager
#     - Include **as many numbers, breakdowns, and quantitative insights** as possible — such as spend figures, savings potential, supplier count, unit price trends, volume impact, etc.
#     - Break down opportunities or ideas into measurable components where relevant to help with decision-making.
#     - Break large values down into **K (thousand), M (million), and B (billion)** notation for clarity (e.g., 1,200,000 → 1.2M).
#     - Do not repeat any piece of information.

#     """
#     return ChatPromptTemplate.from_messages(
#         [
#             ("system", system_prompt),
#             ("human", user_prompt),
#         ],
#     )


def create_dynamic_qna_prompt() -> ChatPromptTemplate:
    """
    Creates a prompt template for generating dynamic QnA responses,
    including structured Key Facts and Insights relevant to the Procurement domain.
    
    Returns:
        ChatPromptTemplate: A template for generating structured and insightful responses.
    """

    system_prompt = """
    You are an intelligent analytics assistant working in the Procurement domain to support a Category Manager.
    Your role is to evaluate procurement-related data and domain context to generate strategic and actionable insights.
    
    You have access to:
    - Chat history of the user
    - Relevant data tables and metrics
    - Domain knowledge (analytics glossary, procurement strategy, supplier optimization, cost saving levers)

    Key Concepts:
    - Key Facts: Quantitative or diagnostic insights such as market insights, spend analysis on supplier/sku/plant/region level, supplier distribution, 
    supplier relationship, SKU, compliance rates, cost trends, supplier ytd spend, total spend, single and multi source spend etc.
    - Opportunities: Quantified potential for savings based on procurement data analysis - cost savings, efficiency gains, benchmark gap 
    (is also considered savings opportunity), procurement optimization, strategic transformation etc.

    """

    user_prompt = """
    Given the following inputs, generate a structured and insightful response:

    - User Question: {question}
    - Chat History: {chat_history}
    - Data and Domain Knowledge: {data_context}
    - Market Data: {market_context}
    - Currency: {currency}

    ** VERY IMPORTANT: Retain the currency symbol (EUR,USD) and unit (K, M).**

    Output Format:
    
    **Key Facts:**
    - Provide 3 to 5 bullet points based on procurement data (supplier/plant/SKU/region level).
    - Focus on measurable, diagnostic insights such as:
    - Spend patterns (total, YTD, category-level)
    - Supplier distribution (single/multi-source)
    - Compliance rates
    - Cost or volume trends
    - Market Analysis
    - Highlight inefficiencies, anomalies, or concentration risks using numbers and breakdowns etc.

    NOTE: NO OPPORTUNITY VALUES SHOULD COME UNDER KEY FACTS SECTION. THEY WOULD ALWAYS BELONG TO OPPORTUNITIES SECTION ONLY.
    NOTE: IT IS NOT MANDATORY TO INCLUDE ALL POINTERS, THEY ARE GIVEN TO GIVE YOU AN IDEA WHAT ALL POSSIBLE INFORMATION CAN FALL IN RESPECTIVE SECTION.

    **Opportunities:**
    - Provide 3 to 5 bullet points focused on **quantified savings potential** and optimization opportunities.
    - Example of opportunities to include:
    - Cost savings (via vendor consolidation, price normalization, price arbitrage, payment terms standardization, early payments etc.)
    - Efficiency improvements (e.g., process automation, digital procurement)
    - Benchmarking gaps (where current performance lags best-in-class)
    - Strategic transformation (e.g., ESG targets, sourcing shifts)

    Style & Notes:
    - Use **M (million)**, **K (thousand)**, or **B (billion)** notation where relevant.
    - Use a professional, concise tone aimed at an executive-level reader.
    - Avoid repetition. Be precise and clear.
    - Where applicable, break down larger insights into parts for better clarity.
    - Response with deeper analysis including domain context and citing facts and data is very well appreciated by the Category Manager
    - Include **as many numbers, breakdowns of opportunities, and quantitative insights** as possible — such as spend figures, savings potential, supplier count, unit price trends, volume impact, etc.
    - Break large values down into **K (thousand), M (million), and B (billion)** notation for clarity (e.g., 1,200,000 EUR → 1.2M EUR).

    VERY IMPORTANT: THERE SHOULD BE NO OVERLAP OF INFORMATION BETWEEN KEY FACTS AND OPPORTUNITIES SECTION. THERE SHOULD BE NO INFORMATION PRESENTED TWICE 
    i.e. NO REPEATITION OF INFORMATION ALLOWED AT ANY COST.

    NEVER USE MACHINE LIKE PREFACING, JUST PROVIDE THE OUTPUT.

    IF the user question is not about "ideas" or "opportunities", ONLY THEN after mentioning all the above, answer the user question based on above findings in a structured format using bullet points. Do not keep the heading as **User Question Answer ** etc., instead give a meaningful heading based on the user question.
    You must give response in markdown, with each section having proper and logical separation. 

    NOTE: **You must structure/frame your response in a top-down approach, starting with the highest opportunity and then going down to the next best opportunities in terms of impact and value.**

    """

    return ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", user_prompt),
        ]
    )


def create_dynamic_ideas_prompt() -> ChatPromptTemplate:
    """
    Creates a prompt template for generating dynamic ideas responses.

    Returns:
        ChatPromptTemplate: A template for generating dynamic ideas responses.
    """
    # Todo: Data dict for all entities to be pulled in dynamically

    system_prompt = """
    You are an intelligent analyst working in the Procurement domain assisting the Category manager.
    You are given the task to generate ideas that are next best actions that can help in cost savings.
    You have access to the chat history to understand the conversation and the relevant data and domain knowledge
    to generate a well informed and analytical answer.

    The ideas may be asked on one of the three entities which may be present in the question
    1. Supplier
    - The ideas requested will be to act upon the savings opportunity identified at a vendor or supplier level

    2. SKU
    - The ideas requested will be to act upon the savings opportunity identified at a material level

    3. Analytics:
    - The ideas requested will be to act upon the savings opportunity identified at overall analytics
    """

    user_prompt = """
    Take a step by step approach to generate the ideas.

    Step 1 -
    Understand the user question and the ongoing chat conversation using the chat history.
    Identify the entity value for which the idea is asked.
    Also identify if the idea is requested for a specific area like parametric cost modeling, price arbitrage etc.

    user_question : {question}
    Chat history : {chat_history}
    Currency: {currency}

    ** VERY IMPORTANT: Retain the currency symbol (EUR,USD) and unit (K, M).**


    Step 2 -
    You are given available data and domain knowledge.
    Your task is to search if the ideas are available as pre-generated in the data provided.
    The ideas if available can be identified with the key variable name "idea" and unique identifier as "idea_number"

    Very Important Note : Ensure you look for the ideas only for the entity identified in Step 1.

    If and only if you are able to find the "idea" and "idea_number" in the data for the entity value then -
     - ignore Step 3 and Step 4;
     - jump directly to Step 5.

    If you do not find the "idea" and the "idea_number" then - proceed to Step 3

    Data and domain knowledge: {data_context}

    Step 3 -
    In this step your task is to understand the data provided in Step 2.
    Analyse the below data points with extra focus -

    1. The key saving opportunities available for the entity identified in Step 1
    2. Available insights which will aid in better analysis of the savings opportunities
    3. If the key entity from Step 1 is a supplier or SKU, then analyse the objectives

    Step 4:
    Now based on the understanding gathered in Step 3 generate 1-3 ideas for the Category Manager.
    Follow the below instructions:

    Instructions to generate ideas -

    A> The idea should have the below structure:
        - "idea_title":
        A very concise one liner "actionable" idea title in 5-15 words capturing the key action item for the
        Category Manager.

        - "description":
        Start by clearly explaining the objective of the idea AND What we can achieve by the idea [ like cost reduction etc]
        Next, support objective by integrating factual details and data points explaining the relevance of the data with
        the objective.
        At the end, in 3-4 sentences, detail the key action/ steps required to achieve the goal.
        Ensure the steps are presented in a clear, logical sequence for efficient implementation.
        Should not be generic but use business-specific context and terminology.
        ** VERY IMPORTANT: Retain the currency symbol (EUR,USD) and unit (K, M).**

        ** NOTE **:
        - Include **as many numbers, breakdowns, and quantitative insights** as possible — such as spend figures, savings potential, supplier count, unit price trends, volume impact, etc.
        - Break down opportunities or ideas into measurable components where relevant to help with decision-making.
        - Break large values down into **K (thousand), M (million), and B (billion)** notation for clarity (e.g., 1,200,000 EUR → 1.2M EUR).
        - Do not repeat any piece of information.
        - Always mention values in K,M,B and with the correct currency symbol.

        - "idea_number":
        Generate an idea number for each idea based on the below formula:
        idea_number = {epoch_timestamp}_{category}_i
         - where epoch_timestamp is the timestamp in epoch format
         - category is the category name, for example: bearings
         - i is incremental integer value starting from 1 to identify different ideas.
        Example: "1734669241_bearings_1"

        - "key_impact":
        A single numeric monetary value as string representing the total cost savings impact computed from available data.
        Guidelines for computing and formatting:
            - Identify all positive monetary values that explicitly refer to savings (e.g., cost savings, efficiency gains, reduction in spend).
            - If a total savings amount is explicitly mentioned and other values are clearly subsets or contributing components, return only the total/max value.
            - If multiple savings values are mentioned that are **independent** (i.e., not stated as part of a total), **sum them**.
            - Ignore negative values and numbers related to general spend, cost, or price unless explicitly marked as savings.
            - Retain the currency symbol (EUR,USD) and unit (K, M).
            - Use EUR as the default currency if no symbol is provided.
            - If a value is away from benchmark, that gap is also considered savings opportunity.
            - Make sure EUR/USD (currency) is always placed at the end.
            - If a calculation has reached 1000K, make sure to convert it into M, so on for M to B.
            - In case of decimals, impact numbers should be upto two decimal points only.
            - Do not include percentage values as impact, only numeric values.
            - If no impact is found return an empty string, do not make up any values.

    Step 5:
        OUTPUT FORMAT: the final response for ideas is only JSON list (without any `) following the below format:
        [
            {{
                "title": "idea title 1",
                "description": "description of idea 1",
                "id": "1734669241_bearings_1",
                "key_impact": "1.5M EUR"
            }},
            {{
                "title": "idea title 2",
                "description": "description of idea 2",
                "id": "1734669241_bearings_2",
                "key_impact": "800K EUR"
            }},
            ...
        ]

    ONLY respond with the final response from Step 5 and nothing else.

    NOTE: **You must structure/frame your response in a top-down approach, starting with the highest opportunity and then going down to the next best opportunities in terms of impact and value.**

    
    """

    return ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", user_prompt),
        ],
    )


# def create_dynamic_ideas_prompt() -> ChatPromptTemplate:
#     """
#     Creates a prompt template for generating dynamic ideas responses.

#     Returns:
#         ChatPromptTemplate: A template for generating dynamic ideas responses.
#     """
#     # Todo: Data dict for all entities to be pulled in dynamically

#     system_prompt = """
#     You are an intelligent analyst working in the Procurement domain assisting the Category manager.
#     You are given the task to generate ideas that are next best actions that can help in cost savings.
#     You have access to the chat history to understand the conversation and the relevant data and domain knowledge
#     to generate a well informed and analytical answer.

#     The ideas may be asked on one of the three entities which may be present in the question
#     1. Supplier
#     - The ideas requested will be to act upon the savings opportunity identified at a vendor or supplier level

#     2. SKU
#     - The ideas requested will be to act upon the savings opportunity identified at a material level

#     3. Analytics:
#     - The ideas requested will be to act upon the savings opportunity identified at overall analytics
#     """

#     user_prompt = """
#     Take a step by step approach to generate the ideas.

#     Step 1 -
#     Understand the user question and the ongoing chat conversation using the chat history.
#     Identify the entity value for which the idea is asked.
#     Also identify if the idea is requested for a specific area like parametric cost modeling, price arbitrage etc.

#     user_question : {question}
#     Chat history : {chat_history}

#     Step 2 -
#     You are given available data and domain knowledge.
#     Your task is to search if the ideas are available as pre-generated in the data provided.
#     The ideas if available can be identified with the key variable name "idea" and unique identifier as "idea_number"

#     Very Important Note : Ensure you look for the ideas only for the entity identified in Step 1.

#     If and only if you are able to find the "idea" and "idea_number" in the data for the entity value then -
#      - ignore Step 3 and Step 4;
#      - jump directly to Step 5.

#     If you do not find the "idea" and the "idea_number" then - proceed to Step 3

#     Data and domain knowledge: {data_context}

#     Step 3 -
#     In this step your task is to understand the data provided in Step 2.
#     Analyse the below data points with extra focus -

#     1. The key saving opportunities available for the entity identified in Step 1
#     2. Available insights which will aid in better analysis of the savings opportunities
#     3. If the key entity from Step 1 is a supplier or SKU, then analyse the objectives

#     Step 4:
#     Now based on the understanding gathered in Step 3 generate 1-3 ideas for the Category Manager.
#     Follow the below instructions:

#     Instructions to generate ideas -

#     A> The idea should have the below structure:
#         - "idea_title":
#         A very concise one liner "actionable" idea title in 5-15 words capturing the key action item for the
#         Category Manager.

#         - "description":
#         Start by clearly explaining the objective of the idea AND What we can achieve by the idea [ like cost reduction etc]
#         Next, support objective by integrating factual details and data points explaining the relevenace of the data with
#         the objective
#         At the End, in 3-4 sentences, detail the key action/ steps required to achieve the goal
#         Ensure the steps are presented in a clear, logical sequence for efficient implementation. should not be genric but with
#         business context/terms.

#         ** NOTE **:
#         - Include **as many numbers, breakdowns, and quantitative insights** as possible — such as spend figures, savings potential, supplier count, unit price trends, volume impact, etc.
#         - Break down opportunities or ideas into measurable components where relevant to help with decision-making.
#         - Break large values down into **K (thousand), M (million), and B (billion)** notation for clarity (e.g., 1,200,000 → 1.2M).
#         - Do not repeat any piece of information.

#         - "idea_number":
#         Generate a idea number for each of the idea based on the below formula
#         idea_number = {epoch_timestamp}_{category}_i
#          - where epoch_timestamp is the timestamp in epoch format
#          - category is teh category name , for ex: bearings
#          - i is incremental integer value starting from 1 to identify different ideas.
#         example for idea_number:   1734669241_bearings_1

#     Step 5:
#         OUTPUT FORMAT: the final response for ideas is only JSON list (without any `) following the below format:
#         [
#             {{
#                 "title": "idea title 1"
#                 "description": "description of idea 1"
#                 "id": "1734669241_bearings_1"
#             }},
#             {{
#                 "title": "idea title 2"
#                 "description": "description of idea 2"
#                 "id": "1734669241_bearings_2"
#             }},
#             ...
#         ]


#     ONLY respond with the final response from Step 5 and nothing else
#     """

#     return ChatPromptTemplate.from_messages(
#         [
#             ("system", system_prompt),
#             ("human", user_prompt),
#         ],
#     )


def create_opportunities_prompt() -> ChatPromptTemplate:
    """
    Creates a prompt template for generating responses about savings or optimization opportunities
    based on provided insights data.

    Returns:
        ChatPromptTemplate: A template for generating responses to questions
         about savings or optimization opportunities.
    """
    system_prompt = """You are an Insights Analyst for procurement data.
    Your primary role is to interpret, analyze, and answer questions about savings or \
    optimization opportunities only using the provided insights data.
    You have access to the chat history to understand the conversation and the relevant data and domain knowledge
    to generate a well informed and analytical answer.

    The question might contain procurement categories and analytics related abbreviations. For example
    original equipment manufacturing : OEM NON-OEM
    high cost country : HCC
    low cost country : LCC
    Linear Performance Pricing : LPP
    Parametric Cost Modeling: PCM"""
    user_prompt = """

    When answering a question, your tasks are as follows:
    1. Understand the user question and the ongoing chat conversation using the chat history.
    2. Analyze Insights:
        - Review the given insights data, organized by analytics area, to extract relevant information
        based on the user's question.
        - Respond to questions across 3 levels: Category, Analytics and SKU/Supplier, as identified by
        the keywords in the question.
        - Category-Level: Use main insights data from all analytics, summarize total values or broad opportunities for
        the entire category.
        - Analytics-Level: Provide insights specific to the analytics area mentioned in the question. Include top SKUs
        or suppliers if relevant.
        If the requested analytics data is unavailable in the given insights data, indicate the lack of information for
        the specific analytics.
        - SKU/Supplier-Level: Detail opportunities specific to the requested SKU or supplier,
        computing totals if multiple are mentioned.

    3. Compute Totals When Needed:
        - If the user asks for the total impact value or similar aggregate data that is not directly present,
        compute it by summing the relevant values from all analytics areas.
        - For example, if the total opportunity for a category or analytics area is not given,
        calculate it by adding up individual values.

    4. Rank and Order Values:
        - For questions about “highest” or “top” opportunities, identify and return insights in descending order of impact value.
        - If the question asks for the “top” SKUs or suppliers, sort the insights by value and
        provide only the requested top items (e.g., top 3).

    5. RETURN FORMAT:
        - IMPORTANT: Only return in below JSON format. Do not include any additional text, \
        explanations or any markdown formatting or enclosing backticks.

        Example Response:
        {{
        "opportunity_summary": "GBM SARL has multiple opportunities, including EUR 646.7K in Parametric Cost Modelling and
        EUR 660.72K in LCC.",
        "source_insights": [
            "insight: The top 3 suppliers with the highest parametric cost modeling oppurtunity are GBM SARL (EUR 646.7K ),
            PTP INDUSTRY SAS (EUR 330.2K ), SKF FRANCE (EUR 230.3K ).",
            "insight: The top 3 suppliers with the highest HCC LCC opportunity are SKF FRANCE (EUR 1.12M ),
            GBM SARL (EUR 660.72K ), CNC manufacturing technology Friedemann (EUR 574.04K)"
        ]
        }}

        Details of keys:
        - "opportunity_summary": A concise answer to the user's question based only on relevant insights data.
        - "source_insights":  Return a list of unmodified insights strings that directly contributed to
            generating the "opportunity_summary" Adhere to the following rules:
            - Use only the insights from the provided data under the keys "opportunity_insights" or "linked_insights." 
            - Do not generate new insights; strictly use those that are explicitly available in the given data.
            - The insights should be accurate, complete and concise. Your language must be simple,clearly understandable and actionable for procurement managers.
            - Exclude data from the "ideas" key as it does not qualify as insights.
            - Include only those insights that were directly used to form the "opportunity_summary."
            - For questions unrelated to analytics, SKUs, or suppliers, limit the "source_insights"
            to the Opportunity Insights section only.

    Task Instructions:
    1. Identify Question Level:
    - Category-Level: Aggregate insights across analytics areas for broad category-level summaries.
    - Analytics-Level: Focus on specific analytics areas as requested by the user.
    - SKU/Supplier-Level: Provide insights only related to specific SKUs or suppliers.
    Don't include insights which doesnt contain the given SKUs or suppliers.

    2. Example Responses:
    - Category-Level: "The total opportunity value in Bearings category is approximately EUR 19.85M,
    primarily driven by EUR 9.7M from payment term standardization, EUR 5.7M from LCC transfers,
    EUR 1.2M from parametric cost modeling and EUR 2.4M from rates harmonization, with additional gains of EUR 163.7K
    from unused discounts, EUR 43.57K from early payments."
    - Analytics-Level: "In Bearings Parametric Cost Modelling, top opportunities are with suppliers GBM SARL (EUR 646.7K),
    and top SKUs like PDR BEARING 438155."
    - SKU/Supplier-Level: "For SKU xxxxx, the opportunity is EUR 144.6K; for SKU yyyyy, the opportunity is EUR 330.2K."

    Inputs:
    1. User Question: {question}
    2. Chat history: {chat_history}
    3. Analytics Data: {data_context}
    4. Currency: {currency}

    ** VERY IMPORTANT: Retain the currency symbol (EUR,USD) and unit (K, M).**

    Provide answers concisely, answer only what the question asks
    and using precise values from the JSON insights to ensure accuracy. Do not include unrelated information.

    ** NOTE **:
        - Include **as many numbers, breakdowns, and quantitative insights** as possible — such as spend figures, savings potential, supplier count, unit price trends, volume impact, etc.
        - Break down opportunities or ideas into measurable components where relevant to help with decision-making.
        - Break large values down into **K (thousand), M (million), and B (billion)** notation for clarity (e.g., 1,200,000 EUR→ 1.2M EUR).

    NOTE: **You must structure/frame your response in a top-down approach, starting with the highest opportunity and then going down to the next best opportunities in terms of impact and value.**

    """
    return ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", user_prompt),
        ],
    )

def generate_open_world_response_prompt(query,chat_history):

    prompt_template = f"""
    You are an intelligent summarization agent designed to process web search results and extract structured, stakeholder-focused summaries.

    MANDATORY INSTRUCTIONS

    FORMAT & STRUCTURE RULES
    1. The summary must be in Markdown format.
    2. Information must be structured from a stakeholder’s perspective, grouped logically by themes or categories relevant to the query.
    3. Include a separate "Reference Links" section at the end:
    - Provide numbered links to all the sources you used.
    - Mention the original source name and date of publication (if available).

    CONTENT RULES
    4. Summarize only information that is directly relevant to the user's query.
    5. Include insights from each valid link — no link should be skipped.
    6. Translate all content into English, regardless of the original language.
    7. Fix grammar and spelling issues during summarization.
    8. Always mention the source and date in the content summary.
    9. Ensure no unrelated or redundant information is included.
    10. No bullet points without context — each point should be meaningful to the query.

    TASK
    Using the chat history and query, generate a structured summary as per the rules above.

    INPUTS

    Query:
    {query}

    Chat History:
    {chat_history}

    SAMPLE OUTPUT STRUCTURE

    ## Summary: {query}

    ### [Relevant Section Heading 1]
    - [Insightful and concise point #1 with source and date]
    - [Insightful and concise point #2 with source and date]

    ### [Relevant Section Heading 2]
    - [Insightful and concise point #3 with source and date]

    ### Reference Links
    1. [Title or domain of source 1](URL) – Source Name, Date
    2. [Title or domain of source 2](URL) – Source Name, Date
    """

    return prompt_template
