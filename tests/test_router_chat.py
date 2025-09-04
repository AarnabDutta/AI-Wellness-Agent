
import sys
import os
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from supervisor_agent.router import route_message

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)

def main():
    print("Welcome to the AI Employee Wellness Chat!")
    user_name = input("First, please enter your name: ").strip()
    print(f"Thank you, {user_name}! Type 'exit' to quit.\n")

    history = []
    agent_domain = "supervisor"
    turn = 0
    while True:
        user_input = input(f"{user_name}: ").strip()
        if user_input.lower() in ['exit', 'quit']:
            print("Session ended.")
            break

        agent_reply, new_agent_domain = route_message(
            user_message=user_input,
            history=history,
            user_name=user_name
        )

        turn += 1
        logging.info(f"Turn {turn}: Routed to [{new_agent_domain}] agent.")

        print(f"Agent: {agent_reply}\n")
        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": agent_reply})

        # Log any domain switch
        if new_agent_domain != agent_domain:
            logging.info(f"*** DOMAIN SWITCH: {agent_domain} → {new_agent_domain} ***")
        agent_domain = new_agent_domain

if __name__ == "__main__":
    main()


# import sys
# import os

# # Add project root to path for domain and supervisor_agent imports
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from dotenv import load_dotenv
# load_dotenv()

# from supervisor_agent.router import route_message

# def main():
#     print("Welcome to the AI Employee Wellness Chat!")
#     user_name = input("First, please enter your name: ").strip()
#     print(f"Thank you, {user_name}! Type 'exit' to quit.\n")

#     history = []
#     agent_domain = "supervisor"
#     while True:
#         user_input = input(f"{user_name}: ").strip()
#         if user_input.lower() in ['exit', 'quit']:
#             print("Session ended.")
#             break

#         agent_reply, agent_domain = route_message(
#             user_message=user_input,
#             history=history,
#             user_name=user_name
#         )
#         print(f"Agent: {agent_reply}\n")
#         # Maintain complete session history
#         history.append({"role": "user", "content": user_input})
#         history.append({"role": "assistant", "content": agent_reply})

# if __name__ == "__main__":
#     main()
