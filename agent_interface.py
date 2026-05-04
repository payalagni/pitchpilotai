"""
PitchPilot AI - Agent Interface (Design System v2)
Pixel-perfect to wireframes from DESIGN.md
"""

import streamlit as st
import json
import os
from datetime import datetime
from typing import List, Dict, Any

# Import local modules
from deck_engine import DeckEngine
from ai_engine import AIEngine
from verification_engine import VerificationEngine
from knowledge_base import KnowledgeBase, render_knowledge_base_manager


# ==================== DESIGN SYSTEM ====================
# Based on DESIGN.md - PitchPilot AI Visual Language
STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Work+Sans:wght@300;400;500;600;700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap');

:root {
    --background: #f7fafc;
    --surface: #ffffff;
    --surface-container: #f1f5f9;
    --surface-container-high: #e2e8f0;
    --surface-container-highest: #cbd5e1;
    --surface-variant: #e2e8f0;
    --on-surface: #0f172a;
    --on-background: #0f172a;
    --outline: #cbd5e1;
    --primary: #2563eb;
    --on-primary: #ffffff;
    --secondary: #10b981;
    --on-secondary: #ffffff;
    --surface-tint: #2563eb;
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

html, body, .stApp {
    background-color: var(--background) !important;
    color: var(--on-background) !important;
    font-family: 'Work Sans', sans-serif !important;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

::-webkit-scrollbar {width: 8px; height: 8px;}
::-webkit-scrollbar-track {background: #e2e8f0;}
::-webkit-scrollbar-thumb {background: #94a3b8; border-radius: 8px;}

.stApp, .block-container {
    padding: 1.5rem 1.5rem 2rem !important;
}

.stSidebar {
    background: #ffffff;
    border-right: 1px solid rgba(15, 23, 42, 0.08);
}

.stSidebar .css-1d391kg, .stSidebar .css-1d8n9bt {
    padding-top: 1.25rem;
}

.stButton>button {
    border-radius: 12px !important;
}

.page-card {
    background: #ffffff;
    border: 1px solid #d1d5db;
    border-radius: 18px;
    padding: 24px;
    box-shadow: 0 22px 45px rgba(15, 23, 42, 0.08);
}

.page-card .card-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 10px;
}

.page-card .card-text {
    color: #475569;
    font-size: 0.95rem;
    line-height: 1.6;
}

.hero-section {
    background: linear-gradient(180deg, rgba(59,130,246,0.12), transparent 92%);
    border: 1px solid #bfdbfe;
    border-radius: 24px;
    padding: 32px;
}

.hero-heading {
    font-size: 2rem;
    font-weight: 800;
    line-height: 1.08;
    margin-bottom: 14px;
}

.hero-subtitle {
    color: #475569;
    font-size: 1rem;
    line-height: 1.7;
}

.section-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 0.75rem;
}

.section-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 22px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.section-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 18px 32px rgba(15, 23, 42, 0.08);
}

.section-card-title {
    font-size: 1rem;
    font-weight: 700;
    color: #111827;
    margin-bottom: 10px;
}

.section-card-text {
    color: #475569;
    font-size: 0.95rem;
    margin-bottom: 18px;
}

.divider {
    height: 1px;
    background: #e2e8f0;
    margin: 28px 0;
}

.caption-pill {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 8px 14px;
    border-radius: 999px;
    background: #eff6ff;
    color: #1d4ed8;
    font-size: 0.9rem;
}

.btn-primary {
    background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
    color: #ffffff !important;
    border: none !important;
}

.btn-secondary {
    background: #ffffff !important;
    color: #2563eb !important;
    border: 1px solid #cbd5e1 !important;
}
::-webkit-scrollbar-thumb {background: #3c4a3c; border-radius: 3px;}
::-webkit-scrollbar-thumb:hover {background: #869583;}

/* Material Symbols */
.material-symbols-outlined {
    font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
    font-family: 'Material Symbols Outlined';
    font-size: 24px;
}

/* Glow Hover Effect */
.glow-hover:hover {
    box-shadow: 0 0 20px rgba(63, 229, 108, 0.15);
    border-color: #3fe56c !important;
}

/* Pulse Dot Animation */
.pulse-dot {
    width: 8px;
    height: 8px;
    background-color: #3fe56c;
    border-radius: 50%;
    animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.7; transform: scale(0.9); }
}

/* Thinking Animation */
.thinking-dot {
    width: 8px;
    height: 8px;
    background-color: #3fe56c;
    border-radius: 50%;
    animation: thinking 1.4s infinite ease-in-out both;
}

.thinking-dot:nth-child(1) { animation-delay: -0.32s; }
.thinking-dot:nth-child(2) { animation-delay: -0.16s; }
.thinking-dot:nth-child(3) { animation-delay: 0s; }

@keyframes thinking {
    0%, 80%, 100% { transform: scale(0.6); opacity: 0.5; }
    40% { transform: scale(1); opacity: 1; }
}

/* Card Styles */
.action-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 24px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.action-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 18px 32px rgba(15, 23, 42, 0.08);
}

.btn-primary {
    background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
    color: #ffffff !important;
    padding: 12px 24px;
    border-radius: 12px;
    font-weight: 700;
    border: none;
    cursor: pointer;
    transition: all 0.2s ease;
}

.btn-primary:hover {
    box-shadow: 0 12px 30px rgba(37, 99, 235, 0.18);
}

.btn-secondary {
    background: #ffffff !important;
    color: #2563eb !important;
    padding: 12px 24px;
    border-radius: 12px;
    font-weight: 600;
    border: 1px solid #cbd5e1;
    cursor: pointer;
    transition: all 0.2s ease;
}

.btn-secondary:hover {
    background: #eff6ff !important;
}

/* Custom button styles for dashboard actions */
[data-testid="stButton-btn_build"] > button,
[data-testid="stButton-btn_update"] > button {
    background: #2563eb !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 16px !important;
    min-height: 56px;
    box-shadow: 0 8px 20px rgba(37, 99, 235, 0.12) !important;
}

[data-testid="stButton-btn_build"] > button:hover,
[data-testid="stButton-btn_update"] > button:hover {
    background: #1d4ed8 !important;
}

[data-testid="stButton-btn_build"] > button span,
[data-testid="stButton-btn_update"] > button span {
    color: #ffffff !important;
}

/* Input Styles */
.input-field {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    color: #0f172a;
    padding: 14px 16px;
    border-radius: 10px;
    width: 100%;
    font-family: 'Work Sans', sans-serif;
    font-size: 14px;
    transition: all 0.2s ease;
}

.input-field:focus {
    outline: none;
    border-color: #2563eb;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
}

.input-field::placeholder {
    color: #64748b;
}

/* Sidebar Navigation */
.nav-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    border-radius: 12px;
    color: #475569;
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 14px;
    font-weight: 500;
}

