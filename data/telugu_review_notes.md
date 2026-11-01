# VaaniShield — Telugu Review Notes

**Review status:** AI-generated preliminary review. Native-speaker verification pending.

## 1. TE-DA-001 — Digital-arrest scam

- Expected classification: Scam
- Preliminary assessment: Plausible.
- Stages: authority_claim, accusation, isolation, payment_demand.
- Tactics: urgency, authority_impersonation, payment_pressure, secrecy.
- Observation: The shift from "we are speaking" to "they say" needs native-speaker review.
- Rulebook note: An authority claim alone does not establish impersonation.

## 2. TE-FF-001 — Financial fraud

- Expected classification: Scam
- Preliminary assessment: Plausible.
- Stages: accusation, payment_demand.
- Tactics: urgency, credential_harvesting, payment_pressure.
- Observation: Verify the naturalness of the payment and OTP request.
- Rulebook note: The account-suspension consequence provides pressure context.

## 3. TE-GB-001 — Genuine banking interaction

- Expected classification: Genuine
- Preliminary assessment: Plausible.
- Stages: None.
- Tactics: None.
- Observation: Verify whether the Telugu term used for bank support is natural.
- Rulebook note: A protective OTP reminder must not trigger credential_harvesting.

## 4. TE-PV-001 — Genuine passport verification

- Expected classification: Genuine
- Preliminary assessment: Plausible.
- Stages: None.
- Tactics: None.
- Observation: Verify honorific agreement and procedural wording.
- Rulebook note: A scheduled police verification is not automatically suspicious.

## 5. TE-OTP-001 — Protective security warning

- Expected classification: Genuine
- Preliminary assessment: Plausible.
- Stages: None.
- Tactics: None.
- Observation: Native-speaker review should verify register and naturalness.
- Rulebook note: Warning against credential disclosure is not credential harvesting.

## 6. TE-EDU-001 — Educational scam discussion

- Expected classification: Genuine
- Preliminary assessment: Plausible.
- Stages: None.
- Tactics: None.
- Observation: Verify the naturalness of the phrase used for digital-arrest scams.
- Rulebook note: Discussing a scam in an educational context is not automatically a scam.

## Overall findings

- 2 scam samples and 4 genuine samples reviewed.
- All six expected classifications appear logically plausible based on the supplied text and preliminary translations.
- Original dataset labels remain unchanged.
- No detection rules have been modified.
- Telugu wording, translations, and labels still require native-speaker verification.

**Next action:** Use these observations to guide native-speaker review before adding Telugu detection patterns.