import os
import tempfile
import io
import streamlit as st
from streamlit_mic_recorder import mic_recorder

# Official Google GenAI SDK imports
from google import genai
from google.genai import types

# Custom backend modules
from src.chat_engine import ChatEngine
from src.export_utils import ChatExporter

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(
    page_title="DocChat-AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================================
# GEMINI STT CLIENT INITIALIZATION
# ==========================================================
client = genai.Client()

def transcribe_voice_bytes(audio_bytes):
    """
    Passes raw audio bytes directly to Gemini to transcribe speech to text.
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                "Transcribe this audio clip accurately. Only output the spoken text.",
                types.Part.from_bytes(
                    data=audio_bytes,
                    mime_type="audio/wav"
                )
            ]
        )
        return response.text
    except Exception as e:
        st.error(f"Gemini transcription failed: {str(e)}")
        return ""

# ==========================================================
# THEME STATE CONFIGURATION
# ==========================================================
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Light"

if st.session_state.theme_mode == "Light":
    theme_styles = {
        "bg": "#FAFAFC",
        "text": "#1E2022",
        "subtext": "#8E8E93",
        "sidebar_bg": "#FFFFFF",
        "border": "#ECECEC",
        "ai_bubble_bg": "#FFFFFF",
        "ai_bubble_text": "#1E2022",
        "ai_bubble_border": "#ECECEC",
        "chip_bg": "#FFFFFF",
        "chip_border": "#E8EEFF"
    }
else:  # Obsidian Dark Premium Mode
    theme_styles = {
        "bg": "#111214",
        "text": "#E3E3E3",
        "subtext": "#9CA3AF",
        "sidebar_bg": "#1A1C1E",
        "border": "#2C2E33",
        "ai_bubble_bg": "#1E1F22",
        "ai_bubble_text": "#E3E3E3",
        "ai_bubble_border": "#2C2E33",
        "chip_bg": "#1A1C1E",
        "chip_border": "#3E404A"
    }

# ==========================================================
# ULTRA-PREMIUM CHATGPT/CLAUDE CUSTOM CSS
# ==========================================================
st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght=300;400;500;600;700&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
    font-family: 'Inter', sans-serif;
    background-color: {theme_styles["bg"]} !important;
    color: {theme_styles["text"]} !important;
}}

#MainMenu {{visibility:hidden;}}
footer {{visibility:hidden;}}
header {{visibility:hidden;}}

.block-container {{
    padding-top: 1rem;
    padding-bottom: 9rem; 
    max-width: 800px !important;
}}

[data-testid="stSidebar"] {{
    background-color: {theme_styles["sidebar_bg"]} !important;
    border-right: 1px solid {theme_styles["border"]} !important;
}}
[data-testid="stSidebar"] h2 {{
    color: {theme_styles["text"]} !important;
}}

.sidebar-heading {{
    font-size: 0.75rem;
    font-weight: 700;
    color: {theme_styles["subtext"]};
    letter-spacing: 0.06rem;
    margin-top: 1.5rem;
    margin-bottom: 0.6rem;
}}

.pdf-card {{
    background: {theme_styles["sidebar_bg"]};
    border: 1px solid {theme_styles["border"]};
    border-radius: 10px;
    padding: 10px 14px;
    margin-bottom: 8px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.01);
}}
.pdf-card-title {{
    font-size: 0.85rem;
    font-weight: 600;
    color: {theme_styles["text"]};
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;
}}
.pdf-card-meta {{
    display: flex;
    justify-content: space-between;
    font-size: 0.75rem;
    color: {theme_styles["subtext"]};
    margin-top: 4px;
}}
.pdf-card-status {{
    color: #5B5CEB;
    font-weight: 600;
}}

.chat-row {{
    display: flex;
    width: 100%;
    margin-bottom: 1.5rem;
}}
.chat-row.user-layout {{
    justify-content: flex-end;
}}
.chat-row.ai-layout {{
    justify-content: flex-start;
}}

.custom-bubble {{
    max-width: 85%;
    padding: 1rem 1.25rem;
    font-size: 0.95rem;
    line-height: 1.5;
}}

.user-bubble {{
    background-color: #5B5CEB !important;
    color: #FFFFFF !important;
    border-radius: 20px 20px 4px 20px;
    box-shadow: 0 4px 15px rgba(91, 92, 235, 0.12);
}}

.ai-bubble {{
    background-color: {theme_styles["ai_bubble_bg"]} !important;
    color: {theme_styles["ai_bubble_text"]} !important;
    border: 1px solid {theme_styles["ai_bubble_border"]};
    border-radius: 20px 20px 20px 4px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.02);
}}

.source-container {{
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 8px;
    padding-left: 4px;
}}
.citation-chip {{
    background-color: {theme_styles["chip_bg"]};
    color: #5B5CEB;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 500;
    border: 1px solid {theme_styles["chip_border"]};
}}

.empty-state-container {{
    text-align: center;
    margin-top: 3rem;
    margin-bottom: 3rem;
}}
.empty-state-title {{
    font-size: 2rem;
    font-weight: 700;
    color: {theme_styles["text"]};
    margin-bottom: 6px;
}}
.empty-state-sub {{
    font-size: 0.95rem;
    color: {theme_styles["subtext"]};
}}

div.stButton > button {{
    width: 100%;
    border-radius: 10px !important;
    border: 1px solid {theme_styles["border"]} !important;
    background-color: {theme_styles["sidebar_bg"]} !important;
    color: {theme_styles["text"]} !important;
    font-weight: 500 !important;
    transition: all 0.2s ease;
}}
div.stButton > button:hover {{
    border-color: #5B5CEB !important;
    color: #5B5CEB !important;
    background-color: #EEF2FF !important;
}}

.action-btn-wrapper div.stButton > button {{
    background-color: #5B5CEB !important;
    color: white !important;
    border: none !important;
    font-weight: 600 !important;
}}
.action-btn-wrapper div.stButton > button:hover {{
    background-color: #6C63FF !important;
    box-shadow: 0 4px 12px rgba(91, 92, 235, 0.2) !important;
}}

div[data-testid="stChatInput"] {{
    border-radius: 24px !important;
    border: 1px solid {theme_styles["border"]} !important;
    background-color: {theme_styles["sidebar_bg"]} !important;
    box-shadow: 0 10px 40px rgba(0,0,0,0.06) !important;
    padding: 4px 8px !important;
}}
div[data-testid="stChatInput"] textarea {{
    color: {theme_styles["text"]} !important;
}}
</style>
""",
    unsafe_allow_html=True,
)

