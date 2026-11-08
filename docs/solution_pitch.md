# VaaniShield — Multilingual AI Scam Detection

**Solution pitch | Gnani AI Competition**

## The Problem
Voice scams exploit trust, urgency, and language barriers. Fraudsters impersonate banks and other authorities to request OTPs, sensitive information, or payments. Suspicious conversations in Indian languages and code-mixed speech can be difficult to assess quickly.

## Our Solution
VaaniShield is a working multilingual scam-awareness prototype that converts short audio recordings into text, identifies suspicious conversational tactics, and provides an explainable risk assessment. Users can also analyze typed transcripts.

## How It Works
1. **Transcribe:** Gnani AI Prisma v3 converts uploaded speech into text using automatic Indic-language recognition and code-mixed transcription.
2. **Protect:** Sensitive information is redacted before optional external AI comparison.
3. **Detect:** A custom multilingual rule engine identifies indicators such as authority impersonation, urgency, credential harvesting, and payment pressure.
4. **Explain:** The application presents a scam verdict, risk level, detected tactics, and supporting transcript evidence.
5. **Compare:** Optional Gemini analysis provides an independent contextual assessment, with rule-based fallback if the AI service fails.

## Technology
**Frontend:** Next.js, React, TypeScript. **Backend:** Python, FastAPI. **Speech AI:** Gnani Prisma v3 via gnani-vachana. **Detection:** Explainable multilingual Python rules. **Optional AI:** Gemini REST API.

## Working Prototype and Validation
- Live Gnani transcription successfully tested with synthetic English, Hindi, and Telugu audio.
- English and Hindi browser-based audio-to-analysis workflows verified; Telugu transcription verified directly.
- **240 automated tests passed**, FastAPI endpoints verified, and Next.js production build passed.
- A six-group, 120-example synthetic development evaluation classified all 120 examples correctly after rule tuning. This is not independent real-world accuracy.
- On a separate 12-case synthetic English challenge, rules classified 9/12 correctly; Gemini classified 12/12 after retries. These are exploratory results, not production performance claims.

## Impact and Next Steps
VaaniShield aims to make scam warning signs understandable across Indian languages. Next steps include native-speaker validation, testing with consented real-world audio, improved code-mixed recognition, and broader robustness evaluation.

**Project:** https://github.com/anusha-coder1/VaaniShield
