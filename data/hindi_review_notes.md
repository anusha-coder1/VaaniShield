# VaaniShield — Hindi Review Notes

**Review status:** AI-generated preliminary review; native-speaker verification is pending. Every translation, interpretation, indicator mapping, ambiguity note, and safeguard assessment below is AI-generated and unverified. This document does not claim native-speaker approval, does not validate the dataset labels, and does not propose or add Hindi detection rules.

The original transcripts are copied verbatim from `evaluation_dataset.json`. Expected labels, stages, and tactics are the existing synthetic-dataset expectations. The distinctions and safeguards follow `docs/detection_rulebook.md`.

## HI-DA-001 — Digital-arrest scam

- **Original Hindi transcript (verbatim):** साइबर अपराध विभाग से कॉल है। आपका आधार नंबर आपराधिक जांच से जुड़ा बताया गया है। कॉल न काटें और परिवार को न बताएं। गिरफ्तारी से बचने के लिए तुरंत पचास हजार रुपये भेजें और इस मामले को गोपनीय रखें।
- **Preliminary English meaning (AI-generated, unverified):** This is a call from the cyber-crime department. Your Aadhaar number is said to be linked to a criminal investigation. Do not disconnect the call or tell your family. To avoid arrest, send fifty thousand rupees immediately and keep this matter confidential.
- **Expected classification (AI-generated, unverified):** Scam (`true`). The dataset frames the combination of an institutional claim, criminal allegation, isolation, and an urgent transfer as a digital-arrest scam.
- **Relevant stages and tactics (AI-generated, unverified):**
  - `authority_claim`: an alleged cyber-crime department presents an institution.
  - `accusation`: the Aadhaar number is said to be connected to a criminal investigation.
  - `isolation`: the recipient is told not to disconnect and not to tell family.
  - `payment_demand`: money is requested to avoid arrest.
  - `urgency`: the transfer is requested immediately.
  - `authority_impersonation`: expected only because the authority claim appears with coercive context; an institutional claim alone is insufficient.
  - `payment_pressure`: the requested payment is tied to avoiding arrest.
  - `secrecy`: the recipient is told not to tell family and to keep the matter confidential.
- **Phrase-to-indicator mapping (AI-generated, unverified; descriptive only, not new rules):** `साइबर अपराध विभाग` → `authority_claim`; `आधार नंबर आपराधिक जांच से जुड़ा` → `accusation`; `कॉल न काटें` and `परिवार को न बताएं` → `isolation`; `पचास हजार रुपये भेजें` → `payment_demand`; `तुरंत` → `urgency`; `गिरफ्तारी से बचने के लिए` with the transfer request → `payment_pressure`; `इस मामले को गोपनीय रखें` → `secrecy`.
- **Possible ambiguity or unnatural wording (AI-generated, unverified):** The opening `कॉल है` and passive construction `जुड़ा बताया गया है` may be less natural than other Hindi scam-call formulations. Confirm the register, the amount expression, and whether the coercive sequence is idiomatic.
- **False-positive safeguards to preserve (AI-generated, unverified):** Do not infer `authority_impersonation` from a cyber-crime or police mention alone. Require the separate coercive context shown here; retain supporting text for each detected indicator.

## HI-FF-001 — Financial fraud scam

- **Original Hindi transcript (verbatim):** आपके बैंक खाते में अवैध लेन-देन होने का आरोप है। खाता बंद होने से बचाने के लिए अभी भुगतान करें और अपना OTP बताएं।
- **Preliminary English meaning (AI-generated, unverified):** Your bank account is accused of having illegal transactions. To prevent the account from being closed, make a payment now and disclose your OTP.
- **Expected classification (AI-generated, unverified):** Scam (`true`). The dataset treats the account allegation, immediate payment request, and OTP request as financial-fraud signals.
- **Relevant stages and tactics (AI-generated, unverified):**
  - `accusation`: alleged illegal transactions are attributed to the bank account.
  - `payment_demand`: payment is requested to avoid account closure.
  - `urgency`: the payment is requested now.
  - `credential_harvesting`: the recipient is asked to disclose an OTP.
  - `payment_pressure`: the threatened account closure supplies pressure for payment.
- **Phrase-to-indicator mapping (AI-generated, unverified; descriptive only, not new rules):** `अवैध लेन-देन होने का आरोप` → `accusation`; `अभी भुगतान करें` → `payment_demand` and `urgency`; `अपना OTP बताएं` → `credential_harvesting`; `खाता बंद होने से बचाने के लिए` with the payment request → `payment_pressure`.
- **Possible ambiguity or unnatural wording (AI-generated, unverified):** `खाते में … होने का आरोप` may be an unusual way to express an allegation against an account. Confirm whether the payment-plus-OTP request and account-closure wording are idiomatic and unambiguous.
- **False-positive safeguards to preserve (AI-generated, unverified):** An OTP mention alone must not indicate credential harvesting; it must be a request for disclosure. Payment pressure must remain distinct from the payment demand itself.

## HI-GB-001 — Genuine banking conversation

