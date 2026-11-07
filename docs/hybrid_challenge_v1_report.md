# VaaniShield Hybrid Challenge ? Evaluation Report

## Executive summary

On a frozen challenge set of 12 synthetic English conversations
(6 scam and 6 legitimate), the rule engine correctly classified 9/12
cases, while Gemini correctly classified 12/12 after retries.

Gemini recovered three scam cases missed by the rule engine:
HC-03 (remote access), HC-07 (electricity payment), and
HC-09 (courier credential harvesting).

These results are exploratory and do not establish real-world accuracy.

## Dataset and methodology

- Dataset: `data/hybrid_challenge_v1.json`
- Size: 12 synthetic, AI-authored English conversations
- Labels: 6 scam, 6 legitimate
- Labels have not been independently reviewed.
- The challenge set was frozen before detector evaluation.
- The rule engine and Gemini were evaluated on the same cases.
- Gemini received redacted transcripts.
- Gemini classification results below include a successful retry for HC-09.

## Classification results

| Metric | Rule engine | Gemini after retries |
|---|---:|---:|
| True positives | 3 | 6 |
| True negatives | 6 | 6 |
| False positives | 0 | 0 |
| False negatives | 3 | 0 |
| Accuracy | 75.0% | 100.0% |
| Precision | 100.0% | 100.0% |
| Recall | 50.0% | 100.0% |
| F1 score | 66.7% | 100.0% |

## API reliability

- Gemini completed 11 of 12 distinct cases on the first attempt (91.7%).
- HC-09 initially failed.
- A diagnostic retry with the original 25-second timeout also failed.
- A subsequent retry with a 60-second timeout succeeded.
- Classification accuracy after retries must not be confused with
  first-attempt completion reliability.
- The application retains a rule-based fallback when Gemini is unavailable.

## Structured tactic extraction

Gemini returned an empty tactic list for these correctly classified
scam cases: HC-01, HC-05, and HC-07.

Therefore, correct scam classification does not imply complete tactic
identification. The evidence-validation and tactic-filtering pipeline
may contribute to missing tactic labels; this has not been isolated.

## Limitations

1. Only 12 cases were tested.
2. All cases are synthetic and AI-authored.
3. All cases are in English; multilingual performance was not evaluated here.
4. Labels require independent human review.
5. These examples are not representative of real-world scam prevalence.
6. Gemini required retries for HC-09.
7. Tactic extraction was incomplete on some scam examples.
8. The results should not be presented as production accuracy guarantees.

## Reproducibility

- Frozen dataset: `data/hybrid_challenge_v1.json`
- Recorded results: `data/hybrid_challenge_v1_results.json`
- Rule-based evaluation implementation: `services/evaluation.py`
- Gemini implementation: `services/gemini_analyzer.py`
- The recorded Gemini outputs are observations from API calls, not
  deterministic results guaranteed on future runs.

## Competition takeaway

The hybrid architecture combines deterministic, locally available
rule-based screening with an optional contextual language-model
assessment. In this exploratory challenge, Gemini recognized three
scams missed by the rules while correctly classifying all six
legitimate examples. Reliability, privacy, evidence grounding, and
honest reporting remain important parts of the design.
