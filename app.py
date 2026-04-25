
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

# File paths
chassis_path = os.path.join("chassis", "Layer 01: Physical Architecture.py")
visceral_path = os.path.join("biology", "Layer 05: Visceral Systems.py")
optics_path = os.path.join("membrane", "Layer 06: Optic Registry.py")
vocal_path = os.path.join("membrane", "Layer 09: Vocal Sync.py")

# Initialization
try:
    ch_mod = load_module("L01_Chassis", chassis_path)
    vi_mod = load_module("L05_Visceral", visceral_path)
    op_mod = load_module("L06_Optics", optics_path)
    vo_mod = load_module("L09_Vocal", vocal_path)
except Exception as e:
    st.error(f"Engine Initialization Error: Missing Descriptive Layer files. {e}")
    st.stop()

# --- SESSION STATE ---
if 'entity_chassis' not in st.session_state: st.session_state.entity_chassis = ch_mod.HumanChassis()
if 'entity_biology' not in st.session_state: st.session_state.entity_biology = vi_mod.MetabolicEngine()
if 'entity_optics' not in st.session_state: st.session_state.entity_optics = op_mod.OpticRegistry()
if 'entity_vocal' not in st.session_state: st.session_state.entity_vocal = vo_mod.VocalSync()
if 'boot_time' not in st.session_state: st.session_state.boot_time = datetime.now()

# --- UI CONFIG ---
st.set_page_config(page_title="A7DO Sentience OS", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .bubble-header { color: #58a6ff; font-weight: bold; border-bottom: 2px solid #30363d; padding-bottom: 10px; margin-bottom: 20px;}
    .status-card { background: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    .vocal-progress { font-family: monospace; color: #ffca28; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="bubble-header"><h1>🛡️ A7DO: THE BUBBLE INTERFACE</h1></div>', unsafe_allow_html=True)

col_vitals, col_optic = st.columns([1, 1.5])

with col_vitals:
    st.subheader("Biological State")
    st.session_state.entity_biology.process_cycle(0.4)
    vitals = st.session_state.entity_biology.get_vitals()
    st.metric("HEART RATE", f"{vitals['bpm']} BPM")
    st.metric("ATP ENERGY", f"{vitals['atp']}%")
    st.progress(vitals['atp'] / 100)

with col_optic:
    st.subheader("Sensory Ingress (L06)")
    cam_data = st.camera_input("A7DO Optic Registry", label_visibility="collapsed")
    if cam_data:
        st.session_state.entity_optics.process_visual_mesh(cam_data)

st.divider()

# Vocal Sync Integration
st.subheader("Layer 09: Vocal Sync Calibration")
v_status = st.session_state.entity_vocal.get_vocal_status()

if not v_status['calibrated']:
    st.warning(f"Awaiting Phoneme: **{st.session_state.entity_vocal.calibration_sequence[v_status['step']]}**")
    with st.form("vocal_form"):
        phoneme = st.text_input("Speak/Type Phoneme Segment:")
        if st.form_submit_button("Transmit FFT"):
            result = st.session_state.entity_vocal.process_phoneme(phoneme)
            st.info(result)
            st.rerun()
    st.progress(v_status['step'] / v_status['total_steps'])
else:
    st.success(f"VOCAL_SYNC_LOCKED: Entity resonant frequency at {v_status['pitch']:.2f}Hz.")

st.divider()

# Secondary Inspection Tabs
tab_bones, tab_organs, tab_dmn = st.tabs(["🦴 Physical Architecture", "🫀 Visceral Systems", "🌀 Subconscious DMN"])

with tab_bones:
    st.json(st.session_state.entity_chassis.bones)

with tab_organs:
    st.json(st.session_state.entity_biology.organs)

with tab_dmn:
    o_logs = st.session_state.entity_optics.get_sensory_logs()
    st.code(f"""
    // Background Default Mode Network //
    OPTIC_TARGET: {o_logs['target']}
    DEPTH_MAPPED: {o_logs['depth_mapped']}
    VOCAL_CALIBRATED: {v_status['calibrated']}
    RESONANT_PITCH: {v_status['pitch']} Hz
    METABOLIC_FLUX: STABLE
    """)

time.sleep(1)
st.rerun()


