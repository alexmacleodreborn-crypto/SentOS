
import streamlit as st
import time
import importlib.util
import os
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from streamlit_webrtc import webrtc_streamer

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
    
    if any(m is None for m in mods.values() if m is not "FRAME"):
        st.error(f"Hardware Fault: Check layer paths.")
        st.stop()

    # Initialize individual layers
    layers = {
        "L00": mods["L00"].SandysLawGovernor(),
        "L01": mods["L01"].HumanChassis(),
        "L02": mods["L02"].MuscularEngine(),
        "L03": mods["L03"].MovementEngine(),
        "L05": mods["L05"].MetabolicEngine(),
        "L06": mods["L06"].OpticRegistry(),
        "L10": mods["L10"].CognitiveArchive(neurotype="ADHD_AUTISM")
    }

    # Initialize Master Frame if module loaded successfully
    if mods["FRAME"]:
        master_frame = mods["FRAME"].A7DO_Frame(layers)
    else:
        st.warning("Master Frame module not found. Running in decentralized mode.")
        master_frame = None

    st.session_state.a7do = {
        "layers": layers,
        "master": master_frame,
        "boot_time": datetime.now()
    }

# --- UI STYLING ---
st.set_page_config(page_title="A7DO Sentience OS", layout="wide", page_icon="🧠")
st.markdown("""
<style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 12px; }
    .status-panel { background: #010409; border-left: 4px solid #58a6ff; padding: 15px; margin: 10px 0; border-radius: 4px; }
    .node-active { color: #3fb950; font-family: monospace; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: MASTER TELEMETRY ---
with st.sidebar:
    st.title("🛡️ A7DO v12.6")
    st.caption("Neurodivergent Cognition (k=0.05)")
    page = st.radio("Access Manifold:", ["Dashboard", "Physical Architecture", "Myology & Motion", "Cognitive Mindprint"])
    st.divider()
    
    # Pulse the master heartbeat
    state = st.session_state.a7do["master"].execute_biological_heartbeat() if st.session_state.a7do["master"] else None
    
    if state:
        st.metric("COHERENCE (C)", f"{state['governance']['coherence_index']:.4f}")
        st.metric("ATP ENERGY", f"{state['vitals']['atp']}%")
        st.metric("HEART RATE", f"{state['vitals']['bpm']} BPM")
    else:
        st.error("Heartbeat Offline")

# --- DASHBOARD: UNIFIED REALITY ---
if page == "Dashboard":
    st.title("👁️ Perceptual Loop & 3D Proprioception")
    
    col_vis, col_phys = st.columns([1, 1])
    
    with col_vis:
        st.subheader("Optic Ingress")
        webrtc_streamer(key="feed")
        e_tele = st.session_state.a7do["layers"]["L06"].get_sensory_telemetry()
        if e_tele["discovery_active"]:
            st.warning(f"Targeting Unknown Mesh: {e_tele['target_mesh']}")
            with st.form("discovery"):
                label = st.text_input("Assign Identity:")
                if st.form_submit_button("Anchor & Reach"):
                    res = st.session_state.a7do["master"].reach_and_symbolize(label, ["OBJECT"])
                    st.success(res)
                    st.rerun()

    with col_phys:
        st.subheader("3D Skeletal Manifold (L03)")
        # Creating a Plotly Scatter Plot to mimic the image's node-based wireframe
        if state and "physics" in state:
            nodes = state["physics"]["skeletal_nodes"]
            df = pd.DataFrame([{"bone": k, "x": v[0], "y": v[1], "z": v[2]} for k, v in nodes.items()])
            
            fig = go.Figure(data=[go.Scatter3d(
                x=df['x'], y=df['z'], z=df['y'],
                mode='markers+text',
                marker=dict(size=4, color='#58a6ff', opacity=0.8),
                text=df['bone'],
                textfont=dict(size=8, color="#8b949e")
            )])
            fig.update_layout(
                margin=dict(l=0, r=0, b=0, t=0),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Awaiting kinematic data...")

# --- PHYSICAL ARCHITECTURE ---
elif page == "Physical Architecture":
    st.title("🦴 206-Bone Individual Registry")
    frame = st.session_state.a7do["layers"]["L01"]
    
    st.markdown('<div class="status-panel"><b>VITRUVIAN STATUS:</b> Manifold Locked</div>', unsafe_allow_html=True)
    
    # Granular breakdown for each bone category
    for category, sub_groups in frame.bone_registry.items():
        with st.expander(f"{category}"):
            if isinstance(sub_groups, dict):
                for sub, bones in sub_groups.items():
                    st.markdown(f"**{sub}:**")
                    st.write(", ".join(bones))
            else:
                st.write(", ".join(sub_groups))

# --- MYOLOGY & MOTION ---
elif page == "Myology & Motion":
    st.title("💪 Actuators & Proprioception")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Muscular Actuators")
        myo_tele = st.session_state.a7do["layers"]["L02"].get_myology_telemetry()
        st.metric("Total Actuators", myo_tele["total_actuators"])
        st.metric("Avg Fatigue", f"{myo_tele['avg_fatigue']:.4f}")
        
        group = st.selectbox("Select Target Group:", list(st.session_state.a7do["layers"]["L02"].groups.keys()))
        intensity = st.slider("Intensity", 0.0, 1.0, 0.1)
        if st.button("Recruit Fibers"):
            st.session_state.a7do["layers"]["L02"].recruit_fibers(group, intensity)
            st.rerun()

    with col2:
        st.subheader("Kinematic Telemetry")
        # Accessing L03 via the new high-res method name
        k_tele = st.session_state.a7do["layers"]["L03"].get_kinematic_telemetry()
        st.metric("Stability Index", f"{k_tele['stability_index']:.3f}")
        st.progress(k_tele['stability_index'])
        st.write(f"Mass Load: {k_tele['mass_load_nm']} Nm")
        st.write(f"State: `{k_tele['balance_state']}`")

# --- MINDPRINT ---
elif page == "Mindprint":
    st.title("🧠 Cognitive Neocortex")
    st.json(st.session_state.a7do["layers"]["L10"].archive)

# Global pulse refresh
time.sleep(1)
st.rerun()

