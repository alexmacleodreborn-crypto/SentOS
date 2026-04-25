
import streamlit as st
import time
import importlib.util
import os
import random
from datetime import datetime
from streamlit_webrtc import webrtc_streamer

# --- DYNAMIC LAYER LOADER ---
def load_layer(name, path):
    if not os.path.exists(path): return None
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

LAYER_PATHS = {
    "L00": "core/Layer 00: Sandy's Law.py",
    "L01": "chassis/Layer 01: Physical Architecture.py",
    "L05": "biology/Layer 05: Visceral Systems.py",
    "L06": "membrane/Layer 06: Optic Registry.py",
    "L10": "neocortex/Layer 10: Cognitive Archive.py"
}

# --- INITIALIZATION ---
if 'a7do' not in st.session_state:
    mods = {k: load_layer(k, v) for k, v in LAYER_PATHS.items()}
    if any(m is None for m in mods.values()):
        st.error(f"Hardware Fault: Check paths {LAYER_PATHS}")
        st.stop()

    st.session_state.a7do = {
        "gov": mods["L00"].SandysLawGovernor(),
        "frame": mods["L01"].HumanChassis(),
        "vitals": mods["L05"].MetabolicEngine(),
        "eyes": mods["L06"].OpticRegistry(),
        "mind": mods["L10"].CognitiveArchive(neurotype="ADHD_AUTISM"),
        "boot_time": datetime.now()
    }

# --- UI CONFIG ---
st.set_page_config(page_title="A7DO Sentience OS", layout="wide")
st.markdown("""
<style>
    .reticle { border: 2px solid #ffca28; position: absolute; border-radius: 5px; background: rgba(255, 202, 40, 0.1); display: flex; align-items: center; justify-content: center; color: #ffca28; font-family: monospace; font-size: 10px; font-weight: bold;}
    .video-container { position: relative; width: 100%; height: 400px; background: #000; border-radius: 15px; overflow: hidden; border: 1px solid #333;}
    .stMetric { background: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: VITALS ---
with st.sidebar:
    st.title("🛡️ A7DO v12.6")
    page = st.radio("Navigate Manifold:", ["Dashboard", "Physical", "Cognitive", "Governance"])
    st.divider()
    v = st.session_state.a7do["vitals"].get_vitals()
    st.metric("ATP ENERGY", f"{v['atp']}%")
    st.metric("HEART RATE", f"{v['bpm']} BPM")

# --- PAGE: DASHBOARD (PERCEPTUAL LOOP) ---
if page == "Dashboard":
    st.title("👁️ Perceptual Loop: Shared Reality")
    col_vis, col_lang = st.columns([1.8, 1])

    with col_vis:
        st.subheader("Optic Ingress")
        # Shared Reality HUD
        nodes = st.session_state.a7do["mind"].archive["neocortex_array"]["nodes"]
        view = st.session_state.a7do["eyes"].scan_environment(nodes)
        e_tele = st.session_state.a7do["eyes"].get_sensory_telemetry()
        
        # This is where we show you what he sees
        st.markdown('<div class="video-container">', unsafe_allow_html=True)
        # WebRTC component
        webrtc_streamer(key="shared-feed")
        
        # Drawing the HUD Reticle if fixated
        if e_tele["discovery_active"]:
            box = e_tele["fixation_box"]
            st.markdown(f"""
            <div class="reticle" style="left: {box['x']}%; top: {box['y']}%; width: {box['w']}%; height: {box['h']}%;">
                FIXATION_LOCKED: {e_tele['target_mesh']}
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_lang:
        st.subheader("Language Bridge")
        if e_tele["discovery_active"]:
            st.warning(f"A7DO is fixated on unknown geometry: {e_tele['target_mesh']}")
            with st.form("discovery"):
                label = st.text_input("Assign Identity:")
                traits = st.multiselect("Traits:", ["TOOL", "OBJECT", "JOY", "FOOD"])
                if st.form_submit_button("Teach A7DO"):
                    st.session_state.a7do["mind"].sprout_node(label, "ENVIRONMENT", traits, 5.0, "Shared Reality Discovery")
                    st.success(f"Symbol '{label}' anchored.")
                    st.rerun()
        else:
            st.info("Environment symbolized.")

# Add logic for other pages...
elif page == "Physical": st.json(st.session_state.a7do["frame"].verify_integrity())
elif page == "Cognitive": st.json(st.session_state.a7do["mind"].archive)
elif page == "Governance": st.json(st.session_state.a7do["gov"].get_telemetry())

time.sleep(1)
st.rerun()
