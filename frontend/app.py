import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/")
STRATEGIES = {
    "Zero Shot": "zero_shot",
    "One Shot": "one_shot",
    "Few Shot": "few_shot",
    "Chain of Thought Style": "chain_of_thought",
    "Role Prompting": "role_prompting",
}

st.set_page_config(page_title="Prompt Engineering Playground", page_icon="🧪", layout="wide")
st.title("🧪 Prompt Engineering Playground")
st.caption("Compare prompting strategies across OpenAI, Gemini, or a no-key mock provider.")

with st.sidebar:
    st.header("Model settings")
    provider = st.selectbox("Provider", ["mock", "openai", "gemini"])
    default_model = {"mock": "demo-model", "openai": "gpt-4o-mini", "gemini": "gemini-1.5-flash"}[provider]
    model = st.text_input("Model", value=default_model)
    temperature = st.slider("Temperature", 0.0, 2.0, 0.2, 0.1)
    top_p = st.slider("Top P", 0.0, 1.0, 0.9, 0.05)
    max_tokens = st.slider("Max output tokens", 32, 4096, 500, 32)
    selected_labels = st.multiselect("Prompt strategies", list(STRATEGIES), default=list(STRATEGIES))

st.subheader("Task")
task = st.text_area(
    "What should the model do?",
    value="Explain temperature and top_p to a beginner, then give production advice.",
    height=120,
)

with st.expander("Learn the core concepts", expanded=False):
    st.markdown(
        """
        - **Tokens:** chunks of text that drive cost, latency, and context usage.
        - **Temperature:** randomness control; low values are stable, high values are creative.
        - **Top P:** limits sampling to a probability mass of likely tokens.
        - **Context window:** total input plus output capacity.
        - **Prompt templates:** reusable prompts with variables and examples.
        - **Hallucinations:** plausible but false content; reduce with grounding and verification.
        - **Prompt evaluation:** repeatable checks for correctness, format, and safety.
        """
    )

if st.button("Compare prompts", type="primary"):
    if not selected_labels:
        st.error("Select at least one strategy.")
    else:
        payload = {
            "task": task,
            "provider": provider,
            "model": model,
            "strategies": [STRATEGIES[label] for label in selected_labels],
            "temperature": temperature,
            "top_p": top_p,
            "max_tokens": max_tokens,
        }
        try:
            response = requests.post(f"{BACKEND_URL}/compare", json=payload, timeout=120)
            response.raise_for_status()
            results = response.json()["results"]
        except requests.RequestException as exc:
            st.error(f"Backend request failed: {exc}")
            st.stop()

        cols = st.columns(min(len(results), 3))
        for index, result in enumerate(results):
            with cols[index % len(cols)]:
                st.markdown(f"### {result['title']}")
                st.metric("Input tokens", result["estimated_input_tokens"])
                st.metric("Output tokens", result["estimated_output_tokens"])
                st.metric("Latency", f"{result['latency_ms']} ms")
                st.write(f"**Hallucination risk:** {result['hallucination_risk']}")
                with st.expander("Prompt template"):
                    st.code(result["prompt"], language="text")
                st.markdown("**Output**")
                st.write(result["output"])
                st.markdown("**Evaluation notes**")
                for note in result["evaluation_notes"]:
                    st.write(f"- {note}")
else:
    st.info("Enter a task and click **Compare prompts** to begin.")
