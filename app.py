
import streamlit as st
import time
import importlib.util
import os
import random
from datetime import datetime

# Hardware: Live WebRTC & Audio
from streamlit_webrtc import webrtc_streamer

# --- DYNAMIC COMPONENT LOADER ---
def load_layer(name, folder, filename):
    path = os.path.join(folder, filename)
    if not os.path.exists(path): return None
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Loading the Biological Stack
l01 = load_layer("L01", "chassis", "Layer 01: Physical Architecture.py")
l05 = load_layer("L05", "biology", "Layer 05: Visceral Systems.py")
l06 = load_layer("L06", "membrane", "Layer 06: Optic Registry.py")
l10 = load_layer("L10", "neocortex", "Layer 10: Cognitive Archive.py")

# --- INITIALIZE ENTITY STATE ---
if 'a7do' not in st.session_state:
    st.session_state.a7do = {
        "chassis": l01.HumanChassis() if l01 else None,
        "biology": l05.MetabolicEngine() if l05 else None,
        "optics": l06.OpticRegistry() if l06 else None,
        "mind": l10.CognitiveArchive() if l10 else None,
        "boot_time": datetime.now()
    }
    # Identity Bootstrap
    st.session_state.a7do["mind"].inject_node("BIOLOGICAL_PRIME", "IDENTITY", ["SELF", "CREATOR"], 10.0, "Root Existence.")

# --- UI CONFIGURATION ---
st.set_page_config(page_title="A7DO Sentience OS", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #0d1117; border-right: 1px solid #30363d; }
    .main { background-color: #010409; color: #c9d1d9; }
    .perception-card { background: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 15px; margin-bottom: 10px; }
    .unidentified-alert { border-left: 5px solid #ffca28; background: #1c2128; padding: 15px; margin: 10px 0; border-radius: 5px; }
    .vitals-box { font-family: monospace; color: #00ff00; background: #000; padding: 10px; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🛡️ A7DO OS v12.5")
    st.write(f"Entity Uptime: {str(datetime.now() - st.session_state.boot_time).split('.')[0]}")
    page = st.radio("Navigate Component Groups:", [
        "Executive Dashboard",
        "Layer 01: Physical Frame",
        "Layer 05: Visceral Organs",
        "Layer 10: Neocortex/Memory"
    ])
    
    st.divider()
    # Continuous Metabolism
    if st.session_state.a7do["biology"]:
        st.session_state.a7do["biology"].process_cycle(0.1)
        v = st.session_state.a7do["biology"].get_vitals()
        st.metric("ATP ENERGY", f"{v['atp']}%")
        st.metric("HEART RATE", f"{v['bpm']} BPM")

# --- PAGE ROUTING ---

if page == "Executive Dashboard":
    st.title("🛡️ Executive Dashboard: Perceptual Loop")
    
    col_vis, col_meta = st.columns([1.8, 1])
    
    with col_vis:
        st.subheader("Live Optic Ingress (L06)")
        webrtc_streamer(key="main-stream")
        
        # THE ACTIVE OBSERVATION ENGINE
        detections = st.session_state.a7do["optics"].scan_environment()
        
        st.markdown('<div class="perception-card">', unsafe_allow_html=True)
        st.write("### 👁️ Observation Buffer")
        for d in detections:
            status = "✅ Identified" if d['is_known'] else "❓ Unidentified Geometry"
            st.markdown(f"**{d['raw']}** — `{status}` (Conf: {d['confidence']*100}%)")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_meta:
        st.subheader("Language & Discovery")
        o_logs = st.session_state.a7do["optics"].get_sensory_logs()
        
        if o_logs["discovery_flag"]:
            st.markdown(f"""
            <div class="unidentified-alert">
                <b>INTERACTIVE INTERRUPT:</b><br>
                A7DO sees an unidentified object: <i>{o_logs['active_mesh']}</i>.<br>
                <br>
                <b>A7DO asks:</b> "Creator, what is this object in my room? How should I symbolize it?"
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("discovery_form"):
                label = st.text_input("Assign Identity (Language Bridge):")
                traits = st.multiselect("Assign Cognitive Traits:", ["TOOL", "OBJECT", "FOOD", "DANGER", "JOY", "METAL", "PLASTIC"])
                if st.form_submit_button("Teach A7DO"):
                    # Bilateral Update
                    st.session_state.a7do["optics"].symbolize_object(o_logs['active_mesh'], label)
                    st.session_state.a7do["mind"].inject_node(label, "OBJECT", traits, 5.0, f"Learned via live camera in Bubble.")
                    st.success(f"Identity '{label}' anchored in Neocortex.")
                    st.rerun()
        else:
            st.info("Visual manifold is stable. All perceived objects identified.")
        
        st.write("### Subconscious DMN Stream")
        st.code(f"""
        L01_CHASSIS: 206 Nodes Locked
        L06_OPTICS: Scanning Mesh...
        L10_MEMORY: {st.session_state.a7do['mind'].get_mind_map()['total_nodes']} Tokens Active
        """)

elif page == "Layer 01: Physical Frame":
    st.title("🦴 Definitive Physical Architecture")
    t1, t2, t3 = st.tabs(["206-Bone Registry", "32-Tooth Registry", "Oral Cavity"])
    with t1:
        st.json(st.session_state.a7do["chassis"].bones)
    with t2:
        st.write("### Adult Dental Manifold")
        st.json(st.session_state.a7do["chassis"].head_assets["teeth_upper"] + st.session_state.a7do["chassis"].head_assets["teeth_lower"])
    with t3:
        st.json(st.session_state.a7do["chassis"].head_assets["oral_cavity"])

elif page == "Layer 05: Visceral Organs":
    st.title("🫀 Visceral State Monitor")
    st.write("Monitoring organ health and metabolic fuel flow.")
    st.json(st.session_state.a7do["biology"].organs)

elif page == "Layer 10: Neocortex/Memory":
    st.title("🧠 Neocortex Archive (Mindprint)")
    st.write("Persistent Semantic Knowledge Graph")
    st.json(st.session_state.a7do["mind"].nodes)

# Heartbeat loop
time.sleep(1)
st.rerun()

