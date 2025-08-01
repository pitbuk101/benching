"""Idea generation v2 - RCA, Ideas and chat prompts"""

from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

from ada.utils.config.config_loader import read_config

idea_generation_conf = read_config("use-cases.yml")["idea_generation_chat"]


def generate_rca_prompt(insight_context: dict, pinned_elements: dict) -> ChatPromptTemplate:
    """
    Prompt for generating RCA given the inputs from user pinned elements and insight's context

    Args:
        insight_context (dict): Data dictionary containing insight context.
        pinned_elements (dict): Dictionary containing pinned elements.

    Returns:
        ChatPromptTemplate: ChatPromptTemplate object with a system prompt
    """
    pinned_main_insight = pinned_elements.get("pinned_main_insight", "")
    related_insights = pinned_elements.get("pinned_related_insight") or insight_context.get(
        "linked_insight",
    )
    context_definition = insight_context.get("definitions", "")
    alert_type = insight_context.get("alert_type", "")

    step_count = 2
    related_insights_step = ""
    if related_insights:
        step_count = step_count + 1
        related_insights_step = f"""
        Step {step_count}: Now understand the related insights and filter only the useful information from the related
        insights that helps you do the root cause analysis:
        {related_insights}
        """

    category_qna_step = ""
    if alert_type in idea_generation_conf["context"]["alert_types_for_category_qna"]:
        step_count = step_count + 1
        category_qna = insight_context.get("category_qna", "")
        category_qna_step = f"""
        Step {step_count}: Next understand the general information below AND only filter the information that helps you
        do the root cause analysis:
        {category_qna}
        """

    step_count = step_count + 1
    supplier_qna = insight_context.get("supplier_qna", "")
    sku_qna = insight_context.get("sku_qna", "")
    supplier_sku_qna_step = ""
    if (
        sku_qna
        or supplier_qna
        and alert_type in idea_generation_conf["context"]["alert_types_for_supplier_sku_qna"]
    ):
        supplier_sku_qna_step = f"""
        Step {step_count}: Next understand the supplier and sku information below AND only filter the information that
        helps you do the root cause analysis:
        {supplier_qna}
        {sku_qna}
        """

    step_count = step_count + 1

    prompt_template = f"""
    Act as procurement domain expert.
    You have been provided some insights and some times you may get additional information

    Insights available are of two types :
    1. Main insight: The primary insight to focus on.
    2. Related insights: Associated insights

    Your task is to do a root cause analysis presented in the main insight.
    Take a step by step approach to achieve this:

    Step 1: Understand the main intent of the insight
    {context_definition}

    Step 2: Understand the main insight provided below:

    {pinned_main_insight}

    {related_insights_step}

    {category_qna_step}

    {supplier_sku_qna_step}

    Step {step_count}: Now based on the understanding gathered and the domain knowledge, do a root cause analysis.

    Notes:
    1. Provide the output from Step {step_count} in 1-3 "very concise" points. Ensure to
    "AVOID duplication" in the output.
    2. Ensure to calculate and add derived metrics such as total opportunity value, percentages, averages etc to
    support the root causes wherever possible.
    3. Assign a appropriate header and generate the root causes separated by "|" as explained in the format below:
    "header": "root cause summary"|"header": "root cause summary"| ..
    Here is an example for the format to be followed:
    "High Price Variance in Top SKUs": "The top 3 SKUs with the highest price variance contribute
    to a significant ….”|"Supplier and Geographic Disparities": "The presence of
    multiple suppliers and geographic locations for the top SKUs indicates potential inconsistencies…”| …

    """
    return ChatPromptTemplate([SystemMessage(prompt_template)])


