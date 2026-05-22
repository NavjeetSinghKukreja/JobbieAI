"""
Context Management with Memory Summarisation

Instead of sending the full conversation history to the LLM every time,
we keep the last few messages verbatim (sliding window) and summarise
everything older into a short paragraph. Keeps costs flat and gives
the model focused context in long conversations.
"""

from openai import OpenAI


RECENT_WINDOW = 6  
SUMMARY_MODEL = "gpt-5.4-mini"  
MAIN_MODEL = "gpt-5.4"


def summarise_messages(client, messages, existing_summary=None):
    conversation = "\n".join(
        f"{m['role']}: {m['content']}" for m in messages
    )

    prompt = ""
    if existing_summary:
        prompt += f"Previous summary: {existing_summary}\n\n"

    prompt += (
        "Summarise this support conversation in 2-3 sentences. "
        "Keep: the customer's issue, key details, and what was resolved.\n\n"
        f"{conversation}"
    )

    try:
        resp = client.chat.completions.create(
            model=SUMMARY_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0,
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"[Earlier conversation with {len(messages)} messages]"


def build_context(messages, summary=None):

    system_content = (
        "You are a helpful customer support assistant. "
        "Keep responses concise (2-3 sentences, suitable for voice)."
    )

    if summary:
        system_content += f"\n\nConversation so far: {summary}"

    recent = messages[-RECENT_WINDOW:]

    prompt = [{"role": "system", "content": system_content}]
    prompt.extend(recent)
    return prompt


def chat(client, messages, summary=None):
    prompt = build_context(messages, summary)

    resp = client.chat.completions.create(
        model=MAIN_MODEL,
        messages=prompt,
        temperature=0.3,
        max_tokens=200,
    )
    return resp.choices[0].message.content

