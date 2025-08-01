"""Prompts for entity extraction component."""

# pylint: disable=C0301
from typing import Literal

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

from ada.use_cases.entity_extraction.pydantic_parsing import (
    FormattedAnswer,
    days_parser,
    months_parser,
)
from ada.utils.format.format import format_json_prompt_example

descriptions_dict = {
    "Contract duration": (
        "Total timeline in months of term of agreement from commencement / date of execution"
        " to expiry of contract"
    ),
    "Buyer termination period by convenience": (
        "The period of advance notice which must be given by buyer to terminate the contract"
        " before its end or expiry date with no reason caused by supplier and if supplier did"
        " not breach any agreements or terms of the contract. Only buyer / both parties"
        " can terminate the contract."
    ),
    "Supplier termination period by convenience": (
        "The period of advance notice which must be given by supplier to terminate the contract before"
        " its end or expiry date with no reason caused by buyer and if buyer did not breach any agreements"
        " orterms of the contract. Only supplier / both parties can terminate the contract."
    ),
    "Payment terms": (
        "The time period in days in which the buyer is supposed to make the "
        "payment for goods or services provided by supplier."
    ),
    "Buyer termination period by cause": (
        "Maximum number of days notice period that the buyer / purchaser or both parties must provide in advance"
        "to terminate the contract based on supplier performance or due to a breach in the contract or bancrupcy"
        " or any other reason caused by supplier. Termination must be initiated by buyer / purchaser or by both"
        " parties. Select maximal number if there are multiple reasons."
    ),
}

FormattedAnswer.update_number_description(
    new_description="Number of days answering the question or NA",
)

buyer_few_shot_examples = [
    {
        "example_query": (
            "Contract shall be extended automatically for a period of one (1) year in each case unless terminated"
            " in writing by either party 180 calendar days before expiry of term."
        ),
        "result": format_json_prompt_example(
            FormattedAnswer.parse_obj(
                {
                    "number": "180",
                    "reasoning": (
                        "Both buyer and supplier can terminate contract without any cause,"
                        " therefore answer is 180 days.\n"
                    ),
                },
            ),
        ),
    },
    {
        "example_query": (
            "Either party can terminate the contract with 60 days"
            " notice if other party had breached any terms of this agreement."
        ),
        "result": format_json_prompt_example(
            FormattedAnswer.parse_obj(
                {
                    "number": "NA",
                    "reasoning": (
                        "Breach of the contract is a cause, not relevant for termination by convenience,"
                        " therefore answer is NA.\n"
                    ),
                },
            ),
        ),
    },
    {
        "example_query": (
            "Buyer/purchaser shall have the right to terminate this Agreement immediately should"
            " supplier/seller in any way breach the contract."
        ),
        "result": format_json_prompt_example(
            FormattedAnswer.parse_obj(
                {
                    "number": "NA",
                    "reasoning": (
                        "Termination with cause from supplier/seller (breach of the contract) is not relevant,"
                        " therefore answer is NA.\n"
                    ),
                },
            ),
        ),
    },
    {
        "example_query": "Supplier has the option to terminate the contract with 60 days notice if buyer has agreed to this.",
        "result": format_json_prompt_example(
            FormattedAnswer.parse_obj(
                {
                    "number": "NA",
                    "reasoning": "No information for buyer/purchaser terminating the contract.\n",
                },
            ),
        ),
    },
]

supplier_few_shot_examples = [
    {
        "example_query": (
            "Contract shall be extended automatically for a period of one (1) year"
            " in each case unless terminated in writing by either party 180 calendar"
            " days before expiry of term."
        ),
        "result": format_json_prompt_example(
            FormattedAnswer.parse_obj(
                {
                    "number": "180",
                    "reasoning": (
                        "Both buyer and supplier can terminate contract without any cause,"
                        " therefore answer is 180 days.\n"
                    ),
                },
            ),
        ),
    },
    {
        "example_query": (
            "Either party can terminate the contract with 60 days notice if other party had breached"
            " any terms of this agreement."
        ),
        "result": format_json_prompt_example(
            FormattedAnswer.parse_obj(
                {
                    "number": "NA",
                    "reasoning": (
                        "Breach of the contract is a cause, not relevant for termination by convenience,"
                        " therefore answer is NA.\n"
                    ),
                },
            ),
        ),
    },
    {
        "example_query": (
            "Supplier shall have the right to terminate this Agreement immediately should buyer"
            " in any way breach the contract."
        ),
        "result": format_json_prompt_example(
            FormattedAnswer.parse_obj(
                {
                    "number": "NA",
                    "reasoning": (
                        "Termination with cause from supplier/seller (breach of the contract) is not relevant,"
                        " therefore answer is NA.\n"
                    ),
                },
            ),
        ),
    },
    {
        "example_query": "Buyer has the option to terminate the contract with 60 days notice if supplier has agreed to this.",
        "result": format_json_prompt_example(
            FormattedAnswer.parse_obj(
                {
                    "number": "NA",
                    "reasoning": "No information for supplier terminating the contract.\n",
                },
            ),
        ),
    },
]

