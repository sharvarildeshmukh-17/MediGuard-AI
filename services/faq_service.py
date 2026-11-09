import json
from pathlib import Path
from difflib import SequenceMatcher
import re



FAQ_PATH = Path(__file__).resolve().parent.parent / "data" / "hospital_faq.json"


def load_faqs():
    """Load hospital FAQs from the JSON dataset."""

    try:
        with open(FAQ_PATH, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        raise FileNotFoundError(
            f"FAQ dataset not found: {FAQ_PATH}"
        )

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid FAQ JSON format: {error}"
        )


def get_faq_context():
    """Prepare all FAQs as context for Gemini."""

    faqs = load_faqs()

    context = []

    for faq in faqs:
        context.append(
            f"Category: {faq['category']}\n"
            f"Question: {faq['question']}\n"
            f"Answer: {faq['answer']}"
        )

    return "\n\n".join(context)

def find_faq_answer(user_question):
    faqs = load_faqs()

    stop_words = {
        "what", "is", "are", "the", "a", "an",
        "of", "to", "in", "on", "for", "can",
        "i", "how", "where", "does", "do",
        "my", "your", "please", "tell", "me",
        "about", "and", "at", "this", "that"
    }

    def tokenize(text):
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        return [
            word for word in text.split()
            if word not in stop_words
        ]

    query_tokens = tokenize(user_question)
    if not query_tokens:
        return None

# Prevent unrelated questions from matching hospital FAQs.
    non_hospital_intent_terms = {
        "salary", "salaries", "income", "earning", "earnings",
        "wage", "wages", "career", "job", "jobs",
        "vacancy", "recruitment", "hiring",
        "capital", "weather", "population", "president",
        "cricket", "football", "politics"
    }

    if any(token in non_hospital_intent_terms for token in query_tokens):
        return None

    aliases = {
        "OPD": ["opd", "outpatient", "opd timings"],
        "Emergency": ["emergency", "emergency department"],
        "Appointments": [
            "appointment", "book appointment",
            "booking", "schedule appointment"
        ],
        "Departments": [
            "cardiology", "cardiologist", "heart department"
        ],
        "Pharmacy": [
            "pharmacy", "pharmacy hours",
            "pharmacy timings", "medicine counter"
        ],
        "Visiting Hours": [
            "visiting hours", "visitor hours"
        ],
        "Billing": [
            "billing", "hospital bill",
            "pay bills", "payment", "billing counter"
        ],
        "Facilities": ["parking", "visitor parking"],
        "Laboratory": ["laboratory", "lab", "blood test"],
        "Location": [
            "main reception", "hospital location",
            "reception location"
        ],
        "Insurance": [
            "insurance", "insurance desk",
            "insurance coverage"
        ],
        "Admission": [
            "admission", "admission documents"
        ]
    }

    matches = []

    for faq in faqs:
        category = faq["category"]

        phrases = [
            faq["question"],
            *aliases.get(category, [])
        ]

        matched = False

        for phrase in phrases:
            phrase_tokens = tokenize(phrase)

            if not phrase_tokens:
                continue

            # Match the phrase in order, allowing stop words
            # between its meaningful words.
            position = 0

            for token in query_tokens:
                if token == phrase_tokens[position]:
                    position += 1

                if position == len(phrase_tokens):
                    matched = True
                    break

            if matched:
                break

        if matched:
            matches.append(faq)

    if len(matches) == 1:
        return {
            "answer": matches[0]["answer"],
            "category": matches[0]["category"],
            "confidence": 1.0
        }

    return None