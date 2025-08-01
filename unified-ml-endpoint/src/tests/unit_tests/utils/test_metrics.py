import pytest
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore
from langchain_openai import AzureOpenAIEmbeddings

from ada.utils.config.config_loader import read_config
from ada.utils.metrics.context_manager import get_ai_cost_tags
from ada.utils.metrics.similarity import (
    get_best_match_from_list,
    get_similarity,
    similarity_search_from_vectorstore,
)

conf = read_config("models.yml")


@pytest.fixture()
def vector_store() -> VectorStore:
    """
    Mock VectorStoreFactory class.
    """
    texts = [
        "Your contract has 3 clauses.",
        "The top news for today is: costs of wheat is going up.",
        "You are losing money in your supply chain.",
        "Here are some ideas for your business: save on costs, save on time, save on resources.",
    ]
    vectorstore = FAISS.from_texts(
        texts,
        AzureOpenAIEmbeddings(
            model=conf["embedding_engine"],
            headers={"X-Aigateway-User-Defined-Tag": f"{get_ai_cost_tags()}"},
        ),
    )
    return vectorstore


def similarity_greater_than(similarity: str, threshold: float) -> bool:
    """
    Check if similarity is greater than threshold.
    """
    return float(similarity.split(",")[1]) >= threshold


@pytest.mark.utils
def test_get_similarity():
    """
    Test get_similarity().
    """
    input1 = "Hello, Good morning"
    input2 = "Hi, Good morning."
    similarity_results = get_similarity(input1, input2, "gpt-4o-mini").lower()
    simialrity_results_and_weightage = similarity_results.split(",")
    simialrity_result = simialrity_results_and_weightage[0]
    simialrity_weightage = simialrity_results_and_weightage[1]
    assert simialrity_result in ["perfect", "similar"]
    assert float(simialrity_weightage) >= 0.7


@pytest.mark.utils
def test_get_similarity_greater_than():
    """
    Test get_similarity().
    """
    input1 = "What is a contract?"
    input2 = "Can you describe a contract?"
    # non deterministic
    assert similarity_greater_than(get_similarity(input1, input2, "gpt-4o-mini"), 0.8)


@pytest.mark.utils
def test_get_similarity_search_from_vectorstore_length(vector_store: VectorStore):
    """
    Test similarity_search_from_vectorstore().
    """
    search_string = "How many clauses in my contract?"
    no_of_docs_to_return = 1
    most_similar_document = similarity_search_from_vectorstore(
        vector_store,
        search_string,
        no_of_docs_to_return,
    )
    assert len(most_similar_document) == 1


@pytest.mark.utils
def test_get_similarity_search_from_vectorstore_top_result(vector_store: VectorStore):
    """
    Test similarity_search_from_vectorstore().
    """
    search_string = "How many clauses in my contract?"
    no_of_docs_to_return = 1
    most_similar_document: Document = similarity_search_from_vectorstore(
        vector_store,
        search_string,
        no_of_docs_to_return,
    )[0]
    assert most_similar_document.page_content == "Your contract has 3 clauses."


@pytest.mark.utils
def test_best_match_from_list_fuzzy():
    test_search_phrase = "SKF"
    test_list_for_comparison = [
        "GBM SARL",
        "SKF FRANCE",
        "SKF US",
        "SKF YZ",
        "America",
        "Horse",
        "Monkey",
    ]
    expected_output = "SKF FRANCE"
    actual_output = get_best_match_from_list(
        test_list_for_comparison,
        test_search_phrase,
        threshold=0.4,
        similarity_model="fuzzy",
        default_value="str",
    )
    assert expected_output == actual_output


@pytest.mark.utils
def test_best_match_from_list_spacy():
    test_search_phrase = "words"
    test_list_for_comparison = [
        "elephant",
        "Sword",
        "word",
        "letter",
        "America",
        "Horse",
        "Monkey",
    ]
    expected_output = "word"
    actual_output = get_best_match_from_list(
        test_list_for_comparison,
        test_search_phrase,
        similarity_model="en_core_web_lg",
        threshold=0.4,
        default_value="str",
    )
    assert expected_output == actual_output
