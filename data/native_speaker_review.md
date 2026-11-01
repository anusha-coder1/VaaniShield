# Native-Speaker Review Sheet

Review the synthetic transcripts and their expected scam labels before using them to guide multilingual detection. All entries below are marked `native_speaker_review_required: true` in `evaluation_dataset.json`.

No English meaning is provided for these samples in the evaluation dataset. No translation has been added here. Please review the original wording, intended meaning, naturalness, and expected labels. These are synthetic examples, not real victim conversations.

For each sample, record corrections below the transcript and mark whether the scam label, stages, and tactics are appropriate. Use only the identifiers already defined in `models/schemas.py`.

## Hindi

### HI-DA-001 — Digital-arrest scam
- **Original transcript:** साइबर अपराध विभाग से कॉल है। आपका आधार नंबर आपराधिक जांच से जुड़ा बताया गया है। कॉल न काटें और परिवार को न बताएं। गिरफ्तारी से बचने के लिए तुरंत पचास हजार रुपये भेजें और इस मामले को गोपनीय रखें।
- **English meaning (dataset-provided):** Not provided.
- **Expected scam:** `true`
- **Expected stages:** `authority_claim`, `accusation`, `isolation`, `payment_demand`
- **Expected tactics:** `urgency`, `authority_impersonation`, `payment_pressure`, `secrecy`
- **Native correction / naturalness notes:** ______________________________________________
- **Label verification:** Scam `[ ] Confirmed [ ] Corrected`; stages `[ ] Confirmed [ ] Corrected`; tactics `[ ] Confirmed [ ] Corrected`

### HI-FF-001 — Financial fraud scam
- **Original transcript:** आपके बैंक खाते में अवैध लेन-देन होने का आरोप है। खाता बंद होने से बचाने के लिए अभी भुगतान करें और अपना OTP बताएं।
- **English meaning (dataset-provided):** Not provided.
- **Expected scam:** `true`
- **Expected stages:** `accusation`, `payment_demand`
- **Expected tactics:** `urgency`, `credential_harvesting`, `payment_pressure`
- **Native correction / naturalness notes:** ______________________________________________
- **Label verification:** Scam `[ ] Confirmed [ ] Corrected`; stages `[ ] Confirmed [ ] Corrected`; tactics `[ ] Confirmed [ ] Corrected`

### HI-GB-001 — Genuine banking conversation
- **Original transcript:** मैंने अपने बैंक के आधिकारिक ऐप से सामान्य UPI भुगतान किया। ग्राहक सहायता ने लेन-देन की स्थिति बताई और OTP साझा न करने की सलाह दी।
- **English meaning (dataset-provided):** Not provided.
- **Expected scam:** `false`
- **Expected stages:** None
- **Expected tactics:** None
- **Native correction / naturalness notes:** ______________________________________________
- **Label verification:** Non-scam label `[ ] Confirmed [ ] Corrected`

### HI-PV-001 — Legitimate police verification discussion
- **Original transcript:** मैं पासपोर्ट सत्यापन के लिए निर्धारित समय पर पुलिस स्टेशन गया। अधिकारी ने पहचान की जांच की और प्रक्रिया समझाई।
- **English meaning (dataset-provided):** Not provided.
- **Expected scam:** `false`
- **Expected stages:** None
- **Expected tactics:** None
- **Native correction / naturalness notes:** ______________________________________________
- **Label verification:** Non-scam label `[ ] Confirmed [ ] Corrected`

### HI-OTP-001 — Protective OTP/security warning
- **Original transcript:** बैंक की सुरक्षा सूचना: अपना OTP, PIN या पासवर्ड किसी कॉल करने वाले व्यक्ति को कभी न बताएं।
- **English meaning (dataset-provided):** Not provided.
- **Expected scam:** `false`
- **Expected stages:** None
- **Expected tactics:** None
- **Native correction / naturalness notes:** ______________________________________________
- **Label verification:** Non-scam label `[ ] Confirmed [ ] Corrected`

### HI-EDU-001 — Educational discussion about scams
- **Original transcript:** जागरूकता कक्षा में हमने एक काल्पनिक डिजिटल-अरेस्ट धोखाधड़ी के उदाहरण पर चर्चा की, जिसमें कोई व्यक्ति पुलिस होने का दावा करता है और पैसे मांगता है।
- **English meaning (dataset-provided):** Not provided.
- **Expected scam:** `false`
- **Expected stages:** None
- **Expected tactics:** None
- **Native correction / naturalness notes:** ______________________________________________
- **Label verification:** Non-scam label `[ ] Confirmed [ ] Corrected`

