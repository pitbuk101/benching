"""Prompts for Dynamic Ideas"""

from langchain_core.prompts import ChatPromptTemplate, PromptTemplate


def get_question_classifier_prompt() -> PromptTemplate:
    """
    Creates a prompt template for classifying user input as ideas, opportunity or others
    """
    prompt_template = """
    You are a Procurement domain assistant to a Category Manager (the user).
    Your task is to classify the given input from the user into one of three labels:
    "ideas", "opportunity", or "others".

    Carefully read the instructions below to understand the scope of each label:

    - "ideas":
      Questions specifically requesting next best actions, recommendations, or strategies for suppliers, SKUs, analytics.
      Few examples -
      1. What are the recommendations for Supplier X?
      2. Suggest some strategies from LCC analytics?

      User inputs like - how do I implement this idea? is not in "ideas" scope, classify it as "others"
      Also, user inputs like "What strategies can we use to improve supplier performance?" which do not have reference
      to any suppliers, SKUs, analytics  are not in "ideas" scope

    - "opportunity":
      Questions specifically requesting savings opportunities , cost reduction, optimization potential for suppliers,
      SKUs, analytics.
      Few examples -  What is the savings potential for Supplier Z?
      Tell the optimizations for SKU 123?

      User inputs like "How do I act upon this opportunity?" is not in "opportunity" scope, classify it as "others".

    - "others":
      Captures all other types of questions or inputs that do not fit into the "ideas" or "opportunity" categories.

    Here is the chat history for context:
    {chat_history}

    Here is the user's input:
    {question}

    Based on the chat history and the instructions provided, classify the user input by returning only one label: "ideas",
    "opportunity", or "others".
    """
    return PromptTemplate(input_variables=["user_q", "chat_history"], template=prompt_template)


def get_history_based_ner_prompt() -> ChatPromptTemplate:
    """
    Creates a prompt template for extracting named entities from user questions and chat history.

    Returns:
        ChatPromptTemplate: The corresponding prompt template for extracting named entities.
    """
    # TODO: Enhance the analytics glossary for all the possible analytics;
    #  must match the actual names in top ideas table
    # TODO: handle scenario where one entity has multiple types : name and id in the same Q
    system_prompt = """
    You are an assistant designed to extract relevant entities from the user question
    and chat history, focusing on entities that are contextually relevant to the question.

    RESPONSE FORMAT :
    Must be valid JSON (list of dicts) response in the below format -

    [
        {{
            "entity": "supplier",
            "value": ["supplier_name"], // can be either name or id
            "type": "name" // can be either name or id
        }},
        {{
            "entity": "sku",
            "value": ["sku name"], // can be either name or id
            "type": "name" // can be either name or id
        }},
        {{
            "entity": "analytics",
            "value": ["analytics_name"], //can only be a name
            "type": "name"

        }},
        {{
            "entity": "idea",
            "value": [1244243], //must only be an id
            "type": "id"
        }},
        {{
            "entity": "insight",
            "value": [123], //must only be an id
            "type": "id"
        }}
    ]

    NOTE:
    1. The comments are only for reference, dont use them in output.
    2. IMPORTANT: ONLY RETURN JSON object in response without any additional text or explanations or any
    formatting like markdown or backticks.

    """

    user_prompt = """
    Your task is to extract below given entities from user question,.

    Instructions for extraction:

    1. Chat history relevance:
        - If the question context switches to a new topic, ignore the chat history.
        - Identify entities from the current question and relevant history only.

    2. Entities to extract:
        - supplier : can be extracted as an id (alphanumeric) or name of the supplier (str)
        - sku : can be extracted as an id (alphanumeric) or name of the supplier (str)
        - analytics : can only be extracted as the name of the analytics (refer to the "analytics glossary" for more info)
        - idea : must only be extracted as an id
        - insight : must only be extracted as an id

    3. Handling `insight id` and `idea id` extraction:
        - Chat History Insights/Ideas: If the chat history contains fields such as `insights` or `ideas`, user might ask questions
        which contextually references the insights or ideas. In this case, extract the id of insights/ideas which is present in
        chat history.
        - Ignore `insight id` and `idea id` extraction: Ignore in below scenarios:
            - If user question is not relevant to any insights/ideas.
            - If there is no insight/idea information present in chat history.
        - Contextual Matching: Use semantic understanding of the user question to identify the relevant insight id or idea id
        from the chat history.
        The reference can be implicit (e.g., a concept, term, or entity matching a label or associated content in the insights).

    4. Analytics Glossary: Below is the list of analytics names which represent commonly used analytics terms:
        {analytics_list}
        When extracting analytics names from a user question, follow below given instructions:
        - Exact Match: Identify the analytics name from the glossary that matches exactly with any term in the user's question.
        - Abbreviations: If an abbreviation is used, resolve it to the corresponding full analytics name from the glossary.
        - Closest Match: If there is no exact match or abbreviation, identify the closest matching analytics name from the
        glossary based on semantic similarity.
        - Output: Return the corresponding exact analytics name from the glossary.

    User Question: {question}
    Chat History: {chat_history}

    """
    return ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", user_prompt),
        ],
    )


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


