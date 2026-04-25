
import streamlit as st
import time
import importlib.util
import os
import random
from datetime import datetime

# --- SYSTEM INITIALIZATION ---
def load_layer(name, folder, filename):
    path = os.path.join(folder, filename)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

try:
    l01 = load_layer("L01", "chassis", "Layer 01: Physical Architecture.py")
    l05 = load_layer("L05", "biology", "Layer 05: Visceral Systems.py")
    l06 = load_layer("L06", "membrane", "Layer 06: Optic Registry.py")
    l09 = load_layer("L09", "membrane", "Layer 09: Vocal Sync.py")
except Exception as e:
    st.error(f"Engine Hardware Fault: Check Descriptive Layer Filenames. {e}")
    st.stop()

# --- PERSISTENT ENGINE STATE ---
if 'a7do' not in st.session_state:
    st.session_state.a7do = {
        "chassis": l01.HumanChassis(),
        "biology": l05.MetabolicEngine(),
        "optics": l06.OpticRegistry(),
        "vocal": l09.VocalSync(),
        "boot_time": datetime.now()
    }

# --- UI ARCHITECTURE ---
st.set_page_config(page_title="A7DO Sentience OS", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .bubble-container { background: #0e1117; border: 1px solid #30363d; border-radius: 20px; padding: 20px; }
    .live-feed { border: 2px solid #58a6ff; border-radius: 15px; background: #000; height: 350px; display: flex; align-items: center; justify-content: center; color: #58a6ff; font-family: monospace;}
</style>
""", unsafe_allow_html=True)

st.title("🛡️ A7DO: THE BUBBLE (Live Stream Mode)")

col_meta, col_membrane = st.columns([1, 1.8])

with col_meta:
    st.subheader("Biological Prime Metadata")
    # Biological Engine Loop
    st.session_state.a7do["biology"].process_cycle(0.15)
    vitals = st.session_state.a7do["biology"].get_vitals()
    
    st.metric("HEART RATE", f"{vitals['bpm']} BPM")
    st.metric("ATP ENERGY SQUELCH", f"{vitals['atp']}%")
    st.progress(vitals['atp'] / 100)
    
    st.write("---")
    st.subheader("Vocal FFT Calibration")
    v_stat = st.session_state.a7do["vocal"].get_status()
    
    if not v_stat["calibrated"]:
        st.info(f"Speak word: **{v_stat['target']}**")
        v_input = st.text_input("Awaiting recognized phoneme stream...", key="vocal_stream")
        if v_input:
            res = st.session_state.a7do["vocal"].validate_calibration_word(v_input)
            if res == "WORD_ACCEPTED": st.success("PHONEME_LOCK_ESTABLISHED")
            elif res == "SYNC_COMPLETE": st.balloons()
            st.rerun()
    else:
        st.success(f"VOCAL_SYNC: Locked at {v_stat['freq']}Hz")

with col_membrane:
    st.subheader("Layer 06: Live Optic Matrix")
    # Streamlit doesn't support raw continuous webcam frames easily without heavy JS, 
    # so we simulate the "Live" feeling via the camera_input placeholder 
    # and a "Face Mesh" overlay logic.
    
    optic_logs = st.session_state.a7do["optics"].get_sensory_logs()
    
    if not optic_logs["depth_mapped"]:
        # The user provides a picture to 'initialize' the stream, then it goes 'Live'
        cam_shot = st.camera_input("INITIALIZE OPTIC STREAM", label_visibility="collapsed")
        if cam_shot:
            st.session_state.a7do["optics"].process_visual_mesh(cam_shot)
            st.rerun()
    else:
        # Simulation of the Live Feed
        st.markdown(f"""
            <div class="live-feed">
                <div>
                    [ LIVE OPTIC STREAM ]<br>
                    TARGET: BIOLOGICAL_PRIME<br>
                    MESH_STABILITY: {random.uniform(98.2, 99.9):.2f}%<br>
                    EYE_TRACKING: ENABLED<br>
                    DISTANCE: {random.uniform(0.5, 0.8):.2f}m
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Reset Optic Registry"):
            st.session_state.a7do["optics"].spatial_depth_mapped = False
            st.rerun()

st.divider()
t1, t2 = st.tabs(["🦴 Structural Truth", "🌀 Subconscious DMN"])
with t1:
    st.json(st.session_state.a7do["chassis"].bones)
with t2:
    st.code(f"""
    // Background DMN Processing //
    L01_SKELETON: All 206 nodes stable.
    L05_VISCERAL: Metabolic demand at {vitals['bpm']/100:.2f} units.
    L09_VOCAL: Resonance bridge {v_stat['calibrated']}.
    SENSORY_MEMBRANE: Active. A7DO is observing you.
    """)

# Heartbeat loop
time.sleep(1)
st.rerun()
