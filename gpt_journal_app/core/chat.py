# core/chat.py
from typing import List, Dict
from core.llm import client

def _sanitize(messages: List[Dict]) -> List[Dict]:
    out = []
    for m in messages:
        role = m.get("role", "user")
        content = m.get("content", "")
        if not isinstance(content, str):
            content = str(content)
        out.append({"role": role, "content": content})
    return out

def chat_with_gpt(user_input: str, chat_log: List[Dict], *, max_reply_tokens: int = 200) -> str:
    messages = [{"role": "system", "content": "You are ChatGPT. Be concise (≤5 sentences)."}]
    messages.extend(chat_log[-12:])  # 12 last messages to control cost
    messages.append({"role": "user", "content": user_input})
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=_sanitize(messages),
        max_tokens=max_reply_tokens,
    )
    return resp.choices[0].message.content

def summarize_chat(chat_log: List[Dict], *, take_last: int = 60) -> str:
    if not chat_log:
        return "No past conversation."
    text = "\n".join(f"{m['role']}: {m['content']}" for m in chat_log[-take_last:])
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You summarize chat history into critical points."},
            {"role": "user", "content": f"Summarize the critical points from this chat:\n{text}"}
        ],
        max_tokens=300,
    )
    return resp.choices[0].message.content.strip()