def generate_ideas_prompt(insight_context: dict, pinned_elements: dict) -> ChatPromptTemplate:
    """
    Prompt for generating ideas based on insight context and user pinned elements.

    rgs:
        insight_context (dict): Data dictionary containing insight context.
        pinned_elements (dict): Dictionary containing pinned elements.

    Returns:
        ChatPromptTemplate: A list containing a dictionary with a role ("system") and the
        content of the prompt.
    """
    pinned_main_insight = pinned_elements.get("pinned_main_insight")
    related_insights = pinned_elements.get("pinned_related_insight") or insight_context.get(
        "linked_insight",
    )
    pinned_root_causes = pinned_elements.get("pinned_root_causes", "")
    context_definition = insight_context.get("definitions", "")
    alert_type = insight_context.get("alert_type", "")

    step_count = 2
    related_insights_step = ""
    if related_insights:
        step_count = step_count + 1
        related_insights_step = f"""
        Step {step_count}: Now understand the related insights and filter only the useful information from
        the related insights that helps to generate ideas:
        {related_insights}
        """

    category_qna_step = ""
    if alert_type in idea_generation_conf["context"]["alert_types_for_category_qna"]:
        step_count = step_count + 1
        category_qna = insight_context.get("category_qna")
        category_qna_step = f"""
        Step {step_count}: Next understand the general information from the procurement category AND only filter
        the information that helps to generate ideas:
        {category_qna}
        """

    step_count = step_count + 1
    supplier_qna = insight_context.get("supplier_qna", "")
    sku_qna = insight_context.get("sku_qna", "")
    supplier_sku_qna_step = ""
    if (
        sku_qna
        or supplier_qna
        and alert_type in idea_generation_conf["context"]["alert_types_for_supplier_sku_qna"]
    ):
        supplier_sku_qna_step = f"""
        Step {step_count}: Next understand the supplier and sku information below AND only filter
        the information that helps to generate ideas:
        {supplier_qna}
        {sku_qna}
        """

    pinned_rca_step = ""
    if pinned_root_causes:
        step_count = step_count + 1
        pinned_rca_step = f"""
               Step {step_count}: Focus on the key root causes the category manager has highlighted:
               {pinned_root_causes}
               """

    step_count = step_count + 1

    prompt_template = f"""
    Act as procurement domain expert.
    You have been provided some insights and some times you may get additional information

    Insights available are of two types :
    1. Main insight: The primary insight to focus on.
    2. Related insights: Associated insights

    Your task is to evaluate of the main insight and provide ideas to take the next best action.
    Take a step by step approach to achieve this:

    Take a step by step approach:

    Step 1: Understand the main intent of the insight
    {context_definition}

    Step 2: Understand the main insight provided below:

    {pinned_main_insight}

    {related_insights_step}

    {category_qna_step}

    {supplier_sku_qna_step}

    {pinned_rca_step}

    Step {step_count}: Now based on the understanding gathered and the domain knowledge, generate the ideas for
    the Category Manager.

    Provide only the summary of the output from Step {step_count} in 1-3 "very concise" points.
    Notes:
    1. Ensure to "NOT REPEAT" any of the insight in the final summary and "AVOID duplication" in the final summary.
    2. Ensure to calculate and add derived metrics such as percentages, averages etc in the final response to
    support the ideas wherever possible.
    3. Assign a actionable title and generate the ideas separated by "|" as explained in the format below:
    "actionable title": "idea summary" | "actionable title": "idea summary" | ..
    4. The actionable title should summarise the precise next step for the Category Manager.
    Here is an actionable title example: "Negotiate with Top Suppliers for high gap SKUs"
    """
    return ChatPromptTemplate([SystemMessage(prompt_template)])


