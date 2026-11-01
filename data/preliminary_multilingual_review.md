# Preliminary Multilingual Review — AI-Generated, Unverified

**Status:** Every translation and assessment in this document is AI-generated and unverified. It is **not** native-speaker approval and must not be used to validate, relabel, or implement multilingual detection without native-speaker review. Original transcripts below are reproduced verbatim from `evaluation_dataset.json`.

## Hindi

### HI-DA-001 — Hindi
- **Original transcript (verbatim):** साइबर अपराध विभाग से कॉल है। आपका आधार नंबर आपराधिक जांच से जुड़ा बताया गया है। कॉल न काटें और परिवार को न बताएं। गिरफ्तारी से बचने के लिए तुरंत पचास हजार रुपये भेजें और इस मामले को गोपनीय रखें।
- **Preliminary English translation (AI-generated, unverified):** This is a call from the cyber-crime department. Your Aadhaar number is said to be linked to a criminal investigation. Do not disconnect the call or tell your family. To avoid arrest, send fifty thousand rupees immediately and keep this matter confidential.
- **Intended meaning (AI-generated, unverified):** A purported authority uses a criminal allegation, isolation, and an urgent money-transfer demand to coerce the recipient.
- **Expected scam classification (AI-generated, unverified):** `true`; the dataset classifies this as a digital-arrest scam because it impersonates authority and demands payment under threat.
- **Expected stages and tactics (AI-generated, unverified):** Stages: `authority_claim`, `accusation`, `isolation`, `payment_demand`. Tactics: `urgency`, `authority_impersonation`, `payment_pressure`, `secrecy`—the text appears designed to establish authority, allege wrongdoing, cut off support, and demand money urgently.
- **Potentially unnatural or ambiguous wording (AI-generated, unverified):** The opening “कॉल है” and the passive “जुड़ा बताया गया है” may need native-speaker review for conversational naturalness; verify the register and whether the coercive sequence reads naturally.

### HI-FF-001 — Hindi
- **Original transcript (verbatim):** आपके बैंक खाते में अवैध लेन-देन होने का आरोप है। खाता बंद होने से बचाने के लिए अभी भुगतान करें और अपना OTP बताएं।
- **Preliminary English translation (AI-generated, unverified):** Your bank account is accused of having illegal transactions. To prevent the account from being closed, make a payment now and disclose your OTP.
- **Intended meaning (AI-generated, unverified):** A supposed bank problem is used to demand immediate payment and an OTP.
- **Expected scam classification (AI-generated, unverified):** `true`; the dataset treats the allegation, urgent payment request, and OTP request as financial-fraud indicators.
- **Expected stages and tactics (AI-generated, unverified):** Stages: `accusation`, `payment_demand`. Tactics: `urgency`, `credential_harvesting`, `payment_pressure`—the claim of illegal activity supplies pressure for payment and credential disclosure.
- **Potentially unnatural or ambiguous wording (AI-generated, unverified):** “खाते में … होने का आरोप” may be an unusual way to frame a bank allegation; native review should confirm meaning and idiomatic wording.

### HI-GB-001 — Hindi
- **Original transcript (verbatim):** मैंने अपने बैंक के आधिकारिक ऐप से सामान्य UPI भुगतान किया। ग्राहक सहायता ने लेन-देन की स्थिति बताई और OTP साझा न करने की सलाह दी।
- **Preliminary English translation (AI-generated, unverified):** I made a routine UPI payment through my bank’s official app. Customer support gave the transaction status and advised me not to share my OTP.
- **Intended meaning (AI-generated, unverified):** A routine banking interaction conducted through an official channel includes a safety reminder.
- **Expected scam classification (AI-generated, unverified):** `false`; the dataset presents this as legitimate banking rather than an unsolicited demand or impersonation.
- **Expected stages and tactics (AI-generated, unverified):** Stages: none. Tactics: none. The apparent reference to OTP is protective advice, not a request for it.
- **Potentially unnatural or ambiguous wording (AI-generated, unverified):** Verify whether “आधिकारिक ऐप से … भुगतान किया” and “लेन-देन की स्थिति बताई” are natural in this context.

