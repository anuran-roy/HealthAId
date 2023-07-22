from typing import Any, Dict, List
import openai
import os
from dotenv import load_dotenv

# from logs.logger import log

load_dotenv()

load_dotenv()

# os.getenv("OPENAI_API_KEY")
openai.api_key = "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"  # "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"


def get_single_message(
    messages: List[Dict[str, Any]],
    model: str = "gpt-3.5-turbo",
    max_tokens: int = 500,
    temperature: float = 0.0,
):
    """
    Use ChatCompletion APIs to get OpenAI model response
    """
    try:
        result = openai.ChatCompletion.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=messages,
        )
        return result["choices"]
    except Exception as openai_exception:
        # log(
        #     alert_level="ERROR",
        #     message=f"Error during calling OpenAI API. Reason: {str(openai_exception)}",
        # )  # Log as an error to the broker
        return {"success": False, "error": str(openai_exception)}
