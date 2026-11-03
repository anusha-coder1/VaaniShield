# VaaniShield — Phase 4 Evaluation Summary

## 1. Evaluation scope

- Dataset: `independent_evaluation_v1_ai_reviewed.json`
- Dataset version: 1.1-ai-reviewed
- Total samples: 120 (60 synthetic scam, 60 synthetic genuine)
- Languages: English, Hindi, Telugu, Tamil, Malayalam and Indian code-mixed speech
- Review method: AI-assisted annotation review
- Native-speaker validation: Not performed
- Samples requiring native-speaker review: 100

> **Important limitation:** These results are from a synthetic dataset. They are not evidence of real-world accuracy or independently validated multilingual performance. The AI-reviewed annotations and mismatch reports must be treated as preliminary.

## 2. Overall scam classification

| Metric | Result |
|---|---:|
| Total samples | 120 |
| True positives | 60 |
| True negatives | 60 |
| False positives | 0 |
| False negatives | 0 |
| Accuracy | 100.00% |
| Precision | 100.00% |
| Recall | 100.00% |
| F1 score | 100.00% |

The detector classified all 120 samples correctly at the overall scam-versus-genuine level in this synthetic evaluation.

## 3. Language-wise performance

| Language | Samples | Accuracy | Precision | Recall | F1 score | Native-speaker review required |
|---|---:|---:|---:|---:|---:|---:|
| English | 20 | 100.00% | 100.00% | 100.00% | 100.00% | 0 |
| Hindi | 20 | 100.00% | 100.00% | 100.00% | 100.00% | 20 |
| Indian code-mixed speech | 20 | 100.00% | 100.00% | 100.00% | 100.00% | 20 |
| Malayalam | 20 | 100.00% | 100.00% | 100.00% | 100.00% | 20 |
| Tamil | 20 | 100.00% | 100.00% | 100.00% | 100.00% | 20 |
| Telugu | 20 | 100.00% | 100.00% | 100.00% | 100.00% | 20 |

All language groups achieved 100% on this synthetic dataset. Non-English and code-mixed results remain preliminary because native-speaker validation was not performed.

## 4. Stage-wise performance

| Stage | Support | Precision | Recall | F1 score |
|---|---:|---:|---:|---:|
| authority_claim | 60 | 100.00% | 90.00% | 94.74% |
| accusation | 34 | 100.00% | 97.06% | 98.51% |
| isolation | 21 | 90.48% | 90.48% | 90.48% |
| payment_demand | 32 | 96.88% | 96.88% | 96.88% |

## 5. Tactic-wise performance

| Tactic | Support | Precision | Recall | F1 score |
|---|---:|---:|---:|---:|
| urgency | 24 | 84.62% | 91.67% | 88.00% |
| authority_based_coercion | 41 | 77.78% | 85.37% | 81.40% |
| credential_harvesting | 18 | 100.00% | 94.44% | 97.14% |
| payment_pressure | 16 | 100.00% | 100.00% | 100.00% |
| secrecy | 19 | 100.00% | 84.21% | 91.43% |
| remote_access_control | No positive examples | 0.00% | 0.00% | 0.00% |

**Interpretation:** Payment pressure achieved 100% F1 on 16 positive examples. Credential harvesting achieved 97.14%, secrecy 91.43%, urgency 88.00%, and authority-based coercion 81.40%. Remote-access control had no positive examples in this dataset, so its performance cannot be meaningfully assessed.

## 6. Baseline comparison

| Metric | Original baseline | Current AI-reviewed evaluation |
|---|---:|---:|
| True positives | 1 | 60 |
| True negatives | 60 | 60 |
| False positives | 0 | 0 |
| False negatives | 59 | 0 |
| Accuracy | 50.83% | 100.00% |
| Precision | 100.00% | 100.00% |
| Recall | 1.67% | 100.00% |
| F1 score | 3.28% | 100.00% |

The baseline and current results use the same synthetic sample collection, with the current version incorporating detector refinements and six AI-assisted payment-pressure annotation corrections. This is a development comparison, not an untouched independent holdout result.

## 7. Annotation adjudication reports

- [Authority-based coercion mismatch report](../data/authority_adjudication_report_v1.json): 16 proposed annotation corrections (10 positive, 6 negative).
- [Urgency mismatch report](../data/urgency_adjudication_report_v1.json): 6 proposed annotation corrections (4 positive, 2 negative).

Both reports are preliminary AI-assisted reviews. Their proposed corrections are pending independent review and have not been applied to the evaluation dataset.

## 8. Evaluation limitations and next steps

1. Obtain independent native-speaker review for the 100 flagged samples before making multilingual performance claims.
2. Review the 22 proposed authority and urgency annotation corrections independently.
3. Add positive remote-access-control samples so that this tactic can be evaluated.
4. Evaluate on a genuinely untouched dataset that was not used to inspect mismatches or refine detection rules.
5. Test with realistic, naturally occurring transcripts before making real-world performance claims.

---

*Generated from the VaaniShield Phase 4 synthetic evaluation. Results describe this dataset only.*