### HI-PV-001 — Hindi
- **Original transcript (verbatim):** मैं पासपोर्ट सत्यापन के लिए निर्धारित समय पर पुलिस स्टेशन गया। अधिकारी ने पहचान की जांच की और प्रक्रिया समझाई।
- **Preliminary English translation (AI-generated, unverified):** I went to the police station at the scheduled time for passport verification. The officer checked my identity and explained the procedure.
- **Intended meaning (AI-generated, unverified):** An in-person, scheduled passport-verification interaction is being described.
- **Expected scam classification (AI-generated, unverified):** `false`; the dataset classifies this as a legitimate verification discussion with no coercive request.
- **Expected stages and tactics (AI-generated, unverified):** Stages: none. Tactics: none. It describes a scheduled official process rather than an authority claim made to induce a transfer.
- **Potentially unnatural or ambiguous wording (AI-generated, unverified):** Native review should confirm whether “निर्धारित समय” and the account of the procedure sound natural.

### HI-OTP-001 — Hindi
- **Original transcript (verbatim):** बैंक की सुरक्षा सूचना: अपना OTP, PIN या पासवर्ड किसी कॉल करने वाले व्यक्ति को कभी न बताएं।
- **Preliminary English translation (AI-generated, unverified):** Bank security notice: never tell your OTP, PIN, or password to anyone who calls you.
- **Intended meaning (AI-generated, unverified):** A safety warning tells the recipient not to disclose credentials to callers.
- **Expected scam classification (AI-generated, unverified):** `false`; the dataset treats it as protective advice, not a scam attempt.
- **Expected stages and tactics (AI-generated, unverified):** Stages: none. Tactics: none. It warns against credential harvesting rather than performing it.
- **Potentially unnatural or ambiguous wording (AI-generated, unverified):** “किसी कॉल करने वाले व्यक्ति” may be less idiomatic than other possible wording; native review should confirm.

### HI-EDU-001 — Hindi
- **Original transcript (verbatim):** जागरूकता कक्षा में हमने एक काल्पनिक डिजिटल-अरेस्ट धोखाधड़ी के उदाहरण पर चर्चा की, जिसमें कोई व्यक्ति पुलिस होने का दावा करता है और पैसे मांगता है।
- **Preliminary English translation (AI-generated, unverified):** In an awareness class, we discussed a hypothetical digital-arrest fraud example in which someone claims to be police and asks for money.
- **Intended meaning (AI-generated, unverified):** An educational discussion describes scam features without carrying them out.
- **Expected scam classification (AI-generated, unverified):** `false`; the dataset classifies it as educational context, not a scam directed at the speaker.
- **Expected stages and tactics (AI-generated, unverified):** Stages: none. Tactics: none. Authority impersonation and a money request are discussed as an example, not issued as instructions.
- **Potentially unnatural or ambiguous wording (AI-generated, unverified):** Verify whether “डिजिटल-अरेस्ट” and “काल्पनिक … उदाहरण” are natural and sufficiently clear in Hindi.

## Telugu

### TE-DA-001 — Telugu
- **Original transcript (verbatim):** సైబర్ క్రైమ్ విభాగం నుండి మాట్లాడుతున్నాం. మీ ఆధార్ నంబర్ క్రిమినల్ దర్యాప్తుతో సంబంధం ఉందని చెబుతున్నారు. కాల్ కట్ చేయకండి, కుటుంబానికి చెప్పకండి. అరెస్టు తప్పించుకోవడానికి వెంటనే డబ్బు బదిలీ చేయండి.
- **Preliminary English translation (AI-generated, unverified):** We are speaking from the cyber-crime department. They say your Aadhaar number is connected to a criminal investigation. Do not cut the call or tell your family. Transfer money immediately to avoid arrest.
- **Intended meaning (AI-generated, unverified):** A caller claiming to be an authority alleges a criminal connection, isolates the recipient, and demands an urgent transfer.
- **Expected scam classification (AI-generated, unverified):** `true`; the dataset identifies a digital-arrest scam pattern.
- **Expected stages and tactics (AI-generated, unverified):** Stages: `authority_claim`, `accusation`, `isolation`, `payment_demand`. Tactics: `urgency`, `authority_impersonation`, `payment_pressure`, `secrecy`—the threat of arrest and instruction not to tell family are central signals.
- **Potentially unnatural or ambiguous wording (AI-generated, unverified):** The shift from “we” to “they say” and the phrase for transferring money require native-speaker confirmation.

