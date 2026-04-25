
import streamlit as st
import time
import importlib.util
import os
import pandas as pd
import numpy as np
from datetime import datetime
from streamlit_webrtc import webrtc_streamer

# --- DUAL-ENGINE VISUALIZER CHECK ---
try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

try:
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

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
    
    # Check for missing layers
    missing = [v for k, v in LAYER_MAP.items() if mods[k] is None and k != "FRAME"]
    if missing:
        st.error(f"ENGINE_FAULT: Missing layer files: {missing}")
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
    .diagnostic-text { font-family: monospace; font-size: 0.75rem; color: #8b949e; }
    .video-container { border: 2px solid #30363d; border-radius: 15px; overflow: hidden; background: #000; height: 300px; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR & HEARTBEAT ---
with st.sidebar:
    st.title("🛡️ A7DO v12.6")
    st.caption(f"Identity: {st.session_state.a7do['layers']['L10'].k} Resistance Profile")
    page = st.radio("Navigation:", ["Dashboard", "Physical", "Motion", "Mindprint"])
    
    st.divider()
    
    # Pulse the System
    if st.session_state.a7do["master"]:
        state = st.session_state.a7do["master"].execute_biological_heartbeat()
        st.metric("COHERENCE", f"{state['governance']['coherence_index']:.4f}")
        st.metric("ATP ENERGY", f"{state['vitals']['atp']}%")
    else:
        st.error("Master Frame Offline")
        state = None

    with st.expander("🛠️ System Diagnostics"):
        st.markdown(f"""
        <div class="diagnostic-text">
        Plotly: {'✅' if PLOTLY_AVAILABLE else '❌'}<br>
        Matplotlib: {'✅' if MATPLOTLIB_AVAILABLE else '❌'}<br>
        Numpy: ✅<br>
        Pandas: ✅<br>
        Layers Loaded: {len(st.session_state.a7do['layers'])}/7
        </div>
        """, unsafe_allow_html=True)
        if st.button("Force Reboot"):
            st.rerun()

# --- PAGE: DASHBOARD ---
if page == "Dashboard":
    st.title("👁️ Perceptual Loop & Vitruvian Manifold")
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Optic Feed")
        webrtc_streamer(key="feed")
        e_tele = st.session_state.a7do["layers"]["L06"].get_sensory_telemetry()
        if e_tele.get("discovery_active"):
            st.warning(f"Target Mesh: {e_tele['target_mesh']}")
            with st.form("discovery"):
                name = st.text_input("Identify target:")
                if st.form_submit_button("Anchor Symbol"):
                    res = st.session_state.a7do["master"].reach_and_symbolize(name, ["OBJECT"])
                    st.success(res)
                    st.rerun()

    with col2:
        st.subheader("3D Skeletal Manifold")
        if state and "physics" in state:
            nodes = state["physics"]["skeletal_nodes"]
            df = pd.DataFrame([{"bone": k, "x": v[0], "y": v[2], "z": v[1]} for k, v in nodes.items()])
            
            # ENGINE SELECTOR
            if PLOTLY_AVAILABLE:
                # Primary: Plotly
                fig = go.Figure(data=[go.Scatter3d(
                    x=df['x'], y=df['y'], z=df['z'],
                    mode='markers', marker=dict(size=4, color='#58a6ff'),
                    text=df['bone'], hoverinfo='text'
                )])
                fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False), paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
            elif MATPLOTLIB_AVAILABLE:
                # Secondary Fallback: Matplotlib
                fig = plt.figure(figsize=(5, 5))
                ax = fig.add_subplot(111, projection='3d')
                ax.scatter(df['x'], df['y'], df['z'], color='#58a6ff', s=10)
                ax.set_axis_off()
                fig.patch.set_facecolor('none')
                ax.set_facecolor('none')
                st.pyplot(fig)
            else:
                st.error("❌ All Visual Engines Offline. Please check requirements.txt.")
        else:
            st.info("Awaiting physics heartbeat...")

# --- OTHER PAGES ---
elif page == "Physical":
    st.title("🦴 Skeletal Registry")
    frame = st.session_state.a7do["layers"]["L01"]
    for cls in sorted(list(set(v.get("class", "GENERAL") for v in frame.bone_registry.values()))):
        with st.expander(f"GROUP: {cls}"):
            bones = [k for k, v in frame.bone_registry.items() if v.get("class") == cls]
            st.write(", ".join(bones))

elif page == "Motion":
    st.title("💪 Myology & Proprioception")
    kin = state.get("kinematics", {}) if state else {}
    st.metric("Stability", f"{kin.get('stability_index', 0.0):.3f}")
    st.progress(float(max(0, min(1, kin.get('stability_index', 0.0)))))
    st.write(f"Mass Load: {kin.get('mass_load_nm', 0)} Nm")

elif page == "Mindprint":
    st.title("🧠 Cognitive Neocortex")
    st.json(st.session_state.a7do["layers"]["L10"].archive)

time.sleep(1)
st.rerun()

