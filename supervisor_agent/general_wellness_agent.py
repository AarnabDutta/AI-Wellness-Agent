import os
from model.customllm import UnifiedLLMClient

def load_general_wellness_prompt(user_name=None):
    prompt_path = os.path.join(
        os.path.dirname(__file__), '..', 'prompts', 'general_wellness.txt'
    )
    with open(prompt_path, encoding='utf-8') as f:
        prompt = f.read().strip()
    if user_name:
        prompt = prompt.replace("{user_name}", str(user_name))
    return prompt

def format_history(prev_messages):
    if not prev_messages:
        return []
    return [
        {"role": msg["role"], "content": msg["content"]}
        for msg in prev_messages if "role" in msg and "content" in msg
    ]

def handle_general_wellness(user_message, history=None, user_name=None):
    llm = UnifiedLLMClient()
    system_prompt = load_general_wellness_prompt(user_name=user_name)

    formatted_history = format_history(history)
    if not formatted_history or formatted_history[0].get("role") != "system":
        formatted_history = [{"role": "system", "content": system_prompt}] + formatted_history
    formatted_history.append({"role": "user", "content": user_message})

    reply = llm.generate_response(
        prompt=user_message,
        history=formatted_history,
        system_prompt=None  # Already included as first msg
    )
    return reply, "general_wellness"