### TE-FF-001 — Telugu
- **Original transcript (verbatim):** మీ బ్యాంకు ఖాతాలో అనుమానాస్పద లావాదేవీలు ఉన్నాయని చెబుతున్నారు. ఖాతా నిలిపివేయకుండా ఉండాలంటే ఇప్పుడే చెల్లించి మీ OTP చెప్పండి.
- **Preliminary English translation (AI-generated, unverified):** They say there are suspicious transactions in your bank account. To prevent the account from being suspended, pay now and tell them your OTP.
- **Intended meaning (AI-generated, unverified):** A claimed account problem is paired with an immediate payment and OTP demand.
- **Expected scam classification (AI-generated, unverified):** `true`; the dataset categorizes the account allegation and payment/OTP request as financial fraud.
- **Expected stages and tactics (AI-generated, unverified):** Stages: `accusation`, `payment_demand`. Tactics: `urgency`, `credential_harvesting`, `payment_pressure`—the account-suspension consequence pressures disclosure and payment.
- **Potentially unnatural or ambiguous wording (AI-generated, unverified):** Confirm whether “చెల్లించి మీ OTP చెప్పండి” naturally conveys payment plus OTP disclosure and whether the suspension wording is idiomatic.

### TE-GB-001 — Telugu
- **Original transcript (verbatim):** నా బ్యాంకు అధికారిక యాప్‌లో సాధారణ UPI బదిలీ స్థితిని చూశాను. సహాయకుడు లావాదేవీ పూర్తయిందని తెలిపి OTP ఎవరితోనూ పంచుకోవద్దని గుర్తుచేశాడు.
- **Preliminary English translation (AI-generated, unverified):** I checked the status of a routine UPI transfer in my bank’s official app. The assistant said the transaction was complete and reminded me not to share my OTP with anyone.
- **Intended meaning (AI-generated, unverified):** A routine official-app transaction check includes an anti-fraud reminder.
- **Expected scam classification (AI-generated, unverified):** `false`; no unsolicited pressure, credential request, or false authority claim is presented.
- **Expected stages and tactics (AI-generated, unverified):** Stages: none. Tactics: none. The OTP reference is a warning not to disclose it.
- **Potentially unnatural or ambiguous wording (AI-generated, unverified):** Native review should check whether “సహాయకుడు” is a suitable term for bank support and whether the phrasing is natural.

### TE-PV-001 — Telugu
- **Original transcript (verbatim):** పాస్‌పోర్ట్ ధృవీకరణ కోసం నిర్ణయించిన సమయంలో పోలీస్ స్టేషన్‌కు వెళ్లాను. అధికారి గుర్తింపును పరిశీలించి తదుపరి విధానాన్ని వివరించారు.
- **Preliminary English translation (AI-generated, unverified):** I went to the police station at the scheduled time for passport verification. The officer examined my identity and explained the next procedure.
- **Intended meaning (AI-generated, unverified):** A scheduled in-person police verification is being described.
- **Expected scam classification (AI-generated, unverified):** `false`; the dataset treats it as a legitimate official process.
- **Expected stages and tactics (AI-generated, unverified):** Stages: none. Tactics: none. There is no payment, credential demand, intimidation, or isolation instruction.
- **Potentially unnatural or ambiguous wording (AI-generated, unverified):** Confirm the gender/honorific agreement and the naturalness of “తదుపరి విధానం.”

### TE-OTP-001 — Telugu
- **Original transcript (verbatim):** భద్రతా సూచన: మీ OTP, PIN లేదా పాస్‌వర్డ్‌ను ఫోన్‌లో అడిగే ఎవరికీ చెప్పవద్దు.
- **Preliminary English translation (AI-generated, unverified):** Security advice: do not tell your OTP, PIN, or password to anyone who asks for it over the phone.
- **Intended meaning (AI-generated, unverified):** A protective warning tells the recipient not to provide credentials to phone callers.
- **Expected scam classification (AI-generated, unverified):** `false`; it warns about credential harvesting rather than requesting credentials.
- **Expected stages and tactics (AI-generated, unverified):** Stages: none. Tactics: none. Its function is preventive.
- **Potentially unnatural or ambiguous wording (AI-generated, unverified):** No specific issue is asserted; native review should verify register and naturalness.

