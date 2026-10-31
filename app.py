from datetime import datetime
from pathlib import Path

import streamlit as st

from services.analyzer import analyze


NAVIGATION_ITEMS = (
	("Dashboard", ":material/space_dashboard:", "dashboard"),
	("Analyze", ":material/manage_search:", "analyze"),
	("Threat Intelligence", ":material/policy:", "threat-intelligence"),
	("Reports", ":material/description:", "reports"),
	("How It Works", ":material/account_tree:", "how-it-works"),
)

STAGES = (
	(
		"authority_claim",
		"A caller claims to represent police, a cybercrime unit, or another authority.",
	),
	(
		"accusation",
		"The caller alleges an investigation, crime, or case involving the recipient.",
	),
	(
		"isolation",
		"The caller discourages contacting family, a bank, or another trusted person.",
	),
	(
		"payment_demand",
		"The caller demands money, a fine, or a transfer as part of the call.",
	),
)

TACTICS = (
	("urgency", "Pressure to act immediately or before a stated deadline."),
	(
		"authority_impersonation",
		"Language that presents the caller as law enforcement or another authority.",
	),
	(
		"credential_harvesting",
		"Requests for an OTP, password, PIN, CVV, or account details.",
	),
	("payment_pressure", "Threats or pressure tied directly to making a payment."),
	("secrecy", "Instructions to keep the conversation or demand confidential."),
)

STAT_ICONS = {
	"activity": (
		'<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
		'<path d="M4 19V5M4 19h16M8 15v-4m4 4V8m4 7v-6"/></svg>'
	),
	"alerts": (
		'<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
		'<path d="M12 3 19 6v5c0 4.5-2.8 7.8-7 10-4.2-2.2-7-5.5-7-10V6z"/>'
		'<path d="M12 8v4m0 3h.01"/></svg>'
	),
	"categories": (
		'<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
		'<path d="m12 3 9 5-9 5-9-5 9-5Zm-9 9 9 5 9-5m-18 4 9 5 9-5"/></svg>'
	),
}


def load_stylesheet() -> None:
	stylesheet_path = Path(__file__).resolve().parent / "assets" / "style.css"
	try:
		stylesheet = stylesheet_path.read_text(encoding="utf-8")
	except OSError:
		st.warning("The VaaniShield stylesheet could not be loaded. Default styling is active.")
	else:
		st.markdown(f"<style>{stylesheet}</style>", unsafe_allow_html=True)


def record_activity(result) -> None:
	"""Keep only non-transcript summary data for this Streamlit session."""
	activity = st.session_state.analysis_activity
	activity.append(
		{
			"time": datetime.now().astimezone().strftime("%b %d · %H:%M"),
			"risk": result.risk_level.value,
			"flagged": result.scam_detected,
			"signals": len(result.stages_detected) + len(result.tactics_detected),
		}
	)
	del activity[:-10]


def page_header(eyebrow: str, title: str, description: str) -> None:
	st.markdown(f'<div class="vs-eyebrow">{eyebrow}</div>', unsafe_allow_html=True)
	st.title(title)
	st.markdown(f'<p class="vs-page-description">{description}</p>', unsafe_allow_html=True)


def stat_card(label: str, value: str, detail: str, icon: str) -> None:
	st.markdown(
		f'<div class="vs-stat-card">'
		f'<div class="vs-stat-heading"><span class="vs-stat-icon">{icon}</span>'
		f'<span class="vs-stat-label">{label}</span></div>'
		f'<div class="vs-stat-value">{value}</div>'
		f'<div class="vs-stat-detail">{detail}</div>'
		"</div>",
		unsafe_allow_html=True,
	)


