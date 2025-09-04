import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
load_dotenv()
from supervisor_agent.main_router import route_message

def print_header(text):
    print("\n" + "="*30)
    print(text)
    print("="*30 + "\n")

def run_mental_health_supervisor_tests():
    user_name = input("Please enter your name to simulate the chat: ").strip() or "Alex"
    history = []
    agent_domain = "main_supervisor"

    test_cases = [
        ("I'm constantly exhausted and don't enjoy my work anymore.", "mental_health_burnout", "burnout"),
        ("Deadlines are giving me a lot of stress. I feel overwhelmed.", "mental_health_stress", "stress"),
        ("I feel anxious in meetings and dread starting my workday.", "mental_health_anxiety", "anxiety"),
        ("I've lost all motivation and can't even get out of bed for work.", "mental_health_depression", "depression"),
        ("I just can't keep work and personal life separated working from home.", "mental_health_work_life_balance", "work-life balance"),
        ("Honestly, I just need someone to listen. I feel alone.", "mental_health_empathy_buddy", "empathy buddy"),
        ("Can you help with my overall mental wellness?", "mental_health_supervisor", "supervisor"),
    ]

    print_header("AI Mental Health Supervisor Routing Integration Test")

    for idx, (user_input, expected_agent, agent_label) in enumerate(test_cases, 1):
        agent_reply, routed_agent = route_message(
            user_message=user_input,
            history=history,
            user_name=user_name
        )
        print(f"Test {idx}: {agent_label.upper()}")
        print(f"User: {user_input}")
        print(f"Expected Routing: {expected_agent}")
        print(f"Actual Routing:   {routed_agent}")
        print(f"Agent Reply:      {agent_reply[:200]}...\n")
        status = "PASSED" if (routed_agent == expected_agent) else "FAILED"
        print(f"[{status}]")
        print("-"*40)
        
        # Add to chat history for session context
        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": agent_reply})

    print_header("Session history check (last 2 messages):")
    for entry in history[-2:]:
        print(f"{entry['role'].capitalize()}: {entry['content'][:200]}...")

if __name__ == "__main__":
    run_mental_health_supervisor_tests()
