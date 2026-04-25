
import streamlit as st
import time
import importlib.util
import os
import random
from datetime import datetime

# Required for Live Feed & Audio
from streamlit_webrtc import webrtc_streamer
from streamlit_mic_recorder import mic_recorder

# --- DYNAMIC MODULE LOADER ---
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
    st.error(f"Engine Hardware Fault: {e}")
    st.stop()

# --- ENGINE STATE ---
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
    .bubble-container { background: #0e1117; border: 2px solid #58a6ff; border-radius: 15px; padding: 20px; }
    .telemetry-font { font-family: 'Courier New', monospace; color: #00ff00; font-size: 0.85rem; }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ A7DO: THE BUBBLE (Active Membrane)")

col_meta, col_membrane = st.columns([1, 1.8])

with col_meta:
    st.subheader("Biological Presence")
    st.session_state.a7do["biology"].process_cycle(0.2)
    vitals = st.session_state.a7do["biology"].get_vitals()
    
    st.metric("HEART RATE", f"{vitals['bpm']} BPM")
    st.metric("ATP ENERGY", f"{vitals['atp']}%")
    
    st.divider()
    st.subheader("Layer 09: Sonic Link")
    v_tele = st.session_state.a7do["vocal"].get_vocal_telemetry()
    
    if not st.session_state.a7do["vocal"].is_calibrated:
        st.info(f"Target Phoneme: **{v_tele['target']}**")
        audio = mic_recorder(start_prompt="🎤 Start Resonance Scan", stop_prompt="⏹ Stop", key='recorder')
        
        # Simulated Speech-to-Text Bridge
        v_manual = st.text_input("Transcription Verification (Type word heard):")
        if v_manual:
            res = st.session_state.a7do["vocal"].validate_segment(v_manual)
            st.write(f"Result: `{res}`")
            if res == "SYNC_COMPLETE": st.balloons()
            st.rerun()
    else:
        st.success(f"VOCAL SYNC LOCKED: {v_tele['hz']}Hz")

with col_membrane:
    st.subheader("Layer 06: Optic Matrix")
    # WebRTC Live Streamer replaces the static camera picture
    webrtc_streamer(key="a7do-live-feed", video_frame_callback=None)
    
    st.markdown("""
    <div class="telemetry-font">
        [ SYSTEM_MESH_ACTIVE ]<br>
        EYE_TRACKING: LOCK_ON<br>
        DEPTH_STABILITY: 0.992<br>
        ENVIRONMENT_SYNC: TRUE
    </div>
    """, unsafe_allow_html=True)

st.divider()
tab_mn, tab_dmn = st.tabs(["🧬 Chassis Map", "🌀 Subconscious DMN"])
with tab_mn:
    st.json(st.session_state.a7do["chassis"].bones)
with tab_dmn:
    st.code(f"""
    // Background DMN Squelch //
    L01_ARCH: 206 nodes stable.
    L05_VISCERAL: BPM {vitals['bpm']}
    L06_OPTICS: Live stream active.
    L09_VOCAL: Resonance {v_tele['status']}
    """)

time.sleep(1)
st.rerun()
