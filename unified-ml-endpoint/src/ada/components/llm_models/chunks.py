"""Functions for the chunking of the documents."""

from typing import List

import numpy as np
import spacy
from langchain_core.documents import Document
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import AzureOpenAIEmbeddings

from ada.utils.config.config_loader import read_config
from ada.utils.metrics.context_manager import get_ai_cost_tags

model_config = read_config("models.yml")["vectorstore"]

# Load spaCy language model
nlp = spacy.load("en_core_web_sm")


def process_chunks(text: str) -> tuple:
    """
    Process the text and generate sentences.

    Args:
      text : The input text to be processed.

    Returns:
      sents : A list of spaCy Sentence objects.
      vecs : An array of sentence vectors normalized by their vector norms.
    """
    # Load the spaCy model
    doc = nlp(text)

    # Extract sentences from the processed document
    sents = list(doc.sents)

    # Create an array of sentence vectors normalized by their vector norms
    vecs = np.stack([sent.vector / sent.vector_norm for sent in sents])

    return sents, vecs


def cluster_text(sents: List[str], vecs: np.ndarray, threshold: float) -> List[List[int]]:
    """
    Cluster similar sentences based on their vector representations.

    Args:
      sents : A list of spaCy Sentence objects.
      vecs : An array of sentence vectors normalized by their vector norms.
      threshold : The similarity threshold to determine cluster boundaries.

    Returns:
      clusters : A list of clusters, where each cluster is represented
      as a list of indices corresponding to the sentences in the input.
    """
    clusters = [[0]]  # Initialize the first cluster with the first sentence

    # Iterate through sentences and form clusters based on similarity
    for i in range(1, len(sents)):
        if np.dot(vecs[i], vecs[i - 1]) < threshold:
            clusters.append([])  # Start a new cluster if the similarity falls below the threshold
        clusters[-1].append(i)  # Add the current sentence index to the current cluster

    return clusters


def create_chunks(corpus: str) -> List[Document]:
    """
    Create chunks of text from a string.

    Args:
        corpus : The text to split into chunks.
    Returns:
        A list of Document-class objects containing chunks of text with metadata.
    """

    documents: List[Document] = []
    text_splitter = SemanticChunker(
        AzureOpenAIEmbeddings(headers={"X-Aigateway-User-Defined-Tag": f"{get_ai_cost_tags()}"}),
        breakpoint_threshold_type="percentile",
        breakpoint_threshold_amount=model_config.get("breakpoint_threshold_amount", 90),
    )
    documents = text_splitter.create_documents(texts=[corpus])
    documents = [
        Document(
            page_content=document.page_content.replace("\n", " "),
            metadata={"source": index},
        )
        for index, document in enumerate(documents)
    ]

    return documents
