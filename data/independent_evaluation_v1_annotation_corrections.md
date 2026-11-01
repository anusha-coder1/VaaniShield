# Independent Evaluation v1 — Annotation Correction Log

Date: 2026-11-01

## Reason
A review of the initial English annotations identified several labels that
did not strictly follow the VaaniShield detection rulebook.

Only expected labels were corrected. Transcripts and detector code were not
changed.

## Corrections
- EN-I-001: Removed secrecy; the transcript supports isolation instead.
- EN-I-002: Removed payment_pressure; the payment request is not explicitly
  connected to a payment-related threat.
- EN-I-003: Removed payment_pressure and secrecy; the transcript supports
  isolation, not a separate secrecy instruction.
- EN-I-004: Removed urgency and payment_pressure; the warrant threat is
  connected to ending the call, not explicitly to payment.
- EN-I-006: Removed payment_demand; retained credential_harvesting and
  added authority_based_coercion because the authority claim accompanies
  credential harvesting.
- EN-I-007: Removed accusation; added authority_based_coercion because
  the authority claim accompanies credential harvesting.
- EN-I-008: Removed payment_demand; added authority_based_coercion because
  the authority claim accompanies credential harvesting.
- EN-I-009: Removed accusation. Remote phone access is not currently
  represented by a dedicated indicator in the taxonomy. The scam label
  is retained as a documented taxonomy gap.
- EN-I-010: Removed payment_pressure; the requested transfer is a
  payment_demand without an explicit payment-related threat.

## Important evaluation notes
- The initial evaluation metrics were calculated before these corrections.
- Recalculate metrics using the revised labels.
- EN-I-019 remains a genuine educational sample. Its detected
  payment_demand is an indicator-level false positive.
- No detector rules were modified during this annotation review.
- This is an annotation audit, not independent human or native-speaker
  validation.
