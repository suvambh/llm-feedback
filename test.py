import streamlit as st
from openai import OpenAI
import os

# ---- Setup OpenAI ----
client = OpenAI(api_key=os.getenv("oai_key"))  # change "xx" if your env var is named differently

st.set_page_config(page_title="Intention Journal", layout="wide")

# ---- Session State ----
if "step" not in st.session_state:
    st.session_state.step = 1
if "intentions" not in st.session_state:
    st.session_state.intentions = {}
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []


# ---- STEP 1: Intentions ----
if st.session_state.step == 1:
    st.header("📝 Step 1: Set Your Intentions")

    with st.form("intentions_form"):
        goal = st.text_input("What do you want to achieve in this session?")
        avoid = st.text_input("What should you avoid?")
        success = st.text_input("How will you know this session was useful?")
        submitted = st.form_submit_button("Save Intentions & Start Chat")

    if submitted:
        st.session_state.intentions = {
            "goal": goal,
            "avoid": avoid,
            "success": success
        }
        st.session_state.step = 2
        st.rerun()


# ---- STEP 2: Chat ----
elif st.session_state.step == 2:
    st.header("💬 Step 2: GPT Session")

    user_input = st.text_input("Ask GPT a question:")

    if st.button("Send") and user_input:
        st.session_state.chat_log.append({"role": "user", "content": user_input})

        # Keep context small to reduce cost
        context_messages = [
            {"role": "system", "content": "You are ChatGPT. Answer concisely (≤5 sentences)."},
            *st.session_state.chat_log[-5:]
        ]

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=context_messages,
            max_tokens=200
        )
        reply = response.choices[0].message.content
        st.session_state.chat_log.append({"role": "assistant", "content": reply})

    # Display chat
    st.subheader("Conversation")
    for msg in st.session_state.chat_log:
        if msg["role"] == "user":
            st.write(f"🧑 **You:** {msg['content']}")
        else:
            st.write(f"🤖 **GPT:** {msg['content']}")

    if st.button("Done (Go to Review)"):
        st.session_state.step = 3
        st.rerun()


# ---- STEP 3: Review ----
elif st.session_state.step == 3:
    st.header("📊 Step 3: Review Your Session")

    transcript = "\n".join(
        f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.chat_log
    )

    report_prompt = f"""
    User's intentions:
    Goal: {st.session_state.intentions.get("goal")}
    Avoid: {st.session_state.intentions.get("avoid")}
    Success criteria: {st.session_state.intentions.get("success")}

    Session transcript:
    {transcript}

    Please generate a structured review:
    - Alignment with intentions (score 0-100%)
    - Instances where conversation drifted
    - Did success criteria get met?
    - Key insights
    - Possible hallucinations
    - Suggestions for next session
    """

    report = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": report_prompt}],
        max_tokens=300
    )

    st.subheader("Session Report")
    st.write(report.choices[0].message.content)

    if st.button("Start New Session"):
        st.session_state.step = 1
        st.session_state.intentions = {}
        st.session_state.chat_log = []
        st.rerun()
