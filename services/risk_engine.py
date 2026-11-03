import re

from models.schemas import AnalysisResult, IndicatorEvidence, RiskLevel

from services.multilingual_patterns import (
    STAGE_PATTERNS as _MULTILINGUAL_STAGE_PATTERNS,
    TACTIC_PATTERNS as _MULTILINGUAL_TACTIC_PATTERNS,
)


_AUTHORITY_PATTERNS = (
    re.compile(r"సైబర్ క్రైమ్ విభాగం నుండి మాట్లాడుతున్నాం"),
    re.compile(
        r"\b(?:i am calling from|i'm calling from|we are calling from|"
        r"we're calling from|this is|i am|i'm|we are|we're|calling from)\s+"
        r"(?:an?\s+)?(?:the\s+)?"
        r"(?:police(?:\s+(?:investigation|crime|cybercrime)\s+"
        r"(?:unit|department|office))?|"
        r"cyber[- ]?crime\s+police\s+(?:unit|department|office)|"
        r"cyber[- ]?crime(?:\s+investigation)?\s+(?:unit|department|office)|"
        r"law enforcement|federal (?:agent|officer)|"
        r"central bureau of investigation|CBI(?:\s+(?:unit|department|office))?|"
        r"UIDAI|income tax department|reserve bank of india|"
        r"national investigation bureau|central investigation agency|"
        r"state police cyber unit|"
        r"(?:your\s+)?bank(?:'s)?\s+(?:security|verification|account recovery)\s+team|"
        r"(?:payment|account recovery)\s+support department)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:officer|agent)\s+(?:from|with)\s+(?:the\s+)?"
        r"(?:police|law enforcement|cyber[- ]?crime\s+(?:unit|department)|"
        r"CBI|national investigation bureau|central investigation agency|"
        r"national cyber investigation office)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\byou are speaking to\s+(?:the\s+)?"
        r"(?:police|law enforcement|cyber[- ]?crime\s+(?:unit|department)|CBI)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\byour case has been transferred to (?:our|the)\s+"
        r"(?:police|cyber[- ]?crime|criminal investigation)?\s*"
        r"(?:unit|department|office)\b",
        re.IGNORECASE,
    ),

    re.compile(
        r"\b(?:i am|i'm|we are|we're|i work|we work)\s+"
        r"(?:from|with)\s+"
        r"(?:(?:your|the)\s+)?(?:bank(?:'s)?\s+)?"
        r"(?:security team|verification team|account recovery team|"
        r"payment support department)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:i represent|i work for)\s+(?:the\s+)?"
        r"(?:cyber[- ]?crime police(?:\s+department)?|"
        r"national cyber investigation office|"
        r"(?:your\s+)?bank(?:'s)?\s+"
        r"(?:verification|security|account recovery)\s+department)\b",
        re.IGNORECASE,
    ),
)

_CREDENTIAL_NEGATION_PATTERN = re.compile(
	r"(?:\b(?:never|do not|don't|should not|shouldn't|must not|mustn't|"
	r"will not|won't|cannot|can't|not to)\b(?:\s+\w+){0,2}\s*$|"
	r"చెప్పవద్దు\s*$)",
	re.IGNORECASE,
)
_CREDENTIAL_SCOPE_BOUNDARY_PATTERN = re.compile(
	r"[.!?;,:\n]|\b(?:but|however|instead|and)\b",
	re.IGNORECASE,
)
_EDUCATIONAL_SCOPE_BOUNDARY_PATTERN = re.compile(
	r"[.!?;\n]|\b(?:but|however|instead)\b",
	re.IGNORECASE,
)
_EDUCATIONAL_CONTEXT_PATTERN = re.compile(
	r"\b(?:scam|fraud|cybercrime)[ -]awareness(?:\s+(?:class|lesson|training|exercise))?\b|"
	r"\b(?:educational|training|cybersecurity)\s+"
	r"(?:example|discussion|scenario|class|lesson|exercise|material)\b|"
	r"\b(?:example|sample|hypothetical)\s+(?:scam|fraud|call|script|phrase)\b|"
	r"\b(?:for example|example script|sample script)\b|"
	r"\bscammers?\s+(?:often\s+)?(?:say|claim|pretend|ask|use)\b|"
	r"\bscammers?\s+(?:may|might|can|often)\s+impersonate\b|"
	r"\b(?:a\s+)?criminals?\s+(?:may|might|can|often)\b|"
	r"\b(?:teaching|learning|discussing)\s+about\s+(?:scams?|fraud|digital arrests?)\b|"
	r"సైబర్ భద్రత తరగతిలో|డిజిటల్ అరెస్ట్ మోసాల గురించి చర్చించాము",
	re.IGNORECASE,
)

