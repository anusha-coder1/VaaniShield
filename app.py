from datetime import datetime
from pathlib import Path

import streamlit as st

from models.schemas import RiskLevel
from services.analyzer import analyze
from services.evaluation import EvaluationDatasetError, evaluate_dataset
from services.speech_to_text import SUPPORTED_AUDIO_FORMATS, transcribe_audio


NAVIGATION_ITEMS = (
	("Dashboard", ":material/space_dashboard:", "dashboard"),
	("Analyze", ":material/manage_search:", "analyze"),
	("Threat Intelligence", ":material/policy:", "threat-intelligence"),
	("Reports", ":material/description:", "reports"),
	("How It Works", ":material/account_tree:", "how-it-works"),
	("Evaluation", ":material/analytics:", "evaluation"),
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
		"authority_based_coercion",
		"A claimed authority is used alongside coercive behaviour, such as isolation, secrecy, credential requests, or payment threats.",
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
			"time": datetime.now().astimezone().strftime("%b %d Â· %H:%M"),
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
		"Keyword baseline active <span class='vs-divider-dot'>Â·</span> "
		"No live threat feed <span class='vs-divider-dot'>Â·</span> "
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
			f"{len(STAGES)} stages Â· {len(TACTICS)} tactics in the baseline",
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
		'<div class="vs-privacy-note"><span class="vs-privacy-mark">âœ“</span>'
		"Sensitive formats are redacted before analysis. Session activity keeps only time, risk, and signal counts; transcripts and phrases are excluded.</div>",
		unsafe_allow_html=True,
	)


def render_analysis_result(result) -> None:
	risk_class = result.risk_level.value.lower()
	status_class = "alert" if result.scam_detected else "clear"
	status_text = "Scam indicators detected" if result.scam_detected else "No scam indicators detected"
	evidence_by_indicator = {
		item.indicator: item for item in result.indicator_evidence
	}

	st.markdown("### Overall risk assessment")
	st.markdown(
		f'<div class="vs-result-banner vs-result-banner--{status_class}">'
		f"<strong>{status_text}</strong>"
		f'<span class="vs-risk vs-risk--{risk_class}">{result.risk_level.value.title()} risk</span>'
		"</div>",
		unsafe_allow_html=True,
	)

	confidence_column, stage_column, tactic_column = st.columns(3)
	with confidence_column:
		st.metric("Baseline confidence (heuristic)", f"{result.confidence:.0%}")
		st.progress(result.confidence)
	with stage_column:
		st.metric("Stages detected", len(result.stages_detected))
	with tactic_column:
		st.metric("Tactics detected", len(result.tactics_detected))

	def render_indicators(title: str, indicator_names: tuple[str, ...]) -> None:
		st.markdown(f"#### {title}")
		for indicator in indicator_names:
			evidence = evidence_by_indicator.get(indicator)
			label = indicator.replace("_", " ").title()
			if evidence is None:
				st.caption(f"{label} — Not detected in the supplied conversation.")
				continue

			with st.expander(label, expanded=True):
				for phrase in evidence.exact_phrases:
					st.code(phrase, language=None)
				st.write(evidence.explanation)
				st.caption(f"Potential risk: {evidence.potential_risk}")

	st.markdown("### Scam stages and tactics")
	stage_column, tactic_column = st.columns(2)
	with stage_column:
		render_indicators("Stages", tuple(name for name, _ in STAGES))
	with tactic_column:
		render_indicators("Tactics", tuple(name for name, _ in TACTICS))

	st.markdown("### Matched evidence")
	if result.exact_phrases:
		for phrase in result.exact_phrases:
			st.code(phrase, language=None)
	else:
		st.caption("No matched evidence found in the supplied conversation.")

	if result.risk_level in {RiskLevel.HIGH, RiskLevel.CRITICAL}:
		st.warning(
			"Suggested safety actions: if it is safe to do so, end the suspicious call. "
			"Do not transfer money or share OTPs, PINs, or passwords. Verify claims using "
			"independently sourced official contact details, and inform someone you trust. "
			"In India, suspected cyber financial fraud can be reported by calling 1930 or "
			"visiting cybercrime.gov.in. VaaniShield will not contact anyone or submit a report."
		)
	else:
		st.info(
			"If anything in the conversation feels unexpected, pause and verify it independently. "
			"Never share authentication credentials with a caller."
		)
	st.info(result.uncertainty_note)