- **Original Hindi transcript (verbatim):** मैंने अपने बैंक के आधिकारिक ऐप से सामान्य UPI भुगतान किया। ग्राहक सहायता ने लेन-देन की स्थिति बताई और OTP साझा न करने की सलाह दी।
- **Preliminary English meaning (AI-generated, unverified):** I made a routine UPI payment through my bank’s official app. Customer support gave the transaction status and advised me not to share my OTP.
- **Expected classification (AI-generated, unverified):** Genuine (`false`). The dataset presents a routine official-app banking interaction and a safety reminder, not an unsolicited demand.
- **Relevant stages and tactics (AI-generated, unverified):** None expected. The OTP wording is advice not to disclose a credential, not `credential_harvesting`.
- **Phrase-to-indicator mapping (AI-generated, unverified; descriptive only, not new rules):** No scam-indicator mapping is expected. `OTP साझा न करने की सलाह` is protective context and must not be treated as a credential request.
- **Possible ambiguity or unnatural wording (AI-generated, unverified):** Confirm whether `आधिकारिक ऐप से … भुगतान किया`, `ग्राहक सहायता`, and `लेन-देन की स्थिति बताई` are natural in this banking context.
- **False-positive safeguards to preserve (AI-generated, unverified):** Do not classify a warning not to share an OTP as credential harvesting. A routine UPI transaction and use of an official app must not be treated as scam evidence without separate coercive indicators.

## HI-PV-001 — Legitimate police verification discussion

- **Original Hindi transcript (verbatim):** मैं पासपोर्ट सत्यापन के लिए निर्धारित समय पर पुलिस स्टेशन गया। अधिकारी ने पहचान की जांच की और प्रक्रिया समझाई।
- **Preliminary English meaning (AI-generated, unverified):** I went to the police station at the scheduled time for passport verification. The officer checked my identity and explained the procedure.
- **Expected classification (AI-generated, unverified):** Genuine (`false`). The dataset describes a scheduled, in-person official procedure with no payment or secrecy demand.
- **Relevant stages and tactics (AI-generated, unverified):** None expected. Mentioning police in a scheduled passport-verification setting does not itself establish `authority_claim` or `authority_impersonation` for scam detection.
- **Phrase-to-indicator mapping (AI-generated, unverified; descriptive only, not new rules):** No scam-indicator mapping is expected. `पुलिस स्टेशन` and `पासपोर्ट सत्यापन` are legitimate-context references in this sample.
- **Possible ambiguity or unnatural wording (AI-generated, unverified):** Confirm whether `निर्धारित समय` and the description of the officer’s procedure sound natural in ordinary Hindi.
- **False-positive safeguards to preserve (AI-generated, unverified):** A genuine scheduled police verification appointment must not be flagged merely because police or identity checking are mentioned. Authority impersonation requires suspicious context, not an official-location reference alone.

## HI-OTP-001 — Protective OTP/security warning

- **Original Hindi transcript (verbatim):** बैंक की सुरक्षा सूचना: अपना OTP, PIN या पासवर्ड किसी कॉल करने वाले व्यक्ति को कभी न बताएं।
- **Preliminary English meaning (AI-generated, unverified):** Bank security notice: never tell your OTP, PIN, or password to anyone who calls you.
- **Expected classification (AI-generated, unverified):** Genuine (`false`). The dataset identifies a security warning, not a request for credentials.
- **Relevant stages and tactics (AI-generated, unverified):** None expected. The utterance negates credential disclosure and therefore should not produce `credential_harvesting`.
- **Phrase-to-indicator mapping (AI-generated, unverified; descriptive only, not new rules):** No scam-indicator mapping is expected. `कभी न बताएं` changes the OTP/PIN/password reference into a protective warning.
- **Possible ambiguity or unnatural wording (AI-generated, unverified):** `किसी कॉल करने वाले व्यक्ति` may be less idiomatic than other possible expressions. Confirm the appropriate register for a bank safety message.
- **False-positive safeguards to preserve (AI-generated, unverified):** OTP, PIN, and password mentions must not trigger credential harvesting when local negation tells the recipient not to disclose them.

## HI-EDU-001 — Educational discussion about scams

- **Original Hindi transcript (verbatim):** जागरूकता कक्षा में हमने एक काल्पनिक डिजिटल-अरेस्ट धोखाधड़ी के उदाहरण पर चर्चा की, जिसमें कोई व्यक्ति पुलिस होने का दावा करता है और पैसे मांगता है।
- **Preliminary English meaning (AI-generated, unverified):** In an awareness class, we discussed a hypothetical digital-arrest fraud example in which someone claims to be police and asks for money.
- **Expected classification (AI-generated, unverified):** Genuine (`false`). The dataset identifies educational discussion about a hypothetical scam, rather than a live scam directed at the recipient.
- **Relevant stages and tactics (AI-generated, unverified):** None expected. The text reports an example that includes an apparent authority claim and money request, but does not perform those acts as a current solicitation.
- **Phrase-to-indicator mapping (AI-generated, unverified; descriptive only, not new rules):** No scam-indicator mapping is expected. `जागरूकता कक्षा`, `काल्पनिक`, and `उदाहरण पर चर्चा` supply educational context that should suppress scam interpretation of the described scenario.
- **Possible ambiguity or unnatural wording (AI-generated, unverified):** Confirm whether `डिजिटल-अरेस्ट`, `काल्पनिक … उदाहरण`, and the overall classroom register are natural and clear in Hindi.
- **False-positive safeguards to preserve (AI-generated, unverified):** Educational discussion of police impersonation or money requests must not automatically be classified as a live scam. Context must be considered before assigning stages or tactics.

## Items requiring native-speaker verification

All six samples remain pending native-speaker verification. A reviewer should confirm:

- Transcript naturalness, grammar, terminology, register, and intended audience for every sample.
- The preliminary English meanings and the scam/genuine interpretation for each sample.
- Whether the preliminary phrase-to-indicator mappings accurately capture the Hindi wording without overgeneralising it.
- The expected labels, stages, and tactics for `HI-DA-001` and `HI-FF-001`.
- That the four genuine examples retain their intended context: official-app banking (`HI-GB-001`), scheduled passport verification (`HI-PV-001`), a negated security warning (`HI-OTP-001`), and education about a hypothetical scam (`HI-EDU-001`).

No native-speaker approval is claimed.
