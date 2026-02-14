# import streamlit as st
# from groq import Groq
# import time
# from datetime import datetime

# # ===== API KEY (PASTE YOUR KEY HERE) =====
# GROQ_API_KEY = "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"
# client = Groq(api_key=GROQ_API_KEY)

# # ===== CONFIG =====
# st.set_page_config(
#     page_title="NovaChat",
#     page_icon="💬",
#     layout="wide"
# )

# # ===== SESSION STATE =====
# if "chats" not in st.session_state:
#     cid = str(int(time.time()))
#     st.session_state.chats = {
#         cid: {
#             "title": "New Chat",
#             "created": datetime.now(),
#             "messages": [
#                 {"role": "system", "content": "You are a helpful AI assistant."}
#             ],
#         }
#     }
#     st.session_state.current = cid

# # ===== FUNCTIONS =====
# def new_chat():
#     cid = str(int(time.time()))
#     st.session_state.chats[cid] = {
#         "title": "New Chat",
#         "created": datetime.now(),
#         "messages": [
#             {"role": "system", "content": "You are a helpful AI assistant."}
#         ],
#     }
#     st.session_state.current = cid

# def add_msg(role, content):
#     chat = st.session_state.chats[st.session_state.current]
#     chat["messages"].append({"role": role, "content": content})

#     if role == "user" and len(chat["messages"]) == 2:
#         chat["title"] = content[:30]

# # ===== CSS (Clean ChatGPT Style) =====
# st.markdown("""
# <style>
# .stApp {background:#0f172a; color:white;}

# .chat-header {
#     text-align:center;
#     font-size:28px;
#     font-weight:700;
#     margin-bottom:10px;
# }

# .chat-message {
#     display:flex;
#     margin:12px 0;
#     animation:fadeIn .25s ease-in;
# }

# @keyframes fadeIn {
#     from {opacity:0; transform:translateY(5px);}
#     to {opacity:1; transform:translateY(0);}
# }

# .user {justify-content:flex-end;}
# .assistant {justify-content:flex-start;}

# .bubble {
#     max-width:70%;
#     padding:14px 18px;
#     border-radius:18px;
#     font-size:15px;
#     line-height:1.5;
# }

# .user-bubble {
#     background:#2563eb;
#     border-bottom-right-radius:6px;
# }

# .assistant-bubble {
#     background:#1e293b;
#     color:#e5e7eb;
#     border-bottom-left-radius:6px;
# }

# section[data-testid="stSidebar"] {
#     background:#020617;
# }

# .stChatInput input {
#     border-radius:20px !important;
#     padding:14px !important;
# }
# </style>
# """, unsafe_allow_html=True)

# # ===== SIDEBAR =====
# with st.sidebar:
#     st.title("💬 NovaChat")

#     if st.button("➕ New Chat", use_container_width=True):
#         new_chat()
#         st.rerun()

#     st.divider()

#     for cid, data in sorted(
#         st.session_state.chats.items(),
#         key=lambda x: x[1]["created"],
#         reverse=True
#     ):
#         if st.button(data["title"], key=cid, use_container_width=True):
#             st.session_state.current = cid
#             st.rerun()

#     st.divider()

#     model = st.selectbox(
#         "Model",
#         ["llama-3.1-8b-instant",
#          "llama-3.3-70b-versatile"]
#     )

# # ===== MAIN =====
# chat = st.session_state.chats[st.session_state.current]

# st.markdown(
#     f"<div class='chat-header'>✨ {chat['title']}</div>",
#     unsafe_allow_html=True
# )

# # ===== SHOW MESSAGES =====
# for m in chat["messages"][1:]:
#     if m["role"] == "user":
#         st.markdown(f"""
#         <div class="chat-message user">
#             <div class="bubble user-bubble">{m["content"]}</div>
#         </div>
#         """, unsafe_allow_html=True)
#     else:
#         st.markdown(f"""
#         <div class="chat-message assistant">
#             <div class="bubble assistant-bubble">{m["content"]}</div>
#         </div>
#         """, unsafe_allow_html=True)

