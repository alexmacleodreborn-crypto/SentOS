
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
    "L07": "biology/Layer_07_Morphological_Sync.py",
    "L10": "neocortex/Layer 10: Cognitive Archive.py",
    "FRAME": "core/A7DO_Frame.py"
}

# --- INITIALIZATION ---
if 'a7do' not in st.session_state:
    mods = {k: load_layer(k, v) for k, v in LAYER_MAP.items()}
    
    # Defensive layer collection
    layers = {}
    for k in ["L00", "L01", "L02", "L03", "L05", "L07", "L10"]:
        m = mods.get(k)
        if m and not isinstance(m, str):
            if k == "L00": layers[k] = m.SandysLawGovernor()
            elif k == "L01": layers[k] = m.HumanChassis()
            elif k == "L02": layers[k] = m.MuscularEngine()
            elif k == "L03": layers[k] = m.MovementEngine()
            elif k == "L05": layers[k] = m.MetabolicEngine()
            elif k == "L07": layers[k] = m.GrowthEngine(birth_scale=0.2)
            elif k == "L10": layers[k] = m.CognitiveArchive(neurotype="ADHD_AUTISM")

    # Master Frame Coordinator
    master_mod = mods.get("FRAME")
    master = None
    if master_mod and not isinstance(master_mod, str):
        master = master_mod.A7DO_Frame(layers)

    st.session_state.a7do = {"master": master, "layers": layers, "boot_time": datetime.now()}

# --- UI STYLING ---
st.set_page_config(page_title="A7DO Maturation Dashboard", layout="wide")
st.markdown("""<style>.stMetric { background-color: #161b22; padding: 15px; border-radius: 12px; border: 1px solid #30363d; }</style>""", unsafe_allow_html=True)

# --- HEARTBEAT ---
state = st.session_state.a7do["master"].execute_biological_heartbeat() if st.session_state.a7do["master"] else None

# --- SIDEBAR ---
with st.sidebar:
    st.title("🛡️ A7DO v12.6")
    if state:
        st.subheader(f"Stage: {state['growth']['stage']}")
        st.metric("HEIGHT (x)", f"{state['growth']['height_scalar']:.4f}")
        st.metric("MASS (x³)", f"{state['growth']['mass_volume']:.4f}")
        st.metric("COHERENCE", f"{state['governance']['coherence_index']:.4f}")
        
        st.divider()
        st.write("### Developmental Log")
        for log in reversed(state.get("logs", [])):
            st.caption(f"{log['milestone']} (H={log['height_cm']}cm)")
    else:
        st.error("System Boot Failure")

# --- MAIN DASHBOARD ---
if state:
    st.title("🌱 Synthetic Maturation: Neonatal to Adult")
    c1, c2 = st.columns([1.5, 1])
    
    with c1:
        st.subheader("3D Synthetic Synthesis")
        bones = state["physics"]["bones"]
        df = pd.DataFrame([{"id": k, "x": v[0], "y": v[1], "z": v[2]} for k, v in bones.items()])
        
        fig = go.Figure()
        # Bones
        fig.add_trace(go.Scatter3d(x=df['x'], y=df['z'], z=df['y'], mode='markers', marker=dict(size=3, color='#58a6ff')))
        # Muscles
        for m in state["physics"]["muscles"]:
            fig.add_trace(go.Scatter3d(x=[m['p1'][0], m['p2'][0]], y=[m['p1'][2], m['p2'][2]], z=[m['p1'][1], m['p2'][1]], mode='lines', line=dict(color='rgba(255,100,100,0.15)')))

        fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False), paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Da Vinci Ratios")
        st.write(f"**Head-to-Body:** `1 / {round(1/state['growth']['head_to_body_ratio'], 1)}`")
        st.write(f"**Limb Length:** `{round(state['growth']['limb_development']*100, 1)}%` matured")
        
        st.divider()
        st.write("### Mindprint Logic")
        st.write(f"ADHD/Autism k-Scalar: `0.05`")
        st.info("Cognitive associative jumps are being logged as the skeletal manifold matures.")

time.sleep(1)
st.rerun()

