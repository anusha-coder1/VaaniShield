import re

from models.schemas import AnalysisResult, RiskLevel


_AUTHORITY_PATTERNS = (
	re.compile(
		r"\b(?:this is|i am|i'm|we are|we're|calling from)\s+"
		r"(?:an?\s+)?(?:the\s+)?(?:police(?: department)?|law enforcement|"
		r"cyber[- ]?crime (?:unit|department)|federal (?:agent|officer)|"
		r"central bureau of investigation)\b",
		re.IGNORECASE,
	),
	re.compile(
		r"\b(?:officer|agent)\s+(?:from|with)\s+(?:the\s+)?"
		r"(?:police|law enforcement|cyber[- ]?crime (?:unit|department))\b",
		re.IGNORECASE,
	),
	re.compile(
		r"\byou are speaking to\s+(?:the\s+)?"
		r"(?:police|law enforcement|cyber[- ]?crime (?:unit|department))\b",
		re.IGNORECASE,
	),
)

_CREDENTIAL_NEGATION_PATTERN = re.compile(
	r"\b(?:never|do not|don't|should not|shouldn't|must not|mustn't|"
	r"will not|won't|cannot|can't)\b(?:\s+\w+){0,2}\s*$",
	re.IGNORECASE,
)
_CREDENTIAL_SCOPE_BOUNDARY_PATTERN = re.compile(
	r"[.!?;,:\n]|\b(?:but|however|instead|and)\b",
	re.IGNORECASE,
)


def _is_negated_credential_request(transcript: str, match_start: int) -> bool:
	"""Check whether a credential request is locally preceded by a negation."""
	preceding_text = transcript[:match_start]
	boundaries = list(_CREDENTIAL_SCOPE_BOUNDARY_PATTERN.finditer(preceding_text))
	if boundaries:
		preceding_text = preceding_text[boundaries[-1].end():]
	return bool(_CREDENTIAL_NEGATION_PATTERN.search(preceding_text))

_STAGE_PATTERNS = {
	"authority_claim": _AUTHORITY_PATTERNS,
	"accusation": (
		re.compile(
			r"\b(?:you are|you're)\s+(?:under investigation|being investigated|"
			r"accused|charged)(?:\s+(?:for|of)\s+[\w -]{1,35})?",
			re.IGNORECASE,
		),
		re.compile(
			r"\b(?:a|an)\s+(?:criminal\s+)?case has been filed against you\b",
			re.IGNORECASE,
		),
		re.compile(
			r"\byour (?:identity|account|phone number)\s+(?:has been|was)\s+"
			r"(?:linked to|used in)\s+(?:a\s+)?(?:crime|fraud|criminal case)\b",
			re.IGNORECASE,
		),
		re.compile(
			r"\b(?:arrest warrant|warrant)\s+(?:has been\s+)?issued against you\b",
			re.IGNORECASE,
		),
	),
	"isolation": (
		re.compile(
			r"\b(?:do not|don't|never)\s+(?:tell|contact|inform)\s+"
			r"(?:anyone|anybody|your family|your friends|your bank|the police)\b",
			re.IGNORECASE,
		),
		re.compile(r"\b(?:stay|remain) on (?:the )?line\b", re.IGNORECASE),
		re.compile(r"\b(?:do not|don't) disconnect\b", re.IGNORECASE),
		re.compile(r"\bkeep this between us\b", re.IGNORECASE),
		re.compile(r"\bmove to a private (?:room|location)\b", re.IGNORECASE),
	),
	"payment_demand": (
		re.compile(
			r"\b(?:transfer|send|deposit)\s+(?:the\s+)?(?:money|funds|amount)\b",
			re.IGNORECASE,
		),
		re.compile(
			r"\b(?:pay|make)\s+(?:the\s+)?(?:payment|fine|fee)\b",
			re.IGNORECASE,
		),
		re.compile(
			r"\b(?:pay|transfer|send)\s+(?:₹|rs\.?|inr)\s?[\d,]+\b",
			re.IGNORECASE,
		),
		re.compile(
			r"\b(?:pay|transfer|send)\s+(?:the\s+)?"
			r"[\d,]+\s*(?:rupees|rs\.?|inr)\b",
			re.IGNORECASE,
		),
	),
}

