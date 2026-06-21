from enum import Enum
from pydantic import BaseModel, Field


class Provider(str, Enum):
    mock = "mock"
    openai = "openai"
    gemini = "gemini"


class Strategy(str, Enum):
    zero_shot = "zero_shot"
    one_shot = "one_shot"
    few_shot = "few_shot"
    chain_of_thought = "chain_of_thought"
    role_prompting = "role_prompting"


class CompareRequest(BaseModel):
    task: str = Field(..., min_length=3, max_length=8000)
    provider: Provider = Provider.mock
    model: str = Field(default="demo-model", min_length=1, max_length=120)
    strategies: list[Strategy] = Field(default_factory=lambda: list(Strategy), min_length=1)
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    top_p: float = Field(default=0.9, ge=0.0, le=1.0)
    max_tokens: int = Field(default=500, ge=32, le=4096)


class PromptResult(BaseModel):
    strategy: Strategy
    title: str
    prompt: str
    output: str
    provider: Provider
    model: str
    estimated_input_tokens: int
    estimated_output_tokens: int
    latency_ms: int
    hallucination_risk: str
    evaluation_notes: list[str]


class CompareResponse(BaseModel):
    results: list[PromptResult]
