
import streamlit as st
import time
import importlib.util
import os
import pandas as pd
from datetime import datetime
from streamlit_webrtc import webrtc_streamer

# --- PLOTLY INSTALLATION CHECK ---
# We use a global flag to check if the 3D engine is online
try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# --- DYNAMIC LAYER LOADER ---
def load_layer(name, path):
    if not os.path.exists(path):
        return None
    try:
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        st.sidebar.error(f"Error loading {name}: {e}")
        return None

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
    
    # Critical Layer Check
    if any(m is None for k, m in mods.items() if k != "FRAME"):
        st.error("SYSTEM_FAULT: Missing core layer files. Ensure folder structure matches LAYER_MAP.")
        st.stop()

    # Initializing the 10-Layer Biomechanical Manifold
    layers = {
        "L00": mods["L00"].SandysLawGovernor(),
        "L01": mods["L01"].HumanChassis(),
        "L02": mods["L02"].MuscularEngine(),
        "L03": mods["L03"].MovementEngine(),
        "L05": mods["L05"].MetabolicEngine(),
        "L06": mods["L06"].OpticRegistry(),
        "L10": mods["L10"].CognitiveArchive(neurotype="ADHD_AUTISM")
    }

    # Initialize Vitruvian Frame Coordinator
    master = mods["FRAME"].A7DO_Frame(layers) if mods.get("FRAME") else None

    st.session_state.a7do = {
        "layers": layers,
        "master": master,
        "boot_time": datetime.now()
    }

# --- UI ARCHITECTURE ---
st.set_page_config(page_title="A7DO Sentience OS", layout="wide", page_icon="🧠")

# Dark Theme Injection
st.markdown("""
<style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 12px; }
    .video-container { border: 2px solid #30363d; border-radius: 15px; overflow: hidden; height: 350px; background: #000; }
    .sidebar-status { font-family: monospace; font-size: 0.8rem; color: #8b949e; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR & GLOBAL HEARTBEAT ---
with st.sidebar:
    st.title("🛡️ A7DO v12.6")
    st.caption("Neurodivergent Manifold (k=0.05)")
    page = st.radio("Navigate Component Groups:", ["Dashboard", "Physical Architecture", "Myology & Motion", "Mindprint"])
    
    st.divider()
    
    # Pulse the System
    if st.session_state.a7do["master"]:
        state = st.session_state.a7do["master"].execute_biological_heartbeat()
        st.metric("COHERENCE (C)", f"{state['governance']['coherence_index']:.4f}")
        st.metric("ATP ENERGY", f"{state['vitals']['atp']}%")
        st.metric("HEART RATE", f"{state['vitals']['bpm']} BPM")
    else:
        st.error("Master Frame Offline")
        state = None

# --- PAGE: DASHBOARD (VITRUVIAN 2.0 VISUALIZER) ---
if page == "Dashboard":
    st.title("👁️ Perceptual Loop & 3D Manifold")
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Optic Feed")
        webrtc_streamer(key="feed-ingress")
        e_tele = st.session_state.a7do["layers"]["L06"].get_sensory_telemetry()
        
        if e_tele.get("discovery_active"):
            st.warning(f"UNIDENTIFIED_MESH: {e_tele['target_mesh']}")
            with st.form("discovery_bridge"):
                name = st.text_input("Name this object:")
                if st.form_submit_button("Anchor Symbol"):
                    res = st.session_state.a7do["master"].reach_and_symbolize(name, ["OBJECT"])
                    st.success(res)
                    st.rerun()

    with col2:
        st.subheader("3D Skeletal Manifold")
        if PLOTLY_AVAILABLE and state:
            # Map the nodes from the Master Frame Buffer
            nodes = state["physics"]["skeletal_nodes"]
            df = pd.DataFrame([{"bone": k, "x": v[0], "y": v[2], "z": v[1]} for k, v in nodes.items()])
            
            # Create the Vitruvian Node Graph
            fig = go.Figure(data=[go.Scatter3d(
                x=df['x'], y=df['y'], z=df['z'],
                mode='markers',
                marker=dict(size=4, color='#58a6ff', opacity=0.7),
                text=df['bone'],
                hoverinfo='text'
            )])
            
            fig.update_layout(
                margin=dict(l=0, r=0, b=0, t=0),
                scene=dict(
                    xaxis_visible=False, yaxis_visible=False, zaxis_visible=False,
                    aspectmode='cube'
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("❌ Visualizer Engine Offline")
            st.info("If you added Plotly to requirements.txt, please go to 'Manage App' -> 'Reboot App' to force a library install.")

# --- PAGE: PHYSICAL ARCHITECTURE ---
elif page == "Physical Architecture":
    st.title("🦴 Skeletal & Dental Registry")
    frame = st.session_state.a7do["layers"]["L01"]
    
    # Defensive display of the 206-bone registry
    registry = frame.bone_registry
    if isinstance(next(iter(registry.values())), dict):
        # Object-based high-res registry
        classes = sorted(list(set(v.get("class", "GENERAL") for v in registry.values())))
        for cls in classes:
            with st.expander(f"SKELETAL GROUP: {cls}"):
                bones = [k for k, v in registry.items() if v.get("class") == cls]
                st.write(", ".join(bones))
    else:
        # String-based registry
        st.json(registry)

# --- PAGE: MYOLOGY & MOTION ---
elif page == "Myology & Motion":
    st.title("💪 Actuators & Proprioception")
    col1, col2 = st.columns(2)
    
    with col1:
        myo = st.session_state.a7do["layers"]["L02"].get_myology_telemetry()
        st.metric("Avg Fatigue", f"{myo['avg_fatigue']:.4f}")
        group = st.selectbox("Recruit Actuator Group:", list(st.session_state.a7do["layers"]["L02"].groups.keys()))
        if st.button("Contract Fibers"):
            st.session_state.a7do["layers"]["L02"].recruit_fibers(group, 0.5)
            st.success(f"{group} recruitment signal sent.")
    
    with col2:
        # KEYERROR FIX: Using .get() for safety
        kin = state.get("kinematics", {}) if state else {}
        stab = kin.get("stability_index", 0.0)
        st.metric("Balance Stability", f"{stab:.3f}")
        st.progress(float(max(0, min(1, stab))))
        st.write(f"Mass Torque: {kin.get('mass_load_nm', 0)} Nm")

elif page == "Mindprint":
    st.title("🧠 Cognitive Neocortex")
    st.caption("Active k-scalar: 0.05 (Neurodivergent Profiling)")
    st.json(st.session_state.a7do["layers"]["L10"].archive)

# Global pulse refresh (1Hz heartbeat)
time.sleep(1)
st.rerun()

