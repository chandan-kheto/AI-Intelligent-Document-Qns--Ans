
from langchain_huggingface import HuggingFaceEmbeddings
import config


def load_embeddings():
    return HuggingFaceEmbeddings(
        model_name=config.EMBEDDING_MODEL
    )
