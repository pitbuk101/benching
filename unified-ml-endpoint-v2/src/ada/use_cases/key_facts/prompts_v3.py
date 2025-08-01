"""Prompt for key facts"""

# flake8: noqa: E501
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate


def generate_dax_one_prompt(
    data_model: str,
    measure_description: str,
    filters_description: str,
    few_shot_questions: list[str],
    few_shot_query_filtered: list[str],
    category: str,
    user_question: str,
    category_filter_level: str,
) -> ChatPromptTemplate:
    """
    Generate a prompt for generating a Power BI DAX query based on :
    user input, data model and example queries

    Args:
        data_model (str): Description of the data model used in Power BI.
        measure_description (str): Description of the measures used in the data model.
        filters_description (str): Description of the business filters to be applied to the query.
        few_shot_questions (list[str]): Examples of few-shot learning questions.
        few_shot_query_filtered (list[str]): Examples of queries with applied filters.
        category (str): The category or domain of the question, e.g., 'Bearings'.
        user_question (str): The user's question to be converted into a DAX query.
        category_filter_level (str): The level at which the category filter should be applied.

    Returns:
        ChatPromptTemplate: A template containing the system and user prompts.
    """

    system_prompt = """
        You are an expert Power BI analyst proficient at converting a user question into Power BI DAX queries.
        You work in the Procurement domain.
        Follow the steps and instructions provided for each task.
        Generate output from Task 3 ONLY as final response.
        """

    user_prompt = f"""
        First understand the data tables, data column description, measures available, and the business filter definitions

        Data Model:
        {data_model}

        Measures:
        {measure_description}

        Business Filters:
        {filters_description}

        ---
        Now proceed to follow tasks sequentially.


        Task 1:
        Understand the user question:
        {user_question}

        Create the step-by-step logic of how to create DAX query following the instructions below:

        Instructions:

        {{
            "General Guidelines": [
                "Return only step-by-step logic description without code",
                "You must NOT return the code",
                "You cannot create new measures",
                "Your logic MUST return output as row or table",
                "Never sort output unless asked in question"
                ],

            "Use of Measures":[
                "If question can be answered by existing measure, use measure",
                "Always use measures where possible",
                "You have access to all available measures"
                ],

            "Specific Calculations":[
                "For questions with XX% top / bottom spend breakdown calculate ordered running total, \
                e.g. for question How many sub-categories make up top XX% of my total spend?",
                "For questions like "What is my tail spend?" NO running total required. Tail spend is the bottom 20% spend"
                ],

            "Key Business terms and Definitions":[
            {{"Breakdown": "Breakdown means distribution across some dimension, \
            e.g. spend breakdown by suppliers means spend distribution across suppliers"}},
            {{"Footprint": "Footprint means distribution over region (unless specified otherwise)"}}
            ]

            "Category Filter":[
                "IMPORTANT - ALWAYS include this category filter in query TREATAS({{ "{category}" }}, {category_filter_level}) unless the question \
                    references tables 'Fact Market Demand Supply Segmentation,' 'Fact Market Analysis,' or 'Fact Market Prices.'",
                "DO NOT consider the category mentioned in the question, IGNORE or REMOVE IT.",
                "Include subcategories filters if specified"
            ]

            "Time-Based Filter":[
                "This year means TREATAS({{ 0 }}, Period[YEAR_OFFSET])",
                "Last year or previous year means TREATAS({{ -1 }}, Period[YEAR_OFFSET])",
                "Last X years means Period[YEAR_OFFSET]>-X",
                "This month means TREATAS({{ 0 }}, Period[MONTH_OFFSET])",
                "Last month or previous month means TREATAS({{ -1 }}, Period[MONTH_OFFSET])",
                "Last X months means Period[MONTH_OFFSET]>-X",
                "If the year is explicitly specified, use 'Period'[TXT_YEAR] (integer) for filtering.",
                "By default, if no time period is provided in the question, apply TREATAS({ 0}, 'Period'[YEAR_OFFSET])\
                    to filter on the latest year."
            ]
        }}

        ---
        Task 2:
        Evaluate whether the step-by-step logic generated in Task 1 using the instructions in Task 1 and requirements in user question.
        Correct if and only if existing logic is incorrect.

        ---

        Task 3:
        Generate correct DAX query following the step-by-step logic from Task 2 and \
        the below DAX Code Writing Instructions to answer the User question.
        You have access to examples of DAX code.
        Make query as step-by-step as possible.

        DAX Code Writing Instructions:

        {{
            "Structure and Syntax":[
                "DAX must start with EVALUATE statement",
                "Always end query with RETURN statement",
                "DAX must return row or table"
                ],

            "Filtering":[
                "Include filters using TREATAS where possible. Apply filters together wherever possible to simplify calculations. \
                    When a value is calculated using filters, the resulting value is fixed and cannot be filtered further.",
                "Filters must be applied to every calculation. \
                    Example - If you calculate total spend, apply these filters. If you have multiple separate calculations, apply filters in every calculation."
                ],

            "Functions and Calculations":[
                "Only listed functions must be used: WINDOW, SUMARIZECOLUMNS, ADDCOLUMNS, DIVIDE, SUMX, TOPN, CALCULATETABLE, CALCULATE, SELECTCOLUMNS, TREATAS, FILTER",
                "To calculate running total ALWAYS use SUMX(WINDOW()) function",
                "You have access to the data model and measures. Always use measures where possible.",
                ],

            "Output Requirements": [
                "DAX MUST return all variables which were used in calculations WHERE POSSIBLE. \
                    If user asks about %, return absolute values too. If user asks about change of value, return also starting and ending values.",
                "Make sure to return correct executable DAX query without any markdown formatting or enclosing backticks.",
                "Do not change calculation logic."
                ]

        }}

        You have examples of how to generate the DAX queries:

        Question 1: {few_shot_questions[0]}
        DAX Query 1: {few_shot_query_filtered[0]}

        Question 2: {few_shot_questions[1]}
        DAX Query 2: {few_shot_query_filtered[1]}

        Question 3: {few_shot_questions[2]}
        DAX Query 3: {few_shot_query_filtered[2]}

        ---

        Return only the final DAX code from Task 3 as the response and nothing else.

        """
    return ChatPromptTemplate(
        [
            SystemMessage(system_prompt),
            HumanMessage(user_prompt),
        ],
    )


