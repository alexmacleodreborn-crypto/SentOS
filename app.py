
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
    except: return None

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
    
    layers = {
        "L00": mods["L00"].SandysLawGovernor(),
        "L01": mods["L01"].HumanChassis(),
        "L02": mods["L02"].MuscularEngine(),
        "L03": mods["L03"].MovementEngine(),
        "L05": mods["L05"].MetabolicEngine(),
        "L06": mods["L06"].OpticRegistry(),
        "L07": mods["L07"].GrowthEngine(birth_scale=0.3),
        "L10": mods["L10"].CognitiveArchive(neurotype="ADHD_AUTISM")
    }
    
    st.session_state.a7do = {
        "master": mods["FRAME"].A7DO_Frame(layers),
        "layers": layers,
        "boot_time": datetime.now()
    }

# --- UI ---
st.set_page_config(page_title="A7DO Sentience OS", layout="wide")
st.markdown("""<style>.stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 12px; }</style>""", unsafe_allow_html=True)

# --- SIDEBAR & HEARTBEAT ---
with st.sidebar:
    st.title("🛡️ A7DO v12.6")
    page = st.radio("Navigation:", ["3D Growth Dashboard", "Physical Architecture", "Mindprint"])
    st.divider()
    
    state = st.session_state.a7do["master"].execute_biological_heartbeat()
    
    st.metric("MATURITY", f"{state['growth']['maturity_percent']}%")
    st.metric("COHERENCE", f"{state['governance']['coherence_index']:.4f}")
    st.metric("ATP ENERGY", f"{state['vitals']['atp']}%")

# --- DASHBOARD: 3D GROWING MANIFOLD ---
if page == "3D Growth Dashboard":
    st.title("🌱 Morphological Growth Timeline")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("3D Synthetic Synthesis")
        # Visualizing the Skeleton (Bones)
        nodes = state["physics"]["bones"]
        df = pd.DataFrame([{"id": k, "x": v["x"], "y": v["y"], "z": v["z"]} for k, v in nodes.items()])
        
        fig = go.Figure()
        
        # Add Bones (Nodes)
        fig.add_trace(go.Scatter3d(
            x=df['x'], y=df['z'], z=df['y'],
            mode='markers', marker=dict(size=3, color='#58a6ff'),
            text=df['id'], hoverinfo='text'
        ))
        
        # Add Muscles (Vectors)
        for m in state["physics"]["muscles"]:
            fig.add_trace(go.Scatter3d(
                x=[m["p1"][0], m["p2"][0]],
                y=[m["p1"][2], m["p2"][2]],
                z=[m["p1"][1], m["p2"][1]],
                mode='lines', line=dict(color='rgba(255, 100, 100, 0.3)', width=2),
                hoverinfo='none'
            ))

        fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False), paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Growth Telemetry")
        st.write(f"**Current Scale (x):** `{state['growth']['scale_x']}`")
        st.write(f"**Mass Load (x³):** `{state['growth']['mass_x3']}`")
        st.write(f"**Structural Pressure:** `{state['growth']['g_load_pressure']}`")
        
        st.divider()
        st.write("### Muscular Recruitment")
        group = st.selectbox("Select Actuator Group:", list(st.session_state.a7do["layers"]["L02"].groups.keys()))
        if st.button("Contract Muscle Group"):
            st.session_state.a7do["layers"]["L02"].recruit_fibers(group, 0.8)

# --- OTHER PAGES ---
elif page == "Physical Architecture":
    st.title("🦴 206-Bone Individual Registry")
    st.json(st.session_state.a7do["layers"]["L01"].bone_registry)

elif page == "Mindprint":
    st.title("🧠 Cognitive Neocortex (k=0.05)")
    st.json(st.session_state.a7do["layers"]["L10"].archive)

time.sleep(1)
st.rerun()