_NUMBER_WORD_PATTERN = (
	r"(?:zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
	r"thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|"
	r"thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|"
	r"lakh|lakhs|crore|crores|and)"
)
_CURRENCY_AMOUNT_PATTERN = (
	r"(?:₹\s*[\d,]+|(?:rs\.?|inr)\s*[\d,]+|"
	r"[\d,]+\s*(?:rupees?|rs\.?|inr)|"
	rf"{_NUMBER_WORD_PATTERN}(?:[\s-]+{_NUMBER_WORD_PATTERN}){{0,5}}\s+rupees?)"
)


def _is_negated_credential_request(transcript: str, match_start: int) -> bool:
	"""Check whether a credential request is locally preceded by a negation."""
	preceding_text = transcript[:match_start]
	boundaries = list(_CREDENTIAL_SCOPE_BOUNDARY_PATTERN.finditer(preceding_text))
	if boundaries:
		preceding_text = preceding_text[boundaries[-1].end():]
	return bool(_CREDENTIAL_NEGATION_PATTERN.search(preceding_text))


def _is_negated_remote_access_request(transcript: str, match_start: int) -> bool:
	"""Check whether a remote-access instruction is locally preceded by a warning."""
	preceding_text = transcript[:match_start]
	boundaries = list(_CREDENTIAL_SCOPE_BOUNDARY_PATTERN.finditer(preceding_text))
	if boundaries:
		preceding_text = preceding_text[boundaries[-1].end():]
	return bool(_CREDENTIAL_NEGATION_PATTERN.search(preceding_text))


def _is_educational_match(transcript: str, match_start: int) -> bool:
	"""Ignore a match only when its current clause is explicitly educational."""
	preceding_text = transcript[:match_start]
	boundaries = list(_EDUCATIONAL_SCOPE_BOUNDARY_PATTERN.finditer(preceding_text))
	if boundaries:
		preceding_text = preceding_text[boundaries[-1].end():]
	return bool(_EDUCATIONAL_CONTEXT_PATTERN.search(preceding_text))


