# Prompt Engineering Playground

A beginner-to-production learning project for comparing prompt engineering techniques side by side across OpenAI and Gemini models.

## What you can compare

- Zero Shot
- One Shot
- Few Shot
- Chain of Thought (implemented as a safe "reason briefly, then answer" style)
- Role Prompting

The Streamlit frontend sends prompt variants to the FastAPI backend, which calls either OpenAI or Gemini when API keys are configured. If keys are missing, the backend returns deterministic mock responses so you can learn the workflow locally without spending money.

## Concepts taught

| Concept | Production meaning |
| --- | --- |
| Tokens | Units models read and generate; token budgets affect cost, latency, and truncation. |
| Temperature | Controls randomness; lower is more predictable, higher is more creative. |
| Top P | Nucleus sampling; restricts output choices to the most likely probability mass. |
| Context Window | Maximum combined input and output tokens a model can handle. |
| Prompt Templates | Reusable prompt structures with variables and examples. |
| Hallucinations | Confident but false outputs; reduce with grounding, retrieval, constraints, and evaluation. |
| Prompt Evaluation | Systematic scoring of prompt outputs for correctness, format, safety, and usefulness. |

## Architecture

```text
Streamlit UI  --->  FastAPI backend  --->  OpenAI / Gemini APIs
                    |
                    +-- mock provider when keys are absent
```

## Project structure

```text
backend/                 FastAPI app, providers, prompt templates, schemas
frontend/                Streamlit app
render.yaml              Render blueprint for backend and frontend services
requirements.txt         Shared Python dependencies
.env.example             Environment variables
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Run the backend:

```bash
uvicorn backend.main:app --reload --port 8000
```

Run the frontend in another terminal:

```bash
streamlit run frontend/app.py
```

Open <http://localhost:8501>.

## API keys

Set one or both keys in your environment:

```bash
export OPENAI_API_KEY="your-openai-key"
export GEMINI_API_KEY="your-gemini-key"
```

The app still works without keys by using mock responses.

## Backend API

### Health check

```bash
curl http://localhost:8000/health
```

### Compare prompt strategies

```bash
curl -X POST http://localhost:8000/compare \
  -H 'Content-Type: application/json' \
  -d '{
    "task": "Explain tokens to a beginner",
    "provider": "mock",
    "model": "demo-model",
    "strategies": ["zero_shot", "one_shot"],
    "temperature": 0.2,
    "top_p": 0.9,
    "max_tokens": 300
  }'
```

## Render deployment

This repo includes `render.yaml` with two services:

1. `prompt-playground-api` - FastAPI web service.
2. `prompt-playground-ui` - Streamlit web service.

On Render:

1. Create a new Blueprint from this repository.
2. Add `OPENAI_API_KEY` and/or `GEMINI_API_KEY` as secret environment variables for the API service.
3. Set `BACKEND_URL` for the UI to the deployed API URL if Render does not inject it automatically.

## Beginner-to-production learning path

1. **Beginner:** Use the mock provider and compare how prompt wording changes output shape.
2. **Core prompting:** Try each strategy on the same task and inspect the generated prompt template.
3. **Model controls:** Adjust temperature, top-p, and max tokens to understand determinism, creativity, cost, and truncation.
4. **Reliability:** Use the evaluation scorecard to check format, groundedness, and hallucination risk.
5. **Provider integration:** Add OpenAI and Gemini keys, compare latency and output quality.
6. **Production:** Deploy the API and UI to Render, keep keys in environment variables, add logging, rate limits, persistent evaluations, and CI tests.

## Safety note about Chain of Thought

The playground teaches structured reasoning prompts without exposing hidden model reasoning. In production, ask models for concise explanations, assumptions, checks, or final-answer summaries rather than private chain-of-thought traces.
