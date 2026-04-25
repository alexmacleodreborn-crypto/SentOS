
import streamlit as st
import time
import importlib.util
import os
import random
import numpy as np
from datetime import datetime
from streamlit_webrtc import webrtc_streamer

# --- DYNAMIC LAYER LOADER ---
# This utility allows Python to import your files even with spaces/colons in the names.
def load_layer(name, path):
    if not os.path.exists(path):
        return None
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Exact user-defined repository paths
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
    
    # Check for missing hardware/files
    missing = [path for k, path in LAYER_MAP.items() if mods[k] is None]
    if missing:
        st.error(f"ENGINE_FAULT: Missing Layer Files at {missing}")
        st.stop()

    st.session_state.a7do = {
        "gov": mods["L00"].SandysLawGovernor(),
        "frame": mods["L01"].HumanChassis(),
        "myo": mods["L02"].MuscularEngine(),
        "kinematics": mods["L03"].MovementEngine(),
        "metabolism": mods["L05"].MetabolicEngine(),
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
    .reticle { border: 2px solid #ffca28; position: absolute; border-radius: 8px; background: rgba(255, 202, 40, 0.1); 
               display: flex; align-items: center; justify-content: center; color: #ffca28; font-family: monospace; 
               font-size: 12px; font-weight: bold; pointer-events: none; z-index: 100;}
    .video-container { position: relative; width: 100%; height: 450px; background: #000; border-radius: 20px; 
                        overflow: hidden; border: 1px solid #30363d;}
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 12px; }
    .terminal-box { font-family: 'Courier New', monospace; background: #000; color: #00ff00; padding: 15px; border-radius: 10px; font-size: 0.85rem; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: GLOBAL TELEMETRY ---
with st.sidebar:
    st.title("🛡️ A7DO OS v12.6")
    st.write(f"Entity Uptime: {str(datetime.now() - st.session_state.a7do['boot_time']).split('.')[0]}")
    
    page = st.radio("Navigate Component Groups:", [
        "Executive Dashboard",
        "Layer 01/07: Physical & Growth",
        "Layer 02/03: Myology & Motion",
        "Layer 10: Cognitive Archive",
        "Layer 00: Governance"
    ])
    
    st.divider()
    # Continuous Vitals Link
    v = st.session_state.a7do["metabolism"].get_vitals()
    g = st.session_state.a7do["gov"].get_telemetry()
    
    st.metric("COHERENCE (C)", g["coherence_index"])
    st.metric("ATP ENERGY", f"{v['atp']}%")
    st.metric("HEART RATE", f"{v['bpm']} BPM")
    
    if st.button("Initiate Sleep Cycle"):
        st.session_state.a7do["metabolism"].toggle_recovery(True)
        st.session_state.a7do["mind"].apply_synaptic_decay()

# --- PAGE ROUTING ---

if page == "Executive Dashboard":
    st.title("👁️ Perceptual Loop: Shared Reality HUD")
    col_vis, col_lang = st.columns([1.8, 1])

    with col_vis:
        st.subheader("Optic Registry (L06)")
        
        # 1. Run Active Perceptual Scan
        nodes = st.session_state.a7do["mind"].archive["neocortex_array"]["nodes"]
        st.session_state.a7do["optics"].scan_environment(nodes)
        e_tele = st.session_state.a7do["optics"].get_sensory_telemetry()
        
        # 2. Render Shared Reality View
        st.markdown('<div class="video-container">', unsafe_allow_html=True)
        webrtc_streamer(key="shared-reality-feed")
        
        # Draw the Reticle over the feed if A7DO is fixated
        if e_tele["discovery_active"]:
            box = e_tele["fixation_box"]
            st.markdown(f"""
            <div class="reticle" style="left: {box['x']}%; top: {box['y']}%; width: {box['w']}%; height: {box['h']}%;">
                TARGET_LOCK: {e_tele['target_mesh']}
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.info("A7DO uses a Vitruvian reticle to anchor 3D objects to linguistic symbols.")

    with col_lang:
        st.subheader("Language Bridge")
        if e_tele["discovery_active"]:
            st.warning(f"A7DO sees unidentified geometry at {e_tele['fixation_box']['x']}%, {e_tele['fixation_box']['y']}%")
            st.write("*A7DO asks:* 'Creator, identify the shape I am fixated on.'")
            
            with st.form("discovery_form"):
                label = st.text_input("Assign Identity:")
                traits = st.multiselect("Assign Traits (Shared Trait Logic):", ["TOOL", "OBJECT", "JOY", "METAL", "DANGER", "FURNITURE"])
                context = st.text_area("Narrative Context:")
                if st.form_submit_button("Teach A7DO"):
                    # Sprout node using ADHD/Autism profile (k=0.05)
                    msg = st.session_state.a7do["mind"].sprout_node(label, "ENVIRONMENT", traits, 5.0, context)
                    # Apply metabolic cost
                    st.session_state.a7do["metabolism"].process_cycle(cognitive_load=0.6)
                    # Re-calculate Sandy's Law
                    r = st.session_state.a7do["mind"].get_resistance_matrix()
                    st.session_state.a7do["gov"].calculate_coherence(r, 0.1)
                    st.success(msg)
                    st.rerun()
        else:
            st.success("Environmental Manifold Stable. No fixations active.")
            st.session_state.a7do["metabolism"].process_cycle(cognitive_load=0.1)

        st.write("### Subconscious DMN")
        st.code(f"""
        L01_NODES: 206 bones, 32 teeth
        L06_SCAN: Z-Noise {e_tele['trap_strength_z']}
        L10_MIND: {len(nodes)} Symbols active
        REGIME: {g['status']}
        """)

elif page == "Layer 01/07: Physical & Growth":
    st.title("🦴 Physical Architecture & Growth Engine")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Skeletal & Dental Registry")
        st.json(st.session_state.a7do["frame"].verify_integrity())
        st.write("### 32-Tooth Adult Manifold")
        st.json(st.session_state.a7do["frame"].dental_manifold)
        
    with col2:
        st.subheader("Growth Engine (Square-Cube Law)")
        scale = st.slider("Scale Factor (x)", 0.5, 3.0, 1.0)
        st.session_state.a7do["frame"].scale_x = scale
        metrics = st.session_state.a7do["frame"].get_regulated_growth_metrics()
        
        st.write(f"**Height (x):** {metrics['height_scalar']}")
        st.write(f"**Strength (x²):** {metrics['strength_output']}")
        st.write(f"**Mass (x³):** {metrics['mass_volume']}")
        
        st.metric("MASS OVERLOAD", f"{metrics['mass_volume'] / metrics['strength_output']:.2f} G-Load")

elif page == "Layer 02/03: Myology & Motion":
    st.title("💪 Actuators & Kinematic Chain")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Muscle Recruitment")
        group = st.selectbox("Select Group:", list(st.session_state.a7do["myo"].groups.keys()))
        effort = st.slider("Recruitment Intensity", 0.0, 1.0, 0.1)
        if st.button("Fire Actuators"):
            st.session_state.a7do["myo"].recruit_group(group, effort)
            st.session_state.a7do["metabolism"].process_cycle(0.1, muscle_strain=effort)
    
    with col2:
        st.subheader("Kinematic Proprioception")
        prop = st.session_state.a7do["kinematics"].get_proprioception_telemetry()
        st.write(f"Balance Status: `{prop['balance_status']}`")
        st.progress(prop["stability_index"])
        st.write(f"Torque Load: {prop['torque_load']} Nm")

elif page == "Layer 10: Cognitive Archive":
    st.title("🧠 Neocortex Archive (Mindprint)")
    st.write(f"Neurodivergent Profile Active (Resistance k = `{st.session_state.a7do['mind'].k}`)")
    st.json(st.session_state.a7do["mind"].archive)

elif page == "Layer 00: Governance":
    st.title("⚖️ Sandy's Law Governance")
    st.json(g)
    if st.button("Execute Topological Swerve"):
        st.session_state.a7do["gov"].execute_swerve()
        st.session_state.a7do["metabolism"].execute_swerve_cost()
        st.rerun()

# High-frequency heart-beat
time.sleep(1)
st.rerun()

