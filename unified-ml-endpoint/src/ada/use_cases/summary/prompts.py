"""Prompts for summary component."""

from langchain_core.prompts import PromptTemplate

CONTRACT_SUMMARY_TEMPLATE = """
            As an experienced legal analyst, create a short and precise summary of the contract using only information from
            the Chunks. Working step by step, organize the Chunks outline into well-structured one-sentence paragraphs in
            the following sections:
                1. General Purpose: Details regarding the background of service and overview of what the contract is for
                2. Contract Length & Renewal: Include details on key dates or timeline of contract and mention process of renewal
                   (if applicable)
                3. Payment Terms: Summarize key points regarding payment such as deadlines, applicable interest rate etc
                4. Performance Management: Summarize requirements regarding KPIs, performance review and cadence
                5. Default: Details on actions regarding failure to perform or default on obligations including remediation
                   (if applicable)
                6. Termination: Key details regarding termination, including requirements, notice and timelines

            Focus only on the key sections of the contract described above.
            Be precise. Limit your response to 1 short sentence in each section.
            Do not include disclosures or disclaimers.
            Do not include any additional information beyond what is provided in the Chunks.
            Do not use words like however, generally speaking, overall, we, they, we think.

            Remember
            - don't use line breaks /n
            - summarize each section in only 1 short sentence

            Chunks: `{data_chunks}`
        """

DOCUMENT_SUMMARY_TEMPLATE = """
            Create a summary of the each chunk (~20-50 words) with the key information content
            and output results as bullet points. Start with a bullet point describing the general purpose of the
            text. Do not include disclosure or disclaimer statements.
            Do not include any extra information other than what is provided. Do not include words like however,
            overall, we, they, we think.
            Focus on key sections of the texts, and highlight them in concise way.

            Remember
            - don't use line breaks /n

            chunks: `{context}`
        """


def get_reduce_template(document_type: str) -> str:
    """
    Returns a template for summarizing a document based on its type.

    This function provides a specific template for summarizing content depending on whether the
    document is a "contract" or a general text. The templates guide how to structure and
    present the summary, focusing on precision and exclusion of unnecessary information.

    Args:
        document_type (str): The type of document to summarize. Must be either "contract"
        or "general".

    Returns:
        str: A string template for summarizing the document. The template is
        tailored to the specified document type and includes instructions on how
        to format the summary.
    """

    contract_instructions = """
            As an experienced legal analyst, create a short and precise final summary of the contract using only information from
            the summary of each chunk. Working step by step, organize the Chunks outline into well-structured one-sentence
            paragraphs in the following sections:
                1. General Purpose: Details regarding the background of service and overview of what the contract is for
                2. Contract Length & Renewal: Include details on key dates or timeline of contract and mention process of renewal
                   (if applicable)
                3. Payment Terms: Summarize key points regarding payment such as deadlines, applicable interest rate etc
                4. Performance Management: Summarize requirements regarding KPIs, performance review and cadence
                5. Default: Details on actions regarding failure to perform or default on obligations including remediation
                   (if applicable)
                6. Termination: Key details regarding termination, including requirements, notice and timelines

            Focus only on the key sections of the contract described above.
            Be precise. Limit your response to 1 short sentence in each section.
            Do not include disclosures or disclaimers.
            Do not include any additional information beyond what is provided in the Chunks.
            Do not use words like however, generally speaking, overall, we, they, we think.

            Remember
            - don't use line breaks /n
            - summarize each section in only 1 short sentence

            Chunk Summary: `{docs}`
        """

    document_instructions = """
            Create a summary of the text with the key information content
            and output results as bullet points. Start with a bullet point describing the general purpose of the
            text.Do not include disclosure or disclaimer statements.
            Do not include any extra information other than what is provided. Do not include words like however,
            overall, we, they, we think. Make sure output is given over a few bullet points
            Focus on key sections of the texts, and highlight them in concise way.
            Return answer strictly in bullet points

            Remember
            - don't use line breaks /n

            Chunk Summary: `{docs}`
        """
    reduce_template = (
        contract_instructions if document_type == "contract" else document_instructions
    )
    return reduce_template


def summary_prompt(template: str, input_var: str = "data_chunks") -> PromptTemplate:
    """
    Creates a prompt template for summary generation.

    Args:
        template (str): input prompt template
        input_var (str): input variable name
    Returns:
        (PromptTemplate): summary prompt
    """
    prompt = PromptTemplate(input_variables=[input_var], template=template)
    return prompt