_STAGE_PATTERNS = {
	"authority_claim": _AUTHORITY_PATTERNS,
	"accusation": (
		re.compile(r"ఆధార్ నంబర్ క్రిమినల్ దర్యాప్తుతో సంబంధం"),
		re.compile(
			r"\b(?:you are|you're)\s+(?:under investigation|being investigated|"
			r"accused|charged)(?:\s+(?:for|of)\s+[\w -]{1,35})?",
			re.IGNORECASE,
		),
		re.compile(
			r"\b(?:you are|you're)\s+(?:under|facing|involved in|part of)\s+"
			r"(?:a\s+)?(?:(?:serious|criminal|cybercrime|fraud)\s+){1,2}"
			r"investigation(?:\s+(?:for|into|involving)\s+[\w -]{1,45})?\b",
			re.IGNORECASE,
		),
		re.compile(
			r"\b(?:a|an)\s+(?:criminal\s+)?case has been filed against you\b",
			re.IGNORECASE,
		),
		re.compile(
			r"\byour\s+(?:(?:aadhaar|aadhar|pan)(?:\s+number)?|bank account|"
			r"identity|account|phone number)(?:\s+\[REDACTED_AADHAAR\])?\s+"
			r"(?:is|was|has been)\s+"
			r"(?:linked to|involved in|used in|used for)\s+(?:a\s+)?"
			r"(?:(?:serious|illegal|suspicious|criminal|financial)\s+){0,2}"
			r"(?:criminal investigation|investigation|transactions?|money laundering|"
			r"financial crime|crime|fraud)\b",
			re.IGNORECASE,
		),
		re.compile(
			r"\byou (?:are|have been) suspected of "
			r"(?:participating in|being involved in|involvement in) "
			r"(?:a\s+)?(?:financial crime|money laundering|fraud|illegal transactions?)\b",
			re.IGNORECASE,
		),
		re.compile(
			r"\b(?:arrest warrant|warrant)\s+(?:has been\s+)?issued against you\b",
			re.IGNORECASE,
	),

                re.compile(
                        r"\byour\s+(?:identity|identity documents)\s+"
                        r"(?:has|have|was|were)\s+(?:been\s+)?"
                        r"(?:linked to|used to open)\s+"
                        r"(?:an?\s+)?(?:international\s+)?"
                        r"(?:money laundering|suspicious|criminal)\s+"
                        r"(?:case|account)\b",
                        re.IGNORECASE,
                ),
                re.compile(
                        r"\byour\s+bank account\s+is suspected of\s+"
                        r"(?:funding|supporting)\s+(?:a\s+)?criminal network\b",
                        re.IGNORECASE,
                ),
                re.compile(
                        r"\b(?:a\s+)?(?:parcel|package)\s+registered in your name\s+"
                        r"contains?\s+(?:illegal|prohibited|criminal) documents\b",
                        re.IGNORECASE,
                ),
		),
	"isolation": (
		re.compile(r"కాల్ కట్ చేయకండి"),
		re.compile(r"కుటుంబానికి చెప్పకండి"),
		re.compile(
			r"\b(?:do not|don't|never)\s+(?:tell|contact|inform)\s+"
			r"(?:anyone|anybody|your family|your friends|your bank|the police)\b",
			re.IGNORECASE,
		),
		re.compile(r"\b(?:stay|remain) on (?:the )?line\b", re.IGNORECASE),
		re.compile(r"\b(?:do not|don't) disconnect(?: this call| the call)?\b", re.IGNORECASE),
		re.compile(r"\bkeep this between us\b", re.IGNORECASE),
		re.compile(r"\bmove to a private (?:room|location)\b", re.IGNORECASE),
		re.compile(
			r"\b(?:you must|you have to|you need to|must|have to) remain "
			r"on (?:a |the )?video call\b",
			re.IGNORECASE,
		),
		re.compile(
			r"\b(?:do not|don't|must not|mustn't) discuss "
			r"(?:this\s+)?(?:investigation|case|conversation) "
			r"with (?:anyone|anybody|your family|your friends)\b",
			re.IGNORECASE,
		),
                re.compile(
                        r"\b(?:must not|mustn't|do not|don't)\s+"
                        r"(?:contact|call|speak to)\s+"
                        r"(?:anyone|anybody|your family|your relatives|your friends)\b",
                        re.IGNORECASE,
                ),
                re.compile(
                        r"\b(?:stay|remain)\s+alone\s+"
                        r"(?:in front of|before)\s+(?:the\s+)?camera\b",
                        re.IGNORECASE,
                ),
                re.compile(
                        r"\b(?:are not allowed to|aren't allowed to|"
                        r"must not|mustn't|do not|don't)\s+"
                        r"discuss\s+(?:this|the matter|the investigation|the case)\s+"
                        r"with\s+(?:anyone|anybody|your relatives|your family|your friends)\b",
                        re.IGNORECASE,
                ),
	),
	"payment_demand": (
		re.compile(r"డబ్బు బదిలీ చేయండి"),
		re.compile(
			r"\b(?:transfer|send|deposit)\s+(?:the\s+)?(?:money|funds|amount)\b",
			re.IGNORECASE,
		),
		re.compile(
			r"\b(?:pay|make)\s+(?:the\s+)?(?:payment|fine|fee|security deposit)\b",
			re.IGNORECASE,
		),
		re.compile(
			rf"\b(?:pay|transfer|send|deposit)\s+(?:the\s+)?"
			rf"{_CURRENCY_AMOUNT_PATTERN}\b",
			re.IGNORECASE,
		),
		re.compile(
			r"\b(?:send|transfer|pay)\s+(?:the\s+)?(?:money|funds|amount)\s+"
			r"to (?:this|the|our) (?:verification|bank|beneficiary)?\s*account\b",
			re.IGNORECASE,
		),
		re.compile(
			r"\b(?:transfer|send|pay)\s+(?:the\s+)?(?:amount|money|funds)\s+"
			r"to avoid arrest\b",
			re.IGNORECASE,
		),
                re.compile(
                        r"\b(?:transfer|send|deposit|pay)\s+"
                        r"(?:the\s+)?(?:verification|investigation|security clearance|"
                        r"security)\s+(?:deposit|fee|payment|amount)\b",
                        re.IGNORECASE,
                ),
                re.compile(
                        r"\b(?:transfer|send|deposit)\s+"
                        r"(?:your\s+)?(?:savings|funds|money)\b"
                        r"|\b(?:send|transfer)\s+(?:a\s+)?(?:small\s+)?"
                        r"verification transfer\b",
                        re.IGNORECASE,
                ),

	),
}

