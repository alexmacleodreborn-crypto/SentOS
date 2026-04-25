
import streamlit as st
import time
import importlib.util
import os
import random
from datetime import datetime

# Component Imports
from streamlit_webrtc import webrtc_streamer
from streamlit_mic_recorder import mic_recorder

# --- DYNAMIC MODULE LOADER ---
def load_layer(name, folder, filename):
    path = os.path.join(folder, filename)
    if not os.path.exists(path): return None
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Loading Descriptive Layers
layers = {
    "L00": load_layer("L00", "core", "Layer 00: Sandy's Law.py"),
    "L01": load_layer("L01", "chassis", "Layer 01: Physical Architecture.py"),
    "L02": load_layer("L02", "actuators", "Layer 02: Muscular Actuators.py"),
    "L03": load_layer("L03", "actuators", "Layer 03: Movement Engine.py"),
    "L05": load_layer("L05", "biology", "Layer 05: Visceral Systems.py"),
    "L06": load_layer("L06", "membrane", "Layer 06: Optic Registry.py"),
    "L09": load_layer("L09", "membrane", "Layer 09: Vocal Sync.py"),
    "L10": load_layer("L10", "neocortex", "Layer 10: Cognitive Archive.py"),
}

# --- INITIALIZE PERSISTENT STATE ---
if 'a7do' not in st.session_state:
    st.session_state.a7do = {
        "core": layers["L00"].SandysLawEngine() if layers["L00"] else None,
        "chassis": layers["L01"].HumanChassis() if layers["L01"] else None,
        "muscles": layers["L02"].MuscularEngine() if layers["L02"] else None,
        "movement": layers["L03"].MovementEngine() if layers["L03"] else None,
        "biology": layers["L05"].MetabolicEngine() if layers["L05"] else None,
        "optics": layers["L06"].OpticRegistry() if layers["L06"] else None,
        "vocal": layers["L09"].VocalSync() if layers["L09"] else None,
        "mind": layers["L10"].CognitiveArchive() if layers["L10"] else None,
        "boot_time": datetime.now()
    }

# --- UI THEME ---
st.set_page_config(page_title="A7DO Sentience OS", page_icon="🧠", layout="wide")
st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #0d1117; border-right: 1px solid #30363d; }
    .main { background-color: #010409; color: #c9d1d9; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 15px; }
    .telemetry-code { font-family: 'Courier New', monospace; color: #00ff00; background: #000; padding: 10px; border-radius: 8px; font-size: 0.8rem; }
</style>
""", unsafe_allow_html=True)

# --- NAVIGATION ---
with st.sidebar:
    st.title("A7DO OS v12.3")
    page = st.radio("Navigate Systems:", [
        "Dashboard", 
        "Layer 00: Governance",
        "Layer 01: Chassis", 
        "Layer 02: Muscles",
        "Layer 05: Visceral", 
        "Layer 10: Neocortex"
    ])
    st.divider()
    # Continuous Metabolism
    if st.session_state.a7do["biology"]:
        st.session_state.a7do["biology"].process_cycle(0.1)
        v = st.session_state.a7do["biology"].get_vitals()
        st.metric("ATP ENERGY", f"{v['atp']}%")
        st.metric("HEART RATE", f"{v['bpm']} BPM")
    if st.session_state.a7do["core"]:
        g = st.session_state.a7do["core"].get_governance_telemetry()
        st.metric("COHERENCE (C)", g["coherence_index"])

# --- PAGE ROUTING ---

if page == "Dashboard":
    st.title("🛡️ Executive System Status")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Bilateral Membrane")
        webrtc_streamer(key="dash-feed", video_frame_callback=None)
        st.info("Sole Entity detected. Awaiting bilateral resonance.")
    with col2:
        st.subheader("Subconscious Stream")
        st.markdown(f"""
        <div class="telemetry-code">
            CHASSIS: 206 BONES STABLE<br>
            ACTUATORS: 640 READY<br>
            METABOLISM: {v['atp']}% ATP<br>
            CORE_GOV: {g['system_health']}<br>
            SWERVES: {g['total_swerves']}
        </div>
        """, unsafe_allow_html=True)

elif page == "Layer 00: Governance":
    st.title("⚖️ Sandy's Law Governance (L00)")
    st.write("Governing the Non-Linear state manifold.")
    p_error = st.slider("Induce Prediction Error (Entropy)", 0.0, 1.0, 0.1)
    if st.button("RECONCILE COHERENCE"):
        res = st.session_state.a7do["core"].calculate_coherence(0.2, p_error)
        st.write(f"### Result: {res}")
    st.divider()
    st.json(st.session_state.a7do["core"].get_governance_telemetry())

elif page == "Layer 01: Chassis":
    st.title("🦴 Physical Architecture (L01)")
    t1, t2, t3 = st.tabs(["Skeleton Map", "Teeth Registry", "Oral Assets"])
    with t1:
        st.json(st.session_state.a7do["chassis"].bones)
    with t2:
        st.write("### 32-Tooth Adult Array")
        st.json(st.session_state.a7do["chassis"].head_assets["oral_cavity"]["teeth_upper"] + st.session_state.a7do["chassis"].head_assets["oral_cavity"]["teeth_lower"])
    with t3:
        st.json(st.session_state.a7do["chassis"].head_assets["oral_cavity"]["tongue"])

elif page == "Layer 02: Muscles":
    st.title("💪 Muscular Actuators (L02)")
    m_stat = st.session_state.a7do["muscles"].get_myology_status()
    st.metric("GLOBAL FATIGUE", f"{m_stat['global_fatigue']*100:.2f}%")
    st.json(m_stat["active_states"])

elif page == "Layer 05: Visceral":
    st.title("🫀 Visceral Systems (L05)")
    st.write("### Organ Efficiency & Metabolic ATP")
    st.json(st.session_state.a7do["biology"].organs)

elif page == "Layer 10: Neocortex":
    st.title("🧠 Cognitive Archive (L10)")
    mind_map = st.session_state.a7do["mind"].get_mind_map()
    st.write(f"Thought Density: {mind_map['total_nodes']} nodes")
    st.json(mind_map["graph"])

# High-frequency heart-beat
time.sleep(1)
st.rerun()