def create_dynamic_qna_prompt() -> ChatPromptTemplate:
    """
    Creates a prompt template for generating dynamic QnA responses.

    Returns:
        ChatPromptTemplate: A template for generating dynamic QnA responses.
    """
    # TODO: add to sys prompt - analytics glossary, high level meaning
    #  and the kind of problems it solves
    # TODO: Add meta info of the key cols for each entity
    # TODO: Ques - does the chat history holds the info of the
    #  prompt as msgs or only Q and A? If it does, then context len may be huge?

    system_prompt = """
    You are an intelligent analyst working in the Procurement domain assisting the Category manager.
    You are given a user question and your task is to generate a response well grounded in facts and domain knowledge.
    You have access to the chat history of the conversation and the relevant data and domain knowledge to generate a
    well informed and analytical answer.

    Some key terms and their meaning -
    Ideas: refers to the strategies, the next best actions etc that can help in cost savings
    Opportunities: Refers to the savings value based on the procurement analytics.

    """

    user_prompt = """
    Give a concise answer for the below question
    - User Question: {question}
    - Chat History: {chat_history}
    - Data and Domain knowledge: {data_context}

    Note :
    - Response with deeper analysis including domain context and citing facts and data is very well appreciated by the
    Category Manager

    """
    return ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", user_prompt),
        ],
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
        Next, support objective by integrating factual details and data points explaining the relevenace of the data with
        the objective
        At the End, in 3-4 sentences, detail the key action/ steps required to achieve the goal
        Ensure the steps are presented in a clear, logical sequence for efficient implementation. should not be genric but with
        business context/terms

        - "idea_number":
        Generate a idea number for each of the idea based on the below formula
        idea_number = {epoch_timestamp}_{category}_i
         - where epoch_timestamp is the timestamp in epoch format
         - category is teh category name , for ex: bearings
         - i is incremental integer value starting from 1 to identify different ideas.
        example for idea_number:   1734669241_bearings_1

    Step 5:
        OUTPUT FORMAT: the final response for ideas is only JSON list (without any `) following the below format:
        [
            {{
                "title": "idea title 1"
                "description": "description of idea 1"
                "id": "1734669241_bearings_1"
            }},
            {{
                "title": "idea title 2"
                "description": "description of idea 2"
                "id": "1734669241_bearings_2"
            }},
            ...
        ]


    ONLY respond with the final response from Step 5 and nothing else
    """

    return ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", user_prompt),
        ],
    )


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

        {{
        "opportunity_summary": "GBM SARL has multiple opportunities, including EUR 646.7K in Parametric Cost Modelling and
        EUR 660.72K in LCC.",
        "source_insights": [
            "insight: top 3 suppliers with the highest parametric cost modeling oppurtunity are GBM SARL (EUR 646.7K ),
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
    2. Analytics Data: {data_context}

    Provide answers concisely, answer only what the question asks
    and using precise values from the JSON insights to ensure accuracy. Do not include unrelated information
    """
    return ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", user_prompt),
        ],
    )