# # ===== INPUT =====
# prompt = st.chat_input("Message Nova...")

# if prompt:
#     add_msg("user", prompt)

#     st.markdown(f"""
#     <div class="chat-message user">
#         <div class="bubble user-bubble">{prompt}</div>
#     </div>
#     """, unsafe_allow_html=True)

#     placeholder = st.empty()
#     reply = ""

#     stream = client.chat.completions.create(
#         model=model,
#         messages=chat["messages"],
#         stream=True,
#     )

#     for chunk in stream:
#         if chunk.choices[0].delta.content:
#             reply += chunk.choices[0].delta.content
#             placeholder.markdown(f"""
#             <div class="chat-message assistant">
#                 <div class="bubble assistant-bubble">{reply}</div>
#             </div>
#             """, unsafe_allow_html=True)

#     add_msg("assistant", reply)

# st.markdown(
#     "<center style='opacity:.5;margin-top:20px'>Made with ❤️ using Groq + Streamlit</center>",
#     unsafe_allow_html=True
# )








import streamlit as st
from groq import Groq
import time
from datetime import datetime
import json
import os
import tempfile
import pdfplumber
from docx import Document
from fpdf import FPDF
import base64

# ===== API KEY =====
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# ===== CONFIG =====
st.set_page_config(
    page_title="Nova Advanced",
    page_icon="✨",
    layout="wide"
)

# ===== SESSION STATE INIT =====
if "chats" not in st.session_state:
    cid = str(int(time.time()))
    st.session_state.chats = {
        cid: {
            "title": "New Chat",
            "created": datetime.now().isoformat(),
            "system_prompt": "You are Nova, a highly accurate and factual AI assistant. Think step-by-step. Give concise, truthful answers. If unsure, say you don't know.",
            "messages": [],  # each message: {"role": str, "content": str}
            "memory": {"user_name": None}  # simple memory
        }
    }
    st.session_state.current = cid
    st.session_state.stop_generation = False
    st.session_state.regenerate_target = None
    st.session_state.theme = "dark"
    st.session_state.user_name = "User"

# ===== HELPER FUNCTIONS =====
def new_chat():
    cid = str(int(time.time()))
    st.session_state.chats[cid] = {
        "title": "New Chat",
        "created": datetime.now().isoformat(),
        "system_prompt": "You are Nova, a highly accurate and factual AI assistant. Think step-by-step. Give concise, truthful answers. If unsure, say you don't know.",
        "messages": [],
        "memory": {"user_name": st.session_state.user_name}
    }
    st.session_state.current = cid

def delete_chat(cid):
    if cid in st.session_state.chats:
        del st.session_state.chats[cid]
    if st.session_state.current == cid:
        if st.session_state.chats:
            st.session_state.current = next(iter(st.session_state.chats))
        else:
            new_chat()
    st.rerun()

def rename_chat(cid, new_title):
    if cid in st.session_state.chats:
        st.session_state.chats[cid]["title"] = new_title

def add_msg(role, content):
    chat = st.session_state.chats[st.session_state.current]
    chat["messages"].append({"role": role, "content": content})
    if role == "user" and len(chat["messages"]) == 1:
        chat["title"] = content[:30]

def update_system_prompt(new_prompt):
    st.session_state.chats[st.session_state.current]["system_prompt"] = new_prompt

def get_messages_for_api():
    """Return messages list without any extra fields (only role, content)"""
    chat = st.session_state.chats[st.session_state.current]
    msgs = [{"role": "system", "content": chat["system_prompt"]}]
    for m in chat["messages"]:
        msgs.append({"role": m["role"], "content": m["content"]})
    return msgs

def export_chat_as_markdown(cid):
    chat = st.session_state.chats[cid]
    lines = [f"# {chat['title']}\n", f"*Created: {chat['created']}*\n"]
    for msg in chat["messages"]:
        role = "**User**" if msg["role"] == "user" else "**Nova**"
        lines.append(f"\n{role}: {msg['content']}\n")
    return "\n".join(lines)

