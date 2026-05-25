import re


# -----------------------------
# Extract Duration
# -----------------------------

def extract_duration(prompt):

    match = re.search(r'(\d+)\s*month', prompt.lower())

    if match:
        return int(match.group(1))

    return 3


# -----------------------------
# Detect Subject
# -----------------------------

def detect_subject(prompt):

    prompt = prompt.lower()

    # Priority-based detection

    if any(word in prompt for word in [
        "machine learning",
        "ml",
        "deep learning",
        "ai"
    ]):
        return "machine learning"

    elif any(word in prompt for word in [
        "dsa",
        "data structures",
        "algorithms",
        "leetcode"
    ]):
        return "dsa"

    elif any(word in prompt for word in [
        "python",
        "java",
        "c++",
        "cpp",
        "programming"
    ]):
        return "programming"

    elif any(word in prompt for word in [
        "physics",
        "thermodynamics",
        "mechanics",
        "electromagnetism"
    ]):
        return "physics"

    elif any(word in prompt for word in [
        "chemistry",
        "chem",
        "organic",
        "inorganic",
        "physical chemistry"
    ]):
        return "chemistry"

    elif any(word in prompt for word in [
        "math",
        "calculus",
        "algebra",
        "trigonometry"
    ]):
        return "math"

    elif any(word in prompt for word in [
        "aptitude",
        "quant",
        "reasoning",
        "logical reasoning",
        "placements"
    ]):
        return "aptitude"

    return "general"

# -----------------------------
# Detect Exam
# -----------------------------

def detect_exam(prompt):

    prompt = prompt.lower()

    exams = [
        "eamcet",
        "jee",
        "placements",
        "interview",
        "tcs nqt"
    ]

    for exam in exams:

        if exam in prompt:
            return exam

    return "general"


# -----------------------------
# Parse Prompt
# -----------------------------

def parse_prompt(prompt):

    return {

        "duration": extract_duration(prompt),

        "subject": detect_subject(prompt),

        "exam": detect_exam(prompt),

        "goal": prompt
    }