import re

from config.prompts import (
    MEDICAL_REFUSAL,
    EMERGENCY_RESPONSE,
    OUT_OF_SCOPE_RESPONSE
)


# Possible emergency indicators.
EMERGENCY_PATTERNS = [
    r"\bchest pain\b",
    r"\bcan't breathe\b",
    r"\bcannot breathe\b",
    r"\bdifficulty breathing\b",
    r"\btrouble breathing\b",
    r"\bsevere bleeding\b",
    r"\bunconscious\b",
    r"\bnot responding\b",
    r"\bpossible stroke\b",
    r"\bheart attack\b",
    r"\boverdose\b",
    r"\bsuicidal\b",
    r"\bwant to kill myself\b"
]


# Requests that require medical advice.
MEDICAL_PATTERNS = [
    r"\bdiagnos\w*\b",
    r"\bprescrib\w*\b",
    r"\bantibiotics?\b",
    r"\bmedicine for\b",
    r"\bmedication for\b",
    r"\bdosage\b",
    r"\bdosages\b",
    r"\bhow much medicine\b",
    r"\btreatment for\b",
    r"\bwhat disease\b",
    r"\bwhat illness\b",
    r"\binterpret my report\b",
    r"\bmedical advice\b",
    r"\bwhat should i take\b",
    r"\bwhat are my symptoms\b"
]


def matches_patterns(text, patterns):
    text = text.lower()

    for pattern in patterns:
        if re.search(pattern, text):
            return True

    return False


def check_guardrails(user_question):

    if not user_question or not user_question.strip():
        return {
            "blocked": True,
            "category": "EMPTY_INPUT",
            "response": "Please enter a question."
        }

    # Emergency checks have the highest priority.
    if matches_patterns(user_question, EMERGENCY_PATTERNS):
        return {
            "blocked": True,
            "category": "EMERGENCY",
            "response": EMERGENCY_RESPONSE
        }

    # Prevent diagnosis and prescription requests.
    if matches_patterns(user_question, MEDICAL_PATTERNS):
        return {
            "blocked": True,
            "category": "MEDICAL_ADVICE",
            "response": MEDICAL_REFUSAL
        }

    return {
        "blocked": False,
        "category": "ALLOWED",
        "response": None
    }