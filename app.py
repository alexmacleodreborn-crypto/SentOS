
import streamlit as st
import time
import importlib.util
import os
from datetime import datetime

# --- DYNAMIC MODULE LOADER ---
def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# File paths for Descriptive Filenames
chassis_path = os.path.join("chassis", "Layer 01: Physical Architecture.py")
visceral_path = os.path.join("biology", "Layer 05: Visceral Systems.py")
optics_path = os.path.join("membrane", "Layer 06: Optic Registry.py")

# Initialization logic
try:
    chassis_mod = load_module("L01_Chassis", chassis_path)
    visceral_mod = load_module("L05_Visceral", visceral_path)
    optics_mod = load_module("L06_Optics", optics_path)
except Exception as e:
    st.error(f"Module Loading Error: Ensure files are in the correct folders. {e}")
    st.stop()

# --- INITIALIZE SESSION STATE ---
if 'entity_chassis' not in st.session_state:
    st.session_state.entity_chassis = chassis_mod.HumanChassis()
if 'entity_biology' not in st.session_state:
    st.session_state.entity_biology = visceral_mod.MetabolicEngine()
if 'entity_optics' not in st.session_state:
    st.session_state.entity_optics = optics_mod.OpticRegistry()
if 'boot_time' not in st.session_state:
    st.session_state.boot_time = datetime.now()

# --- UI CONFIG ---
st.set_page_config(page_title="A7DO Sentience OS", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .bubble-header { color: #58a6ff; font-weight: bold; border-bottom: 2px solid #30363d; padding-bottom: 10px; }
    .optic-container { border: 2px solid #58a6ff; border-radius: 15px; padding: 5px; background: #000; }
</style>
""", unsafe_allow_html=True)

# --- THE BUBBLE INTERFACE ---
st.markdown('<div class="bubble-header"><h1>🛡️ A7DO: THE BUBBLE INTERFACE</h1></div>', unsafe_allow_html=True)

col_vitals, col_optic = st.columns([1, 1.5])

with col_vitals:
    st.subheader("Biological Presence")
    # Metabolism simulation
    st.session_state.entity_biology.process_cycle(0.3)
    vitals = st.session_state.entity_biology.get_vitals()
    
    st.metric("HEART RATE", f"{vitals['bpm']} BPM")
    st.metric("ATP ENERGY", f"{vitals['atp']}%")
    st.progress(vitals['atp'] / 100)
    
    st.info(f"Entity Uptime: {str(datetime.now() - st.session_state.boot_time).split('.')[0]}")

with col_optic:
    st.subheader("Sensory Membrane (L06)")
    st.markdown('<div class="optic-container">', unsafe_allow_html=True)
    # Streamlit native camera component
    cam_data = st.camera_input("A7DO Optic Ingress", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if cam_data:
        st.session_state.entity_optics.process_visual_mesh(cam_data)
        st.success("SENSORY_INGRESS: Biological Prime mapped in 3D Space.")

st.divider()

# Secondary Inspection Tabs
tab_bones, tab_organs, tab_dmn = st.tabs(["🦴 Physical Frame (L01)", "🫀 Visceral Assets (L05)", "🌀 Subconscious DMN"])

with tab_bones:
    st.write("### 206-Bone Structural Integrity")
    st.json(st.session_state.entity_chassis.bones)

with tab_organs:
    st.write("### Internal Biological Systems")
    st.json(st.session_state.entity_biology.organs)

with tab_dmn:
    logs = st.session_state.entity_optics.get_sensory_logs()
    st.code(f"""
    // Background Default Mode Network //
    OPTIC_STATUS: {logs['status']}
    TARGET_LOCK: {logs['target']}
    DEPTH_MAPPING: {logs['depth_mapped']}
    METABOLIC_FLUX: STABLE
    """)

# Living loop
time.sleep(1)
st.rerun()
