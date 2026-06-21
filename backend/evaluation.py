from backend.providers import estimate_tokens


def hallucination_risk(prompt: str, output: str) -> str:
    text = f"{prompt}\n{output}".lower()
    if any(word in text for word in ["cite", "source", "evidence", "verify", "unknown", "not sure"]):
        return "Lower"
    if any(word in text for word in ["always", "guaranteed", "never", "definitely"]):
        return "Higher"
    return "Medium"


def evaluation_notes(prompt: str, output: str) -> list[str]:
    notes: list[str] = []
    if "example" in prompt.lower():
        notes.append("Uses examples, which can improve format consistency.")
    if "role" in prompt.lower() or "you are" in prompt.lower():
        notes.append("Defines a role, which can steer tone and expertise.")
    if estimate_tokens(prompt) + estimate_tokens(output) > 1500:
        notes.append("Large prompt/output pair; monitor context window and cost.")
    if not notes:
        notes.append("Baseline prompt; add constraints, examples, and evaluation criteria for production use.")
    return notes
