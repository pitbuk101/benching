from jinja2 import Template
from langchain_core.messages import (
    SystemMessage
)
import orjson
from src.utils.logs import get_custom_logger
from src.datamodels.state_model import ChartState
from src.datamodels.openai_response_model import ChartRecommendation
from src.providers.llm.openai import recomendation_model
from src.providers.prompts import prompt_library

logger = get_custom_logger(__name__)

def chart_recommendation(state: ChartState) -> ChartState:

    logger.debug(f"State: {state}")
    # Category 
    category = state["category"]
    # User Question
    user_question = state["user_question"]
    # Columns
    columns = state["columns"]
    # Data
    data = state["data"]
    # Preferred Language
    preferred_language=state["preferred_language"]
    # Currency
    preferred_currency = state["preferred_currency"]

    prompt = prompt_library.get_prompts(tenant_id=state["tenant_id"], prompt_name="chart_recommendation")
    prompt_render = Template(prompt).render(
        user_question=user_question,
        columns=columns,
        data=data,
        category=category,
        preferred_language=preferred_language,
        preferred_currency=preferred_currency,
        n=state.get("n", 4),
    )
    
    structured_llm = recomendation_model.with_structured_output(ChartRecommendation)
    structured_llm_response =  structured_llm.invoke([
        SystemMessage(content=prompt_render)
    ])
    # charts = structured_llm_response
    # charts = orjson.loads(structured_llm_response.charts.model_dump_json())
    charts = structured_llm_response.model_dump(exclude_none=True)
    logger.info(f"Charts: {charts}")
    state['charts'] = charts['charts']
    return state