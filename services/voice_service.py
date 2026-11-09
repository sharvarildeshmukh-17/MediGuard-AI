import os
import tempfile
from pathlib import Path

import streamlit as st
from faster_whisper import WhisperModel


# --------------------------------------------------
# WHISPER MODEL CONFIGURATION
# --------------------------------------------------

MODEL_SIZE = "tiny"
MAX_AUDIO_SIZE_MB = 20


# Load the model only once during the Streamlit session.
@st.cache_resource
def load_whisper_model():
    print("Loading Faster-Whisper model...")

    model = WhisperModel(
        MODEL_SIZE,
        device="cpu",
        compute_type="int8"
    )

    print("Faster-Whisper model loaded successfully!")
    return model


# --------------------------------------------------
# AUDIO TRANSCRIPTION
# --------------------------------------------------

def transcribe_audio(audio_file):
    """
    Transcribe an uploaded or recorded audio file.

    Returns:
        {
            "text": transcribed text,
            "language": detected language,
            "language_probability": language confidence
        }
    """

    if audio_file is None:
        raise ValueError("No audio file was provided.")

    # Get audio bytes from Streamlit UploadedFile.
    audio_bytes = audio_file.getvalue()

    if not audio_bytes:
        raise ValueError("The audio file is empty.")

    # Validate file size.
    max_size = MAX_AUDIO_SIZE_MB * 1024 * 1024

    if len(audio_bytes) > max_size:
        raise ValueError(
            f"Audio file is too large. Maximum allowed size is "
            f"{MAX_AUDIO_SIZE_MB} MB."
        )

    # Determine a suitable temporary file extension.
    original_name = getattr(audio_file, "name", "")
    suffix = Path(original_name).suffix.lower()

    if not suffix:
        mime_type = getattr(audio_file, "type", "")

        mime_extensions = {
            "audio/wav": ".wav",
            "audio/x-wav": ".wav",
            "audio/mpeg": ".mp3",
            "audio/mp4": ".m4a",
            "audio/webm": ".webm",
            "audio/ogg": ".ogg",
            "audio/flac": ".flac"
        }

        suffix = mime_extensions.get(mime_type, ".wav")

    temporary_path = None

    try:
        # Save audio temporarily because Whisper needs a file path.
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temporary_file:

            temporary_file.write(audio_bytes)
            temporary_path = temporary_file.name

        model = load_whisper_model()

        segments, information = model.transcribe(
            temporary_path,
            language=None,       # Automatically detect language
            beam_size=5,
            vad_filter=True
        )

        # Convert generated segments into one text string.
        transcription = " ".join(
            segment.text.strip()
            for segment in segments
        ).strip()

        if not transcription:
            raise ValueError(
                "No speech could be detected. Please try recording again."
            )

        return {
            "text": transcription,
            "language": information.language,
            "language_probability": round(
                information.language_probability, 3
            )
        }

    finally:
        # Always remove the temporary audio file.
        if temporary_path and os.path.exists(temporary_path):
            os.remove(temporary_path)