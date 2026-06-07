from dotenv import load_dotenv
load_dotenv()
from groq import Groq
import json
import os

def screen_resume(resume_text: str, job_description: str) -> dict:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))  # moved inside function
    
    prompt = f"""You are an expert ATS system and senior HR recruiter with 10+ years of experience.

Analyze the resume against the job description carefully.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Respond ONLY with a valid JSON object — no markdown, no explanation, no backticks.
Use exactly this format:
{{
  "score": <integer 0-100>,
  "matched_skills": ["skill1", "skill2"],
  "missing_skills": ["skill1", "skill2"],
  "improvements": ["tip1", "tip2", "tip3"],
  "strengths": ["strength1", "strength2"],
  "summary": "<2-3 sentence verdict on fit for this role>"
}}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)