def export_chat_as_pdf(cid):
    chat = st.session_state.chats[cid]
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=chat['title'], ln=1, align='C')
    pdf.ln(10)
    for msg in chat["messages"]:
        role = "User: " if msg["role"] == "user" else "Nova: "
        pdf.multi_cell(0, 10, txt=role + msg['content'])
        pdf.ln(5)
    return pdf.output(dest='S').encode('latin1')

def extract_text_from_file(uploaded_file):
    text = ""
    if uploaded_file.type == "application/pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(uploaded_file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    elif uploaded_file.type == "text/plain":
        text = uploaded_file.read().decode("utf-8")
    return text

# ===== THEME CSS =====
def get_theme_css():
    if st.session_state.theme == "dark":
        return """
        <style>
        .stApp { background: linear-gradient(135deg, #0f172a, #020617); color: white; }
        .assistant-bubble { background:#1e293b; border:1px solid #334155; color:#e5e7eb; }
        section[data-testid="stSidebar"] { background:#020617; border-right:1px solid #1f2937; }
        .stChatInput input { background:#020617 !important; color:white !important; border:1px solid #334155 !important; }
        </style>
        """
    else:
        return """
        <style>
        .stApp { background: #f8fafc; color: #0f172a; }
        .assistant-bubble { background: #e2e8f0; border:1px solid #cbd5e1; color: #0f172a; }
        section[data-testid="stSidebar"] { background: #f1f5f9; border-right:1px solid #cbd5e1; }
        .stChatInput input { background: white !important; color: black !important; border:1px solid #cbd5e1 !important; }
        .chat-header { -webkit-text-fill-color: #0f172a; background: none; }
        </style>
        """

st.markdown(get_theme_css(), unsafe_allow_html=True)

# Base CSS (shared)
st.markdown("""
<style>
.chat-header { text-align:center; font-size:34px; font-weight:800; margin-bottom:10px; }
.chat-message { display:flex; align-items:flex-end; margin:14px 0; animation:fadeIn .25s ease-in; }
@keyframes fadeIn { from {opacity:0; transform:translateY(6px);} to {opacity:1; transform:translateY(0);} }
.avatar { font-size:22px; margin:0 8px; }
.user { justify-content:flex-end; }
.assistant { justify-content:flex-start; }
.bubble { max-width:70%; padding:14px 18px; border-radius:18px; font-size:15px; line-height:1.6; }
.user-bubble { background:linear-gradient(135deg,#2563eb,#7c3aed); color:white; border-bottom-right-radius:6px; }
.assistant-bubble { border-bottom-left-radius:6px; }
.stButton>button { border-radius:12px; }
.chat-controls { display:flex; gap:5px; margin-top:5px; }
.chat-controls button { background:transparent; border:none; color:#aaa; cursor:pointer; font-size:12px; }
.chat-controls button:hover { color:white; }
</style>
""", unsafe_allow_html=True)