_TACTIC_PATTERNS = {
	"urgency": (
		re.compile(
			r"\b(?:act now|respond immediately|right now|"
			r"within (?:the next )?\d+ (?:minutes?|hours?)|before it's too late)\b",
			re.IGNORECASE,
		),
	),
	"authority_impersonation": _AUTHORITY_PATTERNS,
	"credential_harvesting": (
		re.compile(
			r"\b(?:share|send|provide|tell me|read out|give me|reveal|disclose|"
			r"ask(?:s)? for)\s+(?:your\s+)?"
			r"(?:otp|one[ -]time password|verification code|password|pin|cvv|"
			r"card number|bank details|account details)\b",
			re.IGNORECASE,
		),
		re.compile(
			r"\b(?:enter|type)\s+(?:your\s+)?"
			r"(?:otp|password|pin|verification code)\b",
			re.IGNORECASE,
		),
	),
	"payment_pressure": (
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
	),
	"secrecy": (
		re.compile(
			r"\b(?:keep this confidential|keep this secret|do not discuss this|"
			r"don't discuss this|do not tell anyone|don't tell anyone|"
			r"do not inform your family|don't inform your family)\b",
			re.IGNORECASE,
		),
	),
}


def analyze_transcript(transcript: str) -> AnalysisResult:
	"""Return a keyword-based assessment without executing transcript content."""
	detected_stages = []
	detected_tactics = []
	phrase_matches = []

	# Keep only specific phrase matches; a bare mention of police or payment is not enough.
	for stage, patterns in _STAGE_PATTERNS.items():
		matches = [match for pattern in patterns for match in pattern.finditer(transcript)]
		if matches:
			detected_stages.append(stage)
			phrase_matches.extend((match.start(), match.group(0)) for match in matches)

	for tactic, patterns in _TACTIC_PATTERNS.items():
		matches = [match for pattern in patterns for match in pattern.finditer(transcript)]
		if tactic == "credential_harvesting":
			matches = [
				match
				for match in matches
				if not _is_negated_credential_request(transcript, match.start())
			]
		if matches:
			detected_tactics.append(tactic)
			phrase_matches.extend((match.start(), match.group(0)) for match in matches)

	# Preserve transcript order and remove duplicate matches shared by stage and tactic rules.
	exact_phrases = []
	seen_phrases = set()
	for _, phrase in sorted(phrase_matches, key=lambda item: item[0]):
		normalized_phrase = phrase.casefold()
		if normalized_phrase not in seen_phrases:
			exact_phrases.append(phrase)
			seen_phrases.add(normalized_phrase)

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
			"authority_impersonation",
			"payment_pressure",
			"secrecy",
		)
	)
	has_authority_context = "authority_claim" in detected_stages and any(
		indicator in detected_stages + detected_tactics
		for indicator in ("accusation", "isolation", "urgency", "payment_demand", "secrecy")
	)
	has_coercive_context = "accusation" in detected_stages and any(
		indicator in detected_stages + detected_tactics
		for indicator in ("isolation", "urgency", "payment_demand", "payment_pressure", "secrecy")
	)
	scam_detected = (
		has_credential_request or has_payment_context or has_authority_context or has_coercive_context
	)

	# Weights make direct money or credential requests more serious than urgency alone.
	indicator_weights = {
		"authority_claim": 1,
		"accusation": 2,
		"isolation": 1,
		"payment_demand": 3,
		"urgency": 1,
		"authority_impersonation": 2,
		"credential_harvesting": 5,
		"payment_pressure": 3,
		"secrecy": 1,
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
		confidence=confidence,
		uncertainty_note=uncertainty_note,
	)
