# GPT Journal App

A personal AI dashboard built with **Streamlit** and **OpenAI**, designed to help you:

* Chat with GPT in a ChatGPT-like interface
* Review and set intentions for your conversations (goals, avoidances, success criteria)
* Generate blog posts directly from your chat logs
* Correct Markdown files with a CLI tool using OpenAI

---

## 🚀 Features

* **💬 Chat Interface**
  A lightweight ChatGPT-style UI using Streamlit.

* **🔍 Review & Set Goal**
  Review your current chat, analyze drift, and inject guiding prompts based on your intentions.

* **📝 Blogpost Generator**
  Turn chats into clean blog posts with adjustable style and length.

* **🛠️ Markdown Corrector (CLI)**
  Run:

  ```bash
  python -m tools.llm_correct README.md --mode strict --model gpt-4o
  ```

  to fix grammar and clarity in any Markdown file.

---

## 📦 Installation

Clone your repo:

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

Set up a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # on macOS/Linux
.venv\Scripts\activate      # on Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

> Or, if you have a `pyproject.toml`, just do:
>
> ```bash
> pip install -e .
> ```

---

## 🔑 API Key

You need an OpenAI API key. Set it as an environment variable:

```bash
export OPENAI_API_KEY="sk-..."      # macOS/Linux
setx OPENAI_API_KEY "sk-..."        # Windows (PowerShell)
```

---

## ▶️ Usage

### Run the Streamlit app

```bash
streamlit run app.py
```

This opens the GPT Journal App in your browser.

### Use the Markdown corrector

```bash
# From the project root:
python -m tools.llm_correct notes.md --mode strict --model gpt-4o --write
```

Options:

* `--mode` → `light | medium | strict`
* `--model` → `gpt-4o`, `gpt-4o-mini`, etc.
* `--write` → overwrite the file (with `.bak` backup)

---

## 🗂 Project Structure

```
gpt-journal-app/
├─ app.py                 # Streamlit entry point
├─ core/                  # Chat + storage utilities
├─ features/              # Features like review_goal, blogpost
├─ tools/                 # CLI utilities (e.g. llm_correct)
├─ requirements.txt       # Python dependencies
└─ README.md              # This file
```

---

## 🛠 Development Notes

* `.env` files and secrets are ignored via `.gitignore`.
* Use `python -m tools.llm_correct` from the project root, or add an alias for convenience.
* If you want system-wide commands (`llm-correct`), install in editable mode:

  ```bash
  pip install -e .
  ```

---

## 📌 Roadmap

* [ ] Semantic knowledge base for saved chats
* [ ] Analytics to detect themes and patterns across sessions
* [ ] More export options (PDF, HTML)
* [ ] Integrations with task managers
* [ ] Integrations with different models
