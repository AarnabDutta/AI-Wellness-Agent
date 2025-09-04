import os
from model.customllm import UnifiedLLMClient
from supervisor_agent.mental_health_router import route_mental_health

def load_main_supervisor_prompt():
    prompt_path = os.path.join(os.path.dirname(__file__), '..', 'prompts', 'supervisor.txt')
    with open(prompt_path, encoding='utf-8') as f:
        return f.read().strip()

def detect_main_domain(user_message, history=None, user_name=None):
    # For mental health only
    return "mental_health"

def route_message(user_message, history, user_name):
    if not history:
        greeting = (
            f"Hello {user_name}, I'm your AI Mental Health Wellness companion. "
            "How can I support you today (stress, burnout, anxiety, depression, work-life balance, empathy)?"
        )
        return greeting, "main_supervisor"
    
    # Route everything to mental health router
    return route_mental_health(user_message, history=history, user_name=user_name)
