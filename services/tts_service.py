import asyncio
import edge_tts
import streamlit as st


# --------------------------------------------------
# TTS CONFIGURATION
# --------------------------------------------------

DEFAULT_VOICE = "en-IN-NeerjaNeural"
FALLBACK_VOICE = "en-IN-PrabhatNeural"

SPEECH_RATE = "+0%"
SPEECH_VOLUME = "+0%"


# --------------------------------------------------
# TEXT-TO-SPEECH GENERATION
# --------------------------------------------------

async def generate_speech_async(text, voice=DEFAULT_VOICE):

    communicator = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=SPEECH_RATE,
        volume=SPEECH_VOLUME
    )

    audio_chunks = []

    async for chunk in communicator.stream():

        if chunk["type"] == "audio":
            audio_chunks.append(chunk["data"])

    return b"".join(audio_chunks)


def generate_speech(text, voice=DEFAULT_VOICE):
    """
    Convert text into speech.

    Returns MP3 audio bytes.
    """

    if not text or not text.strip():
        return None

    try:
        audio_data = asyncio.run(
            generate_speech_async(text, voice)
        )

        if audio_data:
            return audio_data

        raise RuntimeError("No audio was generated.")

    except Exception as error:

        # Try fallback voice if the primary voice fails.
        if voice != FALLBACK_VOICE:

            try:
                return asyncio.run(
                    generate_speech_async(text, FALLBACK_VOICE)
                )

            except Exception:
                raise RuntimeError(
                    f"Speech generation failed: {error}"
                ) from error

        raise RuntimeError(
            f"Speech generation failed: {error}"
        ) from error