### TE-EDU-001 — Telugu
- **Original transcript (verbatim):** సైబర్ భద్రత తరగతిలో డిజిటల్ అరెస్ట్ మోసాల గురించి చర్చించాము. ఉదాహరణలో కాలర్ పోలీస్ అని చెప్పి డబ్బు అడుగుతాడు.
- **Preliminary English translation (AI-generated, unverified):** In a cyber-security class, we discussed digital-arrest scams. In the example, the caller says he is police and asks for money.
- **Intended meaning (AI-generated, unverified):** A class discusses a fraud scenario as an example.
- **Expected scam classification (AI-generated, unverified):** `false`; the dataset marks the educational context as non-scam.
- **Expected stages and tactics (AI-generated, unverified):** Stages: none. Tactics: none. The text reports an example of authority impersonation and payment pressure; it does not direct those acts at the recipient.
- **Potentially unnatural or ambiguous wording (AI-generated, unverified):** Verify whether “డిజిటల్ అరెస్ట్” and the description of the caller are idiomatic Telugu.

## Tamil

### TA-DA-001 — Tamil
- **Original transcript (verbatim):** சைபர் குற்றப் பிரிவிலிருந்து பேசுகிறோம். உங்கள் ஆதார் எண் குற்ற விசாரணையுடன் இணைக்கப்பட்டதாக கூறுகிறார்கள். அழைப்பை துண்டிக்காதீர்கள், குடும்பத்திடம் சொல்லாதீர்கள். கைது தவிர்க்க உடனே பணத்தை மாற்றுங்கள்.
- **Preliminary English translation (AI-generated, unverified):** We are speaking from the cyber-crime division. They say your Aadhaar number is linked to a criminal investigation. Do not disconnect the call or tell your family. Transfer the money immediately to avoid arrest.
- **Intended meaning (AI-generated, unverified):** A purported cyber-crime official alleges criminal involvement, demands secrecy, and requests money under threat of arrest.
- **Expected scam classification (AI-generated, unverified):** `true`; the dataset classifies this as a digital-arrest scam.
- **Expected stages and tactics (AI-generated, unverified):** Stages: `authority_claim`, `accusation`, `isolation`, `payment_demand`. Tactics: `urgency`, `authority_impersonation`, `payment_pressure`, `secrecy`—the claimed authority, arrest threat, family restriction, and transfer demand map to these labels.
- **Potentially unnatural or ambiguous wording (AI-generated, unverified):** The perspective change in “பேசுகிறோம்” / “கூறுகிறார்கள்” and “பணத்தை மாற்றுங்கள்” should be checked for idiomatic scam-call phrasing.

### TA-FF-001 — Tamil
- **Original transcript (verbatim):** உங்கள் வங்கிக் கணக்கில் சட்டவிரோத பரிவர்த்தனைகள் நடந்ததாக கூறுகிறார்கள். கணக்கு முடக்கப்படாமல் இருக்க உடனே பணம் செலுத்தி OTP-ஐ பகிருங்கள்.
- **Preliminary English translation (AI-generated, unverified):** They say illegal transactions occurred in your bank account. To keep the account from being frozen, pay money immediately and share the OTP.
- **Intended meaning (AI-generated, unverified):** A claimed illegal-account activity is used to press for an urgent payment and OTP disclosure.
- **Expected scam classification (AI-generated, unverified):** `true`; the dataset treats it as financial fraud.
- **Expected stages and tactics (AI-generated, unverified):** Stages: `accusation`, `payment_demand`. Tactics: `urgency`, `credential_harvesting`, `payment_pressure`—a freezing consequence is used to induce payment and disclosure.
- **Potentially unnatural or ambiguous wording (AI-generated, unverified):** Native review should check the naturalness of “பணம் செலுத்தி OTP-ஐ பகிருங்கள்” and whether it clearly denotes a scammer’s request.

### TA-GB-001 — Tamil
- **Original transcript (verbatim):** வங்கியின் அதிகாரப்பூர்வ செயலியில் வழக்கமான UPI பரிவர்த்தனையை பார்த்தேன். ஆதரவு ஊழியர் பரிவர்த்தனை முடிந்ததாகவும் OTP-ஐ பகிர வேண்டாமென்றும் கூறினார்.
- **Preliminary English translation (AI-generated, unverified):** I viewed a routine UPI transaction in the bank’s official app. The support employee said the transaction was complete and that the OTP should not be shared.
- **Intended meaning (AI-generated, unverified):** A regular transaction through an official channel is described, together with security advice.
- **Expected scam classification (AI-generated, unverified):** `false`; it is presented as legitimate banking, not a scam attempt.
- **Expected stages and tactics (AI-generated, unverified):** Stages: none. Tactics: none. The OTP is mentioned as something not to share.
- **Potentially unnatural or ambiguous wording (AI-generated, unverified):** “பரிவர்த்தனையை பார்த்தேன்” and “ஆதரவு ஊழியர்” need native-speaker review for contextual naturalness.