def get_context_prompts_for_ada_chat(
    retrieved_context: dict,
    insight_context: dict,
    pinned_elements: dict,
) -> tuple:
    """
    Generates contextual prompts for ADA chat based on insights data
    and user actions on the feature page

    Args:
        retrieved_context (dict): Dictionary containing historical request responses
        insight_context (dict): Dictionary containing insight context from the pg db
        pinned_elements (dict): Dictionary containing user pinned elements in UI

    Returns:
        tuple: A tuple containing context prompts in the following order:
               context_definition, pinned_main_insight, related_insights_prompt,
               category_qna_prompt, supplier_sku_qna_prompt, rca_prompt, ideas_prompt.
    """
    pinned_main_insight = pinned_elements.get("pinned_main_insight", "")
    pinned_related_insight = pinned_elements.get("pinned_related_insight", "")
    pinned_root_causes = pinned_elements.get("pinned_root_causes", "")
    pinned_ideas = pinned_elements.get("pinned_ideas", "")

    linked_insights = insight_context.get("linked_insights", "")
    context_definition = insight_context.get("context", "")
    alert_type = insight_context.get("alert_type", "")

    recommended_rca = retrieved_context.get("recommended_rca", "")
    recommended_ideas = retrieved_context.get("recommended_ideas", "")

    related_insights = pinned_related_insight or linked_insights
    root_causes = pinned_root_causes or recommended_rca
    ideas = pinned_ideas or recommended_ideas

    category_qna_prompt = ""
    if alert_type in idea_generation_conf["context"]["alert_types_for_category_qna"]:
        category_qna = insight_context.get("category_qna")
        category_qna_prompt = f"""
        General category FAQs :
        {category_qna}
        """

    supplier_sku_qna_prompt = ""
    if alert_type in idea_generation_conf["context"]["alert_types_for_supplier_sku_qna"]:
        supplier_qna = insight_context.get("supplier_qna", "")
        sku_qna = insight_context.get("sku_qna", "")
        supplier_sku_qna_prompt = f"""
        Supplier SKU category FAQs :
        {supplier_qna}
        {sku_qna}
        """

    related_insights_prompt = ""
    if related_insights:
        related_insights_prompt = f"""
        Related Insights: Likely associated with the main insights.
        {related_insights}
        """

    rca_prompt = ""
    if root_causes:
        rca_prompt = f"""
        Root Cause Analysis: Based on the analysis of the insights here are the root causes identified
        {root_causes}
        """

    ideas_prompt = ""
    if ideas:
        ideas_prompt = f"""
        Ideas: Recommendations to address the root causes
        {ideas}
        """

    return (
        context_definition,
        pinned_main_insight,
        related_insights_prompt,
        category_qna_prompt,
        supplier_sku_qna_prompt,
        rca_prompt,
        ideas_prompt,
    )


def get_common_ada_prompt_content(retrieved_context, insight_context, pinned_elements) -> str:
    """

    Generate common prompt content for ada chat responses based on insights data
    and user actions on the feature page

    Args:
        retrieved_context (dict): Dictionary containing historical request responses
        insight_context (dict): Dictionary containing insight context from the pg db
        pinned_elements (dict): Dictionary containing user pinned elements in UI

    Returns:
        str: Common ADA prompt content structured in a step-by-step approach.

    """
    (
        context_definition,
        pinned_main_insight,
        related_insights_prompt,
        category_qna_prompt,
        supplier_sku_qna_prompt,
        rca_prompt,
        ideas_prompt,
    ) = get_context_prompts_for_ada_chat(retrieved_context, insight_context, pinned_elements)

    return f"""
    You are an expert Category manager in the procurement domain.
    Take a step by step approach to respond to the questions:


    Step 1: The category manager is analysing insights on a particular subject
    The main subject of the insights is as explained below:
    {context_definition}

    Step 2: Understand information provided and filter out useful information:
    Main Insights: Considered primary insights.
    {pinned_main_insight}
    {related_insights_prompt}
    {rca_prompt}
    {ideas_prompt}

    Step 3: Understand the additional data available and filter out useful information:
     {category_qna_prompt}
     {supplier_sku_qna_prompt}
    """


def prompt_with_chat_history_v2(
    retrieved_context: dict,
    insight_context: dict,
    pinned_elements: dict,
) -> PromptTemplate:
    """
    Generate a prompt based on chat history, insights context and user pinned elements

    Args:
    - retrieved_context (Dict): Dictionary containing chat history information
    - insight_context (dict): Data dictionary containing insight context.
    - pinned_elements (dict): Dictionary containing pinned elements.

    Returns:
    - PromptTemplate: A template for the generated prompt.

    """

    context_prompt = get_common_ada_prompt_content(
        retrieved_context,
        insight_context,
        pinned_elements,
    )

    prompt_template = PromptTemplate.from_template(
        context_prompt
        + "\n"
        + """
        Step 4: Based on the context in Steps 1,2, and 3 you MUST generate the ACTUAL response ONLY
        WHEN the context is sufficient to generate A HIGHLY ACCURATE response.

        Previous conversation :
        {history}

        Current Conversation :
        {input}

        Notes:
        1. Your response MUST be a very accurate and brief summary that AVOIDS verbiage
        2. Ensure to calculate and add derived metrics such as percentages, averages etc in the final response
        """,
    )
    return prompt_template


