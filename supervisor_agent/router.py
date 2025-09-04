# supervisor_agent/router.py

import os
from model.customllm import UnifiedLLMClient
from domain.stress import handle_stress
from domain.sleep import handle_sleep

def load_supervisor_system_prompt():
    prompt_path = os.path.join(os.path.dirname(__file__), '..', 'prompts', 'supervisor.txt')
    with open(prompt_path, encoding='utf-8') as f:
        return f.read().strip()

def detect_domain_llm(user_message, history=None, user_name=None):
    llm = UnifiedLLMClient()
    formatted_history = []
    if history:
        formatted_history.extend(history)
    formatted_history.append({"role": "user", "content": user_message})

    system_prompt = load_supervisor_system_prompt()

    result = llm.generate_response(
        prompt=user_message,
        history=formatted_history,
        system_prompt=system_prompt
    )
    response = result.strip().lower()
    if "stress" in response:
        return "stress"
    elif "sleep" in response:
        return "sleep"
    else:
        return "general"

def route_message(user_message, history, user_name):
    if not history:
        greeting = (
            f"Hello {user_name}, I'm your AI Employee Wellness companion. "
            "How can I support your well-being today—sleep, stress, recovery, or something else?"
        )
        return greeting, "supervisor"

    domain = detect_domain_llm(user_message, history=history, user_name=user_name)
    if domain == "stress":
        return handle_stress(user_message, history=history, user_name=user_name), "stress"
    elif domain == "sleep":
        return handle_sleep(user_message, history=history, user_name=user_name), "sleep"
    else:
        return (
            f"Thank you, {user_name}. I'm here to help with sleep, stress, and other wellness needs. "
            "Could you tell me a bit more about what you're experiencing?",
            "supervisor"
        )