def analyze_reviewed_transcript(transcript: str) -> None:
	if not transcript.strip():
		st.info("Enter or review a transcript before starting scam analysis.")
		return

	result = analyze(transcript)
	record_activity(result)
	st.divider()
	render_analysis_result(result)


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

	text_tab, audio_tab = st.tabs(["Text transcript", "Audio recording"])
	with text_tab:
		with st.form("transcript_analysis", clear_on_submit=False):
			transcript = st.text_area(
				"Suspicious call transcript",
				height=220,
				placeholder="Paste or type the conversation you want to review...",
				help="Do not include credentials you would not want to share. Text is not added to activity summaries or written to app files.",
				key="analysis_transcript",
			)
			text_submitted = st.form_submit_button(
				"Analyze Conversation",
				type="primary",
				use_container_width=True,
			)

		if text_submitted:
			analyze_reviewed_transcript(transcript)
		else:
			st.caption("The analyzer redacts common sensitive formats before keyword analysis.")

	with audio_tab:
		st.warning(
			"Audio is sent to Gnani's servers for transcription. VaaniShield does not save the uploaded recording to disk. "
			"Review the transcript before submitting it for analysis."
		)
		with st.form("audio_transcription_form", clear_on_submit=False):
			uploaded_audio = st.file_uploader(
				"Upload a call recording",
				type=list(SUPPORTED_AUDIO_FORMATS),
				help="Supported formats: WAV, MP3, M4A, AAC, FLAC, and OGG.",
				key="audio_upload",
			)
			transcribe_submitted = st.form_submit_button(
				"Transcribe Audio",
				type="primary",
				use_container_width=True,
			)

		if transcribe_submitted:
			st.session_state.pop("audio_review_transcript", None)
			st.session_state.pop("audio_detected_language", None)
			if uploaded_audio is None:
				st.info("Choose an audio file before starting transcription.")
			else:
				with st.spinner("Transcribing audio with Gnani Prisma v3..."):
					try:
						transcription = transcribe_audio(uploaded_audio)
					except (ValueError, RuntimeError) as error:
						st.error(str(error))
					except Exception:
						st.error(
							"An unexpected transcription error occurred. Check your connection and try again."
						)
					else:
						st.session_state["audio_review_transcript"] = transcription["transcript"]
						st.session_state["audio_detected_language"] = transcription.get(
							"detected_language"
						)

		if "audio_review_transcript" in st.session_state:
			detected_language = st.session_state.get("audio_detected_language")
			if detected_language:
				st.caption(f"Detected language: {detected_language}")
			with st.form("reviewed_audio_transcript_form", clear_on_submit=False):
				reviewed_transcript = st.text_area(
					"Review and edit the transcription",
					height=220,
					key="audio_review_transcript",
					help="Scam analysis will use this reviewed text, not the original audio.",
				)
				analyze_reviewed = st.form_submit_button(
					"Analyze Reviewed Transcript",
					type="primary",
					use_container_width=True,
				)
			if analyze_reviewed:
				analyze_reviewed_transcript(reviewed_transcript)


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
		("03", "Keyword baseline", "Specific phrase patterns are checked for four stages and six tactics; negated credential warnings are filtered."),
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