few_shot_examples_dict = {
    "Buyer termination period by convenience": buyer_few_shot_examples,
    "Supplier termination period by convenience": supplier_few_shot_examples,
}


def get_system_prompt() -> str:
    """
    Defines the default system prompt to use.
    Returns:
        (str): System prompt
    """
    return "You are a precise and accurate contract accountant."


def get_duration_prompt() -> PromptTemplate:
    """
    Defines the prompt to use extract an entity based on contract duration.
    Returns:
        (PromptTemplate): Prompt to get the duration of the contract
    """
    prompt_template = """
    Extract the entity {entity_name} from the text below based on the entity description:
    {description}

    Focus on the entity description, extract entity only if it's absolutely relevant to description.

    The descriptions are there to show you how this information might be present in the text.

    Transform the output into months.
    Provide output as number of months followed by the concise reasoning why this answer is correct.
    If information in text is irrelevant or incorrect, return NA. If you are not sure return NA.

    {format_instructions}

    TEXT: {query}
    """

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["query"],
        partial_variables={
            "format_instructions": months_parser.get_format_instructions(),
            "entity_name": "Contract duration",
            "description": descriptions_dict["Contract duration"],
        },
    )
    return prompt


def get_few_shot_prompts() -> tuple[str, PromptTemplate, str]:
    """
    Defines the prompt which gives the few shot result.
    Returns:
        (tuple[str, PromptTemplate, str]): prefix, example and suffix prompts
    """
    example_prompt = PromptTemplate(
        input_variables=["example_query", "result"],
        template="TEXT: {example_query}\nOUTPUT:\n{result}",
    )

    prefix_prompt = """
    Extract the entity {entity_name} from the text below based on the entity description:
    {description}

    Focus on the entity description, extract entity only if it's absolutely relevant to description.

    The descriptions are there to show you how this information might be present in the text.

    Provide output as number and unit of measure (only days) followed by the concise reasoning why this answer is correct.
    If information in text is irrelevant or incorrect, return NA. If you are not sure return NA.

    {format_instructions}

    """

    suffix_prompt = """
    TEXT: {query}
    """

    return prefix_prompt, example_prompt, suffix_prompt


def get_convenience_prompt(contract_type: Literal["Buyer", "Supplier"]) -> FewShotPromptTemplate:
    """
    Defines the prompt for entities terminated with a period of convenience.
    Returns:
        (FewShotPromptTemplate): Gives the convenience prompts
    """
    prefix_prompt, example_prompt, suffix_prompt = get_few_shot_prompts()

    prompt = FewShotPromptTemplate(
        examples=few_shot_examples_dict[f"{contract_type} termination period by convenience"],
        example_prompt=example_prompt,
        prefix=prefix_prompt,
        suffix=suffix_prompt,
        input_variables=["query"],
        partial_variables={
            "format_instructions": days_parser.get_format_instructions(),
            "entity_name": f"{contract_type} termination period by convenience",
            "description": descriptions_dict[f"{contract_type} termination period by convenience"],
        },
    )

    return prompt


chain_prompt_template_dict = {
    "Payment terms": """
    You are an experienced lawyer who is specialized in analyzing commercial contracts.

    What are the {entity_name}, which is the {description}

    Return only number of days followed by the concise reasoning why this answer is correct.

    Output must strictly follow the format. Always return your answer in JSON format.

    {format_instructions}

    TEXT: {context}
    """,
    "Buyer termination period by cause": """
    You are an experienced lawyer who is specialized in analyzing commercial contracts.

    What are the {entity_name}, which is the {description}

    Causes can be but not limited to bankruptcy, counterfeit production by supplier,
    change of control or other causes. Termination by convenience is irrelevant.
    Return only number of days followed by the concise reasoning why this answer is correct.

    Output must strictly follow the format. Always return your answer in JSON format.

    {format_instructions}

    TEXT: {context}
    """,
}


def get_chain_prompt(
    entity_name: str | Literal["Payment terms", "Buyer termination period by cause"],
) -> PromptTemplate:
    """
    Defines the chained prompt using LangChain template.
    Args:
        (entity_name: str |  Literal): Gives the entities to extract
    Returns:
        (PromptTemplate): Entity extraction chain prompt
    """
    prompt_template = chain_prompt_template_dict[entity_name]

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context"],
        partial_variables={
            "format_instructions": days_parser.get_format_instructions(),
            "entity_name": entity_name,
            "description": descriptions_dict[entity_name],
        },
    )

    return prompt


def get_pydantic_formatting_prompt(parser: PydanticOutputParser) -> PromptTemplate:
    """
    Defines prompt to format langchain output for pydantic parser.
    Args:
        parser (PydanticOutputParser): parser for the prompt
    Returns:
        (PromptTemplate): prompt with a pydantic parser
    """
    prompt_template = """
        Format input as JSON strictly following the instruction.

        {format_instructions}

        Input: {query}
        """

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["query"],
        partial_variables={
            "format_instructions": parser.get_format_instructions(),
        },
    )

    return prompt
