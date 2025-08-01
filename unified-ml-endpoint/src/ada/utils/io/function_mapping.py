"""
File contains the function mapping for the function names and endpoints
"""

from ada.azml_realtime_deployments.contract_qa_deployment import (
    init as contract_qa_init,
)
from ada.azml_realtime_deployments.contract_qa_deployment import run as contract_qa_run
from ada.azml_realtime_deployments.data_retrieval_service_deployment import (
    init as data_retrival_service_deployment_init,
)
from ada.azml_realtime_deployments.data_retrieval_service_deployment import (
    run as data_retrival_service_deployment_run,
)
from ada.azml_realtime_deployments.document_service_deployment import (
    init as data_retrieval_init,
)
from ada.azml_realtime_deployments.document_service_deployment import (
    run as data_retrieval_run,
)
from ada.azml_realtime_deployments.idea_generation_v3_deployment import (
    init as idea_generation_v3_init,
)
from ada.azml_realtime_deployments.idea_generation_v3_deployment import (
    run as idea_generation_v3_run,
)
from ada.azml_realtime_deployments.key_facts_deployment_v2 import (
    init as key_facts_v2_init,
)
from ada.azml_realtime_deployments.key_facts_deployment_v2 import (
    run as key_facts_v2_run,
)
from ada.azml_realtime_deployments.leakage_extraction_deployment import (
    init as leakage_extraction_init,
)
from ada.azml_realtime_deployments.leakage_extraction_deployment import (
    run as leakage_extraction_run,
)
from ada.azml_realtime_deployments.negotiation_factory_deployment import (
    init as negotiation_factory_init,
)
from ada.azml_realtime_deployments.negotiation_factory_deployment import (
    run as negotiation_factory_run,
)
from ada.azml_realtime_deployments.news_qna_deployment import init as news_qna_init
from ada.azml_realtime_deployments.news_qna_deployment import run as news_qna_run
from ada.azml_realtime_deployments.ppt_generation_deployment import (
    init as ppt_generation_init,
)
from ada.azml_realtime_deployments.ppt_generation_deployment import (
    run as ppt_generation_run,
)
from ada.azml_realtime_deployments.top_idea_deployment import init as top_ideas_init
from ada.azml_realtime_deployments.top_idea_deployment import run as top_ideas_run
from ada.use_cases.idea_generation.dynamic_ideas.dynamic_ideas import (
    run_dynamic_ideas_graph,
)
from ada.use_cases.source_ai_knowledge.source_ai_knowledge import (
    run_source_ai_knowledge,
)
from ada.utils.metrics.context_manager import UseCase


def function_mapping() -> dict:
    """
    Returns the function init and run methods
    Returns:
        (dict): Function and run method mapping
    """
    func_mapping = {
        "generate-ppt": {
            "init": ppt_generation_init,
            "run": ppt_generation_run,
            "use_case": UseCase.PPT_GENERATION,
        },
        # "contract-qa": {
        #     "init": contract_qa_init,
        #     "run": contract_qa_run,
        #     "use_case": UseCase.CONTRACT_QANDA,
        # },
        "data-retrieval": {
            "init": data_retrieval_init,
            "run": data_retrieval_run,
            "use_case": UseCase.NA,
        },
        "source-ai-knowledge": {
            "init": lambda: None,
            "run": run_source_ai_knowledge,
            "use_case": UseCase.KNOWLEDGE_DOC,
        },
        "dynamic-ideas": {
            "init": lambda: None,
            "run": run_dynamic_ideas_graph,
            "use_case": UseCase.DYNAMIC_IDEAS,
        },
        "idea-generation-v3": {
            "init": idea_generation_v3_init,
            "run": idea_generation_v3_run,
            "use_case": UseCase.IDEA_GEN,
        },
        "key-facts-v2": {
            "init": key_facts_v2_init,
            "run": key_facts_v2_run,
            "use_case": UseCase.KEY_FACTS,
        },
        "news-qna": {
            "init": news_qna_init,
            "run": news_qna_run,
            "use_case": UseCase.NEWS_QA,
        },
        "leakage-extraction": {
            "init": leakage_extraction_init,
            "run": leakage_extraction_run,
            "use_case": UseCase.CONTRACT_LEAKAGE,
        },
        "negotiation-factory": {
            "init": negotiation_factory_init,
            "run": negotiation_factory_run,
            "use_case": UseCase.NEGO_FACTORY,
        },
        "top-ideas": {
            "init": top_ideas_init,
            "run": top_ideas_run,
            "use_case": UseCase.TOP_IDEAS,
        },
        "data-retrieval-services": {
            "init": data_retrival_service_deployment_init,
            "run": data_retrival_service_deployment_run,
        },
    }
    return func_mapping
