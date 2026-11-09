# 🏥 MediGuard AI – Guardrailed Hospital Information Assistant

An AI-powered hospital information assistant built using Python, Streamlit, and Google Gemini, featuring multiple safety layers to provide controlled, privacy-aware hospital information.

MediGuard AI demonstrates how Generative AI can be integrated into a healthcare information system with guardrails, PII protection, toxicity detection, voice interaction, and audit monitoring.

---

## 🌟 Features

### 🤖 AI-Powered Hospital Assistant
- Gemini API integration.
- Hospital FAQ-based question answering.
- Few-shot prompting for controlled responses.
- Local FAQ fallback when Gemini is unavailable.
- Conversation history.

### 🛡️ AI Safety and Guardrails
- System prompts and refusal instructions.
- Medical advice and prescription request blocking.
- Emergency-related query detection.
- Toxicity detection using Toxic-BERT.
- Unknown and out-of-scope information handling.

### 🔐 Privacy Protection
- Personally Identifiable Information (PII) detection using Microsoft Presidio.
- Automatic redaction of detected email addresses, phone numbers, names, and other supported entities before AI processing.
- Redacted user messages in audit records.

### 🎙️ Voice and Accessibility
- Voice input using Faster-Whisper.
- Speech-to-text transcription.
- Text-to-speech responses using Edge TTS.
- Quick-access hospital information cards.

### 📊 Audit and Monitoring
- SQLite-based audit logging.
- Event and safety-category tracking.
- Administrator audit dashboard.
- Event filtering and CSV report export.

---

## 🏗️ System Architecture

MediGuard AI follows a five-layer guardrailed architecture.

| Layer | Implementation |
|---|---|
| U1 – System and Refusal Prompts | System instructions and refusal prompts |
| U2 – LLM Tuning | Gemini API and few-shot prompting |
| U3 – Input Safety | Presidio, Toxic-BERT, Faster-Whisper |
| U4 – Output Accessibility | Edge TTS and hospital information visuals |
| U5 – Monitoring | SQLite audit logs and admin dashboard |

### Processing Workflow

1. User submits a text or voice query.
2. Voice queries are transcribed using Faster-Whisper.
3. Presidio detects and redacts supported PII entities.
4. Medical and emergency guardrails evaluate the input.
5. Toxic-BERT evaluates potentially abusive content.
6. Approved queries are processed using Gemini and the hospital FAQ knowledge base.
7. Local FAQ information provides a fallback when Gemini is temporarily unavailable.
8. The response is displayed and can be converted into speech.
9. Relevant application events are recorded in the audit database.

---

## 🧰 Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| Generative AI | Google Gemini API |
| Prompt Engineering | System Prompts, Few-shot Prompting |
| PII Protection | Microsoft Presidio, spaCy |
| Toxicity Detection | Hugging Face Transformers, Toxic-BERT |
| Speech Recognition | Faster-Whisper |
| Text-to-Speech | Edge TTS |
| Database | SQLite |
| Data Storage | JSON |
| Libraries | PyTorch, Pandas |

---

## 📁 Project Structure

```text
MediGuard-AI/
│
├── app.py
├── audit_dashboard.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   └── prompts.py
│
├── data/
│   └── hospital_faq.json
│
├── services/
│   ├── __init__.py
│   ├── faq_service.py
│   ├── gemini_service.py
│   ├── guardrail_service.py
│   ├── pii_service.py
│   ├── toxicity_service.py
│   ├── voice_service.py
│   ├── tts_service.py
│   └── audit_service.py
│
├── tests/
│   ├── test_guardrails.py
│   ├── test_pii.py
│   ├── test_toxicity.py
│   └── test_faq_fallback.py
│
├── docs/
│   └── industry_case_study.md
│
└── .streamlit/
    └── config.toml
```


---

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/MediGuard-AI.git
cd MediGuard-AI
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure API credentials

Create the following file:

`.streamlit/secrets.toml`

Add:

```toml
GEMINI_API_KEY = "your_gemini_api_key"
GEMINI_MODEL = "gemini-3.8-flash"

AUDIT_DASHBOARD_PASSWORD = "your_admin_password"
```

Never upload this file or share your API credentials publicly.

### 6. Run the application

```bash
streamlit run app.py
```

### 7. Run the administrator dashboard

```bash
streamlit run audit_dashboard.py
```

---

## 🧪 Testing and Evaluation

MediGuard AI was evaluated using 15 functional and safety test cases.

| Test Category | Test Cases | Result |
|---|---:|---|
| Hospital FAQ responses | 4 | 4 Passed |
| Medical refusal | 2 | 2 Passed |
| Emergency detection | 2 | 2 Passed |
| Toxicity filtering | 1 | 1 Passed |
| PII redaction | 2 | 2 Passed |
| Unknown/out-of-scope handling | 2 | 2 Passed |
| Prompt injection | 1 | 1 Passed |
| Voice input and TTS | 1 | 1 Passed |
| **Total** | **15** | **15 Passed** |

**Observed prototype test pass rate: 100%.**

The tests were conducted against a fictional hospital FAQ dataset. Some responses were served through the local FAQ fallback when the Gemini API was temporarily unavailable.

---

## 🔮 Future Enhancements

- Integration with real hospital information systems.
- Secure appointment booking and management.
- Persistent cloud-based audit database.
- Multilingual voice interaction.
- Improved PII detection and safety evaluation.
- Secure staff authentication and role-based access.
- Human escalation workflows.

---

## ⚠️ Disclaimer

MediGuard AI is an academic prototype designed to provide general hospital information using a fictional hospital FAQ dataset.

It does not provide medical diagnoses, prescriptions, or treatment recommendations and is not a substitute for qualified healthcare professionals.

Emergency situations require immediate assistance from local emergency services or a hospital emergency department.

The implemented guardrails are prototype safety measures and do not guarantee detection of every unsafe request or protection against every privacy risk.

---

## 👩‍💻 Project Information

**Project Name:** MediGuard AI – Guardrailed Hospital Information Assistant

**Project Domain:** Artificial Intelligence | Generative AI | Healthcare Technology

**Developed Using:** Python, Streamlit, Google Gemini, NLP, and Machine Learning

**Project Type:** Academic Case Study – P60 Guardrailed Industry Assistant

---

⭐ If you find this project interesting, consider giving the repository a star!