# AI Voice Support Agent — Jobbie AI

An improved architecture for an AI-powered voice support assistant that addresses common production issues like hallucination, context loss, repetition, and cost explosion.

## Project Structure
analysis_design.pdf      # Parts 1 & 2: Diagnosis + Architecture Design
agent.py                 # Part 3: Context management with memory summarisation
schema.dbml              # Part 4: Database schema (paste into dbdiagram.io)
schema.png               # Part 4: ER diagram image
README.md

## What it implements

**Sliding window with memory summarisation** — instead of sending the entire conversation history to the LLM every time:

- The last 6 messages are sent verbatim (the sliding window)
- Everything older gets summarised into a short paragraph using a cheaper model (gpt-4o-mini)
- The summary is injected into the system prompt so the model still has context

This keeps token costs roughly flat instead of growing with every message and gives the model focused context instead of a wall of old messages.

## Database Schema

8 tables supporting the full support agent workflow. Paste `schema.dbml` into [dbdiagram.io](https://dbdiagram.io) to view the interactive diagram, or see `schema.png`.

Key tables:
- **conversation_summaries** — stores compressed memory, directly supports the sliding window
- **ai_responses** — tracks confidence, latency, and cache hits per response
- **escalations** — records when and why the AI handed off to a human
- **knowledge_articles** — knowledge base for RAG retrieval
- **feedback** — user ratings and correctness flags

## Setup

```bash
pip install openai
export OPENAI_API_KEY="sk-your-key"
python agent.py
```

## Assumptions

- Uses OpenAI API but the architecture works with any LLM
- Voice layer (STT/TTS) is handled separately — this focuses on the AI reasoning pipeline
- Summarisation uses gpt-5.4-mini to keep costs low

## Limitations

- Summarisation is lossy — compressing messages into a paragraph loses detail
- No RAG implementation (designed but not coded)
- Loop detection and response validation are proposed in the architecture but kept out of scope for Part 3

## Future Improvements

- RAG pipeline with vector search to ground responses in the knowledge base
- Response validation layer with loop detection and confidence checks
- Response caching for frequently asked questions
