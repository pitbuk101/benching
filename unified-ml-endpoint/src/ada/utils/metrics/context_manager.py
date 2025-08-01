import contextvars
import logging
from enum import Enum


class UseCase(Enum):
    NA = "NA"
    NEGO_FACTORY = "NF"
    TOP_IDEAS = "TI"
    IDEA_GEN = "IG"
    KNOWLEDGE_DOC = "KD"
    KEY_FACTS = "KF"
    SOURCEAI_BOT = "SBT"
    OPPORTUNITY = "OPP"
    CONTRACT_QANDA = "CQA"
    CONTRACT_BENCHMARKING = "CB"
    CONTRACT_CLAUSES = "CC"
    CONTRACT_ENTITY_EXTRACTION = "CEE"
    CONTRACT_LEAKAGE = "CL"
    CONTRACT_SUMMARY = "CS"
    PPT_GENERATION = "PPT"
    NEWS_QA = "NQA"
    INTENT_CLASSIFY = "INTENT"
    FUNC = "FUNC"
    NEWS = "NEWS"
    DYNAMIC_IDEAS = "DI"


tenant_context = contextvars.ContextVar("tenant_id", default="NA")
use_case_scenario_context = contextvars.ContextVar("intent_type", default=[UseCase.NA])


def set_tenant_and_intent_flow_context(tenant_id, *intent_type):
    """
    Sets the tenant and use case scenario context for the current flow.

    Args:
        tenant_id (str): The identifier for the tenant to be set in the context.
        *intent_type: Variable-length arguments representing the use case scenario(s).

    Logs:
        Logs the tenant ID and the use case scenario being set in the context.
    """

    tenant_context.set(tenant_id)
    use_case_scenario_context.set(intent_type)
    logging.info(f"Tenant context :{tenant_id} & use case scenario: {intent_type}")


def set_intent_flow_context(*intent_type):
    """
    Sets the use case scenario context for the current flow.

    Args:
        *intent_type: Variable-length arguments representing the use case scenario(s).

    Logs:
        Logs the use case scenario being set in the context.
    """
    use_case_scenario_context.set(intent_type)
    logging.info(f"use case scenario: {intent_type}")


def set_tenant_context(tenant_id):
    """
    Sets the tenant context for the current flow.

    Args:
        tenant_id (str): The identifier for the tenant to be set in the context.

    Logs:
        Logs the tenant ID being set in the context.
    """
    tenant_context.set(tenant_id)
    logging.info(f"Tenant context :{tenant_id}")


def get_ai_cost_tags():
    """
    Generates a cost AI tag based on the current tenant and use case scenario context.

    Returns:
        str: A string representing the cost AI tag, which combines a truncated tenant identifier
        and a sorted concatenation of use case scenario values.

    Logs:
        Logs the generated cost AI tag.
    """
    truncated_tenant_identifier = tenant_context.get()[:8]
    use_case_scenario = use_case_scenario_context.get()
    use_case_scenario_values = sorted(arg.value for arg in use_case_scenario)
    use_case_scenario_cost_tag = "_".join(map(str, use_case_scenario_values))
    cost_AI_tag = f"{truncated_tenant_identifier}-{use_case_scenario_cost_tag}"
    logging.info(f"Cost AI tag is {cost_AI_tag}")
    return cost_AI_tag
