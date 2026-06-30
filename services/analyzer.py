import json
from backend.ai.gemini_clients import call_gemini
from backend.ai.prompts import get_resume_prompt


def safe_json_loads(text: str):
    """
    Safely parse JSON with cleanup.
    """

    if not text:
        raise ValueError("Empty AI response")

    # 🔧 Remove markdown wrappers if present
    text = text.replace("```json", "").replace("```", "").strip()

    # 🛑 Try direct parsing
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # 🔁 Attempt recovery (extract JSON block)
    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1:
        try:
            return json.loads(text[start:end + 1])
        except Exception:
            pass

    raise ValueError("Invalid JSON format from AI")


def analyze_resume_with_ai(cleaned_text: str):
    """
    Main AI pipeline
    """

    try:
        prompt = get_resume_prompt(cleaned_text)

        ai_text = call_gemini(prompt)

        parsed = safe_json_loads(ai_text)

        # 🛡️ Final validation
        required_keys = {"score", "strengths", "weaknesses", "suggestions"}

        if not all(key in parsed for key in required_keys):
            raise ValueError("Missing required fields in AI response")

        return parsed

    except Exception as e:
        return {
            "error": "AI processing failed",
            "details": str(e)
        }