
import streamlit as st
import time
import importlib.util
import os
import random
from datetime import datetime
from streamlit_webrtc import webrtc_streamer

# --- DYNAMIC LOADER ---
def load_layer(name, folder, filename):
    path = os.path.join(folder, filename)
    if not os.path.exists(path): return None
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Loading Descriptive Layers
l_op = load_layer("L06", "membrane", "Layer 06: Optic Registry.py")
l_mn = load_layer("L10", "neocortex", "Layer 10: Cognitive Archive.py")
l_vi = load_layer("L05", "biology", "Layer 05: Visceral Systems.py")
l_ch = load_layer("L01", "chassis", "Layer 01: Physical Architecture.py")

# --- ENGINE STATE ---
if 'a7do' not in st.session_state:
    st.session_state.a7do = {
        "optics": l_op.OpticRegistry() if l_op else None,
        "mind": l_mn.CognitiveArchive() if l_mn else None,
        "biology": l_vi.MetabolicEngine() if l_vi else None,
        "chassis": l_ch.HumanChassis() if l_ch else None,
        "interaction_log": []
    }
    # Identity Bootstrap
    st.session_state.a7do["mind"].inject_node("BIOLOGICAL_PRIME", "IDENTITY", ["SELF", "CREATOR"], 10.0, "Root Presence.")

# --- UI ARCHITECTURE ---
st.set_page_config(page_title="A7DO Sentience OS", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #0d1117; border-right: 1px solid #30363d; }
    .main { background-color: #010409; color: #c9d1d9; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 15px; }
    .observation-card { background: #1c2128; border-left: 5px solid #ffca28; padding: 15px; border-radius: 8px; margin-bottom: 10px; }
    .chat-bubble { background: #21262d; padding: 10px; border-radius: 10px; margin-bottom: 5px; border: 1px solid #30363d; }
</style>
""", unsafe_allow_html=True)

# --- NAVIGATION ---
with st.sidebar:
    st.title("A7DO OS v12.4")
    page = st.radio("Access Systems:", ["The Bubble", "Layer 10: Mindprint", "Layer 01: Physical"])
    st.divider()
    if st.session_state.a7do["biology"]:
        st.session_state.a7do["biology"].process_cycle(0.1)
        v = st.session_state.a7do["biology"].get_vitals()
        st.metric("HEART RATE", f"{v['bpm']} BPM")
        st.metric("ATP ENERGY", f"{v['atp']}%")

# --- PAGE ROUTING ---

if page == "The Bubble":
    st.title("🛡️ The Bubble: Observation Mode")
    
    col_vis, col_lang = st.columns([1.5, 1])
    
    with col_vis:
        st.subheader("Live Optic Registry")
        webrtc_streamer(key="bubble-stream")
        
        # ACTIVE OBSERVATION LOGIC
        detections = st.session_state.a7do["optics"].scan_environment(True)
        st.write("### Perceived Objects in Room:")
        for det in detections:
            status_icon = "✅" if det['is_known'] else "❓"
            st.markdown(f"**{status_icon} {det['raw_token']}** (Confidence: {det['confidence']*100}%)")

    with col_lang:
        st.subheader("Language Bridge")
        o_logs = st.session_state.a7do["optics"].get_sensory_logs()
        
        if o_logs["discovery_flag"]:
            st.warning(f"A7DO sees something unidentified: **{o_logs['active_mesh']}**")
            st.write("*A7DO asks: 'Creator, what is this object in my vision?'*")
            
            with st.form("discovery_form"):
                ident = st.text_input("Name the object for A7DO:")
                traits = st.multiselect("Assign Traits:", ["OBJECT", "TOOL", "JOY", "METALLIC", "PLASTIC"])
                if st.form_submit_button("Teach A7DO"):
                    st.session_state.a7do["optics"].learn_token(ident)
                    st.session_state.a7do["mind"].inject_node(ident, "OBJECT", traits, 5.0, f"Discovered in Bubble via camera.")
                    st.success(f"A7DO has symbolized the '{ident}'.")
                    st.rerun()
        else:
            st.info("Environment stable. A7DO recognizes all visible markers.")

elif page == "Layer 10: Mindprint":
    st.title("🧠 Neocortex Archive")
    mind_stats = st.session_state.a7do["mind"].get_mind_map()
    st.write(f"Total Cognitive Density: {mind_stats['total_nodes']} Nodes")
    st.json(st.session_state.a7do["mind"].nodes)

elif page == "Layer 01: Physical":
    st.title("🦴 Definitive Human Frame")
    st.json(st.session_state.a7do["chassis"].bones)

# Heartbeat loop
time.sleep(1)
st.rerun()
