# app.py
import os
import streamlit as st
from core.chat import chat_with_gpt, summarize_chat
from core.storage import save_chat, load_chats
from features import review_goal, blogpost

st.set_page_config(page_title="GPT Journal App", layout="wide")
st.title("💬 GPT Journal App")

# ---- Session State ----
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []
if "intentions" not in st.session_state:
    st.session_state.intentions = {}
if "chats" not in st.session_state:
    st.session_state.chats = load_chats()

# ---- Sidebar (Navigation) ----
with st.sidebar:
    st.header("🧭 Navigation")
    nav = st.radio("Go to", ["Chat", "Review & Set Goal", "Blogpost Writer"], index=0, key="nav_choice")

    st.divider()
    st.subheader("📜 Saved Chats")
    if st.session_state.chats:
        selected_chat = st.selectbox("Select a saved chat:", list(st.session_state.chats.keys()))
        if st.button("▶️ Continue This Chat"):
            old = st.session_state.chats[selected_chat]["chat_log"]
            summary = summarize_chat(old)
            guiding_prompt = (
                "You are continuing a past conversation.\n"
                "Here are the critical points from the previous chat:\n"
                f"{summary}\n\n"
                "Pick up naturally from this context as if no break occurred."
            )
            st.session_state.chat_log = [{"role": "system", "content": guiding_prompt}]
            st.session_state.intentions = st.session_state.chats[selected_chat].get("intentions", {})
            st.success(f"Loaded “{selected_chat}” as a continuation.")
    else:
        st.caption("No saved chats yet.")

    st.divider()
    if st.button("💾 End Chat & Save"):
        save_chat(st.session_state.chat_log, st.session_state.intentions, st.session_state.chats)
        st.success("Saved current chat.")
        st.session_state.chat_log = []
        st.session_state.intentions = {}

    st.caption(f"API key loaded: {'✅' if os.getenv('OPENAI_API_KEY') or os.getenv('oai_key') else '❌'}")

# ---- Main (Right Content) ----
if st.session_state.nav_choice == "Chat":
    st.subheader("Current Chat Session")

    # show history first
    for msg in st.session_state.chat_log:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # input at bottom; answer displays immediately (no extra click)
    if user_input := st.chat_input("Type your message..."):
        st.session_state.chat_log.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        reply = chat_with_gpt(user_input, st.session_state.chat_log)
        st.session_state.chat_log.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)

elif st.session_state.nav_choice == "Review & Set Goal":
    review_goal.run_feature(st.session_state.chat_log, st.session_state.intentions)

elif st.session_state.nav_choice == "Blogpost Writer":
    blogpost.run_feature(st.session_state.chat_log)
