"""Prompts for langchain chains."""

from typing import Any

from langchain.chains.qa_with_sources.stuff_prompt import template as stuff_template
from langchain_core.messages import SystemMessage
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
)


def doc_q_and_a_prompt(
    sys_prompt_template: str = "",
    model_host: str = "",
    include_sources=True,
    human_prompt_template: str = "",
) -> ChatPromptTemplate | PromptTemplate:
    """
    Prompt for vanilla q and a
    Args:
        sys_prompt_template (str): System prompt template
        model_host (str): Model host
        include_sources (bool): Include sources
        human_prompt_template (str): Human prompt template
    Returns:
        ChatPromptTemplate | PromptTemplate: Prompt template
    """
    if "chat" in model_host:
        if sys_prompt_template == "":
            if include_sources:
                sys_prompt_template = """As a friendly and knowledgeable legal advisor on
                contracts, I am here to assist you with any questions. Given the following \
                extracted parts of a long document and asked question, I will create a \
                final answer with references ("SOURCES").
                Each response will include relevant references under the "SOURCES" section.
                In case document does not provide any information about it or I am unable to provide an answer,\
                 I will be honest and will return only sentence: "ANSWER IS NOT FOUND", nothing more.
                 I will not apoligize for inability to answer.
                 Regardless of the situation, my response will always include a "SOURCES" section. Provided information:
                 {context}."""
            else:
                sys_prompt_template = """As a friendly and knowledgeable chatbot, \
                I am here to assist you with any questions (without disclosing sources or references).
Given the following extracted parts of a long document and a question, I will create a final answer.
In case I am unable to provide an answer, I will be honest and admit my lack of knowledge.
Regardless of the your question, I will never mention any reference, document, policy or the procedure.
I will always exclude "Procurement Services Procedure No: PR-112" from the answer!
Provided information: {context}"""

        if human_prompt_template == "":
            template = "{question}"
        else:
            template = human_prompt_template
        messages = [
            SystemMessagePromptTemplate.from_template(sys_prompt_template),
            HumanMessagePromptTemplate.from_template(template),
        ]
        prompt = ChatPromptTemplate.from_messages(messages)
    else:
        prompt = PromptTemplate(template=stuff_template, input_variables=["context", "question"])

    return prompt


def create_step_by_step_template() -> str:
    """
    Step by step template for reasoning prompt.
    Returns:
        (str): Step by step template
    """
    return """{question}\n Let's think step by step."""


def qna_chain_template() -> str:
    """
    QNnA Chain Template for reasoning.
    Returns:
        (str): QNA Chain Template
    """
    return """Question: Who lived longer, Muhammad Ali or Alan Turing?
                Are follow up questions needed here: Yes.
                Follow up: How old was Muhammad Ali when he died?
                Intermediate answer: Muhammad Ali was 74 years old when he died.
                Follow up: How old was Alan Turing when he died?
                Intermediate answer: Alan Turing was 41 years old when he died.
                So the final answer is: Muhammad Ali

                Question: When was the founder of craigslist born?
                Are follow up questions needed here: Yes.
                Follow up: Who was the founder of craigslist?
                Intermediate answer: Craigslist was founded by Craig Newmark.
                Follow up: When was Craig Newmark born?
                Intermediate answer: Craig Newmark was born on December 6, 1952.
                So the final answer is: December 6, 1952

                Question: Who was the maternal grandfather of George Washington?
                Are follow up questions needed here: Yes.
                Follow up: Who was the mother of George Washington?
                Intermediate answer: The mother of George Washington was Mary Ball Washington.
                Follow up: Who was the father of Mary Ball Washington?
                Intermediate answer: The father of Mary Ball Washington was Joseph Ball.
                So the final answer is: Joseph Ball

                Question: Are both the directors of Jaws and Casino Royale from the same country?
                Are follow up questions needed here: Yes.
                Follow up: Who is the director of Jaws?
                Intermediate Answer: The director of Jaws is Steven Spielberg.
                Follow up: Where is Steven Spielberg from?
                Intermediate Answer: The United States.
                Follow up: Who is the director of Casino Royale?
                Intermediate Answer: The director of Casino Royale is Martin Campbell.
                Follow up: Where is Martin Campbell from?
                Intermediate Answer: New Zealand.
                So the final answer is: No

                Question: {question}
                Are follow up questions needed here: Yes.
                """


def create_grammar_check_message(text: str) -> ChatPromptTemplate:
    """
    Message to send to GPT to determine if grammar is correct.
    Args:
        text (str): Text to check grammar
    Returns:
        ChatPromptTemplate: Prompt message
    """
    return ChatPromptTemplate.from_messages(
        [
            ("system", "You assist in improving sentences."),
            (
                "user",
                (
                    f"Grammatically correct the following sentence: {text}. Return ONLY "
                    f"SENTENCE."
                ),
            ),
        ],
    )