.nav-item:hover {
    background: #eff6ff;
    color: #2563eb;
}

.nav-item.active {
    background: #dbeafe;
    color: #1d4ed8;
    border-left: 2px solid #2563eb;
}

/* Badge Styles */
.badge {
    display: inline-flex;
    align-items: center;
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.badge-primary {
    background: rgba(37, 99, 235, 0.12);
    border: 1px solid rgba(37, 99, 235, 0.22);
    color: #1d4ed8;
}

/* Gradient Background */
.gradient-bg {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: -1;
    overflow: hidden;
}

.gradient-blob-1 {
    position: absolute;
    top: -10%;
    right: -5%;
    width: 40%;
    height: 60%;
    background: rgba(37, 99, 235, 0.08);
    filter: blur(120px);
    border-radius: 50%;
}

.gradient-blob-2 {
    position: absolute;
    bottom: -10%;
    left: -5%;
    width: 30%;
    height: 50%;
    background: rgba(59, 130, 246, 0.06);
    filter: blur(100px);
    border-radius: 50%;
}

/* Chat Messages */
.chat-user {
    background: #eff6ff;
    padding: 16px 20px;
    border-radius: 18px 18px 4px 18px;
    margin: 8px 0 8px 40px;
    color: #0f172a;
}

.chat-assistant {
    background: #ffffff;
    padding: 16px 20px;
    border-radius: 18px 18px 18px 4px;
    margin: 8px 40px 8px 0;
    color: #0f172a;
}

/* Slide Preview Cards */
.slide-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 20px;
    transition: all 0.2s ease;
}

.slide-card:hover {
    border-color: #cbd5e1;
}

