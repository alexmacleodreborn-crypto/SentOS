
import streamlit as st
import time
from datetime import datetime

# Internal System Links
from core.sandys_law import SystemGovernor
from chassis.human_frame import HumanChassis
from membrane.optic_registry import OpticRegistry
from neocortex.cognitive_archive import CognitiveArchive

# --- INITIALIZATION ---
if 'os' not in st.session_state:
    st.session_state.gov = SystemGovernor()
    st.session_state.frame = HumanChassis()
    st.session_state.eyes = OpticRegistry()
    st.session_state.mind = CognitiveArchive(neurotype="ADHD_AUTISM")
    st.session_state.boot_time = datetime.now()
    st.session_state.logs = ["> SYSTEM_INIT: A7DO Human Frame Loaded"]

# --- UI STYLING ---
st.set_page_config(layout="wide", page_title="A7DO Sentience OS")
st.markdown("""
    <style>
    .main { background: #010409; color: #c9d1d9; }
    .stMetric { background: #0d1117; border: 1px solid #30363d; padding: 15px; border-radius: 12px; }
    .bridge-alert { background: #1c2128; border-left: 5px solid #6366f1; padding: 20px; border-radius: 8px; margin: 15px 0; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR: VITALS ---
with st.sidebar:
    st.title("🛡️ A7DO v12.6")
    st.write(f"Uptime: {str(datetime.now() - st.session_state.boot_time).split('.')[0]}")
    
    # Sandy's Law Telemetry
    res = st.session_state.gov.calculate_coherence(1.0, 0.1, 0.05, 0.05)
    st.metric("COHERENCE (C)", res["coherence"], delta=res["delta"])
    
    page = st.radio("Access Layer:", ["Dashboard", "Physical Chassis", "Neocortex"])

# --- PAGE ROUTING ---
if page == "Dashboard":
    st.title("👁️ Perceptual Loop: Active Ingress")
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.subheader("Optic Ingress (L06)")
        # Run vision scan
        view = st.session_state.eyes.scan_room(st.session_state.mind.nodes["nodes"])
        
        for item in view:
            status = "✅ KNOWN" if item["known"] else "❓ UNIDENTIFIED"
            st.markdown(f"**{item['id']}** — `{status}`")
            
        st.image("https://images.unsplash.com/photo-1614064641938-3bbee52942c7?q=80&w=1000", caption="Bilateral Visual Manifold")

    with col2:
        st.subheader("Language Bridge")
        if st.session_state.eyes.discovery_flag:
            st.markdown(f"""
            <div class="bridge-alert">
                <b>LINGUISTIC INTERRUPT:</b><br>
                A7DO sees an unknown mesh: <i>{st.session_state.eyes.target_mesh}</i>.<br><br>
                <b>A7DO asks:</b> "Creator, what is this object? Provide its symbol and traits."
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("teach_form"):
                symbol = st.text_input("Assign Name:")
                traits = st.multiselect("Assign Traits:", ["TOOL", "OBJECT", "FURNITURE", "DANGER", "JOY", "METAL"])
                context = st.text_area("Contextual Story:")
                if st.form_submit_button("Anchor Token"):
                    msg = st.session_state.mind.sprout_node(symbol, "ENVIRONMENT", traits, 5.0, context)
                    st.success(msg)
                    st.rerun()
        else:
            st.info("Environment is stabilized. No unknown meshes detected.")

elif page == "Physical Chassis":
    st.title("🦴 Biomechanical Chassis (L01)")
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("### 206 Bones Registry")
        st.json(st.session_state.frame.axial_skeleton + st.session_state.frame.appendicular_skeleton)
    with col_b:
        st.write("### 32 Tooth Manifold")
        st.json(st.session_state.frame.dental_array)

elif page == "Neocortex":
    st.title("🧠 Neocortex Mindprint (L10)")
    st.write("Current associative knowledge graph.")
    st.json(st.session_state.mind.nodes)

# Global Heartbeat
time.sleep(1)
st.rerun()