# ==========================================================
# TOP UTILITY HEADER: THEME CONTROLLER
# ==========================================================
top_col1, top_col2 = st.columns([8, 2])
with top_col2:
    theme_btn_label = "🌙 Dark Mode" if st.session_state.theme_mode == "Light" else "☀️ Light Mode"
    if st.button(theme_btn_label, key="theme_toggle"):
        st.session_state.theme_mode = "Dark" if st.session_state.theme_mode == "Light" else "Light"
        st.rerun()

# ==========================================================
# SESSION STATE INITIALIZATION
# ==========================================================
if "engine" not in st.session_state:
    st.session_state.engine = ChatEngine()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_exporter" not in st.session_state:
    st.session_state.chat_exporter = ChatExporter()

if "documents_loaded" not in st.session_state:
    st.session_state.documents_loaded = False

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

# ==========================================================
# SIDEBAR: MINIMALIST WORKSPACE CONTROLS
# ==========================================================
with st.sidebar:
    st.markdown("<h2 style='margin-bottom:0px; font-weight:700; font-size:1.4rem;'>📚 chatpdf AI</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:0.8rem; color:{theme_styles['subtext']}; margin-top:2px;'>AI-powered document assistant</p>", unsafe_allow_html=True)
    st.markdown(f"<hr style='margin: 12px 0; border-color: {theme_styles['border']};'>", unsafe_allow_html=True)

    # 1. Upload Section
    st.markdown("<div class='sidebar-heading'>➕ UPLOAD BASE</div>", unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Upload PDFs",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

    # 2. Workspace Selector
    st.markdown("<div class='sidebar-heading'>✨ AI WORKSPACE</div>", unsafe_allow_html=True)
    tool_option = st.selectbox(
        "AI Selection",
        [
            "💬 Chat with PDFs",
            "📄 Summarize PDFs",
            "📝 Generate Study Notes",
            "⚖️ Compare PDFs"
        ],
        label_visibility="collapsed"
    )
    st.markdown('<div class="action-btn-wrapper">', unsafe_allow_html=True)
    execute_tool = st.button("Run AI Tool →", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 3. Preferences Section
    st.markdown("<div class='sidebar-heading'>🌍 LANGUAGE PREFERENCE</div>", unsafe_allow_html=True)
    language = st.selectbox(
        "Language Selection",
        ["English", "Hindi", "Marathi", "French", "German"],
        label_visibility="collapsed"
    )

    # 4. Monitored Active Knowledge Index List
    st.markdown("<div class='sidebar-heading'>📂 UPLOADED DOCUMENTS</div>", unsafe_allow_html=True)
    if st.session_state.uploaded_files:
        for pdf in st.session_state.uploaded_files:
            st.markdown(f"""
            <div class="pdf-card">
                <div class="pdf-card-title">📄 {pdf}</div>
                <div class="pdf-card-meta">
                    <span>Active Memory</span>
                    <span class="pdf-card-status">✓ Indexed</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.caption("No context maps currently active.")

    # 5. Utilities
    st.markdown("<div class='sidebar-heading'>⚙️ SETTINGS</div>", unsafe_allow_html=True)
    col_exp, col_clr = st.columns(2)
    with col_exp:
        export_btn = st.button("Export Chat", use_container_width=True)
    with col_clr:
        clear_btn = st.button("Clear Chat", use_container_width=True)

# ==========================================================
# FILE CONVERSION & PARSING MECHANICS (FIXED RERUN cursor BUG)
# ==========================================================
if uploaded_files:
    current_uploader_filenames = [f.name for f in uploaded_files]
    
    if current_uploader_filenames != st.session_state.uploaded_files:
        with st.spinner("Processing updated knowledge base into vector space..."):
            paths = []
            for file in uploaded_files:
                # FIX: Explicitly reset byte cursor back to head before reading
                file.seek(0)
                file_bytes = file.read()
                
                temp_path = os.path.join(tempfile.gettempdir(), file.name)
                with open(temp_path, "wb") as f:
                    f.write(file_bytes)
                paths.append(temp_path)
            
            st.session_state.engine.load_pdfs(paths)
            st.session_state.uploaded_files = current_uploader_filenames
            st.session_state.documents_loaded = True
            
        st.toast(f"Synchronized {len(current_uploader_filenames)} documents successfully!", icon="⚡")
        st.rerun()

elif not uploaded_files and st.session_state.uploaded_files:
    st.session_state.uploaded_files = []
    st.session_state.documents_loaded = False
    st.rerun()

# ==========================================================
# QUICK ACTIONS / TOOL EXECUTION LOGIC PIPELINE
# ==========================================================
selected_quick_prompt = None

if execute_tool:
    if "Chat" in tool_option:
        st.toast("Submit your prompt using the bottom floating bar entry box.", icon="💬")
    else:
        if not st.session_state.uploaded_files:
            st.sidebar.error("Drop files in the knowledge base first.")
        else:
            selected_quick_prompt = f"Execute Workflow: {tool_option}"

# ==========================================================
# HERO CANVAS (EMPTY STATE PRESENTATION)
# ==========================================================
if not st.session_state.messages:
    st.markdown('<div class="empty-state-container">', unsafe_allow_html=True)
    st.markdown('<div class="empty-state-title">📚 chatpdf AI</div>', unsafe_allow_html=True)
    
    if st.session_state.uploaded_files:
        count = len(st.session_state.uploaded_files)
        st.markdown(f'<div class="empty-state-sub">{count} {"Document" if count==1 else "Documents"} loaded. Ready to execute context workflows.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="empty-state-sub">What would you like to know or dictate about your documents today?</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"<p style='font-size:0.8rem; font-weight:700; color:{theme_styles['subtext']}; letter-spacing:0.04rem; margin-bottom:12px; text-transform:uppercase;'>Suggested Workspace Actions</p>", unsafe_allow_html=True)
    grid_col1, grid_col2 = st.columns(2)
    
    with grid_col1:
        sum_card = st.button("📄 Summarize my uploaded documents", use_container_width=True)
        notes_card = st.button("📝 Formulate comprehensive study notes", use_container_width=True)
    with grid_col2:
        comp_card = st.button("⚖️ Detect structural contradictions & gaps", use_container_width=True)
        ask_card = st.button("❓ Query general semantic overview", use_container_width=True)

    if sum_card: selected_quick_prompt = "Execute Workflow: 📄 Summarize PDFs"
    if notes_card: selected_quick_prompt = "Execute Workflow: 📝 Generate Study Notes"
    if comp_card: selected_quick_prompt = "Execute Workflow: ⚖️ Compare PDFs"
    if ask_card: selected_quick_prompt = "Give me an overview of the core topics inside these files."

    if selected_quick_prompt:
        if not st.session_state.uploaded_files:
            st.error("Please drop reference documents inside the dropzone area first.")
        else:
            st.session_state.messages.append({"role": "user", "content": selected_quick_prompt})
            st.rerun()

# ==========================================================
# FLOATING DUAL CONSOLE INPUT CONTAINER (TEXT + VOICE)
# ==========================================================
st.write("---")
input_prompt_payload = None

# 1. Voice Capture Tray
col_v1, col_v2 = st.columns([7, 3])
with col_v2:
    st.markdown("<p style='font-size:0.75rem; font-weight:600; margin-bottom:2px; color:#5B5CEB;'>🎙️ Tap to Dictate Prompt</p>", unsafe_allow_html=True)
    voice_audio = mic_recorder(
        start_prompt="Record Voice",
        stop_prompt="Stop & Process",
        key="voice_input_processor",
        just_once=True,
        use_container_width=True
    )

    if voice_audio and voice_audio["bytes"]:
        with st.spinner("Gemini is listening..."):
            transcribed_text = transcribe_voice_bytes(voice_audio["bytes"])
            if transcribed_text.strip():
                input_prompt_payload = transcribed_text

# 2. Main Standard Text Entry Box
if user_text := st.chat_input("Ask anything about your uploaded documents..."):
    input_prompt_payload = user_text

# 3. Payload Delivery Pipeline 
if input_prompt_payload:
    st.session_state.messages.append({"role": "user", "content": input_prompt_payload})
    st.rerun()

# ==========================================================
# EXECUTE CORE AI PROCESSING PIPELINE
# ==========================================================
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    last_prompt = st.session_state.messages[-1]["content"]
    
    with st.spinner("Analyzing context structures..."):
        if "Summarize" in last_prompt: 
            answer = st.session_state.engine.summarize()
            source_strings = []
        elif "Study Notes" in last_prompt:
            answer = st.session_state.engine.generate_notes()
            source_strings = []
        elif "Compare" in last_prompt:
            answer = st.session_state.engine.compare_pdfs()
            source_strings = []
        else:
            result = st.session_state.engine.ask(last_prompt)
            answer = result["answer"]
            docs = result["sources"]
            
            source_strings = []
            for doc in docs:
                source_strings.append(f"{doc.metadata.get('source', 'Unknown')} (Pg. {doc.metadata.get('page', '?')})")

        if language != "English":
            answer = st.session_state.engine.translate_answer(answer, language)
        
        deduped_sources = sorted(list(set(source_strings)))
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "sources": deduped_sources
        })
        st.rerun()

# ==========================================================
# CONVERSATION RENDER ENGINE (HTML EMBEDDED LOOP)
# ==========================================================
if st.session_state.messages:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(
                f"""
                <div class="chat-row user-layout">
                    <div class="custom-bubble user-bubble">{message["content"]}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div class="chat-row ai-layout">
                    <div class="custom-bubble ai-bubble">{message["content"]}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            if "sources" in message and message["sources"]:
                unique_sources = sorted(list(set(message["sources"])))
                chips_html = '<div class="source-container">'
                for src in unique_sources:
                    chips_html += f'<span class="citation-chip">📌 {src}</span>'
                chips_html += '</div><br>'
                st.markdown(chips_html, unsafe_allow_html=True)

# ==========================================================
# UTILITIES AND EXPORTS
# ==========================================================
if clear_btn:
    st.session_state.messages = []
    st.rerun()

if export_btn:
    if not st.session_state.messages:
        st.sidebar.warning("No dialog parameters logged.")
    else:
        path = st.session_state.chat_exporter.export_chat(st.session_state.messages)
        with open(path, "rb") as f:
            st.sidebar.download_button(
                "⬇️ Download Chat Log PDF",
                f,
                file_name="chatpdf_history.pdf",
                mime="application/pdf",
                use_container_width=True
            )