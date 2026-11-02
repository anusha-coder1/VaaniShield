import re

# Provisional multilingual patterns.
# These patterns are based on synthetic examples and require native-speaker review.

STAGE_PATTERNS = {
    "authority_claim": (
        re.compile(r"साइबर अपराध विभाग से कॉल है"),
        re.compile(r"சைபர் குற்றப் பிரிவிலிருந்து பேசுகிறோம்"),
        re.compile(r"സൈബർ ക്രൈം വിഭാഗത്തിൽ നിന്നാണ് വിളിക്കുന്നത്"),
        re.compile(r"\bcybercrime department se call kar raha hoon\b", re.I),
    ),
    "accusation": (
        re.compile(r"बैंक खाते में अवैध लेन-देन होने का आरोप है"),
        re.compile(r"வங்கிக் கணக்கில் சட்டவிரோத பரிவர்த்தனைகள் நடந்ததாக"),
        re.compile(r"ബാങ്ക് അക്കൗണ്ടിൽ നിയമവിരുദ്ധ ഇടപാടുകൾ ഉണ്ടായെന്ന്"),
        re.compile(r"आधार नंबर आपराधिक जांच से जुड़ा"),
        re.compile(r"குற்ற விசாரணையுடன் இணைக்கப்பட்டதாக"),
        re.compile(r"ക്രിമിനൽ അന്വേഷണവുമായി ബന്ധിപ്പിച്ചെന്ന്"),
        re.compile(r"\baadhaar number investigation se linked hai\b", re.I),
        re.compile(r"\bbank account mein suspicious transaction hua hai\b", re.I),
        re.compile(r"అనుమానాస్పద లావాదేవీలు ఉన్నాయని"),
    ),
    "isolation": (
        re.compile(r"कॉल न काटें"),
        re.compile(r"परिवार को न बताएं"),
        re.compile(r"அழைப்பை துண்டிக்காதீர்கள்"),
        re.compile(r"குடும்பத்திடம் சொல்லாதீர்கள்"),
        re.compile(r"കോൾ വിച്ഛേദിക്കരുത്"),
        re.compile(r"കുടുംബത്തോട് പറയരുത്"),
        re.compile(r"\bcall disconnect mat kijiye\b", re.I),
        re.compile(r"\bfamily ko mat batayiye\b", re.I),
    ),
    "payment_demand": (
        re.compile(r"पचास हजार रुपये भेजें"),
        re.compile(r"अभी भुगतान करें"),
        re.compile(r"உடனே பணத்தை மாற்றுங்கள்"),
        re.compile(r"உடனே பணம் செலுத்தி"),
        re.compile(r"ഉടൻ പണം കൈമാറുക"),
        re.compile(r"ഉടൻ പണം അടച്ച്"),
        re.compile(r"\bfifty thousand rupees abhi transfer kijiye\b", re.I),
        re.compile(r"\babhi payment karo\b", re.I),
        re.compile(r"ఇప్పుడే చెల్లించి"),
    ),
}

TACTIC_PATTERNS = {
    "urgency": (
        re.compile(r"तुरंत"),
        re.compile(r"अभी"),
        re.compile(r"உடனே"),
        re.compile(r"உடனே"),
        re.compile(r"ഉടൻ"),
        re.compile(r"\babhi\b", re.I),
    ),
    "credential_harvesting": (
        re.compile(r"अपना OTP बताएं"),
        re.compile(r"OTP-ஐ பகிருங்கள்"),
        re.compile(r"OTP പറയുക"),
        re.compile(r"\bapna OTP batao\b", re.I),
    ),
    "payment_pressure": (
        re.compile(r"गिरफ्तारी से बचने के लिए"),
        re.compile(r"खाता बंद होने से बचाने के लिए"),
        re.compile(r"கைது தவிர்க்க"),
        re.compile(r"கணக்கு முடக்கப்படாமல் இருக்க"),
        re.compile(r"അറസ്റ്റ് ഒഴിവാക്കാൻ"),
        re.compile(r"അക്കൗണ്ട് മരവിപ്പിക്കാതിരിക്കാൻ"),
        re.compile(r"\barrest avoid karne ke liye\b", re.I),
        re.compile(r"\baccount freeze hone se bachane ke liye\b", re.I),
    ),
    "secrecy": (
        re.compile(r"परिवार को न बताएं"),
        re.compile(r"குடும்பத்திடம் சொல்லாதீர்கள்"),
        re.compile(r"குடும்பத்திடம் சொல்லாதீர்கள்"),
        re.compile(r"കുടുംബത്തോട് പറയരുത്"),
        re.compile(r"family ko mat batayiye", re.I),
        re.compile(r"इस मामले को गोपनीय रखें"),
        re.compile(r"இந்த விஷயத்தை ரகசியமாக வைத்திருங்கள்"),
        re.compile(r"ഈ കാര്യം രഹസ്യമായി സൂക്ഷിക്കുക"),
    ),
}