def prompt_with_chat_history_v3(
    user_query: str,
    retrieved_context: dict,
    insight_context: dict,
    open_world_response: str,
    # pinned_elements: dict,
) -> PromptTemplate:
    """
    Generate a prompt based on chat history, insights context and user pinned elements

    Args:
    - retrieved_context (Dict): Dictionary containing chat history information
    - insight_context (dict): Data dictionary containing insight context.
    - pinned_elements (dict): Dictionary containing pinned elements.

    Returns:
    - PromptTemplate: A template for the generated prompt.

    """
    
    related_insights = insight_context.get("related_insights",[])
    related_insights = "\n".join(related_insights)
    top_ideas = insight_context["top_ideas"].replace('[', '').replace(']', '').replace('{', '').replace('}', '').replace('"', '').replace(",", "\n")

    prompt_template = f"""

    You are an expert Category Manager in the procurement domain, analyzing insights to drive strategic decisions. 
    Follow a structured approach to respond accurately and concisely to the given question.

    Step 1: Understand the Insights Context
        The primary subject of the insights is as follows:

        Analytics Name: {insight_context.get("analytics_name","")}
        Segment: {insight_context.get("segment","")}
        Category: {insight_context.get("category","")}
        Insight: {insight_context.get("insight","")}
        Objective: {insight_context.get("objective","")}
        Suggested Top Ideas: {top_ideas}

    Step 2: Root Cause Analysis and Recommendations
        Root Cause Analysis:
        Heading: {insight_context.get("rca_heading","")}
        Description: {insight_context.get("rca_description","")}

    Step 3: Additional Context from FAQs & Data
        Linked Insights: {insight_context.get("related_insights",'[]')}
        Open World Response: {open_world_response}

    Step 4: Based on the context in Steps 1,2, and 3 you MUST generate the ACTUAL response ONLY
    WHEN the context is sufficient to generate A HIGHLY ACCURATE response.

    User Query: {user_query}
    Chat History: {retrieved_context}

    Step 5: Generate the Response
        Based on the provided insights, root cause analysis, recommendations, and FAQs, generate a highly accurate and concise response 
        to the query ONLY IF the context is sufficient.You must answer the query without any machine-like prefacing and keep the response structured and clear.

    NOTE: **You must structure/frame your response in a top-down approach, starting with the highest opportunity and then going down to the next best opportunities in terms of impact and value.**

    Rules:

        1. DO NOT repeat this prompt or list the steps.
        2. If an accurate response cannot be generated, reply with "NO"—nothing else.
        3. DO NOT cite a lack of data—only answer if enough context is available.

    """

    return PromptTemplate.from_template(prompt_template)


