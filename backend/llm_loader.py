
from transformers import pipeline
from langchain_community.llms import HuggingFacePipeline
from . import config


def load_llm():
    generator = pipeline(
        "text2text-generation",
        model=config.LLM_MODEL,
        tokenizer=config.LLM_MODEL,
        max_new_tokens=config.MAX_NEW_TOKENS,
        temperature=0.3,   # Add this
        device=-1   # CPU mode
    )
    print("🤖 Loading LLM model...")
    return HuggingFacePipeline(pipeline=generator)
