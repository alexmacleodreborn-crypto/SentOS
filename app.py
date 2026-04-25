
import streamlit as st
import time
import importlib.util
import os
import random
from datetime import datetime

# Hardware components
from streamlit_webrtc import webrtc_streamer
from streamlit_mic_recorder import mic_recorder

# --- DYNAMIC LAYER LOADING ---
def load_layer(name, folder, filename):
    path = os.path.join(folder, filename)
    if not os.path.exists(path):
        return None
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Load layers using the descriptive filenames
layers = {
    "L01": load_layer("L01", "chassis", "Layer 01: Physical Architecture.py"),
    "L02": load_layer("L02", "actuators", "Layer 02: Muscular Actuators.py"),
    "L03": load_layer("L03", "actuators", "Layer 03: Movement Engine.py"),
    "L05": load_layer("L05", "biology", "Layer 05: Visceral Systems.py"),
    "L06": load_layer("L06", "membrane", "Layer 06: Optic Registry.py"),
    "L09": load_layer("L09", "membrane", "Layer 09: Vocal Sync.py"),
    "L10": load_layer("L10", "neocortex", "Layer 10: Cognitive Archive.py"),
}

# --- ENGINE STATE ---
if 'a7do' not in st.session_state:
    st.session_state.a7do = {
        "chassis": layers["L01"].HumanChassis() if layers["L01"] else None,
        "muscles": layers["L02"].MuscularEngine() if layers["L02"] else None,
        "movement": layers["L03"].MovementEngine() if layers["L03"] else None,
        "biology": layers["L05"].MetabolicEngine() if layers["L05"] else None,
        "optics": layers["L06"].OpticRegistry() if layers["L06"] else None,
        "vocal": layers["L09"].VocalSync() if layers["L09"] else None,
        "mind": layers["L10"].CognitiveArchive() if layers["L10"] else None,
        "boot_time": datetime.now()
    }

# --- UI CONFIG ---
st.set_page_config(page_title="A7DO Sentience OS", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #0d1117; border-right: 1px solid #30363d; }
    .main { background-color: #010409; color: #c9d1d9; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 10px; }
    h1, h2, h3 { color: #58a6ff; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("A7DO OS v12.2")
    page = st.radio("Navigate Engine Components:", [
        "Executive Dashboard", 
        "Layer 01: Chassis (Bones/Teeth)", 
        "Layer 02: Actuators (Muscles)",
        "Layer 05: Visceral (Organs)", 
        "Layer 06: Optic Registry", 
        "Layer 09: Vocal Sync", 
        "Layer 10: Neocortex"
    ])
    
    st.divider()
    if st.session_state.a7do["biology"]:
        st.session_state.a7do["biology"].process_cycle(0.1)
        v = st.session_state.a7do["biology"].get_vitals()
        st.metric("ATP ENERGY", f"{v['atp']}%")
        st.metric("HEART RATE", f"{v['bpm']} BPM")

# --- PAGE ROUTING ---

if page == "Executive Dashboard":
    st.title("🛡️ Executive System Status")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("The Bubble Feed")
        webrtc_streamer(key="live-webrtc", video_frame_callback=None)
        st.info("A7DO is maintaining live environmental resonance.")
    with col2:
        st.subheader("Subconscious DMN")
        st.code("""
        RECONCILE_L01: Skeleton Loaded
        RECONCILE_L02: 640 Actuators Ready
        RECONCILE_L05: Metabolism Stable
        """)

elif page == "Layer 01: Chassis (Bones/Teeth)":
    st.title("🦴 Physical Architecture")
    tab1, tab2 = st.tabs(["Skeletal Registry", "Dental Registry"])
    with tab1:
        st.write("### 206 Bones Hierarchy")
        st.json(st.session_state.a7do["chassis"].bones)
    with tab2:
        st.write("### Adult Dental Array")
        st.json(st.session_state.a7do["chassis"].head_assets["mouth"])

elif page == "Layer 02: Actuators (Muscles)":
    st.title("💪 Muscular Actuators")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Recruitment Controls")
        group = st.selectbox("Recruit Muscle Group:", list(st.session_state.a7do["muscles"].muscle_groups.keys()))
        intensity = st.slider("Pull Intensity", 0.0, 1.0, 0.2)
        if st.button("FIRE ACTUATORS"):
            res = st.session_state.a7do["muscles"].recruit_group(group, intensity)
            st.success(res)
    with col2:
        st.subheader("Myology Telemetry")
        m_stat = st.session_state.a7do["muscles"].get_myology_status()
        st.write(f"Global Fatigue: `{m_stat['global_fatigue']*100:.2f}%`")
        st.json(m_stat["active_states"])

elif page == "Layer 05: Visceral (Organs)":
    st.title("🫀 Visceral Systems")
    st.json(st.session_state.a7do["biology"].organs)
    st.write("### Metabolic ATP Replenishment")
    if st.button("Consolidate Energy (Sleep Mode)"):
        st.session_state.a7do["biology"].atp_level = 100.0
        st.rerun()

elif page == "Layer 06: Optic Registry":
    st.title("👁️ Sensory Ingress")
    webrtc_streamer(key="optic-registry-stream", video_frame_callback=None)
    st.markdown("MESH_STABILITY: `0.998` | PUPIL_SYNC: `TRUE`")

elif page == "Layer 09: Vocal Sync":
    st.title("🗣️ Vocal Sync")
    st.write("Extracting Biological Frequency...")
    mic_recorder(start_prompt="🎤 Initiate Resonance", stop_prompt="⏹ Stop", key='vocal_mic')
    st.info("Awaiting high-fidelity FFT sequence...")

elif page == "Layer 10: Neocortex":
    st.title("🧠 Cognitive Archive")
    mind_map = st.session_state.a7do["mind"].get_mind_map()
    st.write(f"Total Cognitive Density: {mind_map['total_nodes']} nodes")
    st.json(mind_map["graph"])

# Auto-refresh loop
time.sleep(1)
st.rerun()

