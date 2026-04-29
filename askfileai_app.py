import streamlit as st
import os
from pathlib import Path
from io import BytesIO

from config import Config
from src.agent.graph import AskFileAIAgent

# ----------------------------------------------------
# Streamlit Page Settings
# ----------------------------------------------------
st.set_page_config(
    page_title="AskFileAI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------------------
# Custom CSS with 3D Animations
# ----------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');
    
    /* Main background with animated gradient */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    /* Sidebar with glass morphism */
    [data-testid="stSidebar"] {
        background: rgba(22, 22, 22, 0.7);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(76, 175, 80, 0.2);
    }
    
    /* Headers with glow effect */
    h1, h2, h3 {
        color: #ffffff;
        font-family: 'Orbitron', sans-serif;
        text-shadow: 0 0 20px rgba(76, 175, 80, 0.5);
        animation: textGlow 2s ease-in-out infinite alternate;
    }
    
    @keyframes textGlow {
        from { text-shadow: 0 0 10px rgba(76, 175, 80, 0.3); }
        to { text-shadow: 0 0 25px rgba(76, 175, 80, 0.8), 0 0 35px rgba(76, 175, 80, 0.4); }
    }
    
    /* Text */
    p, label, .stMarkdown {
        color: #e0e0e0;
        font-family: 'Rajdhani', sans-serif;
    }
    
    /* Input fields with 3D effect */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: linear-gradient(145deg, #2a2a3e, #1f1f2e);
        color: #ffffff;
        border: 2px solid transparent;
        border-radius: 12px;
        box-shadow: 
            5px 5px 15px rgba(0, 0, 0, 0.5),
            -5px -5px 15px rgba(50, 50, 80, 0.1);
        transition: all 0.3s ease;
        font-family: 'Rajdhani', sans-serif;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border: 2px solid #4CAF50;
        box-shadow: 
            0 0 20px rgba(76, 175, 80, 0.4),
            5px 5px 15px rgba(0, 0, 0, 0.5),
            inset 2px 2px 5px rgba(76, 175, 80, 0.1);
        transform: translateY(-2px);
    }
    
    /* File uploader with 3D card */
    [data-testid="stFileUploader"] {
        background: linear-gradient(145deg, #2a2a3e, #1f1f2e);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 
            8px 8px 20px rgba(0, 0, 0, 0.6),
            -8px -8px 20px rgba(50, 50, 80, 0.1);
        border: 1px solid rgba(76, 175, 80, 0.2);
        transition: all 0.4s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        transform: translateY(-5px) scale(1.01);
        box-shadow: 
            12px 12px 30px rgba(0, 0, 0, 0.7),
            -12px -12px 30px rgba(50, 50, 80, 0.15),
            0 0 30px rgba(76, 175, 80, 0.2);
    }
    
    /* Buttons with 3D effect and animation */
    .stButton > button {
        background: linear-gradient(145deg, #4CAF50, #45a049);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 28px;
        font-weight: bold;
        font-family: 'Orbitron', sans-serif;
        box-shadow: 
            6px 6px 15px rgba(0, 0, 0, 0.4),
            -2px -2px 10px rgba(76, 175, 80, 0.2);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton > button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 
            8px 8px 20px rgba(0, 0, 0, 0.5),
            -3px -3px 12px rgba(76, 175, 80, 0.3),
            0 0 25px rgba(76, 175, 80, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(0px) scale(0.98);
        box-shadow: 
            3px 3px 10px rgba(0, 0, 0, 0.4),
            inset 2px 2px 5px rgba(0, 0, 0, 0.3);
    }
    
    /* Answer box with floating animation */
    .answer-box {
        background: linear-gradient(145deg, #2a2a3e, #1f1f2e);
        border-radius: 16px;
        padding: 28px;
        margin-top: 20px;
        border-left: 5px solid #4CAF50;
        box-shadow: 
            10px 10px 25px rgba(0, 0, 0, 0.6),
            -5px -5px 15px rgba(50, 50, 80, 0.1),
            inset 0 0 20px rgba(76, 175, 80, 0.05);
        animation: floatBox 3s ease-in-out infinite;
        position: relative;
    }
    
    @keyframes floatBox {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .answer-box::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #4CAF50, #2196F3, #4CAF50);
        border-radius: 16px;
        opacity: 0;
        z-index: -1;
        transition: opacity 0.3s;
    }
    
    .answer-box:hover::before {
        opacity: 0.3;
        animation: borderRotate 3s linear infinite;
    }
    
    @keyframes borderRotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Logo with 3D effect */
    .logo-container {
        text-align: center;
        padding: 20px;
        margin-bottom: 30px;
        perspective: 1000px;
    }
    
    .logo-title {
        font-size: 32px;
        font-weight: 900;
        font-family: 'Orbitron', sans-serif;
        color: #ffffff;
        margin-bottom: 8px;
        text-shadow: 
            0 0 10px rgba(76, 175, 80, 0.5),
            0 0 20px rgba(76, 175, 80, 0.3),
            0 0 30px rgba(76, 175, 80, 0.2);
        animation: float 3s ease-in-out infinite;
        transform-style: preserve-3d;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotateX(0deg); }
        50% { transform: translateY(-10px) rotateX(5deg); }
    }
    
    .logo-subtitle {
        font-size: 14px;
        color: #4CAF50;
        font-family: 'Rajdhani', sans-serif;
        text-transform: uppercase;
        letter-spacing: 3px;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.6; }
        50% { opacity: 1; }
    }
    
    /* Card with 3D depth */
    
    
    /* Loading spinner with 3D rotation */
    .stSpinner > div {
        border-color: #4CAF50 !important;
        animation: spin3D 1s linear infinite;
    }
    
    @keyframes spin3D {
        0% { transform: rotate(0deg) scale(1); }
        50% { transform: rotate(180deg) scale(1.1); }
        100% { transform: rotate(360deg) scale(1); }
    }
    
    /* Success/Error with slide-in animation */
    .stSuccess, .stError, .stInfo {
        border-radius: 12px;
        animation: slideIn 0.5s ease-out;
        box-shadow: 
            5px 5px 15px rgba(0, 0, 0, 0.4),
            inset 0 0 10px rgba(255, 255, 255, 0.05);
    }
    
    @keyframes slideIn {
        from {
            transform: translateX(-100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    /* Download button special styling */
    .stDownloadButton > button {
        background: linear-gradient(145deg, #8e44ad, #7d3c98);
        box-shadow: 
            6px 6px 15px rgba(0, 0, 0, 0.4),
            -2px -2px 10px rgba(142, 68, 173, 0.2);
    }
    
    .stDownloadButton > button:hover {
        box-shadow: 
            8px 8px 20px rgba(0, 0, 0, 0.5),
            -3px -3px 12px rgba(142, 68, 173, 0.3),
            0 0 25px rgba(142, 68, 173, 0.4);
    }
    
    /* Particle effect background */
    .particle {
        position: fixed;
        width: 4px;
        height: 4px;
        background: rgba(76, 175, 80, 0.5);
        border-radius: 50%;
        animation: particleFloat 20s infinite;
        pointer-events: none;
    }
    
    @keyframes particleFloat {
        0% {
            transform: translateY(100vh) translateX(0);
            opacity: 0;
        }
        10% {
            opacity: 1;
        }
        90% {
            opacity: 1;
        }
        100% {
            transform: translateY(-100vh) translateX(100px);
            opacity: 0;
        }
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a2e;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #4CAF50, #45a049);
        border-radius: 6px;
        box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.5);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #45a049, #3d8b40);
    }
</style>
""", unsafe_allow_html=True)

# Add particle effect
st.markdown("""
<script>
    function createParticles() {
        const container = document.querySelector('.stApp');
        if (!container) return;
        
        for (let i = 0; i < 15; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.animationDelay = Math.random() * 20 + 's';
            particle.style.animationDuration = (15 + Math.random() * 10) + 's';
            container.appendChild(particle);
        }
    }
    
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', createParticles);
    } else {
        createParticles();
    }
</script>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# Ensure TEMP folder exists
# ----------------------------------------------------
TEMP_DIR = Path("./temp")
TEMP_DIR.mkdir(exist_ok=True)

def save_temp_file(uploaded_file):
    """Save uploaded file to ./temp and return path"""
    temp_path = TEMP_DIR / uploaded_file.name
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return str(temp_path)

# ----------------------------------------------------
# Initialize Session State
# ----------------------------------------------------
if 'agent' not in st.session_state:
    config = Config()
    st.session_state.agent = AskFileAIAgent(config)

if 'answer' not in st.session_state:
    st.session_state.answer = ""

if 'temp_file_path' not in st.session_state:
    st.session_state.temp_file_path = None

# ----------------------------------------------------
# Sidebar
# ----------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="logo-container">
        <div class="logo-title">🤖 AskFileAI</div>
        <div class="logo-subtitle">AI File Assistant</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Sidebar Actions
    st.subheader("📋 Actions")
    
    # Copy Answer Button
    if st.button("📋 Copy Answer", key="copy_btn", use_container_width=True):
        if st.session_state.answer:
            st.code(st.session_state.answer, language=None)
            st.success("✅ Answer ready to copy!")
        else:
            st.error("❌ No answer to copy yet.")
    
    # Read Aloud Button
    if st.button("🔊 Read Aloud", key="read_btn", use_container_width=True):
        if st.session_state.answer:
            st.info("💡 Tip: Use your browser's text-to-speech feature!")
        else:
            st.error("❌ No answer to read yet.")
    
    st.markdown("---")
    
    # Download Answer Button
    if st.session_state.answer:
        st.download_button(
            label="⬇️ Download Answer",
            data=st.session_state.answer,
            file_name="answer.txt",
            mime="text/plain",
            use_container_width=True
        )
    else:
        st.button("⬇️ Download Answer", disabled=True, use_container_width=True)
    
    # Clear Vector Store Button
    if st.button("🧹 Clear Vector Store", key="clear_btn", use_container_width=True):
        try:
            st.session_state.agent.vector_store.clear_collection()
            st.success("✅ Vector store cleared!")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    st.markdown("---")
    
    # Info Section
    with st.expander("ℹ️ About", expanded=False):
        st.write("""
        **AskFileAI** uses advanced AI to analyze your documents.
        
        **✨ Supported Formats:**
        - 📄 PDF, TXT, CSV
        - 📊 Excel (XLSX, XLS)
        - 📝 Word (DOCX)
        - 🖼️ Images (PNG, JPG)
        
        **🚀 How to Use:**
        1. Upload your file
        2. Ask a question
        3. Get instant AI answers
        
        **💡 Pro Tips:**
        - Be specific with questions
        - Upload clear, readable files
        - Use action buttons in sidebar
        """)
    
    # Stats
    st.markdown("---")
    st.caption("⚡ Powered by Advanced AI")
    st.caption("🔒 100% Local Processing")

# ----------------------------------------------------
# Main Content Area
# ----------------------------------------------------
st.title("🤖 AskFileAI")
st.markdown("### *Transform Your Documents into Conversations*")
st.markdown("Upload any file and unlock instant insights with AI-powered intelligence.")

st.markdown("<br>", unsafe_allow_html=True)

# File Upload Section
st.markdown('<div class="card">', unsafe_allow_html=True)
col1, col2 = st.columns([3, 1])

with col1:
    uploaded_file = st.file_uploader(
        "📂 Drop Your File Here or Click to Browse",
        type=["pdf", "txt", "csv", "xlsx", "xls", "docx", "png", "jpg", "jpeg"],
        help="Supported: PDF, TXT, CSV, Excel, Word, Images"
    )

with col2:
    if uploaded_file:
        st.success("✅ File Loaded")
        st.caption(f"📄 **{uploaded_file.name}**")
        st.caption(f"📦 {uploaded_file.size / 1024:.1f} KB")
    else:
        st.info("⏳ Awaiting File")
        st.caption("Upload to begin")

st.markdown('</div>', unsafe_allow_html=True)

# Question Section
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("#### ❓ Ask Your Question")
question = st.text_area(
    "",
    placeholder="What insights are you looking for? Ask anything about your document...",
    height=120,
    help="Be specific for better results",
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

# Ask Button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    ask_button = st.button("🚀 Generate Answer", use_container_width=True, type="primary")

# Process Question
if ask_button:
    if uploaded_file is None:
        st.error("⚠️ Please upload a file first!")
    elif question.strip() == "":
        st.error("⚠️ Please enter a question!")
    else:
        # Save uploaded file
        temp_path = save_temp_file(uploaded_file)
        st.session_state.temp_file_path = temp_path

        with st.spinner("🔍 Analyzing your document... AI is thinking..."):
            try:
                result = st.session_state.agent.ask(temp_path, question)
                st.session_state.answer = result["answer"]
                
                # Cleanup temp file
                try:
                    os.remove(temp_path)
                except:
                    pass
                
                st.success("✅ Answer generated successfully!")
                st.balloons()
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.session_state.answer = ""

# Display Answer
if st.session_state.answer:
    st.markdown("---")
    st.markdown("### 🧠 AI-Generated Answer")
    st.markdown(f'<div class="answer-box">{st.session_state.answer}</div>', unsafe_allow_html=True)
    
    # Additional info
    st.caption("💡 Use the sidebar to copy, download, or access more features.")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #4CAF50; padding: 20px; font-family: 'Rajdhani', sans-serif;">
    <p style="font-size: 18px; margin-bottom: 5px;">⚡ Made with Passion & AI</p>
    <p style="font-size: 14px; opacity: 0.7;">Empowering Document Intelligence | Streamlit + Advanced AI</p>
</div>
""", unsafe_allow_html=True)