## Telugu

### TE-DA-001 — Digital-arrest scam
- **Original transcript:** సైబర్ క్రైమ్ విభాగం నుండి మాట్లాడుతున్నాం. మీ ఆధార్ నంబర్ క్రిమినల్ దర్యాప్తుతో సంబంధం ఉందని చెబుతున్నారు. కాల్ కట్ చేయకండి, కుటుంబానికి చెప్పకండి. అరెస్టు తప్పించుకోవడానికి వెంటనే డబ్బు బదిలీ చేయండి.
- **English meaning (dataset-provided):** Not provided.
- **Expected scam:** `true`
- **Expected stages:** `authority_claim`, `accusation`, `isolation`, `payment_demand`
- **Expected tactics:** `urgency`, `authority_impersonation`, `payment_pressure`, `secrecy`
- **Native correction / naturalness notes:** ______________________________________________
- **Label verification:** Scam `[ ] Confirmed [ ] Corrected`; stages `[ ] Confirmed [ ] Corrected`; tactics `[ ] Confirmed [ ] Corrected`

### TE-FF-001 — Financial fraud scam
- **Original transcript:** మీ బ్యాంకు ఖాతాలో అనుమానాస్పద లావాదేవీలు ఉన్నాయని చెబుతున్నారు. ఖాతా నిలిపివేయకుండా ఉండాలంటే ఇప్పుడే చెల్లించి మీ OTP చెప్పండి.
- **English meaning (dataset-provided):** Not provided.
- **Expected scam:** `true`
- **Expected stages:** `accusation`, `payment_demand`
- **Expected tactics:** `urgency`, `credential_harvesting`, `payment_pressure`
- **Native correction / naturalness notes:** ______________________________________________
- **Label verification:** Scam `[ ] Confirmed [ ] Corrected`; stages `[ ] Confirmed [ ] Corrected`; tactics `[ ] Confirmed [ ] Corrected`

### TE-GB-001 — Genuine banking conversation
- **Original transcript:** నా బ్యాంకు అధికారిక యాప్‌లో సాధారణ UPI బదిలీ స్థితిని చూశాను. సహాయకుడు లావాదేవీ పూర్తయిందని తెలిపి OTP ఎవరితోనూ పంచుకోవద్దని గుర్తుచేశాడు.
- **English meaning (dataset-provided):** Not provided.
- **Expected scam:** `false`
- **Expected stages:** None
- **Expected tactics:** None
- **Native correction / naturalness notes:** ______________________________________________
- **Label verification:** Non-scam label `[ ] Confirmed [ ] Corrected`

### TE-PV-001 — Legitimate police verification discussion
- **Original transcript:** పాస్‌పోర్ట్ ధృవీకరణ కోసం నిర్ణయించిన సమయంలో పోలీస్ స్టేషన్‌కు వెళ్లాను. అధికారి గుర్తింపును పరిశీలించి తదుపరి విధానాన్ని వివరించారు.
- **English meaning (dataset-provided):** Not provided.
- **Expected scam:** `false`
- **Expected stages:** None
- **Expected tactics:** None
- **Native correction / naturalness notes:** ______________________________________________
- **Label verification:** Non-scam label `[ ] Confirmed [ ] Corrected`

### TE-OTP-001 — Protective OTP/security warning
- **Original transcript:** భద్రతా సూచన: మీ OTP, PIN లేదా పాస్‌వర్డ్‌ను ఫోన్‌లో అడిగే ఎవరికీ చెప్పవద్దు.
- **English meaning (dataset-provided):** Not provided.
- **Expected scam:** `false`
- **Expected stages:** None
- **Expected tactics:** None
- **Native correction / naturalness notes:** ______________________________________________
- **Label verification:** Non-scam label `[ ] Confirmed [ ] Corrected`

### TE-EDU-001 — Educational discussion about scams
- **Original transcript:** సైబర్ భద్రత తరగతిలో డిజిటల్ అరెస్ట్ మోసాల గురించి చర్చించాము. ఉదాహరణలో కాలర్ పోలీస్ అని చెప్పి డబ్బు అడుగుతాడు.
- **English meaning (dataset-provided):** Not provided.
- **Expected scam:** `false`
- **Expected stages:** None
- **Expected tactics:** None
- **Native correction / naturalness notes:** ______________________________________________
- **Label verification:** Non-scam label `[ ] Confirmed [ ] Corrected`

