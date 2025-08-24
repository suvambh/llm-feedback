# core/storage.py
import os, json
from datetime import datetime

DATA_FILE = "chats.json"

def load_chats():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_chat(chat_log, intentions, chats):
    chat_name = datetime.now().strftime("Chat %Y-%m-%d %H:%M:%S")
    chats[chat_name] = {
        "chat_log": chat_log,
        "intentions": intentions
    }
    with open(DATA_FILE, "w") as f:
        json.dump(chats, f, indent=2)

import json, os
from datetime import datetime

BLOG_FILE = "blogposts.json"

def load_blogs():
    if os.path.exists(BLOG_FILE):
        with open(BLOG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_blog(title, content, blogs):
    blog_name = title if title else datetime.now().strftime("Blog %Y-%m-%d %H:%M:%S")
    blogs[blog_name] = {"title": blog_name, "content": content}

    # Debug: print to console
    print(f"Saving blog: {blog_name} -> {len(content)} chars")

    with open(BLOG_FILE, "w") as f:
        json.dump(blogs, f, indent=2)

    return blogs