_TACTIC_PATTERNS = {
	"urgency": (
		re.compile(r"వెంటనే"),
		re.compile(r"ఇప్పుడే"),
		re.compile(
			r"\b(?:act now|respond immediately|right now|"
			r"within (?:the next )?\d+ (?:minutes?|hours?)|before it's too late)\b",
			re.IGNORECASE,
		),
		re.compile(
			r"\bwithin (?:the next )?(?:one|two|three|four|five|ten|fifteen|"
			r"twenty|thirty) minutes?\b",
			re.IGNORECASE,
		),
		re.compile(
			rf"\b(?:you have|you've got)\s+(?:only\s+)?(?:\d+|"
			rf"{_NUMBER_WORD_PATTERN}(?:[\s-]+{_NUMBER_WORD_PATTERN}){{0,2}})\s+"
			r"minutes?\b",
			re.IGNORECASE,
		),
		re.compile(r"\bimmediately\b", re.IGNORECASE),
		re.compile(
            r"\b(?:arrested|detained|jailed)\s+today\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\b(?:account|card)\s+(?:will|shall)\s+be\s+"
            r"(?:blocked|suspended|frozen)\s+unless\b",
            re.IGNORECASE,
        ),
	),
	"authority_based_coercion": (),
	"remote_access_control": (
		re.compile(
			r"\b(?:install|download)\s+(?:(?:this|the)\s+)?"
			r"(?:remote[- ]access|remote[- ]control)\s+"
			r"(?:application|app|software|program)\b",
			re.IGNORECASE,
		),
		re.compile(
			r"\b(?:give|grant|allow)\s+(?:me|us|them)\s+"
			r"(?:remote\s+)?(?:access|control)\s+(?:to|of)\s+"
			r"(?:your\s+)?(?:phone|device|computer)\b",
			re.IGNORECASE,
		),
		re.compile(
			r"\b(?:let|allow)\s+(?:me|us|them)\s+(?:to\s+)?"
			r"(?:control|access)\s+(?:your\s+)?(?:phone|device|computer)\b",
			re.IGNORECASE,
		),
		re.compile(
			r"\b(?:enable|turn on|activate)\s+(?:the\s+)?remote\s+"
			r"(?:access|control)\s+(?:on|for)\s+"
			r"(?:your\s+)?(?:phone|device|computer)\b",
			re.IGNORECASE,
		),
		re.compile(
			r"\b(?:install|download)\s+"
			r"(?:anydesk|teamviewer|quick\s*support)\b",
			re.IGNORECASE,
		),
	),
	"credential_harvesting": (
		re.compile(r"మీ\s+OTP\s+చెప్ప(?:ండి|వద్దు)"),
		re.compile(
			r"\b(?:share|send|provide|tell me|read out|give me|reveal|disclose|"
			r"ask(?:s)? for)\s+(?:your\s+|an?\s+)?"
			r"(?:otp|one[ -]time password|verification code|password|pin|cvv|"
			r"card number|bank details|account details)\b",
			re.IGNORECASE,
		),
		re.compile(
			r"\b(?:enter|type)\s+(?:your\s+)?"
			r"(?:otp|password|pin|verification code)\b",
			re.IGNORECASE,
		),
		re.compile(
            r"\bconfirm\s+(?:the\s+)?(?:your\s+)?otp\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\bread\s+(?:out\s+)?(?:all\s+)?(?:the\s+)?"
            r"(?:six|6)\s+digits\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"\b(?:enter|type)\s+(?:your\s+)?upi\s+pin\b",
            re.IGNORECASE,
        ),
	),
	"payment_pressure": (
		re.compile(r"అరెస్టు తప్పించుకోవడానికి\s+వెంటనే\s+డబ్బు బదిలీ చేయండి"),
		re.compile(r"ఖాతా నిలిపివేయకుండా ఉండాలంటే"),
		re.compile(r"\bpay (?:now|immediately|right now)\b", re.IGNORECASE),
		re.compile(
			r"\b(?:pay|transfer) (?:the )?money (?:now|immediately)\b",
			re.IGNORECASE,
		),
		re.compile(
			r"\bpay or (?:you will|you'll|we will|we'll) (?:be )?"
			r"(?:arrested|jailed|charged)\b",
			re.IGNORECASE,
		),
		re.compile(r"\bpay (?:the )?(?:fine|fee) to avoid arrest\b", re.IGNORECASE),
		re.compile(
			r"\b(?:pay|transfer) (?:the )?money\b[^.!?\n]{0,60}"
			r"\b(?:or else|otherwise|or you will|or you'll|or we will|or we'll|"
			r"or face|to avoid)\b[^.!?\n]{0,50}"
			r"\b(?:arrest(?:ed)?|jail(?:ed)?|charged|legal action)\b",
			re.IGNORECASE,
		),
		re.compile(
			r"\bpay (?:the )?(?:fine|fee|security deposit|payment)\b"
			r"[^.!?\n]{0,60}\b(?:or else|otherwise|or you will|or you'll|"
			r"or we will|or we'll|or face|to avoid)\b[^.!?\n]{0,50}"
			r"\b(?:arrest(?:ed)?|jail(?:ed)?|charged|legal action|prosecution)\b",
			re.IGNORECASE,
		),
		re.compile(
			r"\bpay or (?:you will|you'll|we will|we'll) (?:be )?"
			r"(?:arrested|jailed|charged)\b",
			re.IGNORECASE,
		),
		re.compile(r"\bpay (?:the )?(?:fine|fee) to avoid arrest\b", re.IGNORECASE),
		re.compile(
			rf"\b(?:pay|transfer|send|deposit)\s+(?:the\s+)?"
			rf"{_CURRENCY_AMOUNT_PATTERN}\b[^.!?\n]{{0,80}}"
			r"\b(?:to avoid|otherwise|or else|or you will|or you'll|or we will|"
			r"or we'll|or face)\b[^.!?\n]{0,50}"
			r"\b(?:arrest(?:ed)?|jail(?:ed)?|prosecution|legal action|penalty)\b",
			re.IGNORECASE,
		),
		re.compile(
			r"\b(?:pay|transfer|send|deposit)\s+(?:the\s+)?(?:amount|money|funds)\s+"
			r"to avoid arrest\b",
			re.IGNORECASE,
		),
		re.compile(
			r"\b(?:pay|make)\s+(?:the\s+)?security deposit\b[^.!?\n]{0,30}"
			r"\b(?:immediately|now|today|right away)\b",
			re.IGNORECASE,
		),
		re.compile(
			r"\b(?:your )?(?:bank )?account (?:will|shall) remain frozen "
			r"until (?:payment|you pay|the payment)\b",
			re.IGNORECASE,
		),

        re.compile(
            r"\b(?:transfer|send|deposit|pay)\b[^.!?\n]{0,100}"
            r"\b(?:or you will|or you'll|or we will|or we'll|to avoid|to prevent)\b"
            r"[^.!?\n]{0,60}\b(?:be arrested|arrested|arrest|detention|detained|"
            r"jailed|jail|legal action)\b",
            re.IGNORECASE,
        ),

	),
	"secrecy": (
		re.compile(
            r"\b(?:or|and)\s+(?:(?:do not|don't|must not|mustn't)\s+)?"
            r"(?:tell|inform)\s+(?:anyone|anybody|your family|your friends)"
            r"(?:\s+about\s+(?:this|the)\s+(?:investigation|case))?\b",
            re.IGNORECASE,
        ),
		re.compile(r"కుటుంబానికి చెప్పకండి"),
		re.compile(
			r"\b(?:keep this confidential|keep this secret|do not discuss this|"
			r"don't discuss this|do not tell anyone|don't tell anyone|"
			r"do not inform your family|don't inform your family)\b",
			re.IGNORECASE,
		),
		re.compile(
			r"\b(?:confidential investigation|keep (?:this|the investigation|"
			r"this investigation) confidential|(?:this|the) investigation is "
			r"(?:strictly )?confidential)\b",
			re.IGNORECASE,
		),
		re.compile(
			r"\b(?:do not|don't|must not|mustn't) discuss "
			r"(?:this\s+)?(?:investigation|case|conversation) "
			r"with (?:anyone|anybody|your family|your friends)\b",
			re.IGNORECASE,
		),
	    re.compile(
            r"\b(?:you are not allowed to|you must not|you cannot|"
            r"you can't|do not|don't)\s+"
            r"discuss\s+(?:this|the matter|the investigation|the case)\s+"
            r"with\s+(?:anyone|anybody|your relatives|your family|your friends)\b",
            re.IGNORECASE,
        ),
	),
}