### TA-PV-001 — Tamil
- **Original transcript (verbatim):** கடவுச்சீட்டு சரிபார்ப்பிற்காக நிர்ணயிக்கப்பட்ட நேரத்தில் காவல் நிலையம் சென்றேன். அதிகாரி அடையாளத்தை சரிபார்த்து நடைமுறையை விளக்கினார்.
- **Preliminary English translation (AI-generated, unverified):** I went to the police station at the scheduled time for passport verification. The officer checked my identity and explained the procedure.
- **Intended meaning (AI-generated, unverified):** A legitimate scheduled passport-verification visit is described.
- **Expected scam classification (AI-generated, unverified):** `false`; the dataset treats this as a genuine police-verification discussion.
- **Expected stages and tactics (AI-generated, unverified):** Stages: none. Tactics: none. It lacks a demand, threat, or instruction to conceal the interaction.
- **Potentially unnatural or ambiguous wording (AI-generated, unverified):** Confirm whether “கடவுச்சீட்டு சரிபார்ப்பு” and the procedural wording are idiomatic for this setting.

### TA-OTP-001 — Tamil
- **Original transcript (verbatim):** பாதுகாப்பு நினைவூட்டல்: உங்கள் OTP, PIN அல்லது கடவுச்சொல்லை தொலைபேசியில் கேட்பவர்களிடம் பகிர வேண்டாம்.
- **Preliminary English translation (AI-generated, unverified):** Security reminder: do not share your OTP, PIN, or password with people who ask for them over the phone.
- **Intended meaning (AI-generated, unverified):** A security message warns against sharing credentials with callers.
- **Expected scam classification (AI-generated, unverified):** `false`; the dataset categorizes this as protective advice.
- **Expected stages and tactics (AI-generated, unverified):** Stages: none. Tactics: none. It discourages credential harvesting.
- **Potentially unnatural or ambiguous wording (AI-generated, unverified):** Native review should confirm phrasing and register; no native approval is implied.

### TA-EDU-001 — Tamil
- **Original transcript (verbatim):** சைபர் பாதுகாப்பு வகுப்பில் டிஜிட்டல் கைது மோசடிகள் பற்றி பேசினோம். எடுத்துக்காட்டில் ஒருவர் காவல்துறை என்று கூறி பணம் கேட்கிறார்.
- **Preliminary English translation (AI-generated, unverified):** In a cyber-security class, we discussed digital-arrest scams. In the example, someone says they are police and asks for money.
- **Intended meaning (AI-generated, unverified):** An awareness class discusses an illustrative scam scenario.
- **Expected scam classification (AI-generated, unverified):** `false`; the dataset considers the educational framing non-scam.
- **Expected stages and tactics (AI-generated, unverified):** Stages: none. Tactics: none. Scam-like elements appear as a lesson example, not a live solicitation.
- **Potentially unnatural or ambiguous wording (AI-generated, unverified):** Verify whether “டிஜிட்டல் கைது” is conventional and whether the example’s wording is natural.

## Malayalam

### ML-DA-001 — Malayalam
- **Original transcript (verbatim):** സൈബർ ക്രൈം വിഭാഗത്തിൽ നിന്നാണ് വിളിക്കുന്നത്. നിങ്ങളുടെ ആധാർ നമ്പർ ക്രിമിനൽ അന്വേഷണവുമായി ബന്ധിപ്പിച്ചെന്ന് പറയുന്നു. കോൾ വിച്ഛേദിക്കരുത്, കുടുംബത്തോട് പറയരുത്. അറസ്റ്റ് ഒഴിവാക്കാൻ ഉടൻ പണം കൈമാറുക.
- **Preliminary English translation (AI-generated, unverified):** This is a call from the cyber-crime division. They say your Aadhaar number has been linked to a criminal investigation. Do not disconnect the call or tell your family. Transfer money immediately to avoid arrest.
- **Intended meaning (AI-generated, unverified):** A caller poses as cyber-crime authorities, alleges criminal involvement, demands silence, and seeks an urgent transfer.
- **Expected scam classification (AI-generated, unverified):** `true`; the dataset labels this a digital-arrest scam.
- **Expected stages and tactics (AI-generated, unverified):** Stages: `authority_claim`, `accusation`, `isolation`, `payment_demand`. Tactics: `urgency`, `authority_impersonation`, `payment_pressure`, `secrecy`—the arrest threat and instruction not to tell family create coercion.
- **Potentially unnatural or ambiguous wording (AI-generated, unverified):** The exact authority-call register and the money-transfer expression should be reviewed by a Malayalam native speaker.

