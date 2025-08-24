# core/llm.py
import os
from openai import OpenAI

def _make_client():
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("oai_key")
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY (or oai_key). Export it before running Streamlit.")
    return OpenAI(api_key=api_key)

client = _make_client()