def render_dashboard() -> None:
	activity = st.session_state.analysis_activity
	alert_count = sum(item["flagged"] for item in activity)

	page_header(
		"Security overview",
		"VaaniShield",
		"A focused workspace for reviewing digital-arrest scam indicators and deciding on a safer next step.",
	)
	st.markdown(
		'<div class="vs-system-line"><span class="vs-status-dot"></span>'
		"Keyword baseline active <span class='vs-divider-dot'>·</span> "
		"No live threat feed <span class='vs-divider-dot'>·</span> "
		"Session summaries only</div>",
		unsafe_allow_html=True,
	)

	st.markdown("### Session overview")
	metric_columns = st.columns(3)
	with metric_columns[0]:
		stat_card(
			"Analyses this session",
			str(len(activity)),
			"Current browser session",
			STAT_ICONS["activity"],
		)
	with metric_columns[1]:
		stat_card(
			"Potential scam alerts",
			str(alert_count),
			"Based on current-session results",
			STAT_ICONS["alerts"],
		)
	with metric_columns[2]:
		stat_card(
			"Detection categories",
			str(len(STAGES) + len(TACTICS)),
			f"{len(STAGES)} stages · {len(TACTICS)} tactics in the baseline",
			STAT_ICONS["categories"],
		)

	st.markdown("### Recent analysis activity")
	if not activity:
		st.markdown(
			'<div class="vs-empty-state"><span class="vs-empty-icon">'
			'<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
			'<path d="M4 19V5M4 19h16M8 15v-4m4 4V8m4 7v-6"/></svg></span>'
			'<div><strong>No analyses yet</strong>'
			"<span>Run an analysis to see a short, transcript-free summary here.</span></div></div>",
			unsafe_allow_html=True,
		)
	else:
		st.caption("This session only. Transcript content is not included in this activity list.")
		for item in reversed(activity):
			outcome = "Potential scam indicators" if item["flagged"] else "No scam indicators"
			risk_class = item["risk"].lower()
			with st.container():
				when_column, outcome_column, risk_column, signal_column = st.columns(
					[1.1, 2.8, 1, 1]
				)
				with when_column:
					st.markdown(f'<span class="vs-activity-time">{item["time"]}</span>', unsafe_allow_html=True)
				with outcome_column:
					st.markdown(f"**{outcome}**")
				with risk_column:
					st.markdown(
						f'<span class="vs-risk vs-risk--{risk_class}">{item["risk"].title()}</span>',
						unsafe_allow_html=True,
					)
				with signal_column:
					st.caption(f'{item["signals"]} signals')

	st.markdown("#### Privacy by design")
	st.markdown(
		'<div class="vs-privacy-note"><span class="vs-privacy-mark">✓</span>'
		"Sensitive formats are redacted before analysis. Session activity keeps only time, risk, and signal counts; transcripts and phrases are excluded.</div>",
		unsafe_allow_html=True,
	)


def render_analysis_result(result) -> None:
	risk_class = result.risk_level.value.lower()
	status_class = "alert" if result.scam_detected else "clear"
	status_text = "Scam indicators detected" if result.scam_detected else "No scam indicators detected"

	st.markdown("### Analysis result")
	st.markdown(
		f'<div class="vs-result-banner vs-result-banner--{status_class}">'
		f"<strong>{status_text}</strong>"
		f'<span class="vs-risk vs-risk--{risk_class}">{result.risk_level.value.title()} risk</span>'
		"</div>",
		unsafe_allow_html=True,
	)

	confidence_column, stage_column, tactic_column = st.columns(3)
	with confidence_column:
		st.metric("Baseline confidence", f"{result.confidence:.0%}")
		st.progress(result.confidence)
	with stage_column:
		st.metric("Stages detected", len(result.stages_detected))
	with tactic_column:
		st.metric("Tactics detected", len(result.tactics_detected))

	st.markdown("### Indicator breakdown")
	stage_column, tactic_column = st.columns(2)
	with stage_column:
		st.markdown("#### Scam stages")
		if result.stages_detected:
			for stage in result.stages_detected:
				st.markdown(f'<span class="vs-badge">{stage.replace("_", " ").title()}</span>', unsafe_allow_html=True)
		else:
			st.caption("No stages detected.")
	with tactic_column:
		st.markdown("#### Tactics")
		if result.tactics_detected:
			for tactic in result.tactics_detected:
				st.markdown(f'<span class="vs-badge">{tactic.replace("_", " ").title()}</span>', unsafe_allow_html=True)
		else:
			st.caption("No tactics detected.")

	st.markdown("### Exact matched phrases")
	if result.exact_phrases:
		for phrase in result.exact_phrases:
			st.code(phrase, language=None)
	else:
		st.caption("No matching phrases found.")
	st.info(result.uncertainty_note)


