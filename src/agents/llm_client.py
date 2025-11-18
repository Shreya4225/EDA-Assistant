# src/agents/llm_client.py

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()  # load .env config

def get_llm():
    api_key = os.getenv("OPENROUTER_API_KEY")
    base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

    if not api_key:
        raise ValueError("Missing OPENROUTER_API_KEY in .env")

    return ChatOpenAI(
        model="meta-llama/llama-3-8b-instruct",
        temperature=0.2,
        max_tokens=300,
        api_key=api_key,
        base_url=base_url
    )
