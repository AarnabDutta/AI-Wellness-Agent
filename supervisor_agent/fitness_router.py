import os
from model.customllm import UnifiedLLMClient

from domain.fitness.weight_loss import handle_weight_loss
from domain.fitness.muscle_building import handle_muscle_building
from domain.fitness.weight_maintenance import handle_weight_maintenance
from domain.fitness.sleep_and_recovery import handle_sleep_and_recovery
from domain.fitness.activity_lifestyle import handle_activity_lifestyle

def load_fitness_supervisor_prompt():
    prompt_path = os.path.join(
        os.path.dirname(__file__),
        '..', 'prompts', 'fitness', 'supervisor.txt'
    )
    with open(prompt_path, encoding='utf-8') as f:
        return f.read().strip()

def detect_fitness_agent(user_message, history=None, user_name=None):
    llm = UnifiedLLMClient()
    # Build history with the system prompt
    formatted_history = []
    if history:
        formatted_history.extend(history)
    system_prompt = load_fitness_supervisor_prompt()
    formatted_history.append({"role": "user", "content": user_message})
    # LLM returns one of: weight_loss, muscle_building, weight_maintenance, sleep_and_recovery, activity_lifestyle
    result = llm.generate_response(
        prompt=user_message,
        history=formatted_history,
        system_prompt=system_prompt
    ).strip().lower()
    valid = {
        "weight_loss",
        "muscle_building",
        "weight_maintenance",
        "sleep_and_recovery",
        "activity_lifestyle"
    }
    return result if result in valid else "general_fitness"

def route_fitness(user_message, history, user_name):
    agent = detect_fitness_agent(user_message, history=history, user_name=user_name)
    if agent == "weight_loss":
        return handle_weight_loss(user_message, history=history, user_name=user_name), "fitness_weight_loss"
    elif agent == "muscle_building":
        return handle_muscle_building(user_message, history=history, user_name=user_name), "fitness_muscle_building"
    elif agent == "weight_maintenance":
        return handle_weight_maintenance(user_message, history=history, user_name=user_name), "fitness_weight_maintenance"
    elif agent == "sleep_and_recovery":
        return handle_sleep_and_recovery(user_message, history=history, user_name=user_name), "fitness_sleep_and_recovery"
    elif agent == "activity_lifestyle":
        return handle_activity_lifestyle(user_message, history=history, user_name=user_name), "fitness_activity_lifestyle"
    else:
        return (
            f"I'm here to help with your fitness goals, {user_name}. "
            "I can support you with weight loss, muscle building, weight maintenance, sleep & recovery, or activity lifestyle. Which would you like to focus on?",
            "fitness_supervisor"
        )