### ML-FF-001 — Malayalam
- **Original transcript (verbatim):** നിങ്ങളുടെ ബാങ്ക് അക്കൗണ്ടിൽ നിയമവിരുദ്ധ ഇടപാടുകൾ ഉണ്ടായെന്ന് പറയുന്നു. അക്കൗണ്ട് മരവിപ്പിക്കാതിരിക്കാൻ ഉടൻ പണം അടച്ച് OTP പറയുക.
- **Preliminary English translation (AI-generated, unverified):** They say illegal transactions occurred in your bank account. To avoid the account being frozen, pay money immediately and state your OTP.
- **Intended meaning (AI-generated, unverified):** A bank-account allegation is used to demand immediate payment and an OTP.
- **Expected scam classification (AI-generated, unverified):** `true`; the dataset identifies a financial-fraud pattern.
- **Expected stages and tactics (AI-generated, unverified):** Stages: `accusation`, `payment_demand`. Tactics: `urgency`, `credential_harvesting`, `payment_pressure`—the threat of freezing pressures the recipient to pay and reveal a credential.
- **Potentially unnatural or ambiguous wording (AI-generated, unverified):** Native review should determine whether “OTP പറയുക” is an idiomatic request and whether the account-freeze phrasing is natural.

### ML-GB-001 — Malayalam
- **Original transcript (verbatim):** ബാങ്കിന്റെ ഔദ്യോഗിക ആപ്പിൽ സാധാരണ UPI ഇടപാട് പരിശോധിച്ചു. ഇടപാട് പൂർത്തിയായെന്നും OTP ആരോടും പങ്കിടരുതെന്നും സഹായ കേന്ദ്രം അറിയിച്ചു.
- **Preliminary English translation (AI-generated, unverified):** I checked a routine UPI transaction in the bank’s official app. The support centre said it was complete and that the OTP should not be shared with anyone.
- **Intended meaning (AI-generated, unverified):** An official-app banking interaction gives a protective OTP reminder.
- **Expected scam classification (AI-generated, unverified):** `false`; the dataset presents it as genuine support, not fraud.
- **Expected stages and tactics (AI-generated, unverified):** Stages: none. Tactics: none. The text warns against sharing an OTP rather than seeking it.
- **Potentially unnatural or ambiguous wording (AI-generated, unverified):** Verify whether the omitted first-person subject and “സഹായ കേന്ദ്രം” are natural in ordinary Malayalam usage.

### ML-PV-001 — Malayalam
- **Original transcript (verbatim):** പാസ്‌പോർട്ട് പരിശോധനയ്ക്കായി നിശ്ചയിച്ച സമയത്ത് പൊലീസ് സ്റ്റേഷനിൽ പോയി. ഉദ്യോഗസ്ഥൻ തിരിച്ചറിയൽ പരിശോധിച്ച് നടപടിക്രമം വിശദീകരിച്ചു.
- **Preliminary English translation (AI-generated, unverified):** I went to the police station at the scheduled time for passport verification. The officer checked my identity and explained the procedure.
- **Intended meaning (AI-generated, unverified):** A normal scheduled police-station visit for passport verification is described.
- **Expected scam classification (AI-generated, unverified):** `false`; the dataset classifies it as a legitimate official interaction.
- **Expected stages and tactics (AI-generated, unverified):** Stages: none. Tactics: none. It has no coercive request or scam-pressure feature.
- **Potentially unnatural or ambiguous wording (AI-generated, unverified):** A native speaker should verify the ordinary terms for passport verification and procedure.

