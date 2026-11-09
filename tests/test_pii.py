
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from services.pii_service import redact_pii


test_cases = [

    {
        "question": (
            "My name is Rahul Sharma and "
            "my email is rahul@gmail.com."
        ),
        "expected": True
    },

    {
        "question": (
            "Please contact me at 9876543210."
        ),
        "expected": True
    },

    {
        "question": (
            "My IP address is 192.168.1.10."
        ),
        "expected": True
    },

    {
        "question": (
            "What are the OPD timings?"
        ),
        "expected": False
    },

    {
        "question": (
            "Where is the cardiology department?"
        ),
        "expected": False
    }
]


print("\n--- MEDIGUARD AI PII TESTS ---\n")

passed = 0

for test in test_cases:

    result = redact_pii(test["question"])

    expected = test["expected"]
    actual = result["pii_detected"]

    status = (
        "PASS" if expected == actual else "FAIL"
    )

    if status == "PASS":
        passed += 1

    print("Input:", test["question"])

    print("PII detected:", actual)

    print("Entities:", result["entities_found"])

    print("Redacted text:", result["redacted_text"])

    print("Expected PII:", expected)

    print("Status:", status)

    print("-" * 60)


print(
    f"\nRESULT: {passed}/{len(test_cases)} tests passed."
)