# Extend existing indicator patterns with provisional multilingual patterns.
for _indicator, _patterns in _MULTILINGUAL_STAGE_PATTERNS.items():
    _STAGE_PATTERNS[_indicator] += _patterns

for _indicator, _patterns in _MULTILINGUAL_TACTIC_PATTERNS.items():
    _TACTIC_PATTERNS[_indicator] += _patterns


_INDICATOR_EXPLANATIONS = {
	"authority_claim": (
		"This phrase presents the caller as an official or institutional representative.",
		"It could establish false credibility; verify the caller through independently sourced details.",
	),
	"accusation": (
		"This phrase alleges that the person or their identity is linked to a crime or investigation.",
		"It may be intended to create fear; an accusation alone is not proof of wrongdoing.",
	),
	"isolation": (
		"This phrase discourages ending the call or consulting other people.",
		"It may limit time for independent verification or trusted advice.",
	),
	"payment_demand": (
		"This phrase requests a payment, transfer, or security deposit.",
		"Pause before sending money and verify the request with the institution independently.",
	),
	"urgency": (
		"This phrase creates time pressure or asks for immediate action.",
		"Time pressure can make independent verification more difficult.",
	),
	"authority_based_coercion": (
		"This phrase uses language associated with an official authority or agency.",
		"A caller's claimed role should be verified through an official number you find yourself.",
	),
	"credential_harvesting": (
		"This phrase asks for a credential such as an OTP, PIN, password, or account detail.",
		"Sharing authentication details can put accounts at risk; legitimate support should not need your OTP or PIN.",
	),
	"payment_pressure": (
		"This phrase connects a payment request to urgency, a threat, or another consequence.",
		"Do not transfer money based only on a caller's demand; verify the situation independently.",
	),
	"secrecy": (
		"This phrase asks that the matter or investigation be kept confidential.",
		"Secrecy may discourage outside advice or independent checks.",
	),
	"remote_access_control": (
		"This phrase asks the recipient to install remote-access software or give another person control of a device.",
		"Remote device access may expose private information or allow unauthorised actions. End the session and verify support independently.",
	),
}


