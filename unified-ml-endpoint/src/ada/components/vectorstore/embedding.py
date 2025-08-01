"""Class to create embeddings"""

import torch
from transformers import AutoModel, AutoTokenizer

from ada.components.llm_models.generic_calls import generate_embeddings_from_string
from ada.utils.config.config_loader import read_config
from ada.utils.logs.logger import get_logger

log = get_logger("embedding")

conf = read_config("models.yml")


class EmbeddingTypeException(Exception):
    """To raise when there is an incorrect embedding type passed."""


class EmbeddingConfigException(Exception):
    """To raise when the wrong configuration for embeddings is provided."""


# pylint: disable=too-few-public-methods
class Embedding:
    """
    A class for creating and managing  embeddings.
    """

    def __init__(self, embedding_type: str = "openai", **kwargs):
        """
        Create vectorstore object
        Args:
            embedding_type: Embedding type
            other_params: if required for particular embeddings
        """
        self.embedding_type = embedding_type
        self.params = kwargs

    def create_embeddings(self, sentence):
        """
        create embedding of the input
        Args:
            sentence: Sentence to create embeddings

        Returns: embeddings

        """
        if self.embedding_type == "bert":
            return self._create_bert_embedding(sentence)
        if self.embedding_type == "openai":
            return self._create_openai_embedding(sentence)
        raise EmbeddingTypeException(f"The embedding type {self.embedding_type} is not an option")

    def _create_openai_embedding(self, sentence):
        """
        Create OpenAI Embeddings of a sentence.

        Args:
            sentence: Sentence to create embeddings

        Returns:
            openai embedding of the sentence

        """
        if "embedding_engine" not in conf:
            raise EmbeddingConfigException("Missing required parameter `embedding_engine`")
        embedding = generate_embeddings_from_string(sentence, conf["embedding_engine"])
        return embedding

    def _create_bert_embedding(self, sentence: str):
        """
        Create Bert Embeddings of a sentence.

        Args:
            sentence: Sentence to create embeddings

        Returns:
            Bert embedding of the sentence
        """
        log.info("Tokenizing the Sentence")

        required_params = ["tokenizer", "bert_model", "max_length"]
        for param in required_params:
            if param not in self.params:
                raise EmbeddingConfigException(f"Missing required parameter `{param}`")

        tokenizer = AutoTokenizer.from_pretrained(self.params["tokenizer"])
        new_tokens = tokenizer.encode_plus(
            sentence,
            max_length=self.params["max_length"],
            truncation=True,
            padding="max_length",
            return_tensors="pt",
        )

        # Create tensors
        input_ids = new_tokens["input_ids"]
        attention_mask = new_tokens["attention_mask"]

        # Get model output
        model = AutoModel.from_pretrained(self.params["bert_model"])
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)

        # Get embeddings
        embeddings = outputs.last_hidden_state

        # Apply mask
        mask = attention_mask.unsqueeze(-1).expand(embeddings.size()).float()
        masked_embeddings = embeddings * mask

        # Calculate average embeddings
        avg_embeddings = torch.sum(masked_embeddings, 1)
        summed_mask = torch.clamp(mask.sum(1), min=1e-9)
        mean_pooled = avg_embeddings / summed_mask

        # Convert from PyTorch tensor to numpy array
        mean_pooled = mean_pooled.detach().numpy()

        return mean_pooled
