# features/blogpost.py
import streamlit as st
from core.llm import client
from core.storage import save_blog, load_blogs

def run_feature(chat_log):
    st.markdown("## 📝 Create Blogpost from Chat")

    if not chat_log:
        st.warning("No chat log found. Start a conversation first.")
        return

    if "blogs" not in st.session_state:
        st.session_state.blogs = load_blogs()
    if "last_blog" not in st.session_state:
        st.session_state.last_blog = None

    model = st.selectbox("Choose a model:", ["gpt-4o-mini", "gpt-4o", "gpt-4o-pro"])
    length = st.selectbox("Select length:", ["Short (~300 words)", "Medium (~600 words)", "Long (~1200 words)"])
    style  = st.selectbox("Blogpost type:", ["Tutorial", "Opinion", "Summary", "Story"])
    title  = st.text_input("Enter blogpost title (optional):")

    if st.button("✍️ Generate Blogpost"):
        chat_text = "\n".join(f"{m['role']}: {m['content']}" for m in chat_log)
        prompt = f"""
Convert the following chat conversation into a coherent {style.lower()} blogpost.
Target length: {length}. Audience: general readers.
Ensure clarity, flow, and engagement.

Chat log:
{chat_text}
"""
        if title:
            prompt += f"\nUse this title: {title}"

        with st.spinner("Generating blogpost..."):
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You write polished blogposts from raw dialogues."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1800,
            )
        blog_text = resp.choices[0].message.content.strip()

        st.session_state.blogs = save_blog(title, blog_text, st.session_state.blogs)
        st.session_state.last_blog = {"title": title or "Blogpost", "content": blog_text}
        st.success("✅ Blogpost generated and saved!")

    if st.session_state.last_blog:
        st.markdown(f"### {st.session_state.last_blog['title']}")
        st.markdown(st.session_state.last_blog['content'])