## Tamil

### TA-DA-001 — Digital-arrest scam
- **Original transcript:** சைபர் குற்றப் பிரிவிலிருந்து பேசுகிறோம். உங்கள் ஆதார் எண் குற்ற விசாரணையுடன் இணைக்கப்பட்டதாக கூறுகிறார்கள். அழைப்பை துண்டிக்காதீர்கள், குடும்பத்திடம் சொல்லாதீர்கள். கைது தவிர்க்க உடனே பணத்தை மாற்றுங்கள்.
- **English meaning (dataset-provided):** Not provided.
- **Expected scam:** `true`
- **Expected stages:** `authority_claim`, `accusation`, `isolation`, `payment_demand`
- **Expected tactics:** `urgency`, `authority_impersonation`, `payment_pressure`, `secrecy`
- **Native correction / naturalness notes:** ______________________________________________
- **Label verification:** Scam `[ ] Confirmed [ ] Corrected`; stages `[ ] Confirmed [ ] Corrected`; tactics `[ ] Confirmed [ ] Corrected`

### TA-FF-001 — Financial fraud scam
- **Original transcript:** உங்கள் வங்கிக் கணக்கில் சட்டவிரோத பரிவர்த்தனைகள் நடந்ததாக கூறுகிறார்கள். கணக்கு முடக்கப்படாமல் இருக்க உடனே பணம் செலுத்தி OTP-ஐ பகிருங்கள்.
- **English meaning (dataset-provided):** Not provided.
- **Expected scam:** `true`
- **Expected stages:** `accusation`, `payment_demand`
- **Expected tactics:** `urgency`, `credential_harvesting`, `payment_pressure`
- **Native correction / naturalness notes:** ______________________________________________
- **Label verification:** Scam `[ ] Confirmed [ ] Corrected`; stages `[ ] Confirmed [ ] Corrected`; tactics `[ ] Confirmed [ ] Corrected`

### TA-GB-001 — Genuine banking conversation
- **Original transcript:** வங்கியின் அதிகாரப்பூர்வ செயலியில் வழக்கமான UPI பரிவர்த்தனையை பார்த்தேன். ஆதரவு ஊழியர் பரிவர்த்தனை முடிந்ததாகவும் OTP-ஐ பகிர வேண்டாமென்றும் கூறினார்.
- **English meaning (dataset-provided):** Not provided.
- **Expected scam:** `false`
- **Expected stages:** None
- **Expected tactics:** None
- **Native correction / naturalness notes:** ______________________________________________
- **Label verification:** Non-scam label `[ ] Confirmed [ ] Corrected`

### TA-PV-001 — Legitimate police verification discussion
- **Original transcript:** கடவுச்சீட்டு சரிபார்ப்பிற்காக நிர்ணயிக்கப்பட்ட நேரத்தில் காவல் நிலையம் சென்றேன். அதிகாரி அடையாளத்தை சரிபார்த்து நடைமுறையை விளக்கினார்.
- **English meaning (dataset-provided):** Not provided.
- **Expected scam:** `false`
- **Expected stages:** None
- **Expected tactics:** None
- **Native correction / naturalness notes:** ______________________________________________
- **Label verification:** Non-scam label `[ ] Confirmed [ ] Corrected`

### TA-OTP-001 — Protective OTP/security warning
- **Original transcript:** பாதுகாப்பு நினைவூட்டல்: உங்கள் OTP, PIN அல்லது கடவுச்சொல்லை தொலைபேசியில் கேட்பவர்களிடம் பகிர வேண்டாம்.
- **English meaning (dataset-provided):** Not provided.
- **Expected scam:** `false`
- **Expected stages:** None
- **Expected tactics:** None
- **Native correction / naturalness notes:** ______________________________________________
- **Label verification:** Non-scam label `[ ] Confirmed [ ] Corrected`

### TA-EDU-001 — Educational discussion about scams
- **Original transcript:** சைபர் பாதுகாப்பு வகுப்பில் டிஜிட்டல் கைது மோசடிகள் பற்றி பேசினோம். எடுத்துக்காட்டில் ஒருவர் காவல்துறை என்று கூறி பணம் கேட்கிறார்.
- **English meaning (dataset-provided):** Not provided.
- **Expected scam:** `false`
- **Expected stages:** None
- **Expected tactics:** None
- **Native correction / naturalness notes:** ______________________________________________
- **Label verification:** Non-scam label `[ ] Confirmed [ ] Corrected`

