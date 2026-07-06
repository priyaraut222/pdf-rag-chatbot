import streamlit as st
from src.chat_engine import ChatEngine

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="DocMind AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ======================================================
# CUSTOM CSS
# ======================================================

st.markdown(
    """
<style>

#MainMenu{
visibility:hidden;
}

footer{
visibility:hidden;
}

header{
visibility:hidden;
}

.block-container{
padding-top:1.5rem;
}

[data-testid="stSidebar"]{
background:#111827;
}

.chat-title{
font-size:38px;
font-weight:700;
color:white;
margin-bottom:5px;
}

.sub-title{
color:#9ca3af;
font-size:15px;
margin-bottom:30px;
}

.feature-box{
background:#1f2937;
padding:15px;
border-radius:12px;
margin-bottom:15px;
}

.source-box{
background:#0f172a;
padding:10px;
border-radius:10px;
border-left:4px solid #38bdf8;
margin-top:15px;
}

.big-button button{
width:100%;
height:48px;
font-size:16px;
}

</style>
""",
    unsafe_allow_html=True,
)

# ======================================================
# SESSION STATE
# ======================================================

if "engine" not in st.session_state:
    st.session_state.engine = ChatEngine()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "documents_loaded" not in st.session_state:
    st.session_state.documents_loaded = False

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

# ======================================================
# SIDEBAR
# ======================================================

with st.sidebar:

    st.title("⚙️ Control Panel")

    st.divider()

    uploaded_files = st.file_uploader(
        "Upload PDFs",
        type=["pdf"],
        accept_multiple_files=True,
    )

    st.divider()

    language = st.selectbox(
        "Language",
        [
            "English",
            "Hindi",
            "Marathi",
            "French",
            "German"
        ]
    )

    st.divider()

    st.markdown("### AI Tools")

    summarize = st.button(
        "📄 Summarize PDFs",
        use_container_width=True,
    )

    notes = st.button(
        "📝 Generate Notes",
        use_container_width=True,
    )

    compare = st.button(
        "⚖ Compare PDFs",
        use_container_width=True,
    )

    st.divider()

    st.markdown("### Chat")

    clear_chat = st.button(
        "🗑 Clear Chat",
        use_container_width=True,
    )

    export_chat = st.button(
        "📥 Export Chat",
        use_container_width=True,
    )

# ======================================================
# MAIN PAGE
# ======================================================

st.markdown(
    """
<div class="chat-title">
📚 DocMind AI
</div>

<div class="sub-title">
Multi PDF RAG Assistant powered by Gemini + FAISS
</div>
""",
    unsafe_allow_html=True,
)

# ======================================================
# LOAD PDFs
# ======================================================

if uploaded_files and not st.session_state.documents_loaded:

    with st.spinner("Indexing PDFs..."):

        import tempfile
        import os

        paths = []

        for file in uploaded_files:

            temp_path = os.path.join(
                tempfile.gettempdir(),
                file.name
            )

            with open(temp_path, "wb") as f:
                f.write(file.read())

            paths.append(temp_path)

        st.session_state.engine.load_pdfs(paths)

        st.session_state.documents_loaded = True

        st.session_state.uploaded_files = [
            f.name for f in uploaded_files
        ]

    st.success("Documents indexed successfully!")

# ======================================================
# SHOW PDF LIST
# ======================================================

if st.session_state.uploaded_files:

    with st.expander("Uploaded Documents"):

        for pdf in st.session_state.uploaded_files:

            st.write("📄", pdf)

# ======================================================
# CHAT HISTORY
# ======================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if "sources" in message:

            st.markdown(
                """
<div class="source-box">
<b>Sources</b><br>
"""
                + "<br>".join(message["sources"])
                + "</div>",
                unsafe_allow_html=True,
            )

# ======================================================
# CHAT INPUT
# ======================================================

prompt = st.chat_input(
    "Ask anything about your PDFs..."
)

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):
    