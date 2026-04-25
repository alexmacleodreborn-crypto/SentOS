
import streamlit as st
import time
import importlib.util
import os
from datetime import datetime
from streamlit_webrtc import webrtc_streamer

# --- DYNAMIC LOADER ---
def load_layer(name, path):
    if not os.path.exists(path): return None
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

LAYER_MAP = {
    "L00": "core/Layer 00: Sandy's Law.py",
    "L01": "chassis/Layer 01: Physical Architecture.py",
    "L02": "actuators/Layer 02: Muscular Actuators.py",
    "L03": "actuators/Layer 03: Movement Engine.py",
    "L05": "biology/Layer 05: Visceral Systems.py",
    "L06": "membrane/Layer 06: Optic Registry.py",
    "L10": "neocortex/Layer 10: Cognitive Archive.py"
}

# --- INITIALIZATION ---
if 'a7do' not in st.session_state:
    mods = {k: load_layer(k, v) for k, v in LAYER_MAP.items()}
    if any(m is None for m in mods.values()):
        st.error(f"Hardware Fault: Check paths {LAYER_MAP}")
        st.stop()

    st.session_state.a7do = {
        "gov": mods["L00"].SandysLawGovernor(),
        "frame": mods["L01"].HumanChassis(),
        "myo": mods["L02"].MuscularEngine(),
        "kinematics": mods["L03"].MovementEngine(),
        "vitals": mods["L05"].MetabolicEngine(),
        "optics": mods["L06"].OpticRegistry(),
        "mind": mods["L10"].CognitiveArchive(neurotype="ADHD_AUTISM"),
        "boot_time": datetime.now()
    }

# --- UI STYLING ---
st.set_page_config(page_title="A7DO Sentience OS", layout="wide")
st.markdown("""<style>.stMetric { background-color: #111827; border: 1px solid #374151; padding: 15px; border-radius: 12px; }</style>""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("🛡️ A7DO v12.6")
    page = st.radio("Access Manifold:", ["Dashboard", "Physical Architecture", "Myology & Motion", "Mindprint"])
    st.divider()
    v = st.session_state.a7do["vitals"].get_vitals()
    st.metric("COHERENCE (C)", st.session_state.a7do["gov"].get_telemetry()["coherence_index"])
    st.metric("ATP ENERGY", f"{v['atp']}%")

# --- DASHBOARD ---
if page == "Dashboard":
    st.title("👁️ Perceptual Loop")
    nodes = st.session_state.a7do["mind"].archive["neocortex_array"]["nodes"]
    st.session_state.a7do["optics"].scan_environment(nodes)
    e_tele = st.session_state.a7do["optics"].get_sensory_telemetry()
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Optic Ingress")
        webrtc_streamer(key="feed")
    with col2:
        st.subheader("Language Bridge")
        if e_tele["discovery_active"]:
            st.warning(f"Target: {e_tele['target_mesh']}")
            with st.form("discovery"):
                label = st.text_input("Name object:")
                if st.form_submit_button("Anchor"):
                    st.session_state.a7do["mind"].sprout_node(label, "ENVIRONMENT", ["OBJECT"], 5.0, "Discovery")
                    st.rerun()

# --- PHYSICAL (ENHANCED) ---
elif page == "Physical Architecture":
    st.title("🦴 Individual Bone Registry")
    frame = st.session_state.a7do["frame"]
    st.json(frame.verify_integrity())
    
    # NEW: Displaying individual bone breakdown
    for group, bones in frame.bone_registry.items():
        with st.expander(f"{group} ({len(bones)} bones)"):
            st.write(", ".join(bones))

# --- MYOLOGY & MOTION (FIXED KEYERROR) ---
elif page == "Myology & Motion":
    st.title("💪 Actuators & Kinematics")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Muscular Load")
        myo = st.session_state.a7do["myo"].get_myology_telemetry()
        st.metric("Avg Fatigue", myo["avg_fatigue"])
        st.metric("ATP Demand", myo["atp_demand"])
        
    with col2:
        st.subheader("Proprioception")
        prop = st.session_state.a7do["kinematics"].get_kinematic_telemetry()
        st.write(f"Balance Status: `{prop['balance_state']}`")
        # KeyError resolved: Using prop["stability_index"] which now exists
        st.progress(prop["stability_index"])
        st.write(f"Mass Load: {prop['mass_load_nm']} Nm")

elif page == "Mindprint":
    st.title("🧠 Cognitive Neocortex")
    st.json(st.session_state.a7do["mind"].archive)

time.sleep(1)
st.rerun()