/* Progress Bar */
.progress-bar {
    width: 100%;
    height: 4px;
    background: #e2e8f0;
    border-radius: 2px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: #2563eb;
    border-radius: 2px;
    transition: width 0.5s ease;
}

/* File Drop Zone */
.drop-zone {
    border: 2px dashed #cbd5e1;
    border-radius: 16px;
    padding: 48px;
    text-align: center;
    transition: all 0.3s ease;
    cursor: pointer;
    background: #ffffff;
}

.drop-zone:hover, .drop-zone.active {
    border-color: #2563eb;
    background: #eff6ff;
}

/* Divider */
.divider {
    height: 1px;
    background: #e2e8f0;
    margin: 16px 0;
}

/* Text Utilities */
.text-primary { color: #2563eb !important; }
.text-muted { color: #64748b !important; }
.text-white { color: #111827 !important; }
.text-zinc-400 { color: #94a3b8 !important; }
.text-zinc-500 { color: #64748b !important; }

.bg-surface { background: #f8fafc !important; }
.bg-surface-container { background: #f1f5f9 !important; }
.bg-primary { background: #2563eb !important; }

.border-default { border-color: #e2e8f0 !important; }
.border-primary { border-color: #2563eb !important; }

.rounded-xl { border-radius: 12px; }
.rounded-2xl { border-radius: 16px; }
.rounded-full { border-radius: 9999px; }
</style>
"""

class Message:
    """Chat message"""
    def __init__(self, role: str, content: str, timestamp: str = None):
        self.role = role
        self.content = content
        self.timestamp = timestamp or datetime.now().isoformat()


class PitchPilotAgent:
    """Agent-style interface matching wireframes"""
    
    def __init__(self):
        self.deck_engine = DeckEngine()
        self.ai_engine = AIEngine()
        self.verification_engine = VerificationEngine()
        self.kb = KnowledgeBase()
        self._init_session_state()
    
    def _init_session_state(self):
        """Initialize session state"""
        if 'messages' not in st.session_state:
            st.session_state.messages = [
                Message('assistant', self._get_welcome_message())
            ]
        if 'deck_data' not in st.session_state:
            st.session_state.deck_data = None
        if 'current_view' not in st.session_state:
            st.session_state.current_view = 'dashboard'
    
    def _get_welcome_message(self) -> str:
        return """🎯 **Welcome to PitchPilot AI**

Your strategic co-pilot for building investor-ready pitch decks.

**What I can do:**
- 📋 **Build Deck** - Create new pitch decks from scratch
- 🔍 **Update Deck** - Improve existing decks
- 📊 **Strategy** - Validate market data and positioning

**How to use:**
Just tell me what you need or choose an action from the menu."""
    
    def render(self):
        """Render the complete UI"""
        # Apply styles
        st.markdown(STYLES, unsafe_allow_html=True)
        
        # Sidebar navigation
        with st.sidebar:
            self._render_sidebar()
        
        self._render_main_content()
    
    def _render_sidebar(self):
        """Render sidebar navigation."""
        st.markdown("### PitchPilot AI")
        st.markdown("---")
        st.markdown("**System Active** ✅")

        nav_items = [
            ('dashboard', 'Dashboard'),
            ('new_deck', 'New Deck'),
            ('audit', 'Audit'),
            ('strategy', 'Strategy'),
            ('knowledge', 'Knowledge Base'),
        ]

        for view_id, label in nav_items:
            if st.button(label, use_container_width=True, key=f"btn_{view_id}"):
                st.session_state.current_view = view_id
                st.rerun()

        st.markdown("---")

        if st.session_state.deck_data:
            st.markdown("### Current Deck")
            st.markdown(f"**Company:** {st.session_state.deck_data.get('company_name', 'N/A')}")
            if st.button("Download PPTX", use_container_width=True, key='btn_download'):
                self._download_deck()

        if st.button("Clear Chat", use_container_width=True, key='btn_clear'):
            st.session_state.messages = [Message('assistant', self._get_welcome_message())]
            st.session_state.deck_data = None
            st.rerun()
    
    def _render_main_content(self):
        """Render main content area based on current view"""
        view = st.session_state.current_view
        
        if view == 'dashboard':
            self._render_dashboard()
        elif view == 'new_deck':
            self._render_new_deck()
        elif view == 'audit':
            self._render_audit()
        elif view == 'strategy':
            self._render_strategy()
        elif view == 'knowledge':
            render_knowledge_base_manager()
    
    def _render_dashboard(self):
        """Render dashboard with action cards."""
        st.markdown("""
        <div style="max-width: 900px; margin: 0 auto; padding: 24px 0;">
            <div style="text-align: center; margin-bottom: 18px;">
                <div class="hero-label">AI Co-Pilot v2.4</div>
                <h1 class="hero-title">Easiest way to build a pitch deck that closes</h1>
                <p class="hero-copy">A clean MVP experience with guided deck creation and simple AI-assisted review.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2, gap='large')

        with col1:
            st.markdown("""
            <div class="page-card">
                <div class="card-title">Build Deck from Scratch</div>
                <p class="card-text">Create a new investor-ready pitch deck using your company details and key story points.</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Build Deck from Scratch", use_container_width=True, key='btn_build'):
                st.session_state.current_view = 'new_deck'
                st.rerun()

        with col2:
            st.markdown("""
            <div class="page-card">
                <div class="card-title">Update Current Deck</div>
                <p class="card-text">Upload an existing deck for AI feedback and improvement suggestions.</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Update Current Deck", use_container_width=True, key='btn_update'):
                st.session_state.current_view = 'audit'
                st.rerun()

        st.markdown("""
        <div style="max-width: 900px; margin: 32px auto 0; padding: 0 0 20px;">
            <div style="display: flex; flex-wrap: wrap; gap: 10px; align-items: center; justify-content: center; color: #475569; font-size: 0.95rem;">
                <span>Joined by 1,240+ founders this week</span>
                <span style="padding: 8px 14px; border-radius: 999px; background: #eff6ff; color: #1d4ed8;">Investor-ready MVP</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def _render_new_deck(self):
        """Render new deck creation wizard"""
        st.markdown("""
        <div style="max-width: 800px; margin: 0 auto; padding: 40px 20px;">
            <h2 style="font-size: 24px; font-weight: 600; color: #ffffff; margin-bottom: 8px;">Build Deck from Scratch</h2>
            <p style="color: #71717a; margin-bottom: 32px;">Create your investor-ready pitch deck in 4 steps.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Step indicator
        steps = [
            (1, 'File Intake', 'upload'),
            (2, 'AI Verification', 'psychology'),
            (3, 'Deck Blueprint', 'view_agenda'),
            (4, 'Export', 'download')
        ]
        
        cols = st.columns(4)
        for i, (step_num, step_name, icon) in enumerate(steps):
            with cols[i]:
                st.markdown(f"""
                <div style="text-align: center; padding: 12px; border-radius: 8px; background: {'rgba(37, 99, 235, 0.12)' if i == 0 else '#f8fafc'}; border: 1px solid {'#2563eb' if i == 0 else '#cbd5e1'};">
                    <span class="material-symbols-outlined" style="color: {'#2563eb' if i == 0 else '#64748b'}; font-size: 20px;">{icon}</span>
                    <p style="font-size: 11px; color: {'#2563eb' if i == 0 else '#64748b'}; margin-top: 4px; text-transform: uppercase; letter-spacing: 0.05em;">{step_name}</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # Company form
        with st.form("deck_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                company_name = st.text_input("Company Name *", placeholder="Acme AI")
            with col2:
                founder_name = st.text_input("Founder Name", placeholder="John Doe")
            
            raw_content = st.text_area("Pitch Notes / Description", height=150, 
                placeholder="Describe your startup, product, target market, competitive advantage...")
            
            col3, col4, col5 = st.columns(3)
            
            with col3:
                target_audience = st.selectbox("Target Audience", ["VC", "Angel", "Corporate", "Accelerator"])
            with col4:
                funding_amount = st.text_input("Funding Amount", placeholder="$2M")
            with col5:
                deck_purpose = st.selectbox("Purpose", ["Seed Round", "Series A", "Series B", "Bridge Round"])
            
            # File upload section
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            
            uploaded_files = st.file_uploader(
                "Upload supporting documents (optional)",
                type=['pdf', 'docx', 'txt'],
                accept_multiple_files=True
            )
            
            if uploaded_files:
                st.success(f"Uploaded {len(uploaded_files)} file(s)")
            
            # Submit button
            submitted = st.form_submit_button("🚀 Generate Pitch Deck", type='primary', use_container_width=True)
            
            if submitted and company_name:
                self._generate_deck(company_name, founder_name, raw_content, target_audience, funding_amount, deck_purpose)
    
    def _render_audit(self):
        """Render deck audit view"""
        st.markdown("""
        <div style="max-width: 800px; margin: 0 auto; padding: 40px 20px;">
            <h2 style="font-size: 24px; font-weight: 600; color: #ffffff; margin-bottom: 8px;">Update Current Deck</h2>
            <p style="color: #71717a; margin-bottom: 32px;">Upload your existing pitch deck for AI-powered analysis and improvement.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Drop zone
        st.markdown("""
        <div class="drop-zone">
            <span class="material-symbols-outlined" style="font-size: 48px; color: #3fe56c; margin-bottom: 16px;">upload_file</span>
            <p style="font-size: 18px; color: #ffffff; margin-bottom: 8px;">Drop files here</p>
            <p style="color: #71717a;">or click to browse • PDF, DOCX, PPTX</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.file_uploader(" ", type=['pdf', 'docx', 'pptx'], key='audit_file')
    
    def _render_strategy(self):
        """Render strategy consulting view"""
        st.markdown("""
        <div style="max-width: 800px; margin: 0 auto; padding: 40px 20px;">
            <h2 style="font-size: 24px; font-weight: 600; color: #ffffff; margin-bottom: 8px;">Strategy Consulting</h2>
            <p style="color: #71717a; margin-bottom: 32px;">Validate market size, value theory, and competitive positioning.</p>
        </div>
        """, unsafe_allow_html=True)
        
        consult_type = st.selectbox("Consulting Type", [
            "Market Size Validation",
            "Competitive Analysis",
            "Value Theory Validation",
            "Go-to-Market Strategy"
        ])
        
        company_info = st.text_area("Company Overview", height=150,
            placeholder="Describe your business model, target customers, and key value proposition...")
        
        questions = st.text_area("Specific Questions", height=100,
            placeholder="What do you want to validate or analyze?")
        
        if st.button("💡 Run Analysis", type='primary', use_container_width=True):
            st.info("Analysis feature coming soon...")
    
    def _generate_deck(self, company_name, founder_name, raw_content, target_audience, funding_amount, deck_purpose):
        """Generate a pitch deck"""
        with st.spinner("🤔 Creating your pitch deck..."):
            # Get knowledge base context
            kb_context = self.kb.get_context_for_prompt(company_name)
            full_content = kb_context + "\n\n" + raw_content if kb_context else raw_content
            
            # Generate with AI
            deck_json = self.ai_engine.generate_deck(
                founder_name=founder_name,
                company_name=company_name,
                raw_content=full_content,
                target_audience=target_audience,
                funding_amount=funding_amount,
                deck_purpose=deck_purpose
            )
            
            if deck_json:
                verified_deck = self.verification_engine.verify_deck_data(deck_json)
                st.session_state.deck_data = verified_deck
                
                # Show success and preview
                st.success("✅ Pitch Deck Generated!")
                
                # Display slides
                slide_titles = {
                    1: "The Hook", 2: "Empathy", 3: "Opportunity", 4: "Solution",
                    5: "Market", 6: "Business Model", 7: "Competition",
                    8: "Technology", 9: "Traction", 10: "The Ask"
                }
                
                for i in range(1, 11):
                    key = f"slide_{i}"
                    if key in verified_deck and verified_deck[key]:
                        with st.expander(f"Slide {i}: {slide_titles.get(i, 'Slide')}"):
                            st.markdown(verified_deck[key])
                
                # Generate PPTX
                pptx_path = self.deck_engine.generate_presentation(verified_deck)
                
                if pptx_path and os.path.exists(pptx_path):
                    with open(pptx_path, 'rb') as f:
                        st.download_button(
                            label="📥 Download PowerPoint",
                            data=f.read(),
                            file_name=f"{company_name}_pitch_deck.pptx",
                            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                        )


def main():
    """Entry point"""
    st.set_page_config(
        page_title="PitchPilot AI | Mission Control",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    agent = PitchPilotAgent()
    agent.render()


if __name__ == "__main__":
    main()