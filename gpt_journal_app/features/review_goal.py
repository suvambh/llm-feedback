# features/review_goal.py
import streamlit as st
from core.llm import client

def _analyze_current_chat(chat_log):
    text = "\n".join(f"{m['role']}: {m['content']}" for m in chat_log)
    prompt = f"""
You are a critical review model. Analyze the dialogue and produce a short report:
1) Main themes (very short)
2) Whether the conversation aligns with user intentions (if known)
3) Key problems or drift points

--- Current Chat ---
{text}
"""
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert reviewer of dialogues."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
    )
    return resp.choices[0].message.content.strip()

def run_feature(chat_log, intentions):
    st.markdown("## 🔍 Review & Set Goal")

    if not chat_log:
        st.info("No chat yet. Start chatting before running review.")
        return

    with st.spinner("Analyzing session..."):
        report = _analyze_current_chat(chat_log)

    st.markdown("### 📑 Review Report")
    st.write(report)

    st.markdown("### 📝 Set Your Intentions")
    with st.form("intentions_form", clear_on_submit=False):
        goal = st.text_input("Goal", value=intentions.get("goal", ""))
        avoid = st.text_input("Avoid", value=intentions.get("avoid", ""))
        success = st.text_input("Success Criteria", value=intentions.get("success", ""))
        submitted = st.form_submit_button("✅ Save & Inject Prompt")

    if submitted:
        intentions.update({"goal": goal, "avoid": avoid, "success": success})

        req = f"""
User intentions for the remainder of the session:
- Goal: {goal or "(not provided)"}
- Avoid: {avoid or "(not provided)"}
- Success: {success or "(not provided)"}

Review report of the chat so far:
{report}

Now produce a concise SYSTEM PROMPT to guide the assistant going forward:
- One short paragraph or 3–6 bullets.
- Steer toward the goal, away from the avoid items.
- Neutral, directive tone.
"""
        with st.spinner("Generating guiding prompt..."):
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You generate high-signal guiding prompts for AI assistants."},
                    {"role": "user", "content": req}
                ],
                max_tokens=250,
            )
        guiding = resp.choices[0].message.content.strip()
        st.session_state.chat_log.append({"role": "system", "content": guiding})
        st.success("✅ Intentions saved and guiding prompt injected into chat!")
        st.code(guiding, language="markdown")
