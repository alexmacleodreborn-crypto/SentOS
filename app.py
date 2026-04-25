
import streamlit as st
import time
import importlib.util
import os
import random
import numpy as np
from datetime import datetime

# Hardware Components
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
    l03 = load_layer("L03", "actuators", "Layer 03: Movement Engine.py")
    l05 = load_layer("L05", "biology", "Layer 05: Visceral Systems.py")
    l06 = load_layer("L06", "membrane", "Layer 06: Optic Registry.py")
    l09 = load_layer("L09", "membrane", "Layer 09: Vocal Sync.py")
    l10 = load_layer("L10", "neocortex", "Layer 10: Cognitive Archive.py")
except Exception as e:
    st.error(f"Engine Hardware Fault: {e}")
    st.stop()

# --- INITIALIZE ENTITY ---
if 'a7do' not in st.session_state:
    st.session_state.a7do = {
        "chassis": l01.HumanChassis(),
        "movement": l03.MovementEngine(),
        "biology": l05.MetabolicEngine(),
        "optics": l06.OpticRegistry(),
        "vocal": l09.VocalSync(),
        "mind": l10.CognitiveArchive(),
        "boot_time": datetime.now()
    }

# --- UI ARCHITECTURE ---
st.set_page_config(page_title="A7DO Sentience OS", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .bubble-header { color: #58a6ff; font-weight: bold; border-bottom: 2px solid #30363d; padding-bottom: 10px; margin-bottom: 20px;}
    .telemetry-box { font-family: 'Courier New', monospace; background: #000; color: #00ff00; padding: 15px; border-radius: 10px; border: 1px solid #333; }
    .reach-indicator { color: #ff5252; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ A7DO: THE BUBBLE (Kinematic Active)")

col_meta, col_vis = st.columns([1, 1.8])

with col_meta:
    st.subheader("Biological Presence")
    # Metabolism reflects movement load
    move_load = st.session_state.a7do["movement"].velocity_m_s
    st.session_state.a7do["biology"].process_cycle(0.1 + move_load)
    vitals = st.session_state.a7do["biology"].get_vitals()
    
    st.metric("HEART RATE", f"{vitals['bpm']} BPM")
    st.metric("ATP ENERGY", f"{vitals['atp']}%")
    
    st.divider()
    st.subheader("Layer 03: Reach Control")
    reach_x = st.slider("Target Coordinate X (meters)", -1.0, 1.0, 0.0)
    reach_y = st.slider("Target Coordinate Y (meters)", 0.0, 2.0, 1.0)
    
    if st.button("EXECUTE REACH"):
        res = st.session_state.a7do["movement"].calculate_ik([reach_x, reach_y, 0.5])
        st.write(f"<span class='reach-indicator'>{res}</span>", unsafe_allow_html=True)

with col_vis:
    tab_stream, tab_anatomy, tab_mind = st.tabs(["👁️ Optic Membrane", "🧬 Anatomy Map", "🧠 Neocortex"])
    
    with tab_stream:
        webrtc_streamer(key="a7do-live", video_frame_callback=None)
        prop = st.session_state.a7do["movement"].get_proprioception()
        st.markdown(f"""
        <div class="telemetry-box">
            [ KINEMATIC TELEMETRY ]<br>
            JOINT_LOCK: STABLE<br>
            CENTER_OF_MASS: {prop['center_of_mass']}<br>
            VELOCITY: {prop['motion_velocity']} m/s<br>
            STABILITY: {prop['stability_index'] * 100}%
        </div>
        """, unsafe_allow_html=True)

    with tab_anatomy:
        st.json(st.session_state.a7do["chassis"].bones)
        
    with tab_mind:
        mind_data = st.session_state.a7do["mind"].get_mind_map()
        st.write(f"Active Memory Nodes: {mind_data['total_nodes']}")
        st.json(st.session_state.a7do["mind"].nodes)

st.divider()
st.code(f"// Subconscious DMN Loop // L03: Proprioception active. L05: ATP at {vitals['atp']}. L10: Thoughts pathing...")

time.sleep(1)
st.rerun()

