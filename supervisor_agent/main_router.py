import os
from model.customllm import UnifiedLLMClient
from supervisor_agent.mental_health_router import route_mental_health
from supervisor_agent.fitness_router import route_fitness
from supervisor_agent.nutrition_router import route_nutrition
from supervisor_agent.general_wellness_agent import handle_general_wellness

def load_main_supervisor_prompt():
    prompt_path = os.path.join(os.path.dirname(__file__), '..', 'prompts', 'supervisor.txt')
    with open(prompt_path, encoding='utf-8') as f:
        return f.read().strip()

def detect_main_domain(user_message, history=None, user_name=None):
    llm = UnifiedLLMClient()
    system_prompt = load_main_supervisor_prompt()
    formatted_history = [] if not history else list(history)
    formatted_history.append({"role": "user", "content": user_message})

    # LLM should return: 'mental_health', 'fitness', 'nutrition', or 'general'
    result = llm.generate_response(
        prompt=user_message,
        history=formatted_history,
        system_prompt=system_prompt
    ).strip().lower()
    valid = {"mental_health", "fitness", "nutrition", "general"}
    return result if result in valid else "general"

def route_message(user_message, history, user_name, stream=False):
    if not history:  # First message only
        greeting = (
            f"Hello {user_name}, I'm your AI Wellness companion. "
            "How can I support you today? (You can talk to me about mental health, fitness, nutrition, or any wellness/life topic — I'm here to chat!)"
        )
        return greeting, "main_supervisor"

    main_domain = detect_main_domain(user_message, history=history, user_name=user_name)
    if main_domain == "mental_health":
        return route_mental_health(user_message, history=history, user_name=user_name, stream=stream)
    elif main_domain == "fitness":
        return route_fitness(user_message, history=history, user_name=user_name, stream=stream)
    elif main_domain == "nutrition":
        return route_nutrition(user_message, history=history, user_name=user_name, stream=stream)
    else:
        # "general" or fallback: general wellness/small talk agent
        return handle_general_wellness(user_message, history=history, user_name=user_name, stream=stream)
