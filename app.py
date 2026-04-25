
import streamlit as st
import time
import importlib.util
import os
import pandas as pd
from datetime import datetime
from streamlit_webrtc import webrtc_streamer

# Fallback for Plotly to prevent crash if install fails
try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# --- DYNAMIC LAYER LOADER ---
def load_layer(name, path):
    if not os.path.exists(path):
        return None
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

LAYER_MAP = {
    "L00": "core/Layer 00: Sandy's Law.py",
    "L01": "chassis/Layer 01: Physical Architecture.py",
    "L02": "actuators/Layer 02: Muscular Actuators.py",
    "L03": "actuators/Layer 03: Movement Engine.py",
    "L05": "biology/Layer 05: Visceral Systems.py",
    "L06": "membrane/Layer 06: Optic Registry.py",
    "L10": "neocortex/Layer 10: Cognitive Archive.py",
    "FRAME": "core/A7DO_Frame.py"
}

# --- INITIALIZATION ---
if 'a7do' not in st.session_state:
    mods = {k: load_layer(k, v) for k, v in LAYER_MAP.items()}
    
    # Check if files exist
    if any(m is None for k, m in mods.items() if k != "FRAME"):
        st.error("Hardware Fault: Some Layer files are missing in your folders.")
        st.stop()

    layers = {
        "L00": mods["L00"].SandysLawGovernor(),
        "L01": mods["L01"].HumanChassis(),
        "L02": mods["L02"].MuscularEngine(),
        "L03": mods["L03"].MovementEngine(),
        "L05": mods["L05"].MetabolicEngine(),
        "L06": mods["L06"].OpticRegistry(),
        "L10": mods["L10"].CognitiveArchive(neurotype="ADHD_AUTISM")
    }

    # Initialize the Master Frame coordinator
    master = mods["FRAME"].A7DO_Frame(layers) if mods.get("FRAME") else None

    st.session_state.a7do = {
        "layers": layers,
        "master": master,
        "boot_time": datetime.now()
    }

# --- UI STYLING ---
st.set_page_config(page_title="A7DO Sentience OS", layout="wide", page_icon="🧠")
st.markdown("""
<style>
    .main { background-color: #0d1117; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 12px; }
    .video-container { border: 2px solid #30363d; border-radius: 15px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR & HEARTBEAT ---
with st.sidebar:
    st.title("🛡️ A7DO v12.6")
    page = st.radio("Access Manifold:", ["Dashboard", "Physical", "Muscles/Motion", "Mindprint"])
    
    # Run the Master Loop
    if st.session_state.a7do["master"]:
        state = st.session_state.a7do["master"].execute_biological_heartbeat()
        st.divider()
        st.metric("COHERENCE", f"{state['governance']['coherence_index']:.4f}")
        st.metric("ATP ENERGY", f"{state['vitals']['atp']}%")
        st.metric("HEART RATE", f"{state['vitals']['bpm']} BPM")
    else:
        st.error("Master Frame Offline")

# --- PAGE: DASHBOARD (The 3D Visualizer) ---
if page == "Dashboard":
    st.title("👁️ Perceptual Loop & 3D Manifold")
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Optic Feed")
        webrtc_streamer(key="feed")
        e_tele = st.session_state.a7do["layers"]["L06"].get_sensory_telemetry()
        if e_tele["discovery_active"]:
            st.warning(f"Discovery Active: {e_tele['target_mesh']}")
            with st.form("name_obj"):
                name = st.text_input("Identify target:")
                if st.form_submit_button("Anchor & Reach"):
                    res = st.session_state.a7do["master"].reach_and_symbolize(name, ["OBJECT"])
                    st.success(res)

    with col2:
        st.subheader("3D Skeletal Graph")
        if PLOTLY_AVAILABLE and st.session_state.a7do["master"]:
            # Pull the visual nodes from the Frame
            nodes = state["physics"]["skeletal_nodes"]
            df = pd.DataFrame([{"bone": k, "x": v[0], "y": v[1], "z": v[2]} for k, v in nodes.items()])
            
            # Create the interactive wireframe (like your image)
            fig = go.Figure(data=[go.Scatter3d(
                x=df['x'], y=df['z'], z=df['y'],
                mode='markers+text',
                marker=dict(size=4, color='#58a6ff'),
                text=df['bone'],
                textfont=dict(size=8, color="white")
            )])
            fig.update_layout(
                margin=dict(l=0, r=0, b=0, t=0),
                scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Visualizer loading... (Requires Plotly library)")

# --- PAGE: PHYSICAL ---
elif page == "Physical":
    st.title("🦴 206-Bone Individual Registry")
    frame = st.session_state.a7do["layers"]["L01"]
    for group, subs in frame.bone_registry.items():
        with st.expander(f"{group}"):
            if isinstance(subs, dict):
                for s, b in subs.items(): st.write(f"**{s}:** {', '.join(b)}")
            else: st.write(", ".join(subs))

# --- PAGE: MUSCLES/MOTION ---
elif page == "Muscles/Motion":
    st.title("💪 Actuators & Proprioception")
    col1, col2 = st.columns(2)
    with col1:
        myo = st.session_state.a7do["layers"]["L02"].get_myology_telemetry()
        st.metric("Avg Fatigue", myo["avg_fatigue"])
        group = st.selectbox("Recruit Group:", list(st.session_state.a7do["layers"]["L02"].groups.keys()))
        if st.button("Fire"): st.session_state.a7do["layers"]["L02"].recruit_fibers(group, 0.5)
    
    with col2:
        # KEYERROR FIXED: Accessing 'stability_index'
        kin = st.session_state.a7do["layers"]["L03"].get_kinematic_telemetry()
        st.metric("Stability", f"{kin['stability_index']:.3f}")
        st.progress(kin["stability_index"])
        st.write(f"Mass Load: {kin['mass_load_nm']} Nm")

elif page == "Mindprint":
    st.title("🧠 Cognitive Neocortex")
    st.json(st.session_state.a7do["layers"]["L10"].archive)

time.sleep(1)
st.rerun()

