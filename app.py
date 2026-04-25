
import streamlit as st
import time
import importlib.util
import os
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# --- DYNAMIC LOADER ---
def load_layer(name, path):
    if not os.path.exists(path): return None
    try:
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        return f"Error: {e}"

LAYER_MAP = {
    "L00": "core/Layer 00: Sandy's Law.py",
    "L01": "chassis/Layer 01: Physical Architecture.py",
    "L02": "actuators/Layer 02: Muscular Actuators.py",
    "L03": "actuators/Layer 03: Movement Engine.py",
    "L05": "biology/Layer 05: Visceral Systems.py",
    "L06": "membrane/Layer 06: Optic Registry.py",
    "L07": "biology/Layer_07_Morphological_Sync.py",
    "L10": "neocortex/Layer 10: Cognitive Archive.py",
    "FRAME": "core/A7DO_Frame.py"
}

# --- INITIALIZATION ---
if 'a7do' not in st.session_state:
    mods = {k: load_layer(k, v) for k, v in LAYER_MAP.items()}
    
    # Store load status
    st.session_state.boot_log = mods

    layers = {}
    for k in ["L00", "L01", "L02", "L03", "L05", "L06", "L07", "L10"]:
        m = mods.get(k)
        if m and not isinstance(m, str):
            if k == "L00": layers[k] = m.SandysLawGovernor()
            elif k == "L01": layers[k] = m.HumanChassis()
            elif k == "L02": layers[k] = m.MuscularEngine()
            elif k == "L03": layers[k] = m.MovementEngine()
            elif k == "L05": layers[k] = m.MetabolicEngine()
            elif k == "L06": layers[k] = m.OpticRegistry()
            elif k == "L07": layers[k] = m.GrowthEngine(birth_scale=0.1)
            elif k == "L10": layers[k] = m.CognitiveArchive(neurotype="ADHD_AUTISM")

    # Initialize Master Frame
    frame_mod = mods.get("FRAME")
    master = None
    if frame_mod and not isinstance(frame_mod, str):
        try:
            master = frame_mod.A7DO_Frame(layers)
        except Exception as e:
            st.session_state.boot_log["FRAME_ERR"] = str(e)

    st.session_state.a7do = {
        "layers": layers,
        "master": master,
        "boot_time": datetime.now()
    }

# --- UI STYLING ---
st.set_page_config(page_title="A7DO Sentience OS", layout="wide")
st.markdown("""<style>.stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 12px; }</style>""", unsafe_allow_html=True)

# --- SIDEBAR & HEARTBEAT ---
with st.sidebar:
    st.title("🛡️ A7DO v12.6")
    page = st.radio("Navigation:", ["Growth Dashboard", "Diagnostics", "Mindprint"])
    
    if st.session_state.a7do["master"]:
        state = st.session_state.a7do["master"].execute_biological_heartbeat()
        st.metric("MATURITY", f"{state['growth']['maturity_percent']}%")
        st.metric("COHERENCE", f"{state['governance']['coherence_index']:.4f}")
        st.metric("ATP ENERGY", f"{state['vitals']['atp']}%")
    else:
        st.error("Master Frame Offline")
        state = None

# --- GROWTH DASHBOARD ---
if page == "Growth Dashboard":
    st.title("🌱 Morphological Growth Timeline")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("3D Synthetic Synthesis")
        if state:
            bones = state["physics"]["bones"]
            df = pd.DataFrame([{"id": k, "x": v[0], "y": v[2], "z": v[1]} for k, v in bones.items()])
            
            fig = go.Figure()
            # Bone Nodes
            fig.add_trace(go.Scatter3d(
                x=df['x'], y=df['y'], z=df['z'],
                mode='markers', marker=dict(size=3, color='#58a6ff'),
                text=df['id'], hoverinfo='text'
            ))
            # Muscle Vectors
            for m in state["physics"]["muscles"]:
                fig.add_trace(go.Scatter3d(
                    x=[m["p1"][0], m["p2"][0]],
                    y=[m["p1"][2], m["p2"][2]],
                    z=[m["p1"][1], m["p2"][1]],
                    mode='lines', line=dict(color='rgba(255,100,100,0.2)', width=2),
                    hoverinfo='none'
                ))
            
            fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False), paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Growth Telemetry")
        if state:
            st.write(f"**Current Scale (x):** `{state['growth']['scale_x']}`")
            st.write(f"**Strength (x²):** `{state['growth']['strength_x2']}`")
            st.write(f"**Mass Load (x³):** `{state['growth']['mass_x3']}`")
            st.progress(state['growth']['maturity_percent'] / 100)

elif page == "Diagnostics":
    st.title("🛠️ System Boot Log")
    for k, v in st.session_state.boot_log.items():
        st.write(f"**{k}:** {v if isinstance(v, str) else '✅ Loaded'}")

elif page == "Mindprint":
    st.title("🧠 Cognitive Neocortex (k=0.05)")
    st.json(st.session_state.a7do["layers"]["L10"].archive)

time.sleep(1)
st.rerun()

