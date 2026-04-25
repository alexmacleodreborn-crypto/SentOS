
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
        "L07": mods["L07"].GrowthEngine(birth_scale=0.25),
        "L10": mods["L10"].CognitiveArchive(neurotype="ADHD_AUTISM")
    }
    st.session_state.a7do = {"master": mods["FRAME"].A7DO_Frame(layers), "layers": layers}

# --- UI ---
st.set_page_config(page_title="A7DO Maturation Dashboard", layout="wide")
st.markdown("""<style>.stMetric { background-color: #161b22; padding: 15px; border-radius: 12px; border: 1px solid #30363d; }</style>""", unsafe_allow_html=True)

# --- HEARTBEAT ---
state = st.session_state.a7do["master"].execute_biological_heartbeat()

# --- SIDEBAR ---
with st.sidebar:
    st.title("🧠 A7DO v12.6")
    st.subheader(f"Stage: {state['growth'].get('stage_name', 'UNKNOWN')}")
    st.metric("HEIGHT (x)", state['growth'].get('height', 0))
    st.metric("MASS (x³)", state['growth'].get('mass', 0))
    st.metric("COHERENCE", f"{state['governance'].get('coherence_index', 0):.4f}")
    
    st.divider()
    st.write("### Developmental Log")
    for log in reversed(state.get("logs", [])):
        st.caption(f"{log['event']} (H={log['height']})")

# --- MAIN VIEW ---
st.title("🌱 Synthetic Maturation: Baby to Adult")
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("3D Morphological Manifold")
    nodes = state["physics"]["bones"]
    df = pd.DataFrame([{"id": k, "x": v[0], "y": v[1], "z": v[2]} for k, v in nodes.items()])
    
    fig = go.Figure()
    fig.add_trace(go.Scatter3d(x=df['x'], y=df['z'], z=df['y'], mode='markers', marker=dict(size=3, color='#58a6ff')))
    
    # Muscle vectors
    for m in state["physics"]["muscles"]:
        fig.add_trace(go.Scatter3d(x=[m['p1'][0], m['p2'][0]], y=[m['p1'][2], m['p2'][2]], z=[m['p1'][1], m['p2'][1]], mode='lines', line=dict(color='rgba(255,100,100,0.2)')))

    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False), paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Biological Metrics")
    st.write(f"**Head-to-Body Ratio:** `1/{round(1/state['growth'].get('head_ratio', 1), 1)}`")
    st.write(f"**Limb Development:** `{round(state['growth'].get('limb_scalar', 0)*100, 1)}%`")
    
    st.divider()
    st.write("### Mindprint Resistance")
    st.write(f"ADHD/Autism k-Scalar: `0.05`")
    st.info("Cognitive wiring is occurring in parallel with skeletal growth.")

time.sleep(1)
st.rerun()