# ===== SIDEBAR =====
with st.sidebar:
    st.title("✨ Nova Advanced")

    # User name (simple memory)
    st.session_state.user_name = st.text_input("Your name", value=st.session_state.user_name)
    if st.button("Remember me"):
        for cid in st.session_state.chats:
            st.session_state.chats[cid]["memory"]["user_name"] = st.session_state.user_name
        st.success("Name saved to memory!")

    st.divider()

    # New chat
    if st.button("➕ New Chat", use_container_width=True):
        new_chat()
        st.rerun()

    st.divider()

    # Chat list with rename/delete
    for cid, data in sorted(
        st.session_state.chats.items(),
        key=lambda x: x[1]["created"],
        reverse=True
    ):
        col1, col2, col3 = st.columns([6, 1, 1])
        with col1:
            if st.button(data["title"], key=f"chat_{cid}", use_container_width=True):
                st.session_state.current = cid
                st.rerun()
        with col2:
            if st.button("✏️", key=f"rename_{cid}"):
                st.session_state[f"renaming_{cid}"] = True
        with col3:
            if st.button("🗑️", key=f"delete_{cid}"):
                delete_chat(cid)

        if st.session_state.get(f"renaming_{cid}", False):
            new_name = st.text_input("New name", value=data["title"], key=f"rename_input_{cid}")
            if st.button("Save", key=f"save_rename_{cid}"):
                rename_chat(cid, new_name)
                st.session_state[f"renaming_{cid}"] = False
                st.rerun()

    st.divider()

    # Model and temperature
    model = st.selectbox(
        "Model",
        ["llama-3.3-70b-versatile",
         "mixtral-8x7b-32768",
         "gemma2-9b-it",
         "llama-3.1-8b-instant"],
        index=0
    )
    temperature = st.slider("Temperature", 0.0, 2.0, 0.0, 0.1)

    # Theme toggle
    theme_choice = st.radio("Theme", ["dark", "light"], index=0 if st.session_state.theme=="dark" else 1)
    if theme_choice != st.session_state.theme:
        st.session_state.theme = theme_choice
        st.rerun()

    st.divider()

    # Smart Modes
    mode = st.selectbox("Mode", ["General", "Study", "Coding", "Interview", "Fun"])
    if mode == "Study":
        sys_prompt = "You are a study assistant. Provide clear explanations and examples. Be concise."
    elif mode == "Coding":
        sys_prompt = "You are a coding expert. Give clean, efficient code with explanations."
    elif mode == "Interview":
        sys_prompt = "You are an interview coach. Ask relevant questions and provide feedback."
    elif mode == "Fun":
        sys_prompt = "You are a fun and creative assistant. Be witty and engaging."
    else:
        sys_prompt = "You are Nova, a helpful assistant. Be accurate and concise."
    if st.button("Apply Mode"):
        update_system_prompt(sys_prompt)
        st.success(f"Switched to {mode} mode")

    st.divider()

    # System prompt editor
    with st.expander("System Prompt (advanced)"):
        current_system = st.session_state.chats[st.session_state.current]["system_prompt"]
        new_system = st.text_area("Edit", value=current_system, height=100)
        if st.button("Update"):
            update_system_prompt(new_system)

    st.divider()

    # PDF/DOCX upload
    uploaded_file = st.file_uploader("Upload document (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
    if uploaded_file is not None:
        with st.spinner("Extracting text..."):
            text = extract_text_from_file(uploaded_file)
            # Store in session or just add to context? We'll add as a user message with note
            if text:
                st.success("Text extracted! You can now ask about it.")
                # Option to include in context automatically? We'll put a button to add as context
                if st.button("Add document to context"):
                    add_msg("user", f"[Uploaded document: {uploaded_file.name}]\n\n{text[:2000]}...")  # limit
                    st.rerun()

    st.divider()

    # Export
    export_format = st.radio("Export format", ["Markdown", "PDF"])
    if st.button("Export current chat"):
        if export_format == "Markdown":
            md = export_chat_as_markdown(st.session_state.current)
            st.download_button("Download Markdown", data=md, file_name="chat.md", mime="text/markdown")
        else:
            pdf_bytes = export_chat_as_pdf(st.session_state.current)
            st.download_button("Download PDF", data=pdf_bytes, file_name="chat.pdf", mime="application/pdf")

# ===== MAIN CHAT AREA =====
chat = st.session_state.chats[st.session_state.current]

# Display header with memory greeting
if chat["memory"]["user_name"]:
    greeting = f"Welcome back, {chat['memory']['user_name']}!"
else:
    greeting = "Welcome to Nova!"
st.markdown(f"<div class='chat-header'>✨ Nova AI <span style='font-size:16px;'>({greeting})</span></div>", unsafe_allow_html=True)

# ===== DISPLAY MESSAGES =====
for idx, m in enumerate(chat["messages"]):
    if m["role"] == "user":
        st.markdown(f"""
        <div class="chat-message user">
            <div class="bubble user-bubble">{m["content"]}</div>
            <div class="avatar">🧑‍💻</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message assistant">
            <div class="avatar">✨</div>
            <div class="bubble assistant-bubble">{m["content"]}</div>
        </div>
        """, unsafe_allow_html=True)

# ===== REGENERATION =====
if chat["messages"] and chat["messages"][-1]["role"] == "assistant":
    if st.button("🔄 Regenerate", help="Regenerate last response"):
        chat["messages"].pop()
        st.session_state.regenerate_target = st.session_state.current
        st.rerun()

# ===== STOP GENERATION =====
if st.session_state.get("streaming", False):
    if st.button("⏹️ Stop", key="stop_button"):
        st.session_state.stop_generation = True

# ===== INPUT =====
prompt = st.chat_input("Ask Nova anything...")

if prompt:
    add_msg("user", prompt)

    st.markdown(f"""
    <div class="chat-message user">
        <div class="bubble user-bubble">{prompt}</div>
        <div class="avatar">🧑‍💻</div>
    </div>
    """, unsafe_allow_html=True)

    # Prepare messages for API (no timestamps)
    messages = get_messages_for_api()

    placeholder = st.empty()
    reply = ""
    st.session_state.streaming = True
    st.session_state.stop_generation = False

    try:
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
            temperature=temperature,
            top_p=0.1,
            max_tokens=1024
        )

        for chunk in stream:
            if st.session_state.stop_generation:
                stream.close()
                break
            if chunk.choices[0].delta.content:
                reply += chunk.choices[0].delta.content
                placeholder.markdown(f"""
                <div class="chat-message assistant">
                    <div class="avatar">✨</div>
                    <div class="bubble assistant-bubble">{reply}</div>
                </div>
                """, unsafe_allow_html=True)

    finally:
        st.session_state.streaming = False
        st.session_state.stop_generation = False

    if reply.strip():
        add_msg("assistant", reply)
    else:
        st.warning("No response generated. Please try again.")

