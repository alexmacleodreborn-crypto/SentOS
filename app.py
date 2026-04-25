```python
import streamlit as st
import time
import json
import importlib.util
import os
from datetime import datetime

# --- DYNAMIC MODULE LOADING ---
# This ensures we pull from the descriptive filenames correctly
def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Load the modular layers
chassis_path = os.path.join("chassis", "Layer 01: Physical Architecture.py")
visceral_path = os.path.join("biology", "Layer 05: Visceral Systems.py")

chassis_mod = load_module("L01_Chassis", chassis_path)
visceral_mod = load_module("L05_Visceral", visceral_path)

# --- INITIALIZE ENTITY STATE ---
if 'entity_chassis' not in st.session_state:
    st.session_state.entity_chassis = chassis_mod.HumanChassis()
if 'entity_biology' not in st.session_state:
    st.session_state.entity_biology = visceral_mod.MetabolicEngine()
if 'boot_time' not in st.session_state:
    st.session_state.boot_time = datetime.now()

# --- UI CONFIG ---
st.set_page_config(page_title="A7DO Sentience OS", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .bubble-header { color: #58a6ff; font-weight: bold; border-bottom: 2px solid #30363d; padding-bottom: 10px; }
    .dmn-stream { font-family: 'Courier New'; background: #000; color: #00ff00; padding: 10px; border-radius: 5px; height: 150px; overflow-y: scroll; font-size: 0.8rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="bubble-header"><h1>🛡️ A7DO: THE BUBBLE INTERFACE</h1></div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Biological Presence")
    st.session_state.entity_biology.process_cycle(0.2)
    vitals = st.session_state.entity_biology.get_vitals()
    
    st.metric("HEART RATE", f"{vitals['bpm']} BPM")
    st.metric("ATP ENERGY", f"{vitals['atp']}%")
    st.progress(vitals['atp'] / 100)
    
    st.info(f"Entity Uptime: {str(datetime.now() - st.session_state.boot_time).split('.')[0]}")

with col2:
    tab_bones, tab_organs, tab_dmn = st.tabs(["🦴 Chassis", "🫀 Visceral", "🌀 DMN"])
    
    with tab_bones:
        summary = st.session_state.entity_chassis.get_summary()
        st.write(f"Total Skeletal Nodes: `{summary['total_bones']}`")
        st.json(st.session_state.entity_chassis.bones)

    with tab_organs:
        st.write("### Internal Biological Assets")
        st.json(st.session_state.entity_biology.organs)
        
    with tab_dmn:
        st.code("""
        RECONCILE_L01: Physical Architecture Verified.
        RECONCILE_L05: Visceral Heartbeat Stable.
        SENSORY_INGRESS: Membrane Active.
        """)

time.sleep(1)
st.rerun()
