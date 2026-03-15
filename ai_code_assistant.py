import streamlit as st
import anthropic
import re

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Code Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Syne:wght@400;600;700;800&display=swap');

/* Root theme */
:root {
    --bg: #0a0a0f;
    --surface: #12121a;
    --border: #1e1e2e;
    --accent: #7c6af7;
    --accent2: #f97066;
    --accent3: #34d399;
    --text: #e2e2f0;
    --muted: #6b6b8a;
    --code-bg: #0d0d14;
}

/* Global */
.stApp {
    background: var(--bg) !important;
    font-family: 'Syne', sans-serif;
    color: var(--text);
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem !important; max-width: 1100px !important; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 3rem 0 2rem;
    position: relative;
}
.hero-tag {
    display: inline-block;
    background: linear-gradient(135deg, #7c6af720, #f9706620);
    border: 1px solid #7c6af740;
    color: var(--accent);
    font-size: 0.7rem;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    padding: 0.35rem 1rem;
    border-radius: 100px;
    margin-bottom: 1.2rem;
}
.hero h1 {
    font-size: clamp(2.2rem, 5vw, 3.5rem);
    font-weight: 800;
    background: linear-gradient(135deg, #e2e2f0 0%, #7c6af7 50%, #f97066 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    line-height: 1.1;
}
.hero p {
    color: var(--muted);
    font-size: 1rem;
    margin-top: 0.8rem;
    font-family: 'JetBrains Mono', monospace;
}

/* ── Tab strip ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid var(--border) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--muted) !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 1.4rem !important;
    border: none !important;
    transition: all 0.2s ease !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, var(--accent), #9b8cf9) !important;
    color: white !important;
}
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* ── Cards ── */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
}
.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--accent2), var(--accent3));
}
.card-title {
    font-size: 0.7rem;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.8rem;
}

/* ── Inputs ── */
.stTextArea textarea, .stTextInput input, .stSelectbox select {
    background: var(--code-bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.88rem !important;
    transition: border 0.2s !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px #7c6af720 !important;
}
.stTextArea label, .stTextInput label, .stSelectbox label {
    color: var(--muted) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.05em !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent), #9b8cf9) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 2rem !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.02em !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 24px #7c6af740 !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: var(--code-bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
}

