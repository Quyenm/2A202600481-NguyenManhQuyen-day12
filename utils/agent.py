import os
from typing import Generator

from openai import OpenAI


MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
OUTPUT_MODE = os.getenv("AGENT_OUTPUT_MODE", "same").strip().lower()
# same | en | vi | ascii_vi


def _get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is missing. Set it in environment or .env before starting the server."
        )
    return OpenAI(api_key=api_key)


def _language_rule() -> str:
    if OUTPUT_MODE == "en":
        return "Always reply in English only."
    if OUTPUT_MODE == "vi":
        return "Always reply in Vietnamese only."
    if OUTPUT_MODE == "ascii_vi":
        return (
            "Always reply in Vietnamese WITHOUT diacritics. "
            "Use ASCII characters only. Example: 'nganh hoc', 'on dinh', 'co hoi viec lam'."
        )
    return (
        "Reply in the same language as the user. "
        "If the user writes in Vietnamese, reply in Vietnamese. "
        "If the user writes in English, reply in English."
    )


SYSTEM_PROMPT = f"""
You are EduGuide, an academic and career guidance AI assistant focused on helping students choose a university major.

Your role:
- Help students explore suitable majors based on interests, strengths, weaknesses, personality, career goals, financial concerns, and preferred learning environment.
- Ask concise follow-up questions when the information is not enough.
- Give practical, structured recommendations instead of vague motivational talk.
- Recommend 2 to 4 suitable majors when enough information is available.
- Explain WHY each major fits.
- Mention possible careers or job directions for each suggested major.
- Mention trade-offs when relevant.

Rules:
- Be clear, supportive, and realistic.
- Do not claim a major is the one and only perfect choice.
- Do not invent specific admissions rules, tuition, or salary data unless the user provides them.
- If the user gives too little information, ask at most 3 follow-up questions.
- Keep the answer readable and well structured.
- Prefer bullet-like structure in plain text if helpful.
- {_language_rule()}

Recommended reasoning flow:
1. Understand the student's profile.
2. Identify strengths, preferences, and constraints.
3. Suggest suitable majors.
4. Explain fit + risks/trade-offs.
5. Suggest next steps, such as what to research or which subjects to strengthen.
""".strip()


def ask(question: str) -> str:
    client = _get_client()

    response = client.responses.create(
        model=MODEL,
        instructions=SYSTEM_PROMPT,
        input=question,
    )

    return response.output_text.strip()


def ask_stream(question: str) -> Generator[str, None, None]:
    client = _get_client()

    stream = client.responses.create(
        model=MODEL,
        instructions=SYSTEM_PROMPT,
        input=question,
        stream=True,
    )

    for event in stream:
        event_type = getattr(event, "type", "")
        if event_type == "response.output_text.delta":
            yield event.delta