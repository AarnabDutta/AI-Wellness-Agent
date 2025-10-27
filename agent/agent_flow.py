import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
load_dotenv()

from supervisor_agent.main_router import route_message

def driver(user_name, streaming_mode=True):
    print("Type 'exit' or 'quit' to end the session at any time.\n")
    history = []
    agent_domain = "main_supervisor"

    while True:
        user_message = input(f"{user_name}: ").strip()
        if user_message.lower() in ['exit', 'quit']:
            print("Session ended.")
            break

        print("thinking...")  # Show before response
        agent_reply, new_agent_domain = route_message(
            user_message=user_message,
            history=history,
            user_name=user_name,
            stream=streaming_mode
        )
        # Only print what is returned, never print from inside any .py domain handler
        print(f"\nAgent ({new_agent_domain}): {agent_reply}\n")
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": agent_reply})
        agent_domain = new_agent_domain

if __name__ == "__main__":
    name = input("Enter your name: ").strip() or "User"
    stream_mode = input("Enable streaming reply output? (yes/no): ").strip().lower() in ["yes", "y", ""]
    driver(name, streaming_mode=stream_mode)
