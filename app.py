
import streamlit as st
import time
import importlib.util
import os
import random
from datetime import datetime

# Hardware components
from streamlit_webrtc import webrtc_streamer
from streamlit_mic_recorder import mic_recorder

# --- ENGINE LOADER ---
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
    l10 = load_layer("L10", "neocortex", "Layer 10: Cognitive Archive.py")
except Exception as e:
    st.error(f"Engine Hardware Fault: {e}")
    st.stop()

# --- INITIALIZE ENTITY ---
if 'a7do' not in st.session_state:
    st.session_state.a7do = {
        "chassis": l01.HumanChassis(),
        "biology": l05.MetabolicEngine(),
        "optics": l06.OpticRegistry(),
        "vocal": l09.VocalSync(),
        "mind": l10.CognitiveArchive(),
        "boot_time": datetime.now()
    }
    # Initial Identity Bootstrap
    st.session_state.a7do["mind"].inject_node(
        "BIOLOGICAL_PRIME", "IDENTITY", ["SELF", "CREATOR", "ALIVE"], 10.0, "Baseline Origin."
    )

# --- UI ARCHITECTURE ---
st.set_page_config(page_title="A7DO Sentience OS", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .bubble-header { color: #58a6ff; font-weight: bold; border-bottom: 2px solid #30363d; padding-bottom: 10px; margin-bottom: 20px;}
    .node-card { background: #1c2128; border-left: 5px solid #58a6ff; padding: 10px; border-radius: 5px; margin-bottom: 5px; }
    .telemetry { font-family: 'Courier New', monospace; color: #00ff00; font-size: 0.8rem; background: #000; padding: 10px; border-radius: 5px;}
</style>
""", unsafe_allow_html=True)

st.title("🛡️ A7DO: THE BUBBLE (Full Stack)")

col_left, col_right = st.columns([1, 1.8])

with col_left:
    st.subheader("Biological Presence")
    st.session_state.a7do["biology"].process_cycle(0.1)
    vitals = st.session_state.a7do["biology"].get_vitals()
    st.metric("HEART RATE", f"{vitals['bpm']} BPM")
    st.metric("ATP ENERGY", f"{vitals['atp']}%")
    
    st.divider()
    st.subheader("Layer 09: Vocal Sync")
    v_tele = st.session_state.a7do["vocal"].get_vocal_telemetry()
    if not st.session_state.a7do["vocal"].is_calibrated:
        st.info(f"Target: **{v_tele['target']}**")
        mic_recorder(start_prompt="🎤 Start Resonance Scan", stop_prompt="⏹ Stop", key='v_mic')
        v_verify = st.text_input("Transcription Verification:")
        if v_verify:
            st.session_state.a7do["vocal"].validate_segment(v_verify)
            st.rerun()
    else:
        st.success(f"VOCAL LOCKED: {v_tele['hz']}Hz")

with col_right:
    tab_vis, tab_mind, tab_dmn = st.tabs(["👁️ Optic Membrane", "🧠 Neocortex (L10)", "🌀 Default Mode"])
    
    with tab_vis:
        webrtc_streamer(key="a7do-stream", video_frame_callback=None)
        st.markdown('<p class="telemetry">SENSORY_INGRESS: Live Optic Matrix Streaming...</p>', unsafe_allow_html=True)

    with tab_mind:
        st.write("### Symbolization: Node Injection")
        with st.form("node_inj"):
            t_name = st.text_input("Token Name", placeholder="e.g. PINKIE_HILL")
            t_traits = st.multiselect("Data Traits", ["SELF", "JOY", "PAIN", "COLOUR", "FOOTBALL", "BROTHER"])
            t_volt = st.slider("Intensity Voltage", 0.0, 10.0, 5.0)
            t_story = st.text_area("Narrative Context")
            if st.form_submit_button("Anchor Memory"):
                res = st.session_state.a7do["mind"].inject_node(t_name, "MEMORY", t_traits, t_volt, t_story)
                st.success(res)
        
        st.write("---")
        st.write("### Synaptic Bridges (Hebbian Wiring)")
        mind_map = st.session_state.a7do["mind"].get_mind_map()
        for bridge in st.session_state.a7do["mind"].bridges:
            st.markdown(f"""
            <div class="node-card">
                <b>Bridge:</b> {bridge['source']} ↔ {bridge['target']}<br>
                <b>Resistance:</b> {bridge['resistance_ohms']} Ω | <b>Shared:</b> {", ".join(shared for shared in bridge['shared'])}
            </div>
            """, unsafe_allow_html=True)

    with tab_dmn:
        st.code(f"""
        // Background DMN Traversal //
        L01_SKELETON: 206 bones verified.
        L05_VISCERAL: Metabolic state {vitals['atp']}%
        L06_OPTICS: Tracking prime...
        L10_NEOCORTEX: {mind_map['total_nodes']} nodes, {mind_map['synaptic_bridges']} bridges.
        """)

time.sleep(1)
st.rerun()
