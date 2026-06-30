from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in environment variables")

client = genai.Client(api_key=API_KEY)


def call_gemini(prompt: str) -> str:
    """
    Calls Gemini API safely and returns text output.
    Includes fallback for future API changes.
    """

    # 🛑 Basic prompt validation (avoid empty / huge payloads)
    if not prompt or len(prompt.strip()) == 0:
        raise ValueError("Prompt is empty")

    if len(prompt) > 30000:  # prevent abuse / huge payloads
        raise ValueError("Prompt too large")

    try:
        # ✅ Primary method (simple + stable)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if not response or not response.text:
            raise ValueError("Empty response from AI")

        return response.text

    except Exception:
        # 🔁 Fallback (future-proof if API changes)
        try:
            stream = client.interactions.create(
                model="gemini-2.5-flash",
                input=prompt,
                stream=True
            )

            full_text = ""
            for event in stream:
                if event.event_type == "step.delta":
                    if getattr(event.delta, "type", None) == "text":
                        full_text += event.delta.text

            if not full_text:
                raise ValueError("Fallback also failed")

            return full_text

        except Exception as e:
            raise RuntimeError(f"AI request failed: {str(e)}")