## Malayalam

### ML-DA-001 — Digital-arrest scam
- **Original transcript:** സൈബർ ക്രൈം വിഭാഗത്തിൽ നിന്നാണ് വിളിക്കുന്നത്. നിങ്ങളുടെ ആധാർ നമ്പർ ക്രിമിനൽ അന്വേഷണവുമായി ബന്ധിപ്പിച്ചെന്ന് പറയുന്നു. കോൾ വിച്ഛേദിക്കരുത്, കുടുംബത്തോട് പറയരുത്. അറസ്റ്റ് ഒഴിവാക്കാൻ ഉടൻ പണം കൈമാറുക.
- **English meaning (dataset-provided):** Not provided.
- **Expected scam:** `true`
- **Expected stages:** `authority_claim`, `accusation`, `isolation`, `payment_demand`
- **Expected tactics:** `urgency`, `authority_impersonation`, `payment_pressure`, `secrecy`
- **Native correction / naturalness notes:** ______________________________________________
- **Label verification:** Scam `[ ] Confirmed [ ] Corrected`; stages `[ ] Confirmed [ ] Corrected`; tactics `[ ] Confirmed [ ] Corrected`

### ML-FF-001 — Financial fraud scam
- **Original transcript:** നിങ്ങളുടെ ബാങ്ക് അക്കൗണ്ടിൽ നിയമവിരുദ്ധ ഇടപാടുകൾ ഉണ്ടായെന്ന് പറയുന്നു. അക്കൗണ്ട് മരവിപ്പിക്കാതിരിക്കാൻ ഉടൻ പണം അടച്ച് OTP പറയുക.
- **English meaning (dataset-provided):** Not provided.
- **Expected scam:** `true`
- **Expected stages:** `accusation`, `payment_demand`
- **Expected tactics:** `urgency`, `credential_harvesting`, `payment_pressure`
- **Native correction / naturalness notes:** ______________________________________________
- **Label verification:** Scam `[ ] Confirmed [ ] Corrected`; stages `[ ] Confirmed [ ] Corrected`; tactics `[ ] Confirmed [ ] Corrected`

### ML-GB-001 — Genuine banking conversation
- **Original transcript:** ബാങ്കിന്റെ ഔദ്യോഗിക ആപ്പിൽ സാധാരണ UPI ഇടപാട് പരിശോധിച്ചു. ഇടപാട് പൂർത്തിയായെന്നും OTP ആരോടും പങ്കിടരുതെന്നും സഹായ കേന്ദ്രം അറിയിച്ചു.
- **English meaning (dataset-provided):** Not provided.
- **Expected scam:** `false`
- **Expected stages:** None
- **Expected tactics:** None
- **Native correction / naturalness notes:** ______________________________________________
- **Label verification:** Non-scam label `[ ] Confirmed [ ] Corrected`

### ML-PV-001 — Legitimate police verification discussion
- **Original transcript:** പാസ്‌പോർട്ട് പരിശോധനയ്ക്കായി നിശ്ചയിച്ച സമയത്ത് പൊലീസ് സ്റ്റേഷനിൽ പോയി. ഉദ്യോഗസ്ഥൻ തിരിച്ചറിയൽ പരിശോധിച്ച് നടപടിക്രമം വിശദീകരിച്ചു.
- **English meaning (dataset-provided):** Not provided.
- **Expected scam:** `false`
- **Expected stages:** None
- **Expected tactics:** None
- **Native correction / naturalness notes:** ______________________________________________
- **Label verification:** Non-scam label `[ ] Confirmed [ ] Corrected`

### ML-OTP-001 — Protective OTP/security warning
- **Original transcript:** സുരക്ഷാ മുന്നറിയിപ്പ്: നിങ്ങളുടെ OTP, PIN, പാസ്‌വേഡ് എന്നിവ ഫോണിൽ ആവശ്യപ്പെടുന്നവരുമായി പങ്കിടരുത്.
- **English meaning (dataset-provided):** Not provided.
- **Expected scam:** `false`
- **Expected stages:** None
- **Expected tactics:** None
- **Native correction / naturalness notes:** ______________________________________________
- **Label verification:** Non-scam label `[ ] Confirmed [ ] Corrected`

