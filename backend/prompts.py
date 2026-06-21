from backend.schemas import Strategy

STRATEGY_TITLES = {
    Strategy.zero_shot: "Zero Shot",
    Strategy.one_shot: "One Shot",
    Strategy.few_shot: "Few Shot",
    Strategy.chain_of_thought: "Chain of Thought Style",
    Strategy.role_prompting: "Role Prompting",
}


def build_prompt(strategy: Strategy, task: str) -> str:
    if strategy == Strategy.zero_shot:
        return f"Complete this task clearly and accurately:\n\n{task}"
    if strategy == Strategy.one_shot:
        return (
            "Use the example style, then complete the new task.\n\n"
            "Example task: Explain APIs to a beginner.\n"
            "Example answer: An API is a menu that software uses to request actions or data from another system.\n\n"
            f"New task: {task}"
        )
    if strategy == Strategy.few_shot:
        return (
            "Follow the pattern in these examples, then answer the new task.\n\n"
            "Example 1\nTask: Explain tokens.\nAnswer: Tokens are chunks of text a model processes.\n\n"
            "Example 2\nTask: Explain temperature.\nAnswer: Temperature controls how predictable or creative a model response is.\n\n"
            "Example 3\nTask: Explain hallucinations.\nAnswer: Hallucinations are outputs that sound confident but are not true.\n\n"
            f"New task: {task}"
        )
    if strategy == Strategy.chain_of_thought:
        return (
            "Solve the task carefully. Do not reveal private hidden reasoning. "
            "Provide a brief approach, the final answer, and one verification check.\n\n"
            f"Task: {task}"
        )
    if strategy == Strategy.role_prompting:
        return (
            "You are a senior prompt engineering instructor teaching a practical production workshop. "
            "Be precise, beginner-friendly, and include production caveats.\n\n"
            f"Task: {task}"
        )
    raise ValueError(f"Unsupported strategy: {strategy}")
