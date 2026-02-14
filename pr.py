import streamlit as st
from groq import Groq
import time
from datetime import datetime

# ===== API KEY (PASTE YOUR KEY HERE) =====
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# ===== CONFIG =====
st.set_page_config(
    page_title="NovaChat",
    page_icon="💬",
    layout="wide"
)

# ===== SESSION STATE =====
if "chats" not in st.session_state:
    cid = str(int(time.time()))
    st.session_state.chats = {
        cid: {
            "title": "New Chat",
            "created": datetime.now(),
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant."}
            ],
        }
    }
    st.session_state.current = cid

# ===== FUNCTIONS =====
def new_chat():
    cid = str(int(time.time()))
    st.session_state.chats[cid] = {
        "title": "New Chat",
        "created": datetime.now(),
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant."}
        ],
    }
    st.session_state.current = cid

def add_msg(role, content):
    chat = st.session_state.chats[st.session_state.current]
    chat["messages"].append({"role": role, "content": content})

    if role == "user" and len(chat["messages"]) == 2:
        chat["title"] = content[:30]

# ===== CSS (Clean ChatGPT Style) =====
st.markdown("""
<style>
.stApp {background:#0f172a; color:white;}

.chat-header {
    text-align:center;
    font-size:28px;
    font-weight:700;
    margin-bottom:10px;
}

.chat-message {
    display:flex;
    margin:12px 0;
    animation:fadeIn .25s ease-in;
}

@keyframes fadeIn {
    from {opacity:0; transform:translateY(5px);}
    to {opacity:1; transform:translateY(0);}
}

.user {justify-content:flex-end;}
.assistant {justify-content:flex-start;}

.bubble {
    max-width:70%;
    padding:14px 18px;
    border-radius:18px;
    font-size:15px;
    line-height:1.5;
}

.user-bubble {
    background:#2563eb;
    border-bottom-right-radius:6px;
}

.assistant-bubble {
    background:#1e293b;
    color:#e5e7eb;
    border-bottom-left-radius:6px;
}

section[data-testid="stSidebar"] {
    background:#020617;
}

.stChatInput input {
    border-radius:20px !important;
    padding:14px !important;
}
</style>
""", unsafe_allow_html=True)

# ===== SIDEBAR =====
with st.sidebar:
    st.title("💬 NovaChat")

    if st.button("➕ New Chat", use_container_width=True):
        new_chat()
        st.rerun()

    st.divider()

    for cid, data in sorted(
        st.session_state.chats.items(),
        key=lambda x: x[1]["created"],
        reverse=True
    ):
        if st.button(data["title"], key=cid, use_container_width=True):
            st.session_state.current = cid
            st.rerun()

    st.divider()

    model = st.selectbox(
        "Model",
        ["llama-3.1-8b-instant",
         "llama-3.3-70b-versatile"]
    )

# ===== MAIN =====
chat = st.session_state.chats[st.session_state.current]

st.markdown(
    f"<div class='chat-header'>✨ {chat['title']}</div>",
    unsafe_allow_html=True
)

# ===== SHOW MESSAGES =====
for m in chat["messages"][1:]:
    if m["role"] == "user":
        st.markdown(f"""
        <div class="chat-message user">
            <div class="bubble user-bubble">{m["content"]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message assistant">
            <div class="bubble assistant-bubble">{m["content"]}</div>
        </div>
        """, unsafe_allow_html=True)

# ===== INPUT =====
prompt = st.chat_input("Message Nova...")

if prompt:
    add_msg("user", prompt)

    st.markdown(f"""
    <div class="chat-message user">
        <div class="bubble user-bubble">{prompt}</div>
    </div>
    """, unsafe_allow_html=True)

    placeholder = st.empty()
    reply = ""

    stream = client.chat.completions.create(
        model=model,
        messages=chat["messages"],
        stream=True,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            reply += chunk.choices[0].delta.content
            placeholder.markdown(f"""
            <div class="chat-message assistant">
                <div class="bubble assistant-bubble">{reply}</div>
            </div>
            """, unsafe_allow_html=True)

    add_msg("assistant", reply)

st.markdown(
    "<center style='opacity:.5;margin-top:20px'>Made with ❤️ using Groq + Streamlit</center>",
    unsafe_allow_html=True
)
