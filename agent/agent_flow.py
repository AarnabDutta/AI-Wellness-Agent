import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph, END
from supervisor_agent.main_router import detect_main_domain, route_message
from supervisor_agent.fitness_router import route_fitness
from supervisor_agent.mental_health_router import route_mental_health
from supervisor_agent.nutrition_router import route_nutrition
from supervisor_agent.general_wellness_agent import handle_general_wellness

def classify_and_route(state):
    user_message = state["current_input"]
    stream = state.get("streaming_mode", False)
    domain = detect_main_domain(user_message, history=state["history"], user_name=state["user_name"])
    state["last_domain"] = domain
    if domain == "fitness":
        reply, subdomain = route_fitness(user_message, state["history"], state["user_name"], stream=stream)
        state["last_reply"] = reply
        state["last_domain"] = f"fitness::{subdomain}"
    elif domain == "mental_health":
        reply, subdomain = route_mental_health(user_message, state["history"], state["user_name"], stream=stream)
        state["last_reply"] = reply
        state["last_domain"] = f"mental_health::{subdomain}"
    elif domain == "nutrition":
        reply, subdomain = route_nutrition(user_message, state["history"], state["user_name"], stream=stream)
        state["last_reply"] = reply
        state["last_domain"] = f"nutrition::{subdomain}"
    else:
        reply, subdomain = handle_general_wellness(user_message, state["history"], state["user_name"], stream=stream)
        state["last_reply"] = reply
        state["last_domain"] = "general"
    state["history"].append({"role": "user", "content": user_message})
    state["history"].append({"role": "assistant", "content": state["last_reply"]})
    state["step_count"] += 1
    return state

graph = StateGraph(dict)
graph.add_node("classify_and_route", classify_and_route)

def route_edge(state):
    if state["history"] and state["history"][-1]["role"] == "user" and state["history"][-1]["content"].lower() in ["exit", "quit"]:
        return END
    else:
        return "classify_and_route"

graph.add_conditional_edges("classify_and_route", route_edge)
graph.set_entry_point("classify_and_route")
agent_graph = graph.compile()

def driver(user_name, streaming_mode=True):
    state = {
        "user_name": user_name,
        "session_id": None,
        "history": [],
        "last_domain": None,
        "last_reply": None,
        "step_count": 0,
        "current_input": None,
        "streaming_mode": streaming_mode
    }
    while True:
        user_message = input(f"{user_name}: ").strip()
        state["current_input"] = user_message
        state = agent_graph.invoke(state)
        # Always print agent response ONCE per message!
        if not streaming_mode:
            print(f"\nAgent ({state['last_domain']}): {state['last_reply']}")
        else:
            print(f"\nAgent ({state['last_domain']}):")  # In streaming mode, output is handled below
        if user_message.lower() in ["exit", "quit"]:
            print("Session ended.")
            break

if __name__ == "__main__":
    name = input("Enter your name: ").strip() or "User"
    stream_mode = input("Enable streaming reply output? (yes/no): ").strip().lower() in ["yes", "y", ""]
    driver(name, streaming_mode=stream_mode)