### ML-OTP-001 — Malayalam
- **Original transcript (verbatim):** സുരക്ഷാ മുന്നറിയിപ്പ്: നിങ്ങളുടെ OTP, PIN, പാസ്‌വേഡ് എന്നിവ ഫോണിൽ ആവശ്യപ്പെടുന്നവരുമായി പങ്കിടരുത്.
- **Preliminary English translation (AI-generated, unverified):** Security warning: do not share your OTP, PIN, or password with people who ask for them by phone.
- **Intended meaning (AI-generated, unverified):** A fraud-prevention message warns against disclosure of authentication credentials.
- **Expected scam classification (AI-generated, unverified):** `false`; the dataset marks the warning itself as non-scam.
- **Expected stages and tactics (AI-generated, unverified):** Stages: none. Tactics: none. It counters credential harvesting rather than attempting it.
- **Potentially unnatural or ambiguous wording (AI-generated, unverified):** Confirm whether “ഫോണിൽ ആവശ്യപ്പെടുന്നവരുമായി” is the most natural construction.

### ML-EDU-001 — Malayalam
- **Original transcript (verbatim):** സൈബർ സുരക്ഷാ ക്ലാസിൽ ഡിജിറ്റൽ അറസ്റ്റ് തട്ടിപ്പിനെക്കുറിച്ച് സംസാരിച്ചു. ഉദാഹരണത്തിൽ വിളിക്കുന്നയാൾ പൊലീസ് ഉദ്യോഗസ്ഥനാണെന്ന് നടിച്ച് പണം ആവശ്യപ്പെടുന്നു.
- **Preliminary English translation (AI-generated, unverified):** In a cyber-security class, we discussed digital-arrest fraud. In the example, the caller pretends to be a police officer and asks for money.
- **Intended meaning (AI-generated, unverified):** A classroom example describes impersonation and a monetary demand to teach about a scam.
- **Expected scam classification (AI-generated, unverified):** `false`; the educational context is expected to be non-scam.
- **Expected stages and tactics (AI-generated, unverified):** Stages: none. Tactics: none. The authority impersonation and payment request are narrative content, not a current solicitation.
- **Potentially unnatural or ambiguous wording (AI-generated, unverified):** Native review should confirm whether “ഡിജിറ്റൽ അറസ്റ്റ്” and the impersonation phrasing are natural.

## Indian Code-Mixed Speech

### MIX-DA-001 — Indian code-mixed speech
- **Original transcript (verbatim):** Cybercrime department se call kar raha hoon. Aapka Aadhaar number investigation se linked hai. Call disconnect mat kijiye aur family ko mat batayiye. Arrest avoid karne ke liye fifty thousand rupees abhi transfer kijiye.
- **Preliminary English translation (AI-generated, unverified):** I am calling from the cybercrime department. Your Aadhaar number is linked to an investigation. Do not disconnect the call or tell your family. To avoid arrest, transfer fifty thousand rupees now.
- **Intended meaning (AI-generated, unverified):** A Hindi-English caller claims official authority, alleges an investigation link, isolates the recipient, and demands an urgent transfer.
- **Expected scam classification (AI-generated, unverified):** `true`; the dataset labels this a digital-arrest scam.
- **Expected stages and tactics (AI-generated, unverified):** Stages: `authority_claim`, `accusation`, `isolation`, `payment_demand`. Tactics: `urgency`, `authority_impersonation`, `payment_pressure`, `secrecy`—the explicit call origin, arrest consequence, and secrecy instruction map to the labels.
- **Potentially unnatural or ambiguous wording (AI-generated, unverified):** Verify whether this Hindi-English mix and the register of “linked,” “arrest avoid,” and “transfer kijiye” are realistic for the intended speakers.

### MIX-FF-001 — Indian code-mixed speech
- **Original transcript (verbatim):** Aapke bank account mein suspicious transaction hua hai. Account freeze hone se bachane ke liye abhi payment karo aur apna OTP batao.
- **Preliminary English translation (AI-generated, unverified):** A suspicious transaction has occurred in your bank account. To prevent the account from being frozen, make a payment now and tell us your OTP.
- **Intended meaning (AI-generated, unverified):** A claimed suspicious transaction and threat of a freeze pressure the recipient to pay and disclose an OTP.
- **Expected scam classification (AI-generated, unverified):** `true`; the dataset treats this as financial fraud.
- **Expected stages and tactics (AI-generated, unverified):** Stages: `accusation`, `payment_demand`. Tactics: `urgency`, `credential_harvesting`, `payment_pressure`—account-freeze pressure accompanies payment and credential demands.
- **Potentially unnatural or ambiguous wording (AI-generated, unverified):** “payment karo” and “OTP batao” are informal; a native reviewer should confirm that this intended register is plausible and unambiguous.

