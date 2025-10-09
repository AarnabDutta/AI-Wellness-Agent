import os
from model.customllm import UnifiedLLMClient
from domain.mental_health.stress import handle_stress
from domain.mental_health.burnout import handle_burnout
from domain.mental_health.anxiety import handle_anxiety
from domain.mental_health.depression import handle_depression
from domain.mental_health.work_life_balance import handle_work_life_balance
from domain.mental_health.empathy_buddy import handle_empathy_buddy

def load_mental_health_supervisor_prompt():
    prompt_path = os.path.join(
        os.path.dirname(__file__), '..', 'prompts', 'mental_health', 'supervisor.txt'
    )
    with open(prompt_path, encoding='utf-8') as f:
        return f.read().strip()

def detect_mental_health_agent(user_message, history=None, user_name=None):
    llm = UnifiedLLMClient()
    formatted_history = []
    if history:
        formatted_history.extend(history)
    formatted_history.append({"role": "user", "content": user_message})
    
    system_prompt = load_mental_health_supervisor_prompt()
    result = llm.generate_response(
        prompt=user_message,
        history=formatted_history,
        system_prompt=system_prompt
    )
    
    response = result.strip().lower()
    # Accept only precise, one-word outputs from the LLM
    if response in [
        "stress",
        "burnout",
        "anxiety",
        "depression",
        "work_life_balance",
        "empathy_buddy"
    ]:
        return response
    else:
        return "general_mental_health"

def route_mental_health(user_message, history, user_name, stream=False):
    agent_type = detect_mental_health_agent(user_message, history=history, user_name=user_name)
    
    if agent_type == "stress":
        return handle_stress(user_message, history=history, user_name=user_name, stream=stream), "mental_health_stress"
    elif agent_type == "burnout":
        return handle_burnout(user_message, history=history, user_name=user_name, stream=stream), "mental_health_burnout"
    elif agent_type == "anxiety":
        return handle_anxiety(user_message, history=history, user_name=user_name, stream=stream), "mental_health_anxiety"
    elif agent_type == "depression":
        return handle_depression(user_message, history=history, user_name=user_name, stream=stream), "mental_health_depression"
    elif agent_type == "work_life_balance":
        return handle_work_life_balance(user_message, history=history, user_name=user_name, stream=stream), "mental_health_work_life_balance"
    elif agent_type == "empathy_buddy":
        return handle_empathy_buddy(user_message, history=history, user_name=user_name, stream=stream), "mental_health_empathy_buddy"
    else:
        return (
            f"I'm here to help with your mental health, {user_name}. "
            "I can support you with stress management, burnout prevention, anxiety, depression, "
            "work-life balance, or just be an empathy buddy. What feels most relevant right now?",
            "mental_health_supervisor"
        )
