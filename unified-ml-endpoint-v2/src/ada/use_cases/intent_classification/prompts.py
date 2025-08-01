"""
Prompts for the intent model v2
"""

# flake8: noqa: E501
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate


def intent_model_prompt(intent_labels: list[str], category_name: str) -> ChatPromptTemplate:
    """
    Takes the chat context and gives the prompts for generating the intent
    Args:
        intent_labels (list[str]): The labels for the intent model which define the scope
        category_name (str): Category name
        matched_intent (str): The intent matched from the chat history
    Returns
        (ChatPromptTemplate): LLM prompt for generating the intent and the modified user query
    """
    contract_qa_prompt = ""
    if "contract-qa" in intent_labels:
        contract_qa_prompt = """
        "contract-qa" -
        Definition : refers to questions asked related to contract document with a supplier for
        procuring one or many SKUs. It can be payment terms, contract duration, termination
        period by convenience and clauses like audit rights, penalties and incentives, compliance
        requirements, renewal, financing terms, administrative fees, operative clause, obligations
        and measurement, escalators, warranty and guarantees related questions should be
        classified as contract QnA. All questions with reference to a contract has to be labeled
        as contract QnA.
        Examples :
        Q: How many of my contracts are expiring over the next 2 years?
        Label: "contract-qa"
        Q: Provide me with a summary of my contract with supplier X for industrial valves?
        Label: "contract-qa"
        """

    key_facts_prompt = ""
    if "key-facts-v2" in intent_labels:
        key_facts_prompt = """
        "key-facts-v2" -
        Definition : refers to questions asked related to numeric facts, KPIs and data available in the
        procurement, market database related to a category
        Examples :
        Q: Did my spend increase or decrease in the last year with my top spend vendor of last year?
        Label: "key-facts-v2"
        Q: Who are the suppliers accounting for X% of my spending?
        Label: "key-facts-v2"
        Q:  What are the latest price rates of xx metal as per London Metal Exchange?
        Label: "key-facts-v2"
        Q: "What was the price of Carbon Steel in India this year?
        Label: "key-facts-v2"
        Q: "What is the Buyer Power as per Porter's Five Forces?"
        Label: "key-facts-v2"
        Q: "What is the cost breakdown?"
        Label: "key-facts-v2"
        Q: "What is the Threat of Substitute Power as per Porter's Five Forces?"
        Label: "key-facts-v2"
        Q: Which are the top 7 SKUs with the biggest potential saving opportunity for year 2024:
        Label: "key-facts-v2"
        """

    news_qa_prompt = ""
    if "news-qna" in intent_labels:
        news_qa_prompt = """
        "news-qna" -
        Definition : ONLY refers to questions asked related to latest news on the category
        Examples :
        Q: What are the latest innovation in the bearings category?
        Label: "news-qna"
        Q:  What are the latest price rates of xx metal as per London Metal Exchange from News?
        Label: "news-qna"
        """

    # TODO : Idea Bank label to be added or not based on biz reqt.
    idea_generation_prompt = ""
    if "idea-generation" in intent_labels:
        idea_generation_prompt = """
        "idea-generation" -
        Definition : refers to questions that can be answered from Procurement knowledge base
        Examples :
        Q: What are the best practices for supplier benchmarking?
        Label: "idea-generation"
        Q:  What risks might exist in the procurement & supply chain process, and how can we mitigate them?
        Label: "idea-generation"
        Q:  Define Net Sales terms in the context of agreements.?
        Label: "idea-generation"
        """

    idea_generation_v3_prompt = ""
    if "idea-generation-v3" in intent_labels:
        idea_generation_v3_prompt = """
        "idea-generation-v3" -
        Definition : refers to questions requesting generation of ideas and root cause analysis (rca) for a given \
        insight
        Examples:
        Q: What are the root causes associated with the cleansheet gap?
        Label: "idea-generation-v3"
        Q: What are the ideas or next best actions for taking corrective measures to reduce the leakage?
        Label: "idea-generation-v3"
        """

    negotiation_factory_prompt = ""
    if "negotiation_factory" in intent_labels:
        negotiation_factory_prompt = """
        "negotiation_factory" -
        Definition : is related to negotiation functions such as the generation of arguments, counter arguments,
          rebuttals, emails and negotiation strategy
        Examples:
        Q: What is the negotiation strategy with the top supplier for the highest purchased SKU?
        Label: "negotiation_factory"
        Q: I would like to generate arguments for the supplier SKF FRANCE?
        Label: "negotiation_factory"
        Q: Can you negotiation counter arguments with SKF FRANCE?
        Label: "negotiation_factory"
        """

    dynamic_ideas_prompt = ""
    if "dynamic-ideas" in intent_labels:
        dynamic_ideas_prompt = """
        "dynamic-ideas" -

        Definition :
        Refers to the questions wrt any entity such as Supplier, SKU, Insights, Analytics or Ideas
        Additionally, any user question requiring domain expertise or knowledge base \
        should also be classified as dynamic-ideas

        Understand the instructions mentioned below for learning more about this label

        Instructions -
        Below class of questions must be referred to dynamic ideas:

        1. Questions on ideas
        Questions asking ideas( or next best actions) or strategies or \
        optimisations for any sku, supplier, analytics \
        (such as Supplier Consolidation, OEM, Parametric Cost Modeling etc)
        Examples:
        a. What are the ideas/recommendations for Supplier X?
        Label: "dynamic-ideas"
        b. What strategies are recommended based on PCM and OEM analytics?
        Label: "dynamic-ideas"
        c. What are the top ideas for area X ? ( refers to analytics i.e. paramteric cost modeling, OEM, \
        Payment standardisations etc)
        Label: "dynamic-ideas"
        d. What do you recommend I shall do to implement idea X?
        Label: "dynamic-ideas"

        2. Questions on Opportunities
        Questions asking opportunities or savings potential or optimisations value or \
        potential gap for any sku, supplier, analytics (such as Supplier Consolidation,\
        OEM, Parametric Cost Modeling etc)
        Examples :
        Q: Give me the savings opportunities
        Label: "dynamic-ideas"
        Q: - SKU 00003294809 opportunities
        Label: "dynamic-ideas"
        Q: - What are the top opportunities in this category
        Label: "dynamic-ideas"
        Q: - Give me the opportunity in PCM
        Label: "dynamic-ideas"


        3. Domain Related and Problem Solving questions :
        This set of questions can be about category and domain specific strategies.
        Examples:
        Q: - How can I reduce my number of suppliers?
        Label: "dynamic-ideas"

        Q. What are the top negotiations I should focus on?
        Label: "dynamic-ideas"

        Q. What are the top impactful actions I can take to reduce my costs?
        Label: "dynamic-ideas"

        Questions may also be related to ADVICE , KNOWLEDGE , PRACTICES or \
        RECOMMENDATIONS based on SPECIFIC data (for supplier , category , sku) or \
        context or defined scenario on  idea generation, insights, \
        and root cause analysis. It also covers GENERIC questions related to \
        negotiation, strategy, objectives, arguments, counter-arguments, \
        rebuttals, emails

        Examples:
        Q. Can you provide me the top LCC suppliers I should target for category X?
        Label: "dynamic-ideas"

        Q.What are the ideas with the highest impact potential?
        Label: "dynamic-ideas"

        """

    source_ai_knowledge_prompt = ""
    if "source-ai-knowledge" in intent_labels:
        source_ai_knowledge_prompt = """
                "source-ai-knowledge" -
                Definition: Refers to GENERIC navigation related Questions -
                This includes  navigation-related inquiries, \
                and any questions not classified under other labels.

                Examples:
                Q: Hi, how are you?
                Label: "source-ai-knowledge"
                Q: - What does the Negotiation factory do
                Label: "source-ai-knowledge"
                """

    system_prompt = f"""
        You are a specialist in identifying the intent of user queries within the procurement
        domain, specifically in the {category_name} category. Your task is to analyze the user's
        question and the conversation history to determine the intent of the query.
        Use a step by step reasoning

        Note: Answer MUST ONLY be the labels from the Label List provided (Step 4), e.g "source-ai-knowledge"
        DO NOT INCLUDE THE WORD "Label".
        USE HISTORICAL CONTEXT ONLY IF NECESSARY.
        DO NOT return user query and Label as response.
        your response should be ONLY LABEL not a full sentence.
        """

    user_prompt = (
        f"""

    --Label List - {intent_labels}

    --Label definitions with examples

    {contract_qa_prompt}
    {key_facts_prompt}
    {news_qa_prompt}
    {idea_generation_prompt}
    {idea_generation_v3_prompt}
    {negotiation_factory_prompt}
    {dynamic_ideas_prompt}
    {source_ai_knowledge_prompt}
"""
        + """
    Step 1: Understand the user question (IMPORTANT)-
    {input}

    Step 2: Understand the historical conversation (IF NEEDED)
    {history}

    Step 3: Rephrase the question with the right entities and nouns such that the
        user question CAN be answered as a STANDALONE question with the same meaning

    Step 4: Predict the label based on understanding from above steps.
    (DO NOT include ## from HISTORY to predict the label)

    """
    )

    messages = [
        (
            "system",
            (
                " (IMPORTANT) If the user query has ##[intent]##, ONLY RETURN "
                " value of `intent` as the label. This RULE take precedence over all other rules."
                "e.g. Q: ##source-ai-knowledge## user query Label: source-ai-knowledge"
            ),
        ),
        ("system", system_prompt),
        ("user", user_prompt),
    ]

    return ChatPromptTemplate.from_messages(messages)


def question_enricher_prompt() -> PromptTemplate:
    """
    Takes the chat context and gives the prompts for generating the modified user query
    Returns
        (PromptTemplate): LLM prompt for generating the modified user query
    """
    return PromptTemplate.from_template(
        """
        Your task as a procurement expert is to enrich the user question such
        that it can be answered as a STANDALONE question without PREVIOUS context.

        Take a step by step approach to achieve this:

        Step 1: Understand the user question (IMPORTANT)-
        {input}

        Step 2: Understand the historical conversation (IF NEEDED)
        {history}

        Step 3: Rephrase the question such that the user question CAN be answered as a
          STANDALONE question.
        a. Enriching the key entities (e.g. category details) using the conversation.
        b. Return the most optimal version of the updated question which maintains the meaning.

        NOTE:
        Return only the updated question and not anything else
        Do not mention procurement domain.
        """,
    )
