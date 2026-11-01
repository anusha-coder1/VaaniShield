# VaaniShield — Detection Rulebook v1.1

## 1. Purpose

This document defines the rules used to identify potential digital-arrest scams in conversations. It establishes consistent definitions for scam stages, tactics, evidence requirements, and safeguards against false positives.

The system identifies suspicious conversational patterns. It does not independently verify a caller's identity or establish that a crime has occurred.

## 2. Scam Stages

A conversation may contain one or more of these stages.

### `authority_claim`

The caller claims to represent an official or trusted institution, such as:
- Police
- CBI
- Cybercrime department
- Bank
- Government department

**Evidence:** An explicit claim of institutional representation.

### `accusation`

The caller alleges that the recipient is involved in a crime, illegal transaction, or suspicious activity.

**Evidence:** A direct allegation, such as claiming the recipient's identity or account is linked to a criminal investigation.

### `isolation`

The caller attempts to prevent the recipient from seeking outside help.

**Evidence:** Instructions not to disconnect the call, contact family, consult others, or seek independent assistance.

### `payment_demand`

The caller explicitly requests or instructs the recipient to provide money, transfer funds, or make a payment.

**Evidence:** An explicit request or instruction to transfer or provide money.

A threat is not required for this indicator. The presence of a payment demand alone does not establish that the demand is fraudulent.

## 3. Scam Tactics

### `urgency`

The caller pressures the recipient to act immediately or within a short deadline.

**Evidence:** Explicit time pressure, such as demands to act immediately or before a stated deadline.

### `authority_based_coercion`

The caller uses a claimed official or trusted authority together with coercive behaviour to pressure the recipient.

**Detection requirement:** Both of the following must be present:
1. An explicit `authority_claim`.
2. At least one independently supported coercive tactic:
   - `isolation`
   - `secrecy`
   - `credential_harvesting`
   - `payment_pressure`

**Important:**
- An authority claim alone is insufficient.
- An accusation alone is insufficient.
- Urgency alone is insufficient.
- A payment demand without coercive pressure is insufficient.
- This indicator describes a detected conversational pattern; it does not prove the caller's real identity or legal impersonation.

### `credential_harvesting`

The caller requests confidential credentials or authentication information, such as:
- OTP
- PIN
- Password
- CVV
- Banking credentials

**Evidence:** An explicit request to disclose or share confidential information.

Merely mentioning credentials does not qualify.

### `payment_pressure`

The caller uses threats, threatened consequences, intimidation, or coercion to force the recipient to make a payment.

**Evidence:** An explicit connection between payment and a threatened or coercive consequence.

A payment request without coercive pressure is not sufficient.

### `secrecy`

The caller explicitly instructs the recipient to keep the matter confidential or not tell others.

**Evidence:** A direct instruction to keep the conversation, investigation, or matter secret.

## 4. Evidence Requirements

1. Every detected stage and tactic must have supporting text from the conversation.
2. Every indicator must include a simple explanation of why the evidence matches it.
3. Do not invent evidence or infer an indicator from unrelated phrases.
4. Remove redundant overlapping evidence where appropriate.
5. If evidence is insufficient, do not mark the indicator as detected.
6. `authority_based_coercion` must have evidence supporting both the authority claim and at least one qualifying coercive tactic.

## 5. False-Positive Safeguards

1. Merely mentioning an OTP must not automatically trigger credential harvesting.
2. Warning someone not to share an OTP is not credential harvesting.
3. Educational discussions about scams must not automatically be classified as scams.
4. Merely mentioning police, banks, or government departments must not automatically indicate impersonation or coercion.
5. A genuine scheduled police verification appointment must not be flagged solely because police are mentioned.
6. A single suspicious keyword must not determine the overall verdict.
7. Missing evidence does not prove that a conversation is safe.
8. A payment request alone must not automatically establish payment pressure.
9. An authority claim alone must not automatically establish authority-based coercion.
10. A protective instruction must not be interpreted as a scam tactic merely because it mentions a sensitive topic.

## 6. Important Distinctions

- `authority_claim` identifies an explicit claim of institutional representation.
- `authority_based_coercion` identifies the use of claimed authority alongside independently detected coercive behaviour. It does not prove real-world impersonation.
- A caller may claim to be an official without enough evidence to establish coercion.
- `payment_demand` describes the explicit request for money; `payment_pressure` describes the coercion used to force payment.
- A conversation may contain both `payment_demand` and `payment_pressure`.
- `credential_harvesting` requires a request for confidential information, not merely a mention of it.
- `isolation` requires an attempt to restrict outside contact or assistance.
- `secrecy` requires an explicit instruction to keep the matter confidential.
- `urgency` describes time pressure and does not independently establish fraud.

## 7. Implementation and Evaluation Order

1. Preserve the current evaluation dataset as the baseline.
2. Review non-English samples with native speakers before treating their wording and labels as verified.
3. Add language-specific detection patterns using reviewed examples.
4. Preserve safeguards for genuine banking, police, and educational conversations.
5. Run the complete evaluation suite after each meaningful detection change.
6. Compare recall, precision, false positives, and false negatives against the baseline.
7. Expand the dataset with reviewed samples across all supported languages.
8. Keep the original dataset unchanged and use a separate version for revised labels or rules.
9. Record changes to detection definitions and dataset labels so evaluation results remain reproducible.

## 8. Preliminary Telugu-Script Examples

The following Telugu-script patterns are preliminary AI-reviewed examples from the synthetic evaluation set. Native-speaker verification remains pending; they are not language-validated production rules.

- Authority claim: `సైబర్ క్రైమ్ విభాగం నుండి మాట్లాడుతున్నాం`
- Accusation: `ఆధార్ నంబర్ క్రిమినల్ దర్యాప్తుతో సంబంధం`
- Isolation: `కాల్ కట్ చేయకండి`; `కుటుంబానికి చెప్పకండి`
- Payment demand: `డబ్బు బదిలీ చేయండి`
- Urgency: `వెంటనే`; `ఇప్పుడే`
- Credential request: `మీ OTP చెప్పండి`
- Payment-pressure context: `ఖాతా నిలిపివేయకుండా ఉండాలంటే`
- TE-DA-001 secrecy: `కుటుంబానికి చెప్పకండి`
- TE-DA-001 payment pressure: `అరెస్టు తప్పించుకోవడానికి వెంటనే డబ్బు బదిలీ చేయండి`

The authority-claim phrase can support `authority_claim`, but cannot by itself support `authority_based_coercion`.

The account-suspension phrase can support `payment_pressure` only when the surrounding conversation establishes that the consequence is being used to force payment. It does not itself establish a `payment_demand`.

Protective OTP warnings and explicitly educational Telugu content remain excluded.

All examples remain preliminary until reviewed by native speakers.

## 9. Limitations

- Rule-based detection may miss unfamiliar wording, regional expressions, transliteration, and code-mixed conversations.
- Heuristic confidence is not a calibrated probability.
- Evaluation on synthetic data does not establish real-world detection accuracy.
- The system cannot independently verify a caller's identity or establish legal impersonation.
- The system should communicate uncertainty and encourage independent verification rather than making definitive legal or identity claims.