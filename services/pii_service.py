
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine


# ==========================================
# 1. INITIALIZE PRESIDIO
# ==========================================

def initialize_pii_engines():

    nlp_configuration = {
        "nlp_engine_name": "spacy",
        "models": [
            {
                "lang_code": "en",
                "model_name": "en_core_web_sm"
            }
        ]
    }

    provider = NlpEngineProvider(
        nlp_configuration=nlp_configuration
    )

    nlp_engine = provider.create_engine()

    analyzer = AnalyzerEngine(
        nlp_engine=nlp_engine,
        supported_languages=["en"]
    )

    anonymizer = AnonymizerEngine()

    return analyzer, anonymizer


analyzer, anonymizer = initialize_pii_engines()


# ==========================================
# 2. DETECT PERSONAL INFORMATION
# ==========================================

def detect_pii(text):

    if not text or not text.strip():
        return []

    results = analyzer.analyze(
        text=text,
        language="en",
        entities=[
            "PERSON",
            "EMAIL_ADDRESS",
            "PHONE_NUMBER",
            "LOCATION",
            "IP_ADDRESS",
            "URL",
            "DATE_TIME"
        ],
        score_threshold=0.35
    )

    # Resolve overlapping detections:
    # Prefer PHONE_NUMBER over DATE_TIME when
    # both identify the same text region.

    phone_results = [
        result for result in results
        if result.entity_type == "PHONE_NUMBER"
    ]

    filtered_results = []

    for result in results:

        if result.entity_type == "DATE_TIME":

            overlaps_phone = any(
                result.start < phone.end
                and result.end > phone.start
                for phone in phone_results
            )

            if overlaps_phone:
                continue

        filtered_results.append(result)

    return filtered_results


# ==========================================
# 3. REDACT PERSONAL INFORMATION
# ==========================================

def redact_pii(text):

    if not text or not text.strip():

        return {
            "original_text": text,
            "redacted_text": text,
            "pii_detected": False,
            "entities_found": []
        }

    results = detect_pii(text)

    if not results:

        return {
            "original_text": text,
            "redacted_text": text,
            "pii_detected": False,
            "entities_found": []
        }

    anonymized_result = anonymizer.anonymize(
        text=text,
        analyzer_results=results
    )

    entities_found = list(
        set(result.entity_type for result in results)
    )

    return {
        "original_text": text,
        "redacted_text": anonymized_result.text,
        "pii_detected": True,
        "entities_found": entities_found
    }


# ==========================================
# 4. CONVENIENCE FUNCTION
# ==========================================

def get_safe_text(text):

    result = redact_pii(text)

    return result["redacted_text"]
