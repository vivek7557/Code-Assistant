# AI Code Assistant

A Streamlit app that uses the Groq API to help you:

- Generate code from natural-language prompts.
- Review existing code with structured feedback.
- Find and fix bugs with root-cause-oriented suggestions.

## Features

- **English → Code** tab with language selection and optional comments/tests.
- **Code Review** tab with checks for quality, performance, and security.
- **Bug Fixer** tab for debugging with optional error/traceback context.
- **Groq model selector** and session-scoped API key input.
- **Python-focused modes** for deeper generation/review/debug guidance.

## Requirements

- Python 3.10+
- A Groq API key

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run locally

```bash
streamlit run ai_code_assistant.py
```

Then open the local URL shown by Streamlit (typically `http://localhost:8501`).

## Configuration

You can provide your Groq API key in either of these ways:

1. In-app (Assistant Settings panel) — stored in Streamlit session state for the current browser session.
2. Streamlit secrets — set `GROQ_API_KEY` in your Streamlit secrets file.

## Project structure

```text
.
├── ai_code_assistant.py
├── requirements.txt
└── README.md
```

## Notes

- This app calls LLMs and may produce imperfect output. Always review generated or fixed code before production use.
- The selected model affects quality, speed, and token limits.
