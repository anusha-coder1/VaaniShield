import streamlit as st

from services.analyzer import analyze


st.set_page_config(
	page_title="VaaniShield",
	page_icon="V",
	layout="wide",
)

st.markdown(
	"""
	<style>
	:root {
		--ink: #19333a;
		--muted: #587078;
		--teal: #087e83;
		--line: #d6e4e3;
		--surface: #f5faf9;
	}
	.stApp {
		background: linear-gradient(135deg, #f8fbfa 0%, #edf6f4 100%);
		color: var(--ink);
		font-family: "Aptos", "Segoe UI", sans-serif;
	}
	.block-container {
		max-width: 1080px;
		padding-top: 2rem;
		padding-bottom: 3rem;
	}
	h1, h2, h3 {
		color: var(--ink);
		letter-spacing: 0;
	}
	.eyebrow {
		color: var(--teal);
		font-size: 0.76rem;
		font-weight: 700;
		letter-spacing: 0.08em;
		text-transform: uppercase;
		margin-bottom: 0.25rem;
	}
	div[data-testid="stTextArea"] textarea {
		background: #ffffff;
		border: 1px solid var(--line);
		border-radius: 6px;
		color: var(--ink);
		line-height: 1.55;
	}
	div[data-testid="stTextArea"] textarea:focus {
		border-color: var(--teal);
		box-shadow: 0 0 0 1px var(--teal);
	}
	div[data-testid="stFormSubmitButton"] button {
		background: var(--teal);
		border: 1px solid var(--teal);
		border-radius: 6px;
		min-height: 2.8rem;
	}
	div[data-testid="stFormSubmitButton"] button:hover {
		background: #06696e;
		border-color: #06696e;
	}
	hr {
		border-color: var(--line);
	}
	</style>
	""",
	unsafe_allow_html=True,
)

st.markdown('<div class="eyebrow">Call safety analysis</div>', unsafe_allow_html=True)
st.title("VaaniShield — Detect. Intervene. Report.")
st.write(
	"Review suspicious call transcripts for common digital-arrest scam patterns. "
	"VaaniShield highlights indicators to support a careful next step."
)

st.warning(
	"Safety notice: This is an experimental tool, not a substitute for official "
	"verification or law-enforcement advice. Do not act on a caller's demands "
	"based on this result alone."
)

with st.form("transcript_analysis"):
	transcript = st.text_area(
		"Suspicious call transcript",
		height=220,
		placeholder="Paste the call transcript here...",
		help="The transcript is analyzed in the current session and is not saved by this app.",
	)
	submitted = st.form_submit_button(
		"Analyze Conversation",
		type="primary",
		use_container_width=True,
	)

if submitted:
	if not transcript.strip():
		st.info("Enter a transcript above to start the analysis.")
	else:
		result = analyze(transcript)

		st.divider()
		st.subheader("Analysis")
		if result.scam_detected:
			st.error("Scam detected")
		else:
			st.success("No scam indicators detected")

		risk_column, confidence_column = st.columns(2)
		with risk_column:
			st.metric("Risk level", result.risk_level.value)
		with confidence_column:
			st.metric("Confidence", f"{result.confidence:.0%}")
			st.progress(result.confidence)

		stage_column, tactic_column = st.columns(2)
		with stage_column:
			st.markdown("#### Detected scam stages")
			if result.stages_detected:
				for stage in result.stages_detected:
					st.markdown(f"- {stage.replace('_', ' ').title()}")
			else:
				st.caption("No stages detected.")

		with tactic_column:
			st.markdown("#### Detected tactics")
			if result.tactics_detected:
				for tactic in result.tactics_detected:
					st.markdown(f"- {tactic.replace('_', ' ').title()}")
			else:
				st.caption("No tactics detected.")

		st.markdown("#### Exact matched phrases")
		if result.exact_phrases:
			for phrase in result.exact_phrases:
				st.code(phrase, language=None)
		else:
			st.caption("No matching phrases found.")

		st.info(result.uncertainty_note)
else:
	st.info("Enter a transcript above, then select Analyze Conversation.")