def render_analyze() -> None:
	page_header(
		"Transcript analysis",
		"Analyze a conversation",
		"Review a suspicious call for known digital-arrest stages and coercive tactics.",
	)
	st.warning(
		"Experimental decision support only. Verify claims using official contact details you find independently. "
		"Never share an OTP, password, PIN, or transfer money based on a caller's instructions."
	)

	with st.form("transcript_analysis", clear_on_submit=False):
		transcript = st.text_area(
			"Suspicious call transcript",
			height=220,
			placeholder="Paste or type the conversation you want to review...",
			help="Do not include credentials you would not want to share. Text is not added to activity summaries or written to app files.",
			key="analysis_transcript",
		)
		submitted = st.form_submit_button(
			"Analyze Conversation",
			type="primary",
			use_container_width=True,
		)

	if not submitted:
		st.caption("The analyzer redacts common sensitive formats before keyword analysis.")
		return
	if not transcript.strip():
		st.info("Enter a transcript above to start the analysis.")
		return

	result = analyze(transcript)
	record_activity(result)
	st.divider()
	render_analysis_result(result)


def render_threat_intelligence() -> None:
	page_header(
		"Static pattern library",
		"Threat intelligence",
		"A transparent reference for the stages and tactics recognized by the current keyword baseline.",
	)
	st.info(
		"This is not a real-time threat feed. These descriptions reflect the rules currently built into VaaniShield."
	)

	st.markdown("### Digital-arrest scam stages")
	stage_columns = st.columns(2)
	for index, (name, description) in enumerate(STAGES):
		with stage_columns[index % 2]:
			st.markdown(
				f'<div class="vs-knowledge-item"><span class="vs-item-index">0{index + 1}</span>'
				f"<div><strong>{name.replace('_', ' ').title()}</strong><p>{description}</p></div></div>",
				unsafe_allow_html=True,
			)

	st.markdown("### Common tactics")
	tactic_columns = st.columns(2)
	for index, (name, description) in enumerate(TACTICS):
		with tactic_columns[index % 2]:
			st.markdown(
				f'<div class="vs-knowledge-item"><span class="vs-item-index">0{index + 1}</span>'
				f"<div><strong>{name.replace('_', ' ').title()}</strong><p>{description}</p></div></div>",
				unsafe_allow_html=True,
			)

	st.markdown("### Interpreting a match")
	st.markdown(
		"A keyword match is a cue to pause and verify, not proof of a crime or a definitive scam verdict. "
		"Legitimate conversations can contain similar language, and new scripts may use wording this baseline does not recognize."
	)


def render_reports() -> None:
	page_header(
		"Local preparation workspace",
		"Prepare a report draft",
		"Organize a concise incident summary for your own review before contacting an official reporting channel.",
	)
	st.warning(
		"Coming soon: document export, case tracking, and official reporting integrations. "
		"This page does not submit or send reports."
	)
	st.caption(
		"Drafts are generated for display in this session only. Do not enter OTPs, passwords, full card numbers, or a full call transcript."
	)

	with st.form("report_draft_form"):
		incident_date = st.date_input("Approximate incident date", value=datetime.now().date())
		incident_type = st.selectbox(
			"Type of concern",
			(
				"Impersonation of an authority",
				"Threat of arrest or investigation",
				"Demand for money or a transfer",
				"Request for a credential or OTP",
				"Other suspicious call",
			),
		)
		summary = st.text_area(
			"Brief incident summary",
			height=130,
			placeholder="Describe what happened without including passwords, OTPs, or full account numbers.",
		)
		actions_taken = st.text_area(
			"Steps already taken (optional)",
			height=90,
			placeholder="For example: ended the call, contacted the bank using its official number.",
		)
		prepare_draft = st.form_submit_button(
			"Prepare local draft",
			type="primary",
			use_container_width=True,
		)

	if prepare_draft:
		if not summary.strip():
			st.info("Add a brief summary to prepare a draft.")
		else:
			draft = (
				"SUSPICIOUS CALL INCIDENT SUMMARY\n\n"
				f"Approximate date: {incident_date.isoformat()}\n"
				f"Type of concern: {incident_type}\n\n"
				f"Incident summary:\n{summary.strip()}\n\n"
				f"Steps taken:\n{actions_taken.strip() or 'Not specified'}\n\n"
				"This is a user-prepared summary, not an official filing. Verify the correct reporting channel independently."
			)
			st.markdown("### Draft preview")
			st.code(draft, language=None)


