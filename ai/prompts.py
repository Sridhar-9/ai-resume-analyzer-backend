def get_resume_prompt(text: str) -> str:
    """
    Builds a strict prompt to ensure JSON output.
    """

    # 🛑 Prevent extremely long input
    text = text[:15000]

    return  f"""
You are a professional ATS (Applicant Tracking System).

Analyze the resume and return STRICT JSON:

{{
  "score": (0-100),
  "strengths": [list],
  "weaknesses": [list],
  "suggestions": [list],
  "missing_keywords": [list],
  "recommended_roles": [list]
}}

Resume:
{text}

"""