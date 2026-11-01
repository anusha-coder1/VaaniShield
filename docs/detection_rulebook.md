# VaaniShield — Detection Rulebook v1.0

## 1. Purpose

This document defines the rules used to identify potential digital-arrest scams in conversations. It establishes consistent definitions for scam stages, tactics, evidence requirements, and safeguards against false positives.

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

**Evidence:** A direct allegation, such as claiming the recipient's identity is linked to a criminal investigation.

### `isolation`
The caller attempts to prevent the recipient from seeking outside help.

**Evidence:** Instructions not to disconnect the call, contact family, or speak to others.

### `payment_demand`
The caller demands money, a transfer, a fee, or another payment to avoid a threatened consequence.

**Evidence:** An explicit demand for payment connected to a threat or promised resolution.

## 3. Scam Tactics

### `urgency`
The caller pressures the recipient to act immediately or within a short deadline.

### `authority_impersonation`
The caller presents themselves as an official or trusted authority in a deceptive or suspicious context.

**Important:** An authority claim alone does not prove impersonation.

### `credential_harvesting`
The caller requests confidential credentials, such as:
- OTP
- PIN
- Password
- CVV
- Banking credentials

### `payment_pressure`
The caller uses threats, consequences, or intimidation to force payment.

### `secrecy`
The caller explicitly instructs the recipient to keep the matter confidential or not tell others.

## 4. Evidence Requirements

1. Every detected stage and tactic must have supporting text from the conversation.
2. Every indicator must include a simple explanation of why the evidence matches it.
3. Do not invent evidence or infer an indicator from unrelated phrases.
4. Remove redundant overlapping evidence where appropriate.
5. If evidence is insufficient, do not mark the indicator as detected.

## 5. False-Positive Safeguards

1. Merely mentioning an OTP must not automatically trigger credential harvesting.
2. Warning someone not to share an OTP is not credential harvesting.
3. Educational discussions about scams must not automatically be classified as scams.
4. Merely mentioning police, banks, or government departments must not automatically indicate impersonation.
5. A genuine scheduled police verification appointment must not be flagged solely because police are mentioned.
6. A single suspicious keyword must not determine the overall verdict.
7. Missing evidence does not prove that a conversation is safe.

## 6. Important Distinctions

- `authority_claim` and `authority_impersonation` are different indicators.
- A caller may claim to be an official without enough evidence to establish deception.
- `payment_demand` describes the demand itself; `payment_pressure` describes the coercion used to force payment.
- `credential_harvesting` requires a request for confidential information, not merely a mention of it.
- `isolation` requires an attempt to restrict outside contact or assistance.

## 7. Implementation and Evaluation Order

1. Preserve the current evaluation dataset as the baseline.
2. Review non-English samples with native speakers before treating their wording and labels as verified.
3. Add language-specific detection patterns using reviewed examples.
4. Preserve safeguards for genuine banking, police, and educational conversations.
5. Run the complete evaluation suite after each meaningful detection change.
6. Compare recall, precision, false positives, and false negatives against the baseline.
7. Expand the dataset with reviewed samples across all supported languages.

## 8. Preliminary Telugu-Script Examples

The following Telugu-script patterns are preliminary AI-reviewed examples from
the synthetic evaluation set. Native-speaker verification remains pending; they
are not language-validated production rules.

- Authority claim: `సైబర్ క్రైమ్ విభాగం నుండి మాట్లాడుతున్నాం`
- Accusation: `ఆధార్ నంబర్ క్రిమినల్ దర్యాప్తుతో సంబంధం`
- Isolation: `కాల్ కట్ చేయకండి`; `కుటుంబానికి చెప్పకండి`
- Payment demand: `డబ్బు బదిలీ చేయండి`
- Urgency: `వెంటనే`; `ఇప్పుడే`
- Credential request: `మీ OTP చెప్పండి`
- Payment-pressure context: `ఖాతా నిలిపివేయకుండా ఉండాలంటే`
- TE-DA-001 secrecy: `కుటుంబానికి చెప్పకండి`
- TE-DA-001 payment pressure: `అరెస్టు తప్పించుకోవడానికి వెంటనే డబ్బు బదిలీ చేయండి`

The authority-claim phrase can support `authority_claim`, but cannot by itself
support `authority_impersonation`. The account-suspension phrase can support
`payment_pressure`, but does not itself create a `payment_demand`. Protective
OTP warnings and explicitly educational Telugu content remain excluded.

## 9. Limitations

- Rule-based detection may miss unfamiliar wording, regional expressions, transliteration, and code-mixed conversations.
- Heuristic confidence is not a calibrated probability.
- Evaluation on synthetic data does not establish real-world detection accuracy.
- The system should communicate uncertainty and encourage independent verification rather than making definitive legal or identity claims.