def dax_response_generation_prompt(
    question: str,
    category: str,
    preferred_currency: str,
    data: str,
    sql_query: str,
) -> ChatPromptTemplate:
    """
    Generate a prompt to create a text response for a chat based on numerical calculations.

    Args:
        question (str): The user's question that needs to be answered.
        category (str): The category or domain of the question.
        preferred_currency (str): The currency to be used in the response.
        data (str): The data generated from the SQL query.
        sql_query (str): The SQL query generated based on the user's question.

    Returns:
        (ChatPromptTemplate): A template containing the system prompt for generating
        the text response.
    """

    
    # system_prompt = f"""
    #         You are a business analyst who presents data findings in a summarized, structured and concise manner.
    #         Your response must answer the user's question based on the provided data without summarizing beyond the available rows.

    #         ### **Key Guidelines:**
    #         - **Handling Missing or Empty Data:**  
    #         - If the dataframe is **completely empty** (no rows or columns), return:  
    #             *"There is no data available for the selected query. Please refine your request."*  
    #         - If the dataframe contains valid columns but only has values of `0`:
    #             **do NOT treat it as empty.** Instead, return the data of each row as "Column: Value".
    #         - If a link or URL is given in the available data:
    #             **ignore it** and focus only on the textual data present.


    #         - **Data Presentation:**  
    #         - **Always display all available data rows** without summarizing beyond what is provided.  
    #         - ! **Do NOT limit or trucate the output unless the output is about news**
    #         - ** Provide news summary in 1 line for each row.**
    #         - **DISPLAY ALL COLUMNS IN THE OUTPUT** unless instructed otherwise.
    #         - Format numbers with **thousands separators** for better readability.  
    #         - Ensure results are **in descending order** where applicable.
            
    #         - **Contextual Information:**  
    #         - **ALWAYS state that the calculation is for category `{category}`**, unless the question is about:  
    #             - Market segmentation  
    #             - Revenue breakup  
    #             - Price of material  
    #             - Market analysis (growth, size, maturity)
    #         - **If user question is about news**, produce the output in  consice manner for each row.

    #         ### **Handling Time Periods:**
    #         - If the dataset contains different time periods, **use only data relevant to the requested time period.**  
    #         - **If the question's date does not match available data**, mention:  
    #         *"We do not have data for the requested date. However, available data is for [date in query results]."*  
    #         - If no time period is mentioned in the question, assume **the current year.**  

    #         ### **Currency Formatting:**
    #         - Include **`{preferred_currency}`** as the currency indicator, unless another currency is specified in the question.

    #         ---

    #         ### **User Question:**
    #         {question}

    #         ### **Available Data:**  
    #         (Only one of these will be present in the input)  
    #         **Top entries:**  
    #         {query_result_head}  

    #         **OR**  

    #         **Tail entries:**  
    #         {query_result_tail}  

    #         ---

    #         ### **Final Output Format:**  
    #         - **Display all rows from the input** without truncation.  
    #         - **Ensure readability** by using multiple lines where necessary.  
    #         - **Do NOT summarize beyond the given data rows** or add "and so on". 
    #         - Never return data in tabular format. Always return in a structured text format.


    #         """

    system_prompt = f"""
    You are a business analyst in a procurement domain who presents data findings in a summarized, structured and concise manner.
    Your response must answer the user's question based on the provided data without summarizing beyond the available rows.
    You will be provided the user's question, it's relvant sql and the data generated from the sql query.
    You will create summary from those data points.

    ### Mandatory Guidelines ###
    1. Summarize the data in a structured and concise manner.
    2. Always display all available data rows without summarizing beyond what is provided.
    3. Do NOT limit or truncate the output unless the output is about news.
    4. For news provide a summary in 1 paragraph in 100-150 words.
    5. DISPLAY ALL COLUMNS IN THE OUTPUT unless instructed otherwise.
    6. Format numbers with thousands separators for better readability.
    7. Ensure results are in descending order where applicable.
    8. Always state that the calculation is for category `{category}` unless the question is about Market segmentation, Revenue breakup, Price of material, Market analysis (growth, size, maturity).
    9. Include **`{preferred_currency}`** as the currency indicator, unless another currency is specified in the question.
    10. There are 4 types of queries generally user asks
        1. Spends:
            - Questions related to SPENDS, SUPPLIERS,COMPANY, CATEGORIES, REGIONS, PLANTS, COUNTRIES, REGIONS, MATERIALS (SKU), CONTINENTS
        2. Analytics
            - Questions related to analytics like SAVINGS OPPURTUNUITY, UNUSED DISCOUNT, PRICE ARBITRAGE, RATE HARMONIZATION, POTENTIAL SAVINGS, EARLY PAYMENT, HCC LCC, OEM NON-OEM
        3. Market
            - Questions related to market like MARKET SEGMENTATION, COMPONENTS, RAW MATERIALS, MARKET PRICE, FORECAST
        4. News
            - Questions related to news like NEWS, EVENTS, ANNOUNCEMENTS, UPDATES, TRENDS, INSIGHTS
    11. ALWAYS MENTION THE TIME PERIOD OF THE DATA IN THE OUTPUT.
    12. DO NOT OUTPUT ANY URL OR LINKS IN THE OUTPUT.
    13. ALWAYS CONVERT NUMBER TO A SHORTER FORMAT LIKE 1.2K, 1.2M, 1.2B
    14. DO NOT OUTPUT USER'S QUESTION, SQL QUERY  IN THE OUTPUT.
    15. MAKE SURE TO RETURN THE ANSWER IN MARKDOWN FORMATTING ONLY.

    ### User Question ###
    {question}

    ### SQL Query ###
    {sql_query}

    ### Available Data ###
    {data}

    ### Final Output Format ###
        1. Display all rows from the input without truncation but NOT FOR NEWS.
        2. Ensure readability by using multiple lines where necessary.  
        3. Do NOT summarize beyond the given data rows or add "and so on". 
        4. Never return data in tabular format. Always return in a structured text format.
        5. For NEWS related questions, create a concise and summarize paragraph from entire data.
    """

    return ChatPromptTemplate([SystemMessage(system_prompt)])


def report_mapping_prompt(question: str, query_report_mapping: str) -> ChatPromptTemplate:
    """
    Generate a prompt to map a user question to the most relevant dashboard report.

    Args:
        question (str): The user's question that needs to be mapped to a report.
        query_report_mapping (str): A JSON string containing the mapping of reports
        to their descriptions.

    Returns:
        ChatPromptTemplate: A template containing the system prompt for mapping the question
        to a report.
    """
    system_prompt = f"""
        You are an accurate and precise data analyst who returns relevant report ID to the user based on input question.
        Identify which report can provide the most useful information to answer the question based on report description.
        If none of reports are relevant, return empty strings.

        Return output in JSON format:
        {{"report_id": <string>}}

        Example:
        ###
        Question:
        Hello?

        Answer:
        {{"report_id" : ""}}
        ###

        Reports:
        {query_report_mapping}

        Question:
        {question}

        Answer:
    """
    return ChatPromptTemplate([SystemMessage(system_prompt)])
