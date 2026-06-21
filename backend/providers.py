import os
import time
from dataclasses import dataclass

from backend.schemas import Provider


@dataclass
class ProviderOutput:
    text: str
    latency_ms: int


def estimate_tokens(text: str) -> int:
    return max(1, len(text.split()) * 4 // 3)


async def generate_text(provider: Provider, model: str, prompt: str, temperature: float, top_p: float, max_tokens: int) -> ProviderOutput:
    start = time.perf_counter()
    if provider == Provider.openai and os.getenv("OPENAI_API_KEY"):
        text = _openai_generate(model, prompt, temperature, top_p, max_tokens)
    elif provider == Provider.gemini and os.getenv("GEMINI_API_KEY"):
        text = _gemini_generate(model, prompt, temperature, top_p, max_tokens)
    else:
        text = _mock_generate(provider, model, prompt, temperature, top_p, max_tokens)
    latency_ms = int((time.perf_counter() - start) * 1000)
    return ProviderOutput(text=text, latency_ms=latency_ms)


def _openai_generate(model: str, prompt: str, temperature: float, top_p: float, max_tokens: int) -> str:
    from openai import OpenAI

    client = OpenAI()
    response = client.chat.completions.create(
        model=model or "gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content or ""


def _gemini_generate(model: str, prompt: str, temperature: float, top_p: float, max_tokens: int) -> str:
    import google.generativeai as genai

    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    generation_config = {
        "temperature": temperature,
        "top_p": top_p,
        "max_output_tokens": max_tokens,
    }
    gemini_model = genai.GenerativeModel(model or "gemini-1.5-flash", generation_config=generation_config)
    response = gemini_model.generate_content(prompt)
    return response.text or ""


def _mock_generate(provider: Provider, model: str, prompt: str, temperature: float, top_p: float, max_tokens: int) -> str:
    preview = prompt.strip().replace("\n", " ")[:220]
    return (
        f"Mock response for {provider.value}/{model}.\n\n"
        f"Prompt preview: {preview}...\n\n"
        f"Settings: temperature={temperature}, top_p={top_p}, max_tokens={max_tokens}.\n\n"
        "Production tip: add task-specific evaluation criteria and test this prompt against a representative dataset before shipping."
    )
