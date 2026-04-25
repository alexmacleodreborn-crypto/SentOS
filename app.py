
import streamlit as st
import time
import importlib.util
import os
import pandas as pd
from datetime import datetime
from streamlit_webrtc import webrtc_streamer

# --- PLOTLY SAFETY CHECK ---
try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# --- DYNAMIC LOADER ---
def load_layer(name, path):
    if not os.path.exists(path): return None
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
    
    if any(m is None for k, m in mods.items() if k != "FRAME"):
        st.error("Hardware Fault: Some Layer files are missing. Check folders.")
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

    # Initialize Master Frame
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
    .main { background-color: #0d1117; color: #c9d1d9; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 12px; }
    .video-container { border: 2px solid #30363d; border-radius: 15px; overflow: hidden; height: 350px; background: #000; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR & HEARTBEAT ---
with st.sidebar:
    st.title("🛡️ A7DO v12.6")
    page = st.radio("Access Manifold:", ["Dashboard", "Physical Architecture", "Myology & Motion", "Cognitive Mindprint"])
    
    # Pulse the system
    if st.session_state.a7do["master"]:
        state = st.session_state.a7do["master"].execute_biological_heartbeat()
        st.divider()
        st.metric("COHERENCE", f"{state['governance']['coherence_index']:.4f}")
        st.metric("ATP ENERGY", f"{state['vitals']['atp']}%")
    else:
        st.error("Master Frame Offline")
        state = None

# --- PAGE: DASHBOARD ---
if page == "Dashboard":
    st.title("👁️ Perceptual Loop & Vitruvian 2.0")
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Optic Feed")
        webrtc_streamer(key="feed")
        e_tele = st.session_state.a7do["layers"]["L06"].get_sensory_telemetry()
        if e_tele["discovery_active"]:
            st.warning(f"Target Mesh: {e_tele['target_mesh']}")
            with st.form("discovery"):
                name = st.text_input("Identify target:")
                if st.form_submit_button("Anchor Symbol"):
                    res = st.session_state.a7do["master"].reach_and_symbolize(name, ["OBJECT"])
                    st.success(res)

    with col2:
        st.subheader("3D Skeletal Manifold")
        if PLOTLY_AVAILABLE and state:
            nodes = state["physics"]["skeletal_nodes"]
            df = pd.DataFrame([{"bone": k, "x": v[0], "y": v[2], "z": v[1]} for k, v in nodes.items()])
            
            fig = go.Figure(data=[go.Scatter3d(
                x=df['x'], y=df['y'], z=df['z'],
                mode='markers', marker=dict(size=3, color='#58a6ff'),
                text=df['bone'], hoverinfo='text'
            )])
            fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False), paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Visualizer requires 'plotly' library. Add it to requirements.txt.")

# --- PAGE: PHYSICAL ARCHITECTURE ---
elif page == "Physical Architecture":
    st.title("🦴 Skeletal & Dental Registry")
    frame = st.session_state.a7do["layers"]["L01"]
    
    registry = frame.bone_registry
    if any(isinstance(v, dict) for v in registry.values()):
        # Handle High-Res object-based registry
        classes = sorted(list(set(v.get("class", "GENERAL") for v in registry.values())))
        for cls in classes:
            with st.expander(f"GROUP: {cls}"):
                bones = [k for k, v in registry.items() if v.get("class") == cls]
                st.write(", ".join(bones))
    else:
        # Handle string-based registry
        st.json(registry)

# --- PAGE: MYOLOGY & MOTION ---
elif page == "Myology & Motion":
    st.title("💪 Myology & Proprioception")
    col1, col2 = st.columns(2)
    
    with col1:
        myo = st.session_state.a7do["layers"]["L02"].get_myology_telemetry()
        st.metric("Avg Fatigue", f"{myo['avg_fatigue']:.4f}")
        group = st.selectbox("Recruit Group:", list(st.session_state.a7do["layers"]["L02"].groups.keys()))
        if st.button("Fire Actuators"):
            st.session_state.a7do["layers"]["L02"].recruit_fibers(group, 0.5)
    
    with col2:
        # DEFENSIVE ACCESS TO PREVENT KEYERROR
        kin = state.get("kinematics", {}) if state else {}
        st.write(f"Balance Status: `{kin.get('balance_state', 'N/A')}`")
        
        # Stability check
        stab = kin.get("stability_index", 0.0)
        st.metric("Stability", f"{stab:.3f}")
        st.progress(float(stab))
        st.write(f"Load: {kin.get('mass_load_nm', 0)} Nm")

# Global heartbeat
time.sleep(1)
st.rerun()

