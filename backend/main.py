from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.evaluation import evaluation_notes, hallucination_risk
from backend.prompts import STRATEGY_TITLES, build_prompt
from backend.providers import estimate_tokens, generate_text
from backend.schemas import CompareRequest, CompareResponse, PromptResult

load_dotenv()

app = FastAPI(title="Prompt Engineering Playground API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/compare", response_model=CompareResponse)
async def compare(request: CompareRequest) -> CompareResponse:
    results: list[PromptResult] = []
    for strategy in request.strategies:
        prompt = build_prompt(strategy, request.task)
        generated = await generate_text(
            request.provider,
            request.model,
            prompt,
            request.temperature,
            request.top_p,
            request.max_tokens,
        )
        results.append(
            PromptResult(
                strategy=strategy,
                title=STRATEGY_TITLES[strategy],
                prompt=prompt,
                output=generated.text,
                provider=request.provider,
                model=request.model,
                estimated_input_tokens=estimate_tokens(prompt),
                estimated_output_tokens=estimate_tokens(generated.text),
                latency_ms=generated.latency_ms,
                hallucination_risk=hallucination_risk(prompt, generated.text),
                evaluation_notes=evaluation_notes(prompt, generated.text),
            )
        )
    return CompareResponse(results=results)
