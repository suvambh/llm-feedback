import os

# Define project structure
folders = [
    "gpt_journal_app/core",
    "gpt_journal_app/features",
    "gpt_journal_app/data"
]

files = {
    "gpt_journal_app/app.py": "# Main Streamlit entry point\n",
    "gpt_journal_app/core/chat.py": "# Chat logic with GPT\n",
    "gpt_journal_app/core/storage.py": "# Save/load sessions\n",
    "gpt_journal_app/core/prompts.py": "# System + helper prompts\n",
    "gpt_journal_app/core/utils.py": "# Shared helpers (token counter, formatters)\n",
    "gpt_journal_app/features/review_goal.py": "# Feature 1: Review & Set Goal\n",
    "gpt_journal_app/features/reflection.py": "# Feature 2: Reflection questions\n",
    "gpt_journal_app/features/tracking.py": "# Feature 3: Progress tracking\n",
    "gpt_journal_app/data/sessions.json": "[]",  # start empty JSON list
    "gpt_journal_app/requirements.txt": "streamlit\nopenai\n"
}

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create files with starter content
for filepath, content in files.items():
    if not os.path.exists(filepath):
        with open(filepath, "w") as f:
            f.write(content)

print("✅ Project structure created successfully.")