def render_evaluation() -> None:
	page_header(
		"Synthetic regression set",
		"Detection evaluation",
		"A transparent summary of the 36-sample synthetic regression dataset, separate from the 120-sample Phase 4 evaluation.",
	)
	st.warning(
		"This small synthetic evaluation is not real-world validated performance. "
		"Native-speaker validation has not been performed. Hindi, Telugu, Tamil, Malayalam, and code-mixed samples retain review-required flags. "
		"Weak results are shown as measured; no samples are skipped."
	)

	try:
		report = evaluate_dataset()
	except EvaluationDatasetError as error:
		st.error(f"Evaluation could not be completed: {error}")
		return

	st.markdown("### Dataset summary")
	summary_columns = st.columns(5)
	summary_values = (
		("Total samples", report["total_samples"]),
		("Scam samples", report["scam_samples"]),
		("Genuine samples", report["genuine_samples"]),
		("Correct scam detections", report["correct_scam_detections"]),
		("Missed scams", report["missed_scams"]),
	)
	for column, (label, value) in zip(summary_columns, summary_values):
		with column:
			st.metric(label, value)
	st.caption(f"False alarms: {report['false_alarms']}")

	st.markdown("### Overall metrics")
	metric_names = (
		("Accuracy", "accuracy"),
		("Precision", "precision"),
		("Recall", "recall"),
		("F1-score", "f1_score"),
		("False-positive rate", "false_positive_rate"),
		("True-positive rate", "true_positive_rate"),
	)
	metric_values = report["overall_metrics"]
	for row_start in (0, 3):
		columns = st.columns(3)
		for column, (label, key) in zip(columns, metric_names[row_start:row_start + 3]):
			with column:
				st.metric(label, f"{metric_values[key]:.1%}")

	st.markdown("### Confusion matrix")
	confusion = report["confusion_matrix"]
	st.table(
		[
			{
				"Actual label": "Scam",
				"Predicted scam": confusion["true_positive"],
				"Predicted genuine": confusion["false_negative"],
			},
			{
				"Actual label": "Genuine",
				"Predicted scam": confusion["false_positive"],
				"Predicted genuine": confusion["true_negative"],
			},
		]
	)

	def metric_rows(performance: dict, label_name: str) -> list[dict]:
		rows = []
		for label, details in performance.items():
			metrics = details["metrics"]
			rows.append(
				{
					label_name: label.replace("_", " ").title(),
					"Samples": details.get("total_samples", details.get("support", 0)),
					"Native review needed": details.get(
						"native_speaker_review_required_samples", "\u2014"
					),
					"Accuracy": f"{metrics['accuracy']:.1%}",
					"Precision": f"{metrics['precision']:.1%}" if details.get("support", 1) > 0 else "N/A",
					"Recall": f"{metrics['recall']:.1%}" if details.get("support", 1) > 0 else "N/A",
					"F1": f"{metrics['f1_score']:.1%}" if details.get("support", 1) > 0 else "N/A",
					"FPR": f"{metrics['false_positive_rate']:.1%}",
					"TPR": f"{metrics['true_positive_rate']:.1%}",
				}
			)
		return rows

	st.markdown("### Language-wise performance")
	st.table(metric_rows(report["language_performance"], "Language"))

	st.markdown("### Stage-wise performance")
	st.table(metric_rows(report["stage_wise_performance"], "Stage"))

	st.markdown("### Tactic-wise performance")
	st.table(metric_rows(report["tactic_wise_performance"], "Tactic"))
	st.caption(
		f"{report['native_speaker_review_required_samples']} of {report['total_samples']} "
		"samples are marked for native-speaker review. Evaluation labels are manually assigned and were not generated by the detector."
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
		"<strong>Keyword baseline</strong><span class='vs-header-separator'>Â·</span>"
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

page = st.session_state.active_page

if page == "Dashboard":
	render_dashboard()
elif page == "Analyze":
	render_analyze()
elif page == "Threat Intelligence":
	render_threat_intelligence()
elif page == "Reports":
	render_reports()
elif page == "How It Works":
	render_how_it_works()
else:
	render_evaluation()