### ML-EDU-001 — Educational discussion about scams
- **Original transcript:** സൈബർ സുരക്ഷാ ക്ലാസിൽ ഡിജിറ്റൽ അറസ്റ്റ് തട്ടിപ്പിനെക്കുറിച്ച് സംസാരിച്ചു. ഉദാഹരണത്തിൽ വിളിക്കുന്നയാൾ പൊലീസ് ഉദ്യോഗസ്ഥനാണെന്ന് നടിച്ച് പണം ആവശ്യപ്പെടുന്നു.
- **English meaning (dataset-provided):** Not provided.
- **Expected scam:** `false`
- **Expected stages:** None
- **Expected tactics:** None
- **Native correction / naturalness notes:** ______________________________________________
- **Label verification:** Non-scam label `[ ] Confirmed [ ] Corrected`

## Indian Code-Mixed Speech

### MIX-DA-001 — Digital-arrest scam
- **Original transcript:** Cybercrime department se call kar raha hoon. Aapka Aadhaar number investigation se linked hai. Call disconnect mat kijiye aur family ko mat batayiye. Arrest avoid karne ke liye fifty thousand rupees abhi transfer kijiye.
- **English meaning (dataset-provided):** Not provided.
- **Expected scam:** `true`
- **Expected stages:** `authority_claim`, `accusation`, `isolation`, `payment_demand`
- **Expected tactics:** `urgency`, `authority_impersonation`, `payment_pressure`, `secrecy`
- **Native correction / naturalness notes:** ______________________________________________
- **Label verification:** Scam `[ ] Confirmed [ ] Corrected`; stages `[ ] Confirmed [ ] Corrected`; tactics `[ ] Confirmed [ ] Corrected`

### MIX-FF-001 — Financial fraud scam
- **Original transcript:** Aapke bank account mein suspicious transaction hua hai. Account freeze hone se bachane ke liye abhi payment karo aur apna OTP batao.
- **English meaning (dataset-provided):** Not provided.
- **Expected scam:** `true`
- **Expected stages:** `accusation`, `payment_demand`
- **Expected tactics:** `urgency`, `credential_harvesting`, `payment_pressure`
- **Native correction / naturalness notes:** ______________________________________________
- **Label verification:** Scam `[ ] Confirmed [ ] Corrected`; stages `[ ] Confirmed [ ] Corrected`; tactics `[ ] Confirmed [ ] Corrected`

### MIX-GB-001 — Genuine banking conversation
- **Original transcript:** Maine bank ke official app mein apna UPI transfer check kiya. Support ne bola transaction complete hai aur OTP kisi ke saath share nahi karna.
- **English meaning (dataset-provided):** Not provided.
- **Expected scam:** `false`
- **Expected stages:** None
- **Expected tactics:** None
- **Native correction / naturalness notes:** ______________________________________________
- **Label verification:** Non-scam label `[ ] Confirmed [ ] Corrected`

### MIX-PV-001 — Legitimate police verification discussion
- **Original transcript:** Passport verification ke liye police station par appointment tha. Officer ne identity check ki aur normal process explain kiya.
- **English meaning (dataset-provided):** Not provided.
- **Expected scam:** `false`
- **Expected stages:** None
- **Expected tactics:** None
- **Native correction / naturalness notes:** ______________________________________________
- **Label verification:** Non-scam label `[ ] Confirmed [ ] Corrected`

### MIX-OTP-001 — Protective OTP/security warning
- **Original transcript:** Bank ka security message hai: apna OTP, PIN ya password kisi caller ko kabhi share mat karo. Official app use karo.
- **English meaning (dataset-provided):** Not provided.
- **Expected scam:** `false`
- **Expected stages:** None
- **Expected tactics:** None
- **Native correction / naturalness notes:** ______________________________________________
- **Label verification:** Non-scam label `[ ] Confirmed [ ] Corrected`

### MIX-EDU-001 — Educational discussion about scams
- **Original transcript:** Scam awareness class mein ek example script discuss ki: caller bolta hai 'This is the police', investigation ka dar dikhata hai aur payment maangta hai.
- **English meaning (dataset-provided):** Not provided.
- **Expected scam:** `false`
- **Expected stages:** None
- **Expected tactics:** None
- **Native correction / naturalness notes:** ______________________________________________
- **Label verification:** Non-scam label `[ ] Confirmed [ ] Corrected`
