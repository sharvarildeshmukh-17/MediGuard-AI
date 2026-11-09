from transformers import pipeline

# ---------------------------------------
# CONFIGURATION
# ---------------------------------------

MODEL_NAME = "unitary/toxic-bert"

# Conservative threshold to reduce false positives.
TOXICITY_THRESHOLD = 0.80

TOXIC_LABELS = {
    "toxic",
    "severe_toxic",
    "obscene",
    "threat",
    "insult",
    "identity_hate"
}

# ---------------------------------------
# LOAD MODEL
# ---------------------------------------

_classifier = None


def load_toxicity_model():
    """
    Load the BERT toxicity model only once.
    The model is downloaded the first time it runs.
    """

    global _classifier

    if _classifier is None:
        print("Loading BERT toxicity detection model...")

        _classifier = pipeline(
            task="text-classification",
            model=MODEL_NAME,
            tokenizer=MODEL_NAME,
            top_k=None,
            device=-1
        )

        print("Toxicity model loaded successfully.")

    return _classifier


# ---------------------------------------
# ANALYZE TOXICITY
# ---------------------------------------

def analyze_toxicity(text):
    """
    Returns the toxicity scores predicted by BERT.
    """

    if not text or not text.strip():
        return {}

    classifier = load_toxicity_model()

    predictions = classifier(
        text[:2000],
        truncation=True
    )

    # Pipeline output is a list of dictionaries.
    if predictions and isinstance(predictions[0], list):
        predictions = predictions[0]

    scores = {
        item["label"].lower(): float(item["score"])
        for item in predictions
    }

    return scores


# ---------------------------------------
# CHECK TOXICITY
# ---------------------------------------

def check_toxicity(text):
    """
    Determines whether a message should be blocked.
    """

    if not text or not text.strip():
        return {
            "blocked": False,
            "category": "EMPTY_INPUT",
            "message": None,
            "scores": {}
        }

    scores = analyze_toxicity(text)

    flagged_categories = [
        label
        for label in TOXIC_LABELS
        if scores.get(label, 0.0) >= TOXICITY_THRESHOLD
    ]

    if flagged_categories:
        return {
            "blocked": True,
            "category": "TOXIC_CONTENT",
            "message": (
                "I'm here to help with hospital-related questions. "
                "Please keep the conversation respectful and avoid "
                "abusive or threatening language."
            ),
            "scores": scores,
            "flagged_categories": flagged_categories
        }

    return {
        "blocked": False,
        "category": "ALLOWED",
        "message": None,
        "scores": scores,
        "flagged_categories": []
    }