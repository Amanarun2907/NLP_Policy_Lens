"""
Groq AI Client
Centralised wrapper around the Groq SDK.
All AI calls go through this module.
"""

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

_client = None

def get_client() -> Groq:
    global _client
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY", "")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found. Check your .env file.")
        _client = Groq(api_key=api_key)
    return _client


def chat(
    system_prompt: str,
    user_message:  str,
    model:         str  = "llama-3.3-70b-versatile",
    temperature:   float = 0.3,
    max_tokens:    int   = 2048,
) -> str:
    """
    Single-turn chat with Groq.
    Returns the assistant's reply as a string.
    """
    try:
        client   = get_client()
        response = client.chat.completions.create(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            messages=[
                {"role": "system",  "content": system_prompt},
                {"role": "user",    "content": user_message},
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Groq Error] {str(e)}"


def chat_with_history(
    system_prompt: str,
    history:       list[dict],
    model:         str   = "llama-3.3-70b-versatile",
    temperature:   float = 0.4,
    max_tokens:    int   = 1024,
) -> str:
    """
    Multi-turn chat with message history.
    history = [{"role": "user"|"assistant", "content": "..."}]
    """
    try:
        client   = get_client()
        messages = [{"role": "system", "content": system_prompt}] + history
        response = client.chat.completions.create(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            messages=messages,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Groq Error] {str(e)}"
