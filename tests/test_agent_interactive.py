import sys
import os
import logging
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from supervisor_agent.main_router import route_message, detect_main_domain
from model.customllm import UnifiedLLMClient

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)

def main():
    print("==== AI Wellness Agent Interactive Test with Granular Timing ====")
    user_name = input("Your name for this session: ").strip() or "Friend"
    print("Type 'exit' or 'quit' to leave at any time.")
    stream_mode = input("Enable streaming reply output? (yes/no) [default: yes]: ").strip().lower()
    stream_mode = False if stream_mode not in ["yes", "y", ""] else True
    print(f"Streaming mode is {'ON' if stream_mode else 'OFF'}.\n")

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

        # Timing for total turn
        full_start = time.time()

        # 1. Classification Time
        classify_start = time.time()
        main_domain = detect_main_domain(
            user_input,
            history=history,
            user_name=user_name
        )
        classify_end = time.time()
        classify_time = classify_end - classify_start

        # 2. Agent Reply Time
        reply_start = time.time()
        # Route to appropriate domain agent; pass streaming argument
        agent_reply, new_agent_domain = route_message(
            user_message=user_input,
            history=history,
            user_name=user_name,
            stream=stream_mode  # Use the new streaming feature!
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

        # Print a newline after streaming for clarity (reply has already shown)
        print(f"\n\033[94mAgent ({new_agent_domain}):\033[0m", end="")
        if not stream_mode:
            print(agent_reply)
        else:
            # agent_reply already streamed to terminal, but you can access full text for history/logging
            pass

        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": agent_reply})

        # Visual domain switch info
        if new_agent_domain != agent_domain:
            logging.info(f"*** DOMAIN SWITCH: {agent_domain} → {new_agent_domain} ***")
        agent_domain = new_agent_domain

if __name__ == "__main__":
    main()