### MIX-GB-001 — Indian code-mixed speech
- **Original transcript (verbatim):** Maine bank ke official app mein apna UPI transfer check kiya. Support ne bola transaction complete hai aur OTP kisi ke saath share nahi karna.
- **Preliminary English translation (AI-generated, unverified):** I checked my UPI transfer in the bank’s official app. Support said the transaction was complete and that the OTP should not be shared with anyone.
- **Intended meaning (AI-generated, unverified):** A normal official-app banking interaction includes an OTP safety reminder.
- **Expected scam classification (AI-generated, unverified):** `false`; the dataset presents it as a genuine conversation.
- **Expected stages and tactics (AI-generated, unverified):** Stages: none. Tactics: none. The OTP reference is protective, not a disclosure request.
- **Potentially unnatural or ambiguous wording (AI-generated, unverified):** The code mix and “Support ne bola” should be reviewed for naturalness and intended regional register.

### MIX-PV-001 — Indian code-mixed speech
- **Original transcript (verbatim):** Passport verification ke liye police station par appointment tha. Officer ne identity check ki aur normal process explain kiya.
- **Preliminary English translation (AI-generated, unverified):** There was an appointment at the police station for passport verification. The officer checked identity and explained the normal process.
- **Intended meaning (AI-generated, unverified):** A scheduled, ordinary passport-verification procedure is described.
- **Expected scam classification (AI-generated, unverified):** `false`; the dataset classifies it as a legitimate police-verification discussion.
- **Expected stages and tactics (AI-generated, unverified):** Stages: none. Tactics: none. It reports a normal appointment, with no pressure or payment request.
- **Potentially unnatural or ambiguous wording (AI-generated, unverified):** Confirm whether “police station par appointment” and “normal process” are natural for the intended code-mixed variety.

### MIX-OTP-001 — Indian code-mixed speech
- **Original transcript (verbatim):** Bank ka security message hai: apna OTP, PIN ya password kisi caller ko kabhi share mat karo. Official app use karo.
- **Preliminary English translation (AI-generated, unverified):** This is a bank security message: never share your OTP, PIN, or password with any caller. Use the official app.
- **Intended meaning (AI-generated, unverified):** A security reminder tells recipients to protect credentials and use the official channel.
- **Expected scam classification (AI-generated, unverified):** `false`; the dataset treats it as protective advice.
- **Expected stages and tactics (AI-generated, unverified):** Stages: none. Tactics: none. It prevents rather than performs credential harvesting.
- **Potentially unnatural or ambiguous wording (AI-generated, unverified):** Native review should check the mix of informal imperative “mat karo” with the message’s intended institutional register.

### MIX-EDU-001 — Indian code-mixed speech
- **Original transcript (verbatim):** Scam awareness class mein ek example script discuss ki: caller bolta hai 'This is the police', investigation ka dar dikhata hai aur payment maangta hai.
- **Preliminary English translation (AI-generated, unverified):** In a scam-awareness class, we discussed an example script: the caller says, “This is the police,” creates fear about an investigation, and asks for payment.
- **Intended meaning (AI-generated, unverified):** A class discusses the components of a scam script for awareness purposes.
- **Expected scam classification (AI-generated, unverified):** `false`; the dataset considers the educational framing non-scam.
- **Expected stages and tactics (AI-generated, unverified):** Stages: none. Tactics: none. Authority impersonation, fear, and payment are described as lesson content rather than directed at a target.
- **Potentially unnatural or ambiguous wording (AI-generated, unverified):** Verify the naturalness of “investigation ka dar dikhata hai,” the quoted English line, and the overall classroom register.

## Verification result

**AI-generated, unverified check:** The 30 unique `sample_id` values marked `native_speaker_review_required: true` in `evaluation_dataset.json` are each represented exactly once in this document: 6 Hindi, 6 Telugu, 6 Tamil, 6 Malayalam, and 6 Indian code-mixed samples. No native-speaker approval is claimed.
