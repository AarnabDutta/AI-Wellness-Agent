import os
from model.customllm import UnifiedLLMClient

from domain.nutrition.personalized_plan import handle_personalized_plan
from domain.nutrition.nutritional_tracking import handle_nutritional_tracking
from domain.nutrition.weight_loss_meal import handle_weight_loss_meal
from domain.nutrition.muscle_building_plan import handle_muscle_building_plan
from domain.nutrition.diabetic_plan import handle_diabetic_plan

def load_nutrition_supervisor_prompt():
    prompt_path = os.path.join(
        os.path.dirname(__file__),
        '..', 'prompts', 'nutrition', 'supervisor.txt'
    )
    with open(prompt_path, encoding='utf-8') as f:
        return f.read().strip()

def detect_nutrition_agent(user_message, history=None, user_name=None):
    llm = UnifiedLLMClient()
    formatted_history = []
    if history:
        formatted_history.extend(history)
    system_prompt = load_nutrition_supervisor_prompt()
    formatted_history.append({"role": "user", "content": user_message})
    # LLM returns one of: personalized_plan, nutritional_tracking, weight_loss_meal, muscle_building_plan, diabetic_plan
    result = llm.generate_response(
        prompt=user_message,
        history=formatted_history,
        system_prompt=system_prompt
    ).strip().lower()
    valid = {
        "personalized_plan",
        "nutritional_tracking",
        "weight_loss_meal",
        "muscle_building_plan",
        "diabetic_plan"
    }
    return result if result in valid else "general_nutrition"

def route_nutrition(user_message, history, user_name, stream=False):
    agent = detect_nutrition_agent(user_message, history=history, user_name=user_name)
    if agent == "personalized_plan":
        return handle_personalized_plan(user_message, history=history, user_name=user_name, stream=stream), "nutrition_personalized_plan"
    elif agent == "nutritional_tracking":
        return handle_nutritional_tracking(user_message, history=history, user_name=user_name, stream=stream), "nutrition_nutritional_tracking"
    elif agent == "weight_loss_meal":
        return handle_weight_loss_meal(user_message, history=history, user_name=user_name, stream=stream), "nutrition_weight_loss_meal"
    elif agent == "muscle_building_plan":
        return handle_muscle_building_plan(user_message, history=history, user_name=user_name, stream=stream), "nutrition_muscle_building_plan"
    elif agent == "diabetic_plan":
        return handle_diabetic_plan(user_message, history=history, user_name=user_name, stream=stream), "nutrition_diabetic_plan"
    else:
        return (
            f"I'm here to support your nutrition goals, {user_name}. "
            "I can help with personalized meal plans, nutritional tracking, weight-loss meals, muscle-building plans, or diabetic meal planning. What would you like to explore?",
            "nutrition_supervisor"
        )
