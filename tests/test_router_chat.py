import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from supervisor_agent.main_router import route_message

def main():
    print("==== AI Employee Wellness Chat! ====")
    user_name = input("First, please enter your name: ").strip() or "Friend"
    print(f"Thank you, {user_name}! Type 'exit' to quit.\n")

    history = []
    agent_domain = "main_supervisor"

    while True:
        try:
            user_input = input(f"{user_name}: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSession ended.")
            break

        if user_input.lower() in ['exit', 'quit']:
            print("Session ended.")
            break

        agent_reply, new_agent_domain = route_message(
            user_message=user_input,
            history=history,
            user_name=user_name
        )

        print(f"\033[94mAgent ({new_agent_domain}): {agent_reply}\033[0m\n")

        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": agent_reply})

        if new_agent_domain != agent_domain:
            print(f"*** DOMAIN SWITCH: {agent_domain} → {new_agent_domain} ***\n")
        agent_domain = new_agent_domain

if __name__ == "__main__":
    main()