def create_similar_question_message(question: str) -> ChatPromptTemplate:
    """
    Message to send to GPT to rephrase a question.
    Args:
        question (str): Question to rephrase
    Returns:
        ChatPromptTemplate: Prompt message
    """
    return ChatPromptTemplate.from_messages(
        [
            ("system", "You are a creator of similar questions."),
            (
                "user",
                f"Ask following question: '{question}' in a different way. "
                "Return the original question if it is not possible.",
            ),
        ],
    )


def check_answer_prompt(question: str, answer: str) -> PromptTemplate:
    """
    Prompt to check whether LLM was capable to answer the question
    Args:
        question (str): User question
        answer (str): LLM answer
    Returns:
        PromptTemplate: Prompt message to check the answer
    """
    prompt_template = f"""user asked the question, and the AI chatbot provided an answer from
     provided document information.
    user question: {question}
    chatbot answer: {answer}

    YOUR TASK:
    Yes: The chatbot provided any form of relevant response to the question, even if it was a
         greeting or a follow-up question.
    No: The chatbot explicitly mentioned its inability to answer or lacked the necessary
        information.
    Reply with one word—"yes" or "no" only!

    Your answer:"""
    return PromptTemplate.from_template(prompt_template)


def general_answer_prompt(question: str, category: str) -> ChatPromptTemplate:
    """
    Prompt to provide an answer using LLM internal knowledge.

    Args:
        question (str): The question asked by the user.
        category (str): The category related to the question.

    Returns:
        ChatPromptTemplate: A template for generating a chat response.
    """
    prompt_template = f"""
        You are a procurement expert. The Category Manager for the {category} category has asked the
        following question:
        {question}

        Provide an answer to this question using your procurement knowledge. Additionally,
        include a response to any general greetings or basic questions to keep the user engaged in
        the interaction with the chatbot.
        """
    return ChatPromptTemplate([SystemMessage(prompt_template)])


def doc_info_answer_prompt(question: str, doc_info: dict[str, Any]) -> PromptTemplate:
    """
    Prompt to provide an answer using LLM internal knowledge
    Args:
        question (str): User question
        doc_info (dict[str, Any]): Document information
    Returns:
        PromptTemplate: Prompt message
    """
    prompt_template = f"""
        You are the procurement expert. You have AI procurement assistant
        which helps you with the work. This AI assistant was asked:

        {question}

        Provide an answer from given document information {doc_info}
        Answer to the point and only on asked question

        ANSWER:
        """
    return PromptTemplate.from_template(prompt_template)


def doc_clause_match_prompt(question: str, doc_clauses: list[Any]) -> PromptTemplate:
    """
    Prompt to provide best match clause to question using LLM internal knowledge
    Args:
        question (str): User question
        doc_clauses (list[Any]): Document clauses
    Returns:
        PromptTemplate: Prompt message to provide best match clause in document
    """
    prompt_template = f"""
            You are the procurement expert. You have AI procurement assistant
            which helps you with the work. This AI assistant was asked:

            {question}

            Provide best ONLY one match clause dictionary from given list of clauses {doc_clauses}
            Return complete dictionary containing "Answer", "Clause/section", "Most Similar
            Sections" in strictly single python dictionary object format ONLY
            EXAMPLE:'{{"Answer": "NO", "Clause/section": "Share commitment level", "Most Similar
            Sections": [78, 18, 17, 59]}}'
            """
    return PromptTemplate.from_template(prompt_template)


def doc_qna_step_by_step_sys_prompt() -> str:
    """
    Prompt to get answer from user question using step-by-step approach on available documents
    Returns:
        (str): Prompt message
    """
    return """Act as procurement expert and AI procurement assistant.
    Given the following pieces of retrieved context and a question, You will create a final
    answer following below steps.
    STEP 1. Understand the question (IMPORTANT) - {question}
    STEP 2. Try to answer question from provided document texts.
    STEP 3. If you are unable to find answer directly from the provided document text,
    try to use chain of thoughts question answering technique to provide answer.

    NOTE:
    1. Be concise in answer, provide only details which user asked for.
    2. Do not use retrieved content if not relevant
    3. Do not include phrases like "based on the provided document" in your answer.
    4. If you cannot provide an answer from the provided document, return "NO" without any
       explanation.
    5. If there is a reference link in the documents, include the link as part
    of the response in [key_word](link) format.

    Provided document texts: {context}
    """