# ===== REGENERATION HANDLER =====
if st.session_state.get("regenerate_target") == st.session_state.current:
    st.session_state.regenerate_target = None
    # Find last user message
    last_user = None
    for m in reversed(chat["messages"]):
        if m["role"] == "user":
            last_user = m["content"]
            break
    if last_user:
        # We have removed the last assistant, so we can re-run generation by simulating input
        # To avoid duplicating code, we set a flag to regenerate in next run with same prompt
        st.session_state.regenerate_prompt = last_user
        st.rerun()

if "regenerate_prompt" in st.session_state:
    prompt = st.session_state.pop("regenerate_prompt")
    # Use same generation code (we'll just call the same block, but careful not to add duplicate user message)
    # Since we already removed the assistant, the messages list is ready. We'll just call the API again.
    messages = get_messages_for_api()
    placeholder = st.empty()
    reply = ""
    st.session_state.streaming = True
    st.session_state.stop_generation = False

    try:
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
            temperature=temperature,
            top_p=0.1,
            max_tokens=1024
        )

        for chunk in stream:
            if st.session_state.stop_generation:
                stream.close()
                break
            if chunk.choices[0].delta.content:
                reply += chunk.choices[0].delta.content
                placeholder.markdown(f"""
                <div class="chat-message assistant">
                    <div class="avatar">✨</div>
                    <div class="bubble assistant-bubble">{reply}</div>
                </div>
                """, unsafe_allow_html=True)

    finally:
        st.session_state.streaming = False
        st.session_state.stop_generation = False

    if reply.strip():
        add_msg("assistant", reply)

# Footer
st.markdown(
    "<center style='opacity:.4;margin-top:20px'>Nova Advanced • Powered by Groq • Memory • PDF Chat • Themes • Export</center>",
    unsafe_allow_html=True
)
