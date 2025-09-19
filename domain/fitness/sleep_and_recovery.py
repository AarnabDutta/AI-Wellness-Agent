from model.customllm import UnifiedLLMClient
import os

def load_system_prompt(user_name=None):
    prompt_path = os.path.join(
        os.path.dirname(__file__), '..', '..', 'prompts', 'fitness', 'sleep_and_recovery.txt'
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

def handle_sleep_and_recovery(user_message, history=None, user_name=None):
    llm = UnifiedLLMClient()
    system_prompt = load_system_prompt(user_name=user_name)

    formatted_history = format_history(history)
    if not formatted_history or formatted_history[0].get("role") != "system":
        formatted_history = [{"role": "system", "content": system_prompt}] + formatted_history
    formatted_history.append({"role": "user", "content": user_message})

    reply = llm.generate_response(
        prompt=user_message,
        history=formatted_history,
        system_prompt=None
    )
    return reply