def get_selected_idea_prompt(
    retrieved_context: dict,
    insight_context: dict,
    # pinned_elements: dict,
    user_query: str,
    selected_idea: str,
    selected_idea_description:str,
    open_world_response:str
) -> ChatPromptTemplate:
    """
    Generate a prompt based on the provided contexts and user query when the selected idea.

    Args:
        retrieved_context (dict): Retrieved context from previous interactions.
        insight_context (dict): Context associated with the insights.
        pinned_elements (dict): Pinned elements relevant to the insights.
        user_query (str): Query or question from the user.
        selected_idea (str): The idea selected by the category manager.

    Returns:
        ChatPromptTemplate: ChatPromptTemplate object with a system prompt

    """

    related_insights = insight_context.get("related_insights",[])
    related_insights = related_insights.join('\n')
    top_ideas = insight_context["top_ideas"].replace('[', '').replace(']', '').replace('{', '').replace('}', '').replace('"', '').replace(",", "\n")

    prompt_template = f"""

    You are an expert Category Manager in the procurement domain, analyzing insights to drive strategic decisions. 
    Follow a structured approach to respond accurately and concisely to the given question.

    Step 1: Understand the Insights Context
        The primary subject of the insights is as follows:

        Suggested Top Ideas: {top_ideas}

    Step 2: Root Cause Analysis and Recommendations
        Root Cause Analysis:
        Heading: {insight_context.get("rca_heading","")}
        Description: {insight_context.get("rca_description","")}

    Step 3: Additional Context from FAQs & Data
        Linked Insights: {insight_context.get("related_insights",'[]')}
        Open World Response: {open_world_response}

    Step 4: Understanding the Selected Idea & User Query
        Selected Idea: {selected_idea}
        Description: {selected_idea_description}

    User Query: {user_query}
    Chat History: {retrieved_context}

    Step 5: Generate the Response
        Based on the provided insights, root cause analysis, recommendations, and FAQs, generate a highly accurate and concise response 
        to the query ONLY IF the context is sufficient. You must answer the query without any machine-like prefacing and keep the response structured and clear.

    NOTE: **You must structure/frame your response in a top-down approach, starting with the highest opportunity and then going down to the next best opportunities in terms of impact and value.**

    Rules:

        1. DO NOT repeat this prompt or list the steps.
        2. If an accurate response cannot be generated, reply with "NO"—nothing else.
        3. DO NOT cite a lack of data—only answer if enough context is available.
    
    """

    return ChatPromptTemplate([SystemMessage(prompt_template)])


def get_intent_prompt() -> PromptTemplate:
    """
    The function provides a prompt template to understand and categorize
    the user's input on idea generation feature
    into one of the predefined labels: "rca", "ideas", "linked_insights", or "user_input".

    Returns:
     (PromptTemplate): A list containing a dictionary with a system role and the
    generated prompt content.
    """

    prompt = """
    You are an intelligent procurement domain AI assistant.
    Your task is to understand the user input and classify it in one of the labels specified in the label list below:
    Label list - "rca", "ideas", "linked_insights", "user_input"

    Use the below definitions and examples for each label to determine the accurate label for the user question

    "rca"
    Definitions - this label refers to the root cause analysis requested by the user for an insight
    Example -
    Q: Can you tell me the root causes for the high clean sheet gap observed in the insight?
    Label : "rca"
    Q: Generate root causes
    Label: "rca"

    "ideas"
    Definitions - this label refers to ideas or next best actions or
    corrective measures for a given insight
    Example -
    Q: Can you give me the next steps to consolidate the suppliers for the SKU?
    Label : "ideas"
    Q: Generate ideas
    Label : "ideas"

    "linked_insights"
    Definitions - this label refers to the user requests for getting similar or linked insight
    Example -
    Q: Can you show me insights that are similar to the pinned insight?
    Label : "linked_insights"
    Q: Generate linked insights.
    Label: "linked_insights"

    "user_input"
    Definitions - this label refers to the any other user question which do not fall into the other three labels
    Examples -
    Q: Can you tell me the spend data for SKU 1123?
    Label : "user_input"

    Q: What is the leverage I have for negotiating with the supplier XYZ?
    Label : "user_input"

    Q: What should be my strategy to negotiate with the top supplier?
    Label: "user_input"

    Note : Only respond with one of the labels from the list e.g. "user_input"
    DO NOT include the word "label" in the final answer

    """

    prompt_template = PromptTemplate.from_template(
        prompt
        + """
            Previous conversation with the Procurement Assistant:
            {history}
            Current Conversation-
            User query: {input}
            """,
    )
    return prompt_template


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
        generate a single structured and refined idea ensuring clarity, impact, and business relevance for Category Managers based on following
        data.

        Insight: {insight}
        Linked Insight: {linked_insights}
        Analytics: {analytics_name}

        # Instructions for Generating the "Title"

        1. Make it a concise, actionable one-liner (5-15 words) capturing the most critical action.
        2. Prioritize ideas involving direct supplier engagement (example, negotiation or consolidation).
        3. Keep the title crisp and to the point—avoid unnecessary words.
        4. Do not use generic phrases like “Optimize Procurement Costs through…”

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
        }}}}
        ]
        ```

        """

        return PromptTemplate.from_template(prompt)

    except Exception as e:
        print("Error",e)
        return None

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
