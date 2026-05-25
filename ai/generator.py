import requests
import os
import re

from dotenv import load_dotenv
import streamlit as st

from ai.prompt_engine import detect_subject

load_dotenv()

# -----------------------------
# API KEY
# -----------------------------

API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    API_KEY = st.secrets.get("OPENROUTER_API_KEY")

# -----------------------------
# EXTRACT DURATION
# -----------------------------

def extract_duration(text):

    text = text.lower()

    # Match months
    month_match = re.search(r'(\d+)\s*month', text)

    if month_match:
        return int(month_match.group(1))

    # Match years
    year_match = re.search(r'(\d+)\s*year', text)

    if year_match:
        return int(year_match.group(1)) * 12

    return 3

# -----------------------------
# GENERATE COURSE
# -----------------------------

def generate_course(user_prompt):

    duration = extract_duration(user_prompt)

    # -----------------------------
    # DETECT SUBJECT FROM GOAL
    # -----------------------------

    goal_match = re.search(
        r'Goal:\s*(.*)',
        user_prompt
    )

    goal_text = (
        goal_match.group(1)
        if goal_match
        else user_prompt
    )

    subject = detect_subject(goal_text)

    # -----------------------------
    # PROJECT RULES
    # -----------------------------

    include_projects = subject in [
        "programming",
        "machine learning"
    ]

    # -----------------------------
    # MAIN PROMPT
    # -----------------------------

    prompt = f"""
Create a personalized learning roadmap.

User Request:
{user_prompt}

IMPORTANT:
Generate EXACTLY {duration} months.

STRICT RULES:
- Every month must be UNIQUE
- No repeated content
- Keep roadmap concise
- Maximum 5 topics per month
- Maximum 2 resources per month
- Maximum 2 practice platforms
- Keep explanations short
- Avoid overly academic wording
- Match roadmap difficulty with study hours
- Prioritize practical learning
"""

    # -----------------------------
    # PROJECTS FOR AI/PROGRAMMING
    # -----------------------------

    if include_projects:

        prompt += """
- For programming and AI subjects,
  projects are MANDATORY
"""

    # -----------------------------
    # INCLUDE SECTIONS
    # -----------------------------

    prompt += """

Include:
- Topics
- Resources
- Practice Platforms
"""

    if include_projects:

        prompt += """
- Mini Project
"""

    # -----------------------------
    # SPECIAL RULES
    # -----------------------------

    prompt += """

SPECIAL RULES:
- Use REAL resource links
- Beginner friendly
- Clean markdown formatting
- Avoid fake/artificial projects
- For theory subjects like Physics,
  Chemistry, Thermodynamics,
  Aptitude, Math:
  DO NOT generate projects

FORMAT:

## Month 1 - Title

Topics:
- Topic 1
- Topic 2
"""

    # -----------------------------
    # PROJECT FORMAT
    # -----------------------------

    if include_projects:

        prompt += """

Project:
- Include EXACTLY 1 practical mini project
- Project must match the month's topics
- Project should be beginner-friendly
"""

    # -----------------------------
    # RESOURCE FORMAT
    # -----------------------------

    prompt += """

Resources:
- Maximum 2 high-quality resources

Practice:
- Maximum 2 relevant practice platforms

Continue until all months are completed.
"""

    # -----------------------------
    # API REQUEST
    # -----------------------------

    try:

        response = requests.post(

            url="https://openrouter.ai/api/v1/chat/completions",

            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },

            json={

                "model": "openrouter/auto",

                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
        )

        data = response.json()

        if "choices" in data:

            return data["choices"][0]["message"]["content"]

        else:

            return "Unable to generate roadmap currently."

    except Exception:

        return "Error generating roadmap. Please try again."