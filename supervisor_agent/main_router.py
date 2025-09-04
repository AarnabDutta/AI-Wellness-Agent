import os
from model.customllm import UnifiedLLMClient
from supervisor_agent.mental_health_router import route_mental_health
from supervisor_agent.fitness_router import route_fitness
from supervisor_agent.nutrition_router import route_nutrition

def load_main_supervisor_prompt():
    prompt_path = os.path.join(os.path.dirname(__file__), '..', 'prompts', 'supervisor.txt')
    with open(prompt_path, encoding='utf-8') as f:
        return f.read().strip()

def detect_main_domain(user_message, history=None, user_name=None):
    llm = UnifiedLLMClient()
    formatted_history = []
    if history:
        formatted_history.extend(history)
    formatted_history.append({"role": "user", "content": user_message})
    
    system_prompt = load_main_supervisor_prompt()
    result = llm.generate_response(
        prompt=user_message,
        history=formatted_history,
        system_prompt=system_prompt
    )
    
    response = result.strip().lower()
    if "mental_health" in response or "mental health" in response:
        return "mental_health"
    elif "fitness" in response:
        return "fitness"
    elif "nutrition" in response:
        return "nutrition"
    else:
        return "general"

def route_message(user_message, history, user_name):
    if not history:
        greeting = (
            f"Hello {user_name}, I'm your AI Employee Wellness companion. "
            "I can help you with mental health, fitness, or nutrition. "
            "What would you like to focus on today?"
        )
        return greeting, "main_supervisor"
    
    main_domain = detect_main_domain(user_message, history=history, user_name=user_name)
    
    if main_domain == "mental_health":
        return route_mental_health(user_message, history=history, user_name=user_name)
    elif main_domain == "fitness":
        return route_fitness(user_message, history=history, user_name=user_name)
    elif main_domain == "nutrition":
        return route_nutrition(user_message, history=history, user_name=user_name)
    else:
        return (
            f"Thank you, {user_name}. I'm here to help with mental health, fitness, and nutrition. "
            "Could you tell me more specifically what you'd like support with?",
            "main_supervisor"
        )
