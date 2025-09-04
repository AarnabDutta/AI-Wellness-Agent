import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from domain.stress import handle_stress

def main():
    print("Welcome to the AI Employee Wellness (Stress Domain) Chat!")
    user_name = input("First, please enter your name: ").strip()
    print(f"Thank you, {user_name}! Type 'exit' to quit.\n")

    history = []
    while True:
        user_input = input(f"{user_name}: ").strip()
        if user_input.lower() in ['exit', 'quit']:
            print("Session ended.")
            break

        agent_reply = handle_stress(
            user_message=user_input,
            history=history,
            user_name=user_name       # <--- pass user's name to the handler
        )

        print(f"Agent: {agent_reply}\n")
        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": agent_reply})

if __name__ == "__main__":
    main()
