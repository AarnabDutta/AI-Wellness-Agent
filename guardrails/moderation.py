import os
from dotenv import load_dotenv
import openai
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODERATION_ENDPOINT = os.getenv("OPENAI_MODERATION_ENDPOINT", "https://api.openai.com/v1/moderations")

openai.api_key = OPENAI_API_KEY

def openai_moderation_check(input_text: str) -> bool:
    """
    Checks if the input contains abusive, hateful, violent, or otherwise unsafe content
    using OpenAI's Moderation API. Returns True if unsafe, False if safe.
    """
    try:
        response = openai.Moderation.create(
            input=input_text
        )
        # 'flagged' is True if any moderation category is triggered
        return response["results"][0]["flagged"]
    except Exception as e:
        # Fail safely: Do not block if moderation API fails, but log error
        print(f"Moderation API error: {e}")
        return False

def moderate_or_block(input_text: str):
    """
    Returns (True, warning_message) if input is unsafe (should be blocked), else (False, None).
    Use this at the very first step of your chat pipeline.
    """
    if not input_text.strip():
        return False, None

    if openai_moderation_check(input_text):
        warning = (
            "Sorry, I can't engage with content that violates our community standards. "
            "Please avoid abusive, hateful, or unsafe language. "
            "If you need support, I'm here for you with care—and for urgent help, please seek a qualified professional or helpline."
        )
        return True, warning
    return False, None
