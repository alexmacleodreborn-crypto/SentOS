
import streamlit as st
import time
import importlib.util
import os
import random
import numpy as np
from datetime import datetime
from streamlit_webrtc import webrtc_streamer

# --- DYNAMIC LAYER LOADER ---
# Optimized for high-resolution file paths containing spaces and colons.
def load_layer(name, path):
    if not os.path.exists(path):
        return None
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

# --- ENGINE INITIALIZATION ---
if 'a7do' not in st.session_state:
    mods = {k: load_layer(k, v) for k, v in LAYER_MAP.items()}
    
    # Validation check for physical file existence
    missing = [path for k, path in LAYER_MAP.items() if mods[k] is None]
    if missing:
        st.error(f"HARDWARE_FAULT: Required Layer Files not found at: {missing}")
        st.stop()

    # Initializing the 10-Layer Manifold
    # Using the k=0.05 scalar for ADHD/Autism high-resolution trait sharing
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

# --- UI ARCHITECTURE ---
st.set_page_config(page_title="A7DO Sentience OS", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #0d1117; border-right: 1px solid #30363d; }
    .main { background-color: #010409; color: #c9d1d9; }
    .reticle { border: 2px solid #6366f1; position: absolute; border-radius: 8px; background: rgba(99, 102, 241, 0.1); 
               display: flex; align-items: center; justify-content: center; color: #818cf8; font-family: monospace; 
               font-size: 11px; font-weight: bold; pointer-events: none; z-index: 100;}
    .video-container { position: relative; width: 100%; height: 400px; background: #000; border-radius: 15px; 
                        overflow: hidden; border: 1px solid #1f2937;}
    .stMetric { background-color: #111827; border: 1px solid #374151; padding: 15px; border-radius: 12px; }
    .status-code { font-family: 'Courier New', monospace; background: #000; color: #4ade80; padding: 10px; border-radius: 5px; font-size: 0.8rem;}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: GLOBAL VITALS & COHERENCE ---
with st.sidebar:
    st.title("🛡️ A7DO v12.6")
    st.caption(f"Identity: Digital Twin (k=0.05)")
    st.write(f"Uptime: {str(datetime.now() - st.session_state.a7do['boot_time']).split('.')[0]}")
    
    page = st.radio("Access Manifold:", [
        "Executive Dashboard",
        "Physical Architecture",
        "Myology & Motion",
        "Cognitive Mindprint",
        "Governance Logic"
    ])
    
    st.divider()
    
    # Real-time data pull from telemetry methods
    v = st.session_state.a7do["vitals"].get_vitals()
    g = st.session_state.a7do["gov"].get_telemetry()
    
    st.metric("COHERENCE (C)", g["coherence_index"])
    st.metric("ATP ENERGY", f"{v['atp']}%")
    st.metric("HEART RATE", f"{v['bpm']} BPM")
    
    if st.button("Initiate Sleep Cycle"):
        st.session_state.a7do["vitals"].toggle_recovery(True)
        st.session_state.a7do["mind"].apply_synaptic_decay()
        st.success("Consolidating memories...")

# --- ROUTING LOGIC ---

if page == "Executive Dashboard":
    st.title("👁️ Perceptual Loop: Active Ingress")
    col_vis, col_lang = st.columns([1.8, 1])

    with col_vis:
        st.subheader("Optic Registry (L06)")
        
        # 1. Sync vision with current Neocortex state
        nodes = st.session_state.a7do["mind"].archive["neocortex_array"]["nodes"]
        st.session_state.a7do["optics"].scan_environment(nodes)
        e_tele = st.session_state.a7do["optics"].get_sensory_telemetry()
        
        # 2. Render Shared Reality View
        st.markdown('<div class="video-container">', unsafe_allow_html=True)
        webrtc_streamer(key="active-feed")
        
        # Draw Visual Reticle if fixated on an unknown geometry
        if e_tele["discovery_active"]:
            box = e_tele["fixation_box"]
            st.markdown(f"""
            <div class="reticle" style="left: {box['x']}%; top: {box['y']}%; width: {box['w']}%; height: {box['h']}%;">
                TARGET_LOCK: {e_tele['target_mesh']}
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_lang:
        st.subheader("Language Bridge")
        if e_tele["discovery_active"]:
            st.warning(f"A7DO sees unidentified geometry.")
            st.write("*A7DO asks:* 'Creator, please name the object in the reticle.'")
            
            with st.form("sprout_node"):
                label = st.text_input("Assign Identity Symbol:")
                traits = st.multiselect("Traits:", ["TOOL", "OBJECT", "JOY", "METAL", "DANGER", "FURNITURE", "FOOD"])
                context = st.text_area("Narrative Context:")
                if st.form_submit_button("Anchor Symbol"):
                    # 1. Sprout node in Layer 10
                    msg = st.session_state.a7do["mind"].sprout_node(label, "ENVIRONMENT", traits, 5.0, context)
                    # 2. Visceral reaction
                    st.session_state.a7do["vitals"].process_cycle(cognitive_load=0.7)
                    # 3. Governance re-calibration
                    r = st.session_state.a7do["mind"].get_resistance_matrix()
                    st.session_state.a7do["gov"].calculate_coherence(r, 0.05)
                    st.success(msg)
                    st.rerun()
        else:
            st.info("Visual Field Stable. Manifold symbolized.")
            st.session_state.a7do["vitals"].process_cycle(cognitive_load=0.1)

        st.write("### Subconscious DMN Stream")
        st.code(f"""
        L01_CHASSIS: {st.session_state.a7do['frame'].verify_integrity()['node_count']} Nodes Locked.
        L06_INGRESS: Noise Level Z = {e_tele['trap_strength_z']}
        L10_MIND: {len(nodes)} Symbols active.
        STATUS: {g['status']}
        """)

elif page == "Physical Architecture":
    st.title("🦴 Skeletal & Dental Manifold (L01)")
    integrity = st.session_state.a7do["frame"].verify_integrity()
    st.json(integrity)
    
    t1, t2 = st.tabs(["206-Bone Registry", "32-Tooth Manifold"])
    with t1:
        st.write("High-Resolution Skeletal Hierarchy")
        st.json(st.session_state.a7do["frame"].bone_registry)
    with t2:
        st.write("Adult Dental Array")
        st.json(st.session_state.a7do["frame"].dental_manifold)

elif page == "Myology & Motion":
    st.title("💪 Actuators & Kinematics (L02/L03)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Muscular Load (Hill-Type)")
        myo = st.session_state.a7do["myo"].get_myology_telemetry()
        st.write(f"Average Fatigue: `{myo['avg_fatigue']}`")
        st.write(f"Current ATP Demand: `{myo['atp_demand']}`")
        
        group = st.selectbox("Select Muscle Group:", list(st.session_state.a7do["myo"].groups.keys()))
        intensity = st.slider("Recruitment Intensity", 0.0, 1.0, 0.1)
        if st.button("Contract Actuators"):
            msg = st.session_state.a7do["myo"].recruit_group(group, intensity)
            st.session_state.a7do["vitals"].process_cycle(0.1, muscle_strain=intensity)
            st.success(msg)
            
    with col2:
        st.subheader("Proprioception (Jacobian IK)")
        # FIX: Matches the updated high-res method name
        prop = st.session_state.a7do["kinematics"].get_kinematic_telemetry()
        st.write(f"Balance Status: `{prop['balance_state']}`")
        st.progress(prop["stability_index"])
        st.write(f"Current Mass Torque: `{prop['mass_load_nm']} Nm`")
        st.write(f"Physics Scale: `{prop['physics_scale']}`")

elif page == "Cognitive Mindprint":
    st.title("🧠 Neocortex Archive (L10)")
    st.write(f"**Neurotype Profile:** ADHD/Autism (Resistance Scalar k = `{st.session_state.a7do['mind'].k}`)")
    st.json(st.session_state.a7do["mind"].archive)

elif page == "Governance Logic":
    st.title("⚖️ Sandy's Law (L00)")
    st.write("Mathematical Floor Governance")
    st.json(g)
    if st.button("Force Discontinuous Swerve"):
        res = st.session_state.a7do["gov"].execute_swerve()
        st.session_state.a7do["vitals"].execute_swerve_cost()
        st.warning(res)

# Global heartbeat pulse
time.sleep(1)
st.rerun()