/* ── Code output ── */
.stCodeBlock, pre {
    background: var(--code-bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    font-family: 'JetBrains Mono', monospace !important;
}
pre code { color: #c9d1d9 !important; }

/* ── Result panels ── */
.result-box {
    background: var(--code-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    line-height: 1.7;
    color: var(--text);
    white-space: pre-wrap;
    word-break: break-word;
}
.badge {
    display: inline-block;
    padding: 0.25rem 0.7rem;
    border-radius: 6px;
    font-size: 0.7rem;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}
.badge-green { background: #34d39920; color: #34d399; border: 1px solid #34d39940; }
.badge-yellow { background: #fbbf2420; color: #fbbf24; border: 1px solid #fbbf2440; }
.badge-red { background: #f9706620; color: #f97066; border: 1px solid #f9706640; }
.badge-blue { background: #7c6af720; color: #7c6af7; border: 1px solid #7c6af740; }

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }

/* ── Spinner ── */
.stSpinner > div { border-top-color: var(--accent) !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--muted); }
</style>
""", unsafe_allow_html=True)


# ── Anthropic client ──────────────────────────────────────────────────────────
@st.cache_resource
def get_client():
    return anthropic.Anthropic()


def call_claude(system: str, user: str) -> str:
    client = get_client()
    msg = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return msg.content[0].text


# ── Helpers ───────────────────────────────────────────────────────────────────
def extract_code_blocks(text: str) -> list[tuple[str, str]]:
    """Return list of (lang, code) from fenced blocks."""
    pattern = r"```(\w*)\n(.*?)```"
    return re.findall(pattern, text, re.DOTALL)


LANGUAGES = [
    "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "Go",
    "Rust", "Swift", "Kotlin", "PHP", "Ruby", "SQL", "Bash", "HTML/CSS",
]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-tag">⚡ Powered by Claude</div>
  <h1>AI Code Assistant</h1>
  <p>// english → code · code review · bug fixing</p>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["✦ English → Code", "⊞ Code Review", "⚑ Bug Fixer"])


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — English → Code
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Describe what you want to build</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns([3, 1])
    with col_a:
        english_input = st.text_area(
            "Natural language description",
            placeholder="e.g. Write a function that takes a list of numbers and returns the top 3 largest values sorted in descending order",
            height=140,
            key="eng_input",
            label_visibility="collapsed",
        )
    with col_b:
        lang_choice = st.selectbox("Language", LANGUAGES, key="lang_pick")
        add_comments = st.checkbox("Add comments", value=True)
        add_tests = st.checkbox("Add unit tests", value=False)

    gen_btn = st.button("⚡ Generate Code", key="gen_btn", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if gen_btn:
        if not english_input.strip():
            st.warning("Please describe what you want to build.")
        else:
            extras = []
            if add_comments:
                extras.append("Add clear inline comments explaining each step.")
            if add_tests:
                extras.append("After the main code, include basic unit tests.")
            extra_str = " ".join(extras)

            system_prompt = f"""You are an expert {lang_choice} developer.
Convert the user's plain-English description into clean, idiomatic {lang_choice} code.
{extra_str}
Wrap the code in a fenced code block with the correct language tag.
After the code block, add a short 'How it works' explanation in 3-5 bullet points."""

            with st.spinner("Generating code…"):
                result = call_claude(system_prompt, english_input)

            blocks = extract_code_blocks(result)
            explanation = re.sub(r"```.*?```", "", result, flags=re.DOTALL).strip()

            st.markdown('<span class="badge badge-green">✓ Generated</span>', unsafe_allow_html=True)

            if blocks:
                for lang_tag, code in blocks:
                    st.code(code.strip(), language=lang_tag or lang_choice.lower())
            else:
                st.code(result, language=lang_choice.lower())

            if explanation:
                st.markdown("**How it works**")
                st.markdown(explanation)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — Code Review
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Paste your code for review</div>', unsafe_allow_html=True)

    review_lang = st.selectbox("Language", LANGUAGES, key="rev_lang")
    code_to_review = st.text_area(
        "Your code",
        placeholder="Paste the code you want reviewed here…",
        height=220,
        key="review_code",
        label_visibility="collapsed",
    )

    col_r1, col_r2, col_r3 = st.columns(3)
    with col_r1:
        chk_quality = st.checkbox("Code quality", value=True)
    with col_r2:
        chk_perf = st.checkbox("Performance", value=True)
    with col_r3:
        chk_security = st.checkbox("Security", value=True)

    review_btn = st.button("⊞ Review Code", key="rev_btn", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if review_btn:
        if not code_to_review.strip():
            st.warning("Please paste some code to review.")
        else:
            focuses = [f for f, c in [("code quality & readability", chk_quality),
                                       ("performance & efficiency", chk_perf),
                                       ("security vulnerabilities", chk_security)] if c]
            focus_str = ", ".join(focuses) if focuses else "general best practices"

            system_prompt = f"""You are a senior {review_lang} engineer conducting a thorough code review.
Analyze the code focusing on: {focus_str}.

Structure your response as:
## Overall Score
Give a score out of 10 with one sentence verdict.

## Strengths
List 2-4 things done well.

## Issues Found
For each issue: state the problem, severity (🔴 Critical / 🟡 Medium / 🟢 Minor), line reference if applicable, and a suggested fix.

## Refactored Snippet (optional)
If significant improvements exist, show a key refactored portion in a code block.

## Summary
One paragraph takeaway."""

            with st.spinner("Reviewing code…"):
                review_result = call_claude(system_prompt, code_to_review)

            st.markdown('<span class="badge badge-blue">⊞ Review Complete</span>', unsafe_allow_html=True)
            st.markdown(review_result)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — Bug Fixer
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Paste buggy code + error (optional)</div>', unsafe_allow_html=True)

    fix_lang = st.selectbox("Language", LANGUAGES, key="fix_lang")
    buggy_code = st.text_area(
        "Buggy code",
        placeholder="Paste your code with bugs here…",
        height=180,
        key="buggy_code",
        label_visibility="collapsed",
    )
    error_msg = st.text_area(
        "Error message / traceback (optional)",
        placeholder="Paste any error message or stack trace here…",
        height=90,
        key="error_msg",
        label_visibility="collapsed",
    )

    fix_btn = st.button("⚑ Find & Fix Bugs", key="fix_btn", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if fix_btn:
        if not buggy_code.strip():
            st.warning("Please paste the buggy code.")
        else:
            context = f"Code:\n```\n{buggy_code}\n```"
            if error_msg.strip():
                context += f"\n\nError/Traceback:\n{error_msg}"

            system_prompt = f"""You are an expert {fix_lang} debugger.

Analyze the provided code (and error message if given).

Respond in this exact structure:

## Bugs Found
List each bug with:
- **Bug #N**: Brief title
  - **What's wrong**: Clear explanation
  - **Why it fails**: Root cause
  - **Severity**: 🔴 Critical / 🟡 Medium / 🟢 Minor

## Fixed Code
Provide the complete corrected code in a fenced code block.

## What Changed
Bullet-point summary of every change made and why."""

            with st.spinner("Hunting bugs…"):
                fix_result = call_claude(system_prompt, context)

            blocks = extract_code_blocks(fix_result)

            st.markdown('<span class="badge badge-red">⚑ Bugs Found & Fixed</span>', unsafe_allow_html=True)

            # Show full markdown response — fixed code blocks render automatically
            st.markdown(fix_result)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; color: #3a3a5c; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; padding: 2rem 0 1rem; border-top: 1px solid #1e1e2e;">
  AI Code Assistant · Built with Streamlit + Claude · Anthropic
</div>
""", unsafe_allow_html=True)