def _select_non_redundant_matches(matches):
	"""Prefer complete phrases while retaining separate, non-contained evidence."""
	unique_matches = {}
	for start, end, phrase in matches:
		unique_matches[(start, end, phrase.casefold())] = (start, end, phrase)

	selected = []
	for candidate in sorted(unique_matches.values(), key=lambda item: (item[0], -item[1])):
		start, end, _ = candidate
		if any(existing_start <= start and existing_end >= end for existing_start, existing_end, _ in selected):
			continue
		selected = [
			existing
			for existing in selected
			if not (start <= existing[0] and end >= existing[1])
		]
		selected.append(candidate)

	return sorted(selected, key=lambda item: (item[0], item[1]))


def analyze_transcript(transcript: str) -> AnalysisResult:
	"""Return a keyword-based assessment without executing transcript content."""
	detected_stages = []
	detected_tactics = []
	indicator_matches = {}

	# Keep only specific phrase matches; a bare mention of police or payment is not enough.
	for stage, patterns in _STAGE_PATTERNS.items():
		matches = [
			match
			for pattern in patterns
			for match in pattern.finditer(transcript)
			if not _is_educational_match(transcript, match.start())
		]
		if matches:
			detected_stages.append(stage)
			indicator_matches[stage] = matches

	for tactic, patterns in _TACTIC_PATTERNS.items():
		matches = [
			match
			for pattern in patterns
			for match in pattern.finditer(transcript)
			if not _is_educational_match(transcript, match.start())
		]
		if tactic == "credential_harvesting":
			matches = [
				match
				for match in matches
				if not _is_negated_credential_request(transcript, match.start())
			]
		if tactic == "remote_access_control":
			matches = [
				match
				for match in matches
				if not _is_negated_remote_access_request(transcript, match.start())
			]
		if matches:
			detected_tactics.append(tactic)
			indicator_matches[tactic] = matches

	# A claimed authority requires separate coercive behaviour.
	authority_coercion_context_indicators = (
		"isolation",
		"secrecy",
		"credential_harvesting",
		"payment_pressure",
		"remote_access_control",
	)
	if "authority_claim" in detected_stages and any(
	    indicator in detected_stages + detected_tactics
	    for indicator in authority_coercion_context_indicators
	):
	    detected_tactics.append("authority_based_coercion")
	    context_matches = [
	        match
	        for indicator in authority_coercion_context_indicators
	        for match in indicator_matches.get(indicator, [])
	    ]
	    indicator_matches["authority_based_coercion"] = (
	        indicator_matches["authority_claim"] + context_matches
	    )

	# Remove only fully contained phrase matches; independent evidence stays separate.
	all_matches = [
		(match.start(), match.end(), match.group(0))
		for matches in indicator_matches.values()
		for match in matches
	]
	selected_matches = _select_non_redundant_matches(all_matches)
	exact_phrases = [phrase for _, _, phrase in selected_matches]

	indicator_evidence = []
	for indicator in detected_stages + detected_tactics:
		matches = indicator_matches[indicator]
		supporting_phrases = [
			phrase
			for phrase_start, phrase_end, phrase in selected_matches
			if any(phrase_start <= match.start() and phrase_end >= match.end() for match in matches)
		]
		if not supporting_phrases:
			continue
		explanation, potential_risk = _INDICATOR_EXPLANATIONS[indicator]
		indicator_evidence.append(
			IndicatorEvidence(
				indicator=indicator,
				exact_phrases=supporting_phrases,
				explanation=explanation,
				potential_risk=potential_risk,
			)
		)

	# An explicit request for credentials is strong evidence; other findings need
	# coercive or deceptive context before they produce a scam verdict.
	has_credential_request = "credential_harvesting" in detected_tactics
	has_payment_context = "payment_demand" in detected_stages and any(
		indicator in detected_stages + detected_tactics
		for indicator in (
			"authority_claim",
			"accusation",
			"isolation",
			"urgency",
			"authority_based_coercion",
			"payment_pressure",
			"secrecy",
		)
	)
	has_authority_context = "authority_claim" in detected_stages and any(
		indicator in detected_stages + detected_tactics
		for indicator in ("accusation", "isolation", "urgency", "payment_demand", "secrecy", "remote_access_control")
	)
	has_coercive_context = "accusation" in detected_stages and any(
		indicator in detected_stages + detected_tactics
		for indicator in ("isolation", "urgency", "payment_demand", "payment_pressure", "secrecy", "remote_access_control")
	)
	has_remote_access_context = "remote_access_control" in detected_tactics and any(
		indicator in detected_stages + detected_tactics
		for indicator in (
			"authority_claim", "accusation", "isolation", "urgency",
			"secrecy", "credential_harvesting", "payment_demand", "payment_pressure",
		)
	)
	scam_detected = (
		has_credential_request or has_payment_context or has_authority_context
		or has_coercive_context or has_remote_access_context
	)

	# Keep the existing indicator weights and risk thresholds unchanged.
	indicator_weights = {
		"authority_claim": 1,
		"accusation": 2,
		"isolation": 1,
		"payment_demand": 3,
		"urgency": 1,
		"authority_based_coercion": 2,
		"credential_harvesting": 5,
		"payment_pressure": 3,
		"secrecy": 1,
		"remote_access_control": 4,
	}
	risk_score = sum(
		indicator_weights[indicator]
		for indicator in detected_stages + detected_tactics
	)

	if risk_score >= 9:
		risk_level = RiskLevel.CRITICAL
	elif risk_score >= 5:
		risk_level = RiskLevel.HIGH
	elif risk_score >= 2:
		risk_level = RiskLevel.MEDIUM
	else:
		risk_level = RiskLevel.LOW

	indicator_count = len(detected_stages) + len(detected_tactics)
	if scam_detected:
		confidence = min(0.9, 0.55 + 0.05 * max(0, indicator_count - 1))
	else:
		confidence = 0.3 if indicator_count else 0.1

	uncertainty_note = (
		"This is a basic keyword baseline, not a reliable final scam verdict. "
		"It can miss unfamiliar wording and may flag legitimate conversations "
		"that contain similar phrases."
	)

	return AnalysisResult(
		scam_detected=scam_detected,
		risk_level=risk_level,
		stages_detected=detected_stages,
		tactics_detected=detected_tactics,
		exact_phrases=exact_phrases,
		indicator_evidence=indicator_evidence,
		confidence=confidence,
		uncertainty_note=uncertainty_note,
	)
