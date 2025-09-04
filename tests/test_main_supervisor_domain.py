import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
load_dotenv()
from supervisor_agent.main_router import detect_main_domain

def run_domain_tests():
    test_cases = [
        # MENTAL HEALTH (should NOT be 'mental_health' because your prompt allows only 'stress', 'sleep', or 'general')
        ("I'm feeling a lot of pressure at work and it's really stressing me out.", "stress"),
        ("My manager keeps giving me difficult deadlines. What should I do?", "stress"),
        ("I've been overwhelmed, tense, and frustrated lately due to work.", "stress"),

        # SLEEP
        ("I'm so tired all day and my sleep is terrible.", "sleep"),
        ("How can I stop using my phone before bed and get better rest?", "sleep"),
        ("My insomnia is getting worse every week.", "sleep"),
        ("What's a healthy bedtime routine?", "sleep"),

        # GENERAL
        ("Hello! Can you help me with wellbeing?", "general"),
        ("What do you offer?", "general"),
        ("Just wanted to say thank you!", "general"),
        ("I want to improve my overall health.", "general"),
        ("Give me advice.", "general"),

        # Ambiguous (should default to general)
        ("Do you have any tips?", "general"),
        ("Tell me more about your features.", "general"),
        ("I'm looking for guidance.", "general"),
    ]

    all_passed = True
    for idx, (input_text, expected_domain) in enumerate(test_cases, 1):
        result = detect_main_domain(input_text)
        passed = result == expected_domain
        print(f"Test {idx}: '{input_text}' --> got: '{result}' | expected: '{expected_domain}' | {'PASSED' if passed else 'FAILED'}")
        if not passed:
            all_passed = False

    if all_passed:
        print("\nAll main supervisor domain tests PASSED.")
    else:
        print("\nSome main supervisor domain tests FAILED. Review your API/.env/model or the domain routing code if needed.")

if __name__ == "__main__":
    run_domain_tests()
