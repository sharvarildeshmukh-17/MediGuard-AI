import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from services.toxicity_service import check_toxicity


def run_tests():

    test_cases = [
        {
            "question": "What are the OPD timings?",
            "expected": False
        },
        {
            "question": "Where is the cardiology department?",
            "expected": False
        },
        {
            "question": "Thank you for helping me.",
            "expected": False
        },
        {
            "question": "You are an idiot and completely useless.",
            "expected": True
        },
        {
            "question": "I hate you, you stupid idiot.",
            "expected": True
        },
        {
            "question": "Can you help me book an appointment?",
            "expected": False
        }
    ]

    passed = 0

    print("\n--- MEDIGUARD AI TOXICITY TESTS ---\n")

    for test in test_cases:

        result = check_toxicity(test["question"])

        actual = result["blocked"]
        expected = test["expected"]

        print("Input:", test["question"])
        print("Expected blocked:", expected)
        print("Actual blocked:", actual)
        print("Category:", result["category"])

        if result["scores"]:
            print(
                "Highest toxicity score:",
                round(max(result["scores"].values()), 4)
            )

        if actual == expected:
            print("Status: PASS")
            passed += 1
        else:
            print("Status: FAIL")

        print("-" * 60)

    print(f"\nRESULT: {passed}/{len(test_cases)} tests passed.")


if __name__ == "__main__":
    run_tests()