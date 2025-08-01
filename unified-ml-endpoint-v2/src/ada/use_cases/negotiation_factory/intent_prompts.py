"""Negotiation Factory Intent Prompts"""

from __future__ import annotations

from typing import Any

from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

from ada.utils.config.config_loader import read_config

negotiation_conf = read_config("use-cases.yml")["negotiation_factory"]


def intent_prompt(
    category_name: str,
    selected_elements: dict[str, Any],
    previous_response_type: str,
    likely_current_intent: str,
) -> PromptTemplate:
    """Find the sub intents from the negotiation factory
    Args:
        category name (str): category name
        selected_ekements (dict): dictionary of selected elements
        previous_response_type (str): Response type of the previous response
        likely_current_intent (str): Likely value of the current intent
    Returns:
        PromptTemplate: A template for the generated prompt."""
    intent_list = [
        "init",
        "begin",
        "insights",
        "objective",
        "counter_arguments",
        "arguments",
        "rebuttals",
        "emails",
        "user_questions",
        "strategy",
        "approach_cp",
        "approach_sp",
        "approach_bp",
        "approach_tnt",
        "approach_tnt_change",
        "strategy_change",
        "offer",
        "finished",
        "summary_email",
        "select_carrot_sticks",
    ]
    init_examples = """Definition : Helping the user identify the suppliers.
    Its limited to the following list with varying values for `n`
    1. "Top `n` suppliers by spend"
    2. "`n` Tail suppliers"
    3. "`n` Single source suppliers"
    4. "`n` suppliers with missing PO"
    5. "`n` suppliers with largest YoY spend evolution"
    6. Top supplier
    Label: "init"
    """
    beginning_examples = """ "begin" -
        Definition : The starting point for negotiation. If someone
        wants to START Negotiation ( INCLUDING OR EXCLUDING  specific supplier ) WITHOUT any additional details.
        if user wants to start negotiation but has NOT mentioned any specific steps \
        such as show insight or set objective etc.
        Example:
        Q: Supplier Abc company
        Label: "begin"
        Q: "lets start negotiation?",
        Label: "begin"
        Q: "help me in negotiation with abc supplier?",
        Label: "begin"
        """

    insights_examples = """ "insights" -
        Definition : If someone wants to show INSIGHTS ( INCLUDING or EXCLUDING supplier name )
        Insights are the valuable pieces of information or understanding gained for the negotiation
        process. They can be used to inform future strategies or decisions.

        Note: here, NOT all details about supplier/spend are Insights. user will mention Insight specifically
        any mention of the word insight will have the label "insights"

        Examples :
        Q: show me insights
        Label: "insights"
        Q. Share insights for supplier XYZ
        Label: "insights" \n"""

    objectives_examples = """ "objective" -
        Definition : If someone wants to see or set negotiation objectives ( INCLUDING or EXCLUDING supplier name ).
        `Negotiation objective` can be defined as a desired outcome required during negotiations with the supplier, \
                 like reducing price , optimize cost saving etc.
        Note: Any mention of the word `objectives` will have the label "objectives"
        Examples :
        Q: set negotiation objectives
        Label: "objective"
        Q: Set negotiation objectives
        Label: "objective"
        Q: Set Negotiation Objectives
        Label: "objective"
        Q. May i see probable objectives for supplier XYZ
        Label: "objective"
        Q.Change negotiation objectives
        Label: "objective"
        Q: change negotiation objectives
        Label: "objective"
        Q: Change Negotiation Objectives
        Label: "objective"
        """

    counter_argument_examples = """ "counter_arguments" -
        Definition : These are the points raised in opposition to a supplier's argument or claim. They
        are used to challenge the validity of the supplier's stance and to negotiate better terms.
        This label is used when the user is asking for counter arguments to a given argument.
        Note: Any explicit mention of counter arguments will have the label "counter_arguments"

        Example:
        Q: "What could be a supplier's counter argument to a 10% reduction in price request?",
        Label: "counter_arguments" \n
        Q: "Regenerate counter arguments in a more subtle tone",
        Label: "counter_arguments" \n"""

    argument_examples = """ "arguments" -
        Definition : These are the points or reasons put forward to persuade the supplier in favor of a
        certain action or decision. This label is used when the user is asking for arguments based on supplier context information

        Note: Any explicit mention of arguments will have the label "arguments"

        Examples :
        Q: Start new round
        Label: "arguments"
        Q: Start New Round
        Label: "arguments"
        Q: New Round
        Label: "arguments"
        Q: Begin New Round
        Label: "arguments"
        Q: start new round
        Label: "arguments"
        Q: Please generate arguments for negotiating with Supplier X?
        Label: "arguments" \n
        Q: Regenerate arguments in a more aggressive tone?
        Label: "arguments" \n"""

    rebuttal_examples = """ "rebuttals" -
        Definition : These are responses to the supplier's arguments. They are used to refute or
        invalidate the supplier's counterpoints, thereby strengthening the buyer's position in the
        negotiation. When the previous response is `negotiation_arguments_reply` the current Label is
        rebuttals

        Examples :
        Q: Generate rebuttals for the above counters
        Label: "rebuttals" \n
        Q: Regenerate rebuttals in a more aggressive tone?
        Label: "rebuttals" \n
        Q: Reply to a supplier's argument\n
        Label: arguments
        Q: Supplier is saying they will not give a discont
        Label: rebuttals
        """

    email_examples = """ "emails" -
        Definition : generates e-mails, This refers to the written communication sent to the supplier
        It generally includes generate a new email, generate a follow up email, and reply to a supplier's email
        Examples :
        Q1: Generate a new email for price reduction?
        Label: "emails" \n
        Response message: Can you provide the context for the emails?
        Q2: I would like to negotiate volume disounts and set up a meeting.
        Label: "emails" \n
        Q3: Can you provide the email from supplier?
        Response: Thank you for your email, sorry, we can't reduce price
        Lable: "emails" \n
        """

    user_query_examples = """ "user_questions" -
        Definition : All user questions which DO NOT fit under other intents, can be classified as
        negotiation 'user_questions'. Majorly fact questions about the supplier, SKU or category are
        categorized here.
        Keep in mind that in procurement, terms such as supplier, vendor, provider, seller,
        and any similar synonyms can be used interchangeably
        These are the queries or doubts raised by the user regarding the negotiation process, terms, or
        conditions. They are used to seek clarification or additional information.
        Examples :
        Q: Hi
        Label: "user_questions"
        Q. Can you give me the top SKU for supplier C?
        Label: "user_questions"
        Q. What is Framework led approach or define any methodology
        Label: "user_questions" \n"""

    approach_cp_name = negotiation_conf["cta_button_map"]["approach_cp"].replace("Set ", "")
    approach_sp_name = negotiation_conf["cta_button_map"]["approach_sp"].replace("Set ", "")
    approach_bp_name = negotiation_conf["cta_button_map"]["approach_bp"].replace("Set ", "")

    strategy_name = negotiation_conf["cta_button_map"]["strategy"].replace("Set ", "")
    strategy_examples = f""" "strategy" -
        Definition : This refers to the plan of action designed to achieve a particular goal in the
        negotiation. When user asks to get {strategy_name} to use for a supplier. User can also ask
        about components of {strategy_name} such as market approach, sourcing approach, \
        pricing methodology or contracting methodology.

        Note: When the user need {strategy_name}, the user will mention {strategy_name} or negotiation {strategy_name}

        Important:
        1. Only mention of negotiation 'strategy' or {strategy_name} should be in this category.
        2. When the user asks to change market approach, pricing methodology or
        contracting methodology the label is 'strategy_change' intent.
        3. When the user asks to change {approach_cp_name}, the label is 'strategy_change' intent.
        4. When the user asks to change {approach_sp_name}, the label is 'strategy_change' intent.

        Examples :
        Q: I want to know what type of {strategy_name} to use with Supplier X?
        Label: "strategy"
        Q: {strategy_name} with Supplier X?
        Label: "strategy"
        Q: change the maket approach or pricing methodology
        Label: "strategy_change"
        Q: change the pricing methodology
        Label: "strategy_change"
        Q: change the contracting methodology
        Label: "strategy_change"
        Q. change the supplier positioning
        Label: "strategy_change"
        Q. change the category positioning
        Label: "strategy_change"
        Q: I want to know what {approach_cp_name} to use with Supplier X?
        Label: "strategy_change"
        """

    category_positioning_values = "/".join(negotiation_conf["category_positioning"])
    supplier_positioning_values = "/".join(negotiation_conf["supplier_positioning"])

    user_query_examples = """ "user_questions" -
        Definition : All user questions which DO NOT fit under other intents, can be classified as
        negotiation 'user_questions'. Majorly fact questions about the supplier, SKU or category are
        categorized here.
        Keep in mind that in procurement, terms such as supplier, vendor, provider, seller,
        and any similar synonyms can be used interchangeably
        These are the queries or doubts raised by the user regarding the negotiation process, terms, or
        conditions. They are used to seek clarification or additional information.
        Examples :
        Q: Hi
        Label: "user_questions"
        Q. Can you give me the top SKU for supplier C?
        Label: "user_questions"
        Q. What is Framework led approach or define any methodology
        Label: "user_questions" \n"""

    approach_cp_examples = f""" "approach_cp" -
        Definition : This refers to the approach for category positions
        for negotiation. When user asks to get {approach_cp_name} to use for a supplier.

        Also be mindful about these {approach_cp_name} names: \
        {category_positioning_values} \
        Any mention of "Set " before these names, will have the label `approach_cp`

        Important:
        1. Only mention of {approach_cp_name} should be in this category.
        2. If the user request to Set {category_positioning_values} then the label is "approach_cp"

        Examples :
        Q. Set {approach_cp_name}
        Label: "approach_cp"
        Q: Change {approach_cp_name}
        Label: "strategy_change"
        """

    approach_sp_examples = f""" "approach_sp" -
        Definition : This refers to the approach for supplier positions
        for negotiation. When user asks to get {approach_sp_name} to use for a supplier.

        Also be mindful about these {approach_sp_name} names: \
        {supplier_positioning_values} \
        Any mention of "Set " before these names, will have the label `approach_sp`

        Important:
        1. Only mention of {approach_sp_name} should be in this category.
        2. If the user request to Set {supplier_positioning_values} then the label is "approach_sp"

       Examples :
        Q. Set {approach_sp_name}
        Label: "approach_sp"
        Q: Change {approach_sp_name}
        Label: "strategy_change"
        """

    approach_bp_examples = f""" "approach_bp" -
        Definition : This refers to the approach for buyer positions
        for negotiation. When user asks to get {approach_bp_name} to use for a supplier.

       Examples :
        Q. Set {approach_bp_name}
        Label: "approach_bp"
        Q. Set Buyer Attractiveness
        Label: "approach_bp"
        Q. Set buyer attractiveness
        Label: "approach_bp"
        Q. Set buyer positioning
        Label: "approach_bp"
        Q: Change {approach_bp_name}
        Label: "approach_bp"
        Q. Change Buyer Attractiveness
        Label: "approach_bp"
        Q. Change buyer attractiveness
        Label: "approach_bp"
        Q. Change buyer positioning
        Label: "approach_bp"
        """

    approach_tnt_examples = """ "approach_tnt" -
        Definition : This refers to the set negotiation tone & tactics.
        Important:
            1. If the user request to Set tones & tactics then the label is "approach_tnt"
       Examples :
        Q. Set tone & tactics
        Label: "approach_tnt"
        Q: Set tones & tactics
        Label: "approach_tnt"
        Q: Set tones
        Label: "approach_tnt"
        Q: Set tactics
        Label: "approach_tnt"
        Q. Set Tone and Tactics
        Label: "approach_tnt"
        Q. Set Tone & tactics
        Label: "approach_tnt"
        Q. Tone & tactics
        Label: "approach_tnt"
        """

    approach_tnt_change_examples = """ "approach_tnt_change" -
        Definition : This refers to the change negotiation tone & tactics.
        Important:
            1. If the user request to change tones & tactics then the label is "approach_tnt_change"
            2. If the word change is there then the label is "approach_tnt_change"
       Examples :
        Q. Change tone & tactics
        Label: "approach_tnt_change"
        Q: Change tones & tactics
        Label: "approach_tnt_change"
        Q: Change tones
        Label: "approach_tnt_change"
        Q: Change tactics
        Label: "approach_tnt_change"
        Q. Change Tone and Tactics
        Label: "approach_tnt_change"
        Q. Change Tone & tactics
        Label: "approach_tnt_change"
        """

    offer_examples = """ "offer" -
        Definition : This refers to add or save or change latest offer.
        Important:
            1. If the user request to add or save or change latest offer then the label is "approach_tnt_change"
            2. If the word add or save or change is there then the label is "offer"
       Examples :
        Q. add latest offer
        Label: "offer"
        Q: save latest offer
        Label: "offer"
        Q: add offer
        Label: "offer"
        Q: save offer
        Label: "offer"
        Q. Save latest offer
        Label: "offer"
        Q. Save offer
        Label: "offer"
        Q. Add latest offer
        Label: "offer"
        Q. Add offer
        Label: "offer"
        """

    finished_examples = """ "finished" -
        Definition : This refers to finish the negotiation.
        Important:
            1. If the user request to finish negoiation then the label is "finished"
            2. If the word finish or stop or end or complete is there then the label is "finished"
       Examples :
        Q. Finish Negotiation
        Label: "finished"
        Q: Finish negotiation
        Label: "finished"
        Q: Finish a negotiation
        Label: "finished"
        Q: finish a negotiation
        Label: "finished"
        Q. End Negotiation
        Label: "finished"
        Q: End negotiation
        Label: "finished"
        Q: End a negotiation
        Label: "finished"
        Q: complete a negotiation
        Label: "finished"
        """

    summary_email_examples = """ "summary_email" -
        Definition : Generate summary e-mail upon ending the negotiation, This refers to the
        written communication sent to the supplier
        It generally includes information regarding offers received,targets and insights
        Examples :
        Q: Generate Summary Email
        Label: "summary_email"
        Q: Generate summary email
        Label: "summary_email"
        Q: I would like to generate summary email
        Label: "summary_email"
        Q: Summary Email
        Label: "summary_email"
        Q: generate summary email
        Label: "summary_email"
        """

    carrots_sticks_examples = """ "select_carrot_sticks" -
        Definition : Generate carrots and sticks for negotiation.
        Examples :
        Q: Select carrots and Sticks
        Label: "select_carrot_sticks"
        Q: Selects carrots
        Label: "select_carrot_sticks"
        Q: I would like to selects sticks
        Label: "select_carrot_sticks"
    """

    context_prompt = f"""
    Label List - [{", ".join(intent_list)}]

    1. {beginning_examples}
    2. {insights_examples}
    3. {objectives_examples}
    4. {strategy_examples}
    5. {argument_examples}
    6. {counter_argument_examples}
    7. {rebuttal_examples}
    8. {email_examples}
    9. {approach_cp_examples}
    10. {approach_sp_examples}
    11. {approach_bp_examples}
    12. {user_query_examples}
    13. {init_examples}
    14. {approach_tnt_examples}
    15. {approach_tnt_change_examples}
    16. {offer_examples}
    17. {finished_examples}
    18. {summary_email_examples}
    19. {carrots_sticks_examples}
    """
    selected_elements_type = [key for key, item in selected_elements.items() if item]
    selected_elements_type_str = ", ".join(selected_elements_type) if selected_elements_type else ""

    selected_element_str = (
        f"""Current User Selected Element Type - {selected_elements_type_str}
                             -- (IMPORTANT since it define the UI element user is querying about)"""
        if selected_elements_type_str
        else ""
    )
    system_prompt = f"""
        You are a specialist in identifying the intent of user queries within the procurement
        domain, specifically in the {category_name} category. Your task is to analyze the user's
        question and the conversation history to determine the intent of the query.
        Use a step by step reasoning

        Step 1: Understand the possible labels for the intents:
        {context_prompt}

        Step 2: Understand the available context,
         -- {selected_element_str}
         -- Previous response type: {previous_response_type} - Determines current label
         {likely_current_intent}

        Step 3: Generate the intent for the CURRENT input, ONLY from the list of labels.
        """
    user_prompt = """
        Instructions: (IMPORTANT)
        1. Answer MUST be from step 3 and only be the label from the Label List provided.
        2. UNLESS the previous response type is strategy or approach, the CURRENT label is NOT  negotiation strategy change.
        3. You will receive conversation history as well, but only generate the intent for the current input.
           Use the conversation history to understand which flow the user is in,
           This is super helpful when identifying arguments and emails
        4. ONLY generate label. DO NOT GENERATE a full sentence.
        5. Look at the Probable current intent, its a good indicator of the current intent.
        6. The user_questions is the label only when it cannot match any of the others.
        7. If previous_response has '_modify', the label is the same.
           e.g. previous_response is `counter_argument_modify` then the label counter_argument.

        Previous `conversation history (UNDERSTAND PREVIOUS REQUEST/ RESPONSE, CONTEXT, AND DO FILL PRONOUNS):
        {history}
        Current input: {input}
        """

    prompt_template = ChatPromptTemplate.from_messages(
        [("system", system_prompt), ("user", user_prompt)],
    )

    return prompt_template