def render_how_it_works() -> None:
	page_header(
		"Method and safeguards",
		"How VaaniShield works",
		"A small, explainable pipeline that helps surface familiar patterns without replacing human judgment.",
	)

	pipeline = (
		("01", "Transcript", "Text is provided for one analysis in the current app session."),
		("02", "Redaction", "Common Aadhaar, card, phone, and context-labeled OTP formats are replaced before analysis."),
		("03", "Keyword baseline", "Specific phrase patterns are checked for four stages and five tactics; negated credential warnings are filtered."),
		("04", "Risk summary", "Matched indicators inform a weighted risk level, confidence estimate, and uncertainty note."),
	)

	for number, title, description in pipeline:
		st.markdown(
			f'<div class="vs-pipeline-step"><span class="vs-item-index">{number}</span>'
			f"<div><strong>{title}</strong><p>{description}</p></div></div>",
			unsafe_allow_html=True,
		)

	st.markdown("### Limitations")
	st.markdown(
		"VaaniShield uses a basic keyword baseline, not an AI model or a live intelligence service. "
		"It can miss unfamiliar wording, misunderstand context, or flag legitimate speech. "
		"Risk and confidence values are heuristic indicators, not calibrated probabilities."
	)

	st.markdown("### Safety principles")
	st.markdown(
		"- Do not share OTPs, passwords, PINs, or payment details with callers.\n"
		"- End a suspicious call and verify claims using independently sourced official contact information.\n"
		"- Contact your bank through its official channel if payment details may be at risk.\n"
		"- Use appropriate official reporting channels; this app does not contact authorities for you."
	)


st.set_page_config(
	page_title="VaaniShield",
	page_icon="V",
	layout="wide",
	initial_sidebar_state="collapsed",
)
load_stylesheet()

if "analysis_activity" not in st.session_state:
	st.session_state.analysis_activity = []
if "active_page" not in st.session_state:
	st.session_state.active_page = "Dashboard"

header_brand, header_status = st.columns([1.8, 1], vertical_alignment="center")
with header_brand:
	st.markdown(
		'<div class="vs-brand vs-top-brand"><span class="vs-brand-mark">V</span>'
		'<span><strong>VaaniShield</strong><small>CALL SAFETY WORKSPACE</small></span></div>',
		unsafe_allow_html=True,
	)
with header_status:
	st.markdown(
		'<div class="vs-header-status"><span class="vs-status-dot"></span>'
		"<strong>Keyword baseline</strong><span class='vs-header-separator'>·</span>"
		"<span>Session-only analysis</span></div>",
		unsafe_allow_html=True,
	)

with st.container(key="vs-horizontal-nav"):
	for page_name, icon, page_key in NAVIGATION_ITEMS:
		is_active = st.session_state.active_page == page_name
		if st.button(
			page_name,
			key=f"vs_nav_{page_key}",
			icon=icon,
			type="primary" if is_active else "secondary",
			use_container_width=False,
		):
			st.session_state.active_page = page_name
			st.rerun()

page = st.session_state.active_page

if page == "Dashboard":
	render_dashboard()
elif page == "Analyze":
	render_analyze()
elif page == "Threat Intelligence":
	render_threat_intelligence()
elif page == "Reports":
	render_reports()
else:
	render_how_it_works()