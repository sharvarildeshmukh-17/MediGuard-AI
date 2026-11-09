import streamlit as st

from services.pii_service import redact_pii
from services.gemini_service import generate_response
from services.voice_service import transcribe_audio
from services.tts_service import generate_speech

from config.settings import (
    APP_NAME,
    APP_TAGLINE,
    WELCOME_MESSAGE
)


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #F5F8FC;
}

header[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    display: none;
}

.block-container {
    max-width: 1050px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Main Header */

.main-header {
    background: linear-gradient(120deg, #123B70, #2376C9);
    padding: 28px;
    border-radius: 18px;
    color: white;
    margin-bottom: 25px;
}

.main-header h1 {
    font-size: 32px;
    font-weight: 800;
    color: white;
    margin-bottom: 5px;
}

.main-header p {
    color: #EAF3FF !important;
    font-size: 15px;
}

.status {
    background: #E5F5EC;
    color: #187344;
    display: inline-block;
    padding: 6px 13px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    margin-top: 8px;
}

/* Information Cards */

.info-card {
    background: white;
    padding: 20px;
    border: 1px solid #E5EAF2;
    border-radius: 14px;
    min-height: 140px;
    height: 140px;
    box-sizing: border-box;
    margin-bottom: 10px;
}

.info-card h4 {
    color: #183B63;
    font-size: 15px;
    margin-bottom: 8px;
}

.info-card p {
    color: #64748B;
    font-size: 12px;
}

/* Section Titles */

.section-title {
    font-size: 19px;
    font-weight: 700;
    color: #173B63;
    margin-top: 25px;
    margin-bottom: 12px;
}

/* Chat Messages */

div[data-testid="stChatMessage"] {
    background-color: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 14px !important;
    padding: 12px;
    margin-bottom: 12px;
    color: #183B63 !important;
}

div[data-testid="stChatMessage"] p,
div[data-testid="stChatMessage"] li,
div[data-testid="stChatMessage"] span {
    color: #334155 !important;
}

/* Buttons */

.stButton button {
    border-radius: 10px;
    border: 1px solid #DCE6F2;
    background: white;
    color: #174B80;
    font-weight: 600;
}

.stButton button:hover {
    border-color: #2376C9;
    color: #2376C9;
}

/* Chat Input */

div[data-testid="stChatInput"] {
    background-color: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 14px !important;
}

div[data-testid="stChatInput"] textarea {
    background-color: #FFFFFF !important;
    color: #183B63 !important;
    -webkit-text-fill-color: #183B63 !important;
}

/* Bottom Chat Container */

div[data-testid="stBottom"] {
    background-color: #F5F8FC !important;
}

div[data-testid="stBottom"] > div {
    background-color: #F5F8FC !important;
}

/* General Text */

.stApp,
.stApp p,
.stApp label {
    color: #183B63;
}

/* Footer */

.footer {
    text-align: center;
    color: #94A3B8;
    font-size: 12px;
    margin-top: 35px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": WELCOME_MESSAGE
        }
    ]

if "tts_audio" not in st.session_state:
    st.session_state.tts_audio = {}

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

if "voice_result" not in st.session_state:
    st.session_state.voice_result = None

if "transcribed_question" not in st.session_state:
    st.session_state.transcribed_question = ""


# ==========================================
# MAIN HEADER
# ==========================================

st.html(f"""
<div class="main-header">

    <h1>🏥 {APP_NAME}</h1>

    <p>{APP_TAGLINE}</p>

    <div class="status">
        ● Hospital Information Assistant
    </div>

</div>
""")


# ==========================================
# INFORMATION CARDS
# ==========================================

st.markdown(
    '<div class="section-title">How can I assist you?</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

cards = [
    (
        "📅 Appointments",
        "Get information about booking appointments."
    ),
    (
        "🩺 Departments",
        "Explore hospital departments and services."
    ),
    (
        "🏥 Hospital Facilities",
        "Find information about hospital facilities."
    )
]

for col, (heading, description) in zip(
    [col1, col2, col3],
    cards
):

    with col:

        st.html(f"""
        <div class="info-card">

            <h4>{heading}</h4>

            <p>{description}</p>

        </div>
        """)


# ==========================================
# U4.2 - VISUAL HOSPITAL ASSISTANCE
# ==========================================

st.markdown("---")

st.markdown(
    '<div class="section-title">🏥 Quick Hospital Guide</div>',
    unsafe_allow_html=True
)

st.caption(
    "Explore hospital services, facilities and important information."
)

# Emergency assistance banner
st.html("""
<div style="
    background: #FFF0EF;
    border: 1px solid #F5C2BE;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 20px;
">
    <div style="font-size: 28px;">🚨</div>
    <h3 style="color: #B42318; margin: 5px 0;">
        Emergency Department
    </h3>
    <p style="color: #7A271A; margin: 0;">
        Emergency services are available 24 hours a day,
        7 days a week.
    </p>
    <p style="color: #7A271A; font-weight: 600; margin-bottom: 0;">
        For a medical emergency, seek immediate professional help.
    </p>
</div>
""")

# Hospital service cards
hospital_services = [
    {
        "icon": "❤️",
        "name": "Cardiology",
        "description": "Heart-related department",
        "location": "Second floor",
        "question": "Where is the cardiology department?"
    },
    {
        "icon": "💊",
        "name": "Pharmacy",
        "description": "Hospital pharmacy services",
        "location": "8 AM – 10 PM",
        "question": "What are pharmacy timings?"
    },
    {
        "icon": "🧪",
        "name": "Laboratory",
        "description": "Laboratory services",
        "location": "7 AM – 7 PM",
        "question": "What are laboratory timings?"
    },
    {
        "icon": "🧾",
        "name": "Billing",
        "description": "Billing and payment assistance",
        "location": "Near main reception",
        "question": "Where is the billing counter?"
    },
    {
        "icon": "🅿️",
        "name": "Parking",
        "description": "Visitor parking facility",
        "location": "Near main entrance",
        "question": "Where is visitor parking?"
    },
    {
        "icon": "📍",
        "name": "Reception",
        "description": "Hospital information desk",
        "location": "Ground floor",
        "question": "Where is the main reception?"
    }
]

service_columns = st.columns(3)

for index, service in enumerate(hospital_services):

    with service_columns[index % 3]:

        st.html(f"""
        <div style="
            background: white;
            border: 1px solid #E2E8F0;
            border-radius: 14px;
            padding: 17px;
            min-height: 155px;
            margin-bottom: 8px;
        ">
            <div style="font-size: 28px;">
                {service['icon']}
            </div>

            <h4 style="
                color: #183B63;
                margin: 8px 0 5px 0;
            ">
                {service['name']}
            </h4>

            <p style="
                color: #64748B;
                font-size: 12px;
                margin: 0 0 8px 0;
            ">
                {service['description']}
            </p>

            <p style="
                color: #2376C9;
                font-size: 12px;
                font-weight: 600;
                margin: 0;
            ">
                {service['location']}
            </p>
        </div>
        """)

        if st.button(
            f"Ask about {service['name']}",
            key=f"visual_service_{index}",
            use_container_width=True
        ):

            st.session_state.pending_question = service["question"]
            st.rerun()

# ==========================================
# CHAT HEADER
# ==========================================

st.markdown(
    '<div class="section-title">💬 Chat with MediGuard AI</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns([5, 1])

with col2:

    if st.button(
        "Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = [
            {
                "role": "assistant",
                "content": WELCOME_MESSAGE
            }
        ]

        st.session_state.tts_audio = {}
        st.session_state.pending_question = None
        st.session_state.voice_result = None
        st.session_state.transcribed_question = ""

        st.rerun()


# ==========================================
# SUGGESTED QUESTIONS
# ==========================================

st.caption("Try asking:")

suggestions = [
    "What are OPD timings?",
    "How can I book an appointment?",
    "Where is the cardiology department?"
]

suggestion_cols = st.columns(3)

for index, question in enumerate(suggestions):

    with suggestion_cols[index]:

        if st.button(
            question,
            key=f"suggestion_{index}",
            use_container_width=True
        ):

            st.session_state.pending_question = question


# ==========================================
# DISPLAY CHAT HISTORY WITH TTS
# ==========================================

chat_container = st.container()

with chat_container:

    for i, message in enumerate(st.session_state.messages):

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

            # Text-to-Speech for assistant responses
            if message["role"] == "assistant":

                if st.button(
                    "🔊 Listen to response",
                    key=f"listen_{i}"
                ):

                    try:

                        with st.spinner("Generating speech..."):

                            audio_bytes = generate_speech(
                                message["content"]
                            )

                        if audio_bytes:

                            st.session_state.tts_audio[i] = audio_bytes

                    except Exception as error:

                        st.error(
                            f"Speech generation failed: {error}"
                        )

                # Display generated audio
                if i in st.session_state.tts_audio:

                    st.audio(
                        st.session_state.tts_audio[i],
                        format="audio/mp3"
                    )


# ==========================================
# VOICE INPUT SECTION
# ==========================================

st.markdown("---")

st.markdown("### 🎙️ Ask using your voice")

st.caption(
    "Record your question or upload an audio file. "
    "MediGuard AI will convert your speech into text."
)

voice_col1, voice_col2 = st.columns(2)


# Record audio

with voice_col1:

    recorded_audio = st.audio_input(
        "Record your question",
        key="voice_recording"
    )


# Upload audio

with voice_col2:

    uploaded_audio = st.file_uploader(
        "Or upload an audio file",
        type=["wav", "mp3", "m4a", "webm", "ogg", "flac"],
        key="voice_upload"
    )


# Select audio source

audio_file = (
    recorded_audio
    if recorded_audio is not None
    else uploaded_audio
)


if audio_file is not None:

    st.audio(audio_file)

    if st.button(
        "Convert Speech to Text",
        key="convert_voice"
    ):

        try:

            with st.spinner(
                "Listening and converting your speech..."
            ):

                result = transcribe_audio(audio_file)

                st.session_state.voice_result = result

                st.session_state.transcribed_question = result["text"]

        except Exception as error:

            st.error(
                f"Audio transcription failed: {error}"
            )


# ==========================================
# TRANSCRIPTION PREVIEW
# ==========================================

if st.session_state.voice_result:

    result = st.session_state.voice_result

    st.success("Speech converted successfully!")

    st.markdown(
        "**Detected language:** " + result["language"]
    )

    st.text_area(
        "Your transcribed question",
        value=result["text"],
        height=100,
        disabled=True,
        key="transcription_preview"
    )

    if st.button(
        "Send Transcription to Chat",
        key="send_voice_question"
    ):

        st.session_state.pending_question = result["text"]

        st.session_state.voice_result = None

        st.session_state.transcribed_question = ""

        st.rerun()


# ==========================================
# PROCESS USER INPUT
# ==========================================

user_input = st.chat_input(
    "Ask anything about hospital services..."
)


# Handle suggested questions and voice input

if st.session_state.pending_question:

    user_input = st.session_state.pending_question

    st.session_state.pending_question = None


if user_input:

    user_input = user_input.strip()

    if not user_input:

        st.warning("Please enter a question.")

    elif len(user_input) > 2000:

        st.warning(
            "Please keep your question below 2000 characters."
        )

    else:

        # ----------------------------------
        # STEP 1: PII DETECTION AND REDACTION
        # ----------------------------------

        pii_result = redact_pii(user_input)

        safe_user_input = pii_result["redacted_text"]

        if pii_result["pii_detected"]:

            st.info(
                "🔒 Personal information detected and redacted "
                "for privacy."
            )

        # ----------------------------------
        # STEP 2: STORE SANITIZED USER INPUT
        # ----------------------------------

        st.session_state.messages.append({
            "role": "user",
            "content": safe_user_input
        })

        # ----------------------------------
        # STEP 3: PREPARE CHAT HISTORY
        # ----------------------------------

        history = st.session_state.messages[:-1]

        # ----------------------------------
        # STEP 4: GENERATE AI RESPONSE
        # ----------------------------------

        try:

            with st.spinner("MediGuard AI is thinking..."):

                answer = generate_response(
                    user_question=user_input,
                    chat_history=history
                )

            # ----------------------------------
            # STEP 5: STORE ASSISTANT RESPONSE
            # ----------------------------------

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as error:

            print("APPLICATION ERROR:", repr(error))

            error_message = (
                "I'm sorry, I couldn't generate a response.\n\n"
                "Please check the application configuration "
                "and try again."
            )

            st.session_state.messages.append({
                "role": "assistant",
                "content": error_message
            })

        # ----------------------------------
        # STEP 6: REFRESH APPLICATION
        # ----------------------------------

        st.rerun()


# ==========================================
# DISCLAIMER
# ==========================================
# ==========================================
# DISCLAIMER
# ==========================================

st.html("""
<div class="footer">

    <p>MediGuard AI | AI-Powered Hospital Information Assistant</p>

    <p>
        This application provides general hospital information only.
        <br>
        It does not provide medical diagnosis or treatment.
        <br>
        For emergencies, seek immediate medical attention.
    </p>

</div>
""")
