# Industry Case Study: MediGuard AI – Guardrailed Hospital FAQ Assistant

## 1. Industry Background

Healthcare organizations receive a large number of routine questions from patients and visitors about OPD timings, hospital departments, appointments, pharmacy hours, billing, laboratory services, and other facilities.

Handling these repetitive enquiries manually can increase the workload on reception staff and lead to delays in providing basic information.

MediGuard AI is a guardrailed AI-powered hospital information assistant designed to help address this challenge.

## 2. Problem Statement

Patients and visitors often need quick access to basic hospital information. However, a general-purpose AI chatbot may generate inaccurate information, provide inappropriate medical suggestions, or expose sensitive personal information.

A hospital assistant therefore needs controlled responses, privacy protection, content filtering, and clear escalation to human professionals.

## 3. Proposed Solution

MediGuard AI uses the Gemini API with few-shot prompting and multiple safety layers to answer approved hospital-related questions.

The assistant supports:
- Hospital FAQ responses.
- Department and facility information.
- OPD, pharmacy, and laboratory timings.
- Appointment and billing enquiries.
- Voice-based question input.
- Text-to-speech responses.
- PII detection and redaction.
- Toxicity filtering.
- Audit logging and administrator monitoring.

## 4. Guardrail Architecture

| Layer | Implementation | Purpose |
|---|---|---|
| U1 – Prompt Guardrails | System and refusal prompts | Restricts responses to hospital information |
| U2 – Few-shot Prompting | Gemini API with examples | Demonstrates correct answers and refusals |
| U3 – Input Safety | Presidio, Toxic-BERT, Faster-Whisper | Redacts PII, filters abusive input, supports voice |
| U4 – Output Accessibility | Edge TTS and hospital guide visuals | Improves accessibility and usability |
| U5 – Monitoring | SQLite audit logs and admin dashboard | Records safety events and supports monitoring |

## 5. Example Industry Scenarios

**Scenario 1: Routine hospital enquiry**

A visitor asks: "What are the OPD timings?"

Expected behaviour: MediGuard AI provides the configured OPD timings: 9:00 AM to 5:00 PM, Monday to Saturday.

**Scenario 2: Medical advice request**

A patient asks: "Can you prescribe antibiotics?"

Expected behaviour: The assistant refuses to prescribe medication and directs the user to a qualified healthcare professional.

**Scenario 3: Emergency situation**

A visitor asks: "My father is having severe chest pain. What should I do?"

Expected behaviour: The assistant provides an emergency warning and directs the person to seek immediate emergency medical assistance. It does not attempt to diagnose the condition.

**Scenario 4: Personal information**

A visitor asks: "My email is rahul@gmail.com. What are OPD timings?"

Expected behaviour: Presidio detects and redacts the email address before the message is passed to the AI response pipeline and recorded in the audit log.

**Scenario 5: Abusive input**

A user sends insulting or threatening language.

Expected behaviour: The toxicity classifier evaluates the input and blocks messages that exceed the configured toxicity threshold.

**Scenario 6: Unknown hospital information**

A visitor asks: "What is the salary of a cardiologist?"

Expected behaviour: The assistant does not invent an answer and responds that the information is unavailable.

## 6. Monitoring and Accountability

The SQLite audit system records important application events, including:
- Successful chatbot responses.
- Medical-advice and emergency blocks.
- Toxicity blocks.
- Local FAQ fallbacks.
- Unknown-information responses.
- API errors.

The administrator dashboard provides event counts, category breakdowns, filters, and CSV export for reviewing system activity.

Audit records should contain redacted information and be accessible only to authorized administrators.

## 7. Benefits to the Healthcare Industry

- Reduces repetitive information enquiries handled by reception staff.
- Makes basic hospital information easier to access.
- Provides consistent responses based on configured hospital FAQs.
- Adds privacy and content-safety checks.
- Supports voice interaction and audio responses.
- Provides an audit trail for reviewing application behaviour.

These are intended benefits; they have not yet been established through a real hospital deployment.

## 8. Limitations and Future Scope

**Current limitations**
- The assistant is a prototype using fictional hospital FAQ data.
- Keyword-based medical guardrails may miss some unsafe requests.
- Toxicity detection can produce false positives and false negatives.
- PII detection may not identify every sensitive entity.
- The assistant is not a substitute for doctors, nurses, or emergency services.
- The audit dashboard and local SQLite database require stronger infrastructure before production use.

**Future improvements**
- Integrate verified hospital databases and appointment systems.
- Add role-based authentication for hospital staff.
- Use secure, persistent audit storage.
- Conduct clinical and security testing before real-world deployment.
- Expand multilingual voice support.
- Add human escalation and emergency contact workflows.

## 9. Conclusion

MediGuard AI demonstrates how generative AI can be applied to routine hospital information enquiries while incorporating prompt restrictions, few-shot examples, PII redaction, toxicity detection, voice interaction, text-to-speech, and audit monitoring.

The project illustrates the importance of combining AI capabilities with safety controls, privacy protection, and human oversight in a sensitive industry such as healthcare.