from jinja2 import Template
from langchain_core.messages import (
    SystemMessage,
    HumanMessage
)
from src.utils.logs import get_custom_logger
from src.datamodels.state_model import RecommendationState
from src.datamodels.openai_response_model import QuestionRecommendation
from src.providers.llm.openai import recomendation_model
from src.providers.prompts import prompt_library

logger = get_custom_logger(__name__)

def question_recommendation(state: RecommendationState) -> dict:
    logger.debug(f"State: {state}")
    previous_questions = state["previous_questions"]
    if previous_questions:
        logger.info(f"Previous Questions: {previous_questions}")
        previous_questions = "\n".join(previous_questions)
    else:
        previous_questions = "No previous questions available."

    prompt = prompt_library.get_prompts(tenant_id=state["tenant_id"], prompt_name="question_recommendation")
    prompt_render = Template(prompt).render(
        previous_questions=previous_questions,
        category=state["category"],
        preferred_language=state["language"],
        preferred_currency=state["preferred_currency"],
        n=state.get("n", 20),
    )
    structured_llm = recomendation_model.with_structured_output(QuestionRecommendation)
    structured_llm_response = structured_llm.invoke([
        SystemMessage(content=prompt_render),
        HumanMessage(content=previous_questions),
    ])
    recommendation = structured_llm_response.model_dump()
    logger.info(f"Recommendations: {recommendation}")
    return {"recommendations": recommendation.get("recommendations", [])}