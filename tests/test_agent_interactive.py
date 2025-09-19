import sys
import os
import logging
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from supervisor_agent.main_router import route_message, detect_main_domain

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)

def main():
    print("==== AI Wellness Agent Interactive Test with Granular Timing ====")
    user_name = input("Your name for this session: ").strip() or "Friend"
    print("Type 'exit' or 'quit' to leave at any time.\n")

    history = []
    agent_domain = "main_supervisor"
    turn = 0

    while True:
        try:
            user_input = input(f"{user_name}: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting chat.")
            break

        if user_input.lower() in ['exit', 'quit']:
            print("Session ended.")
            break

        # Measurement for full turn
        full_start = time.time()

        # First, measure supervisor (classification) time specifically:
        classify_start = time.time()
        main_domain = detect_main_domain(
            user_input,
            history=history,
            user_name=user_name
        )
        classify_end = time.time()
        classify_time = classify_end - classify_start

        # Now measure reply generation
        reply_start = time.time()
        agent_reply, new_agent_domain = route_message(
            user_message=user_input,
            history=history,
            user_name=user_name
        )
        reply_end = time.time()
        reply_time = reply_end - reply_start

        full_end = time.time()
        total_turn_time = full_end - full_start

        turn += 1
        logging.info(f"Turn {turn}: Routed to [{new_agent_domain}]")
        logging.info(f"Classification/domain detection time: {classify_time:.2f} sec")
        logging.info(f"Agent reply generation time: {reply_time:.2f} sec")
        logging.info(f"Total turn time (incl. both): {total_turn_time:.2f} sec")

        print(f"\033[94mAgent ({new_agent_domain}): {agent_reply}\033[0m\n")  # Agent reply in blue

        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": agent_reply})

        # Log domain/agent switch visually
        if new_agent_domain != agent_domain:
            logging.info(f"*** DOMAIN SWITCH: {agent_domain} → {new_agent_domain} ***")
        agent_domain = new_agent_domain

if __name__ == "__main__":
    main()
