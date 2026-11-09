
import sys
from pathlib import Path

# Add the project root to Python's module search path
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Import FAQ service
from services.faq_service import find_faq_answer


def test_faq_fallback():

    questions = [
    "What is the salary of a cardiologist?",
    "Where is cardiology?",
    "What are OPD timings?",
    "What are pharmacy timings?",
    "What is the capital of France?",
    "Can I book an appointment?",
    ]

    for question in questions:

        print("\nQuestion:", question)

        result = find_faq_answer(question)

        if result:

            print("Status: PASS")
            print("Category:", result["category"])
            print("Answer:", result["answer"])
            print("Confidence:", result["confidence"])

        else:

            print("Status: NO MATCH")
            print("Safe result: Information unavailable.")


if __name__ == "__main__":
    test_faq_fallback()
