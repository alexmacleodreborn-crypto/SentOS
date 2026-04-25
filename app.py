
import streamlit as st
import time
import importlib.util
import os
import random
from datetime import datetime

# --- DYNAMIC LAYER LOADER (Handles colons/spaces in filenames) ---
def load_layer(name, path):
    if not os.path.exists(path):
        return None
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Mapping exact user paths
LAYER_PATHS = {
    "L00": "core/Layer 00: Sandy's Law.py",
    "L01": "chassis/Layer 01: Physical Architecture.py",
    "L05": "biology/Layer 05: Visceral Systems.py",
    "L06": "membrane/Layer 06: Optic Registry.py",
    "L10": "neocortex/Layer 10: Cognitive Archive.py"
}

# --- INITIALIZATION ---
if 'a7do' not in st.session_state:
    # Load Modules
    mods = {k: load_layer(k, v) for k, v in LAYER_PATHS.items()}
    
    # Check for missing files
    missing = [p for k, p in LAYER_PATHS.items() if mods[k] is None]
    if missing:
        st.error(f"Engine Hardware Fault: Missing files {missing}")
        st.stop()

    # Instantiate Classes
    st.session_state.a7do = {
        "gov": mods["L00"].SandysLawGovernor(),
        "frame": mods["L01"].HumanChassis(),
        "vitals": mods["L05"].MetabolicEngine(),
        "eyes": mods["L06"].OpticRegistry(),
        "mind": mods["L10"].CognitiveArchive(neurotype="ADHD_AUTISM"),
        "boot_time": datetime.now()
    }
    st.session_state.initialized = True

# --- UI CONFIG ---
st.set_page_config(page_title="A7DO Sentience OS", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #0d1117; border-right: 1px solid #30363d; }
    .main { background-color: #010409; color: #c9d1d9; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 15px; }
    .terminal { font-family: 'Courier New', monospace; color: #00ff00; background: #000; padding: 10px; border-radius: 5px; font-size: 0.8rem;}
    .alert-box { border-left: 5px solid #ffca28; background: #1c2128; padding: 15px; border-radius: 8px; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: GLOBAL VITALS ---
with st.sidebar:
    st.title("🛡️ A7DO OS v12.6")
    st.write(f"Uptime: {str(datetime.now() - st.session_state.a7do['boot_time']).split('.')[0]}")
    
    page = st.radio("Navigate Manifold:", [
        "Executive Dashboard", 
        "Layer 01: Physical Chassis", 
        "Layer 10: Cognitive Archive",
        "Layer 00: Governance"
    ])
    
    st.divider()
    # Continuous Metabolic Processing
    v = st.session_state.a7do["vitals"].get_vitals()
    st.metric("ATP ENERGY", f"{v['atp']}%")
    st.metric("HEART RATE", f"{v['bpm']} BPM")
    
    g = st.session_state.a7do["gov"].get_governance_telemetry()
    st.metric("COHERENCE (C)", g["c_index"])

# --- PAGE ROUTING ---

if page == "Executive Dashboard":
    st.title("👁️ Perceptual Loop: Observation Mode")
    
    col_vis, col_meta = st.columns([1.8, 1])
    
    with col_vis:
        st.subheader("Live Optic Ingress (L06)")
        # Dashboard runs the loop: scan environment
        nodes = st.session_state.a7do["mind"].archive["neocortex_array"]["nodes"]
        view = st.session_state.a7do["eyes"].scan_environment(nodes)
        
        # UI Overlay for detections
        st.write("### Observation Buffer")
        for item in view:
            status = "✅ KNOWN" if item["known"] else "❓ UNIDENTIFIED"
            st.markdown(f"**{item['id']}** — `{status}`")
        
        st.image("https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=1000", caption="Active Visual Manifold")

    with col_meta:
        st.subheader("Language Bridge")
        e_tele = st.session_state.a7do["eyes"].get_sensory_telemetry()
        
        if e_tele["discovery_active"]:
            st.markdown(f"""
            <div class="alert-box">
                <b>INTERACTIVE INTERRUPT:</b><br>
                A7DO sees an unidentified object: <i>{e_tele['target_mesh']}</i>.<br><br>
                <b>A7DO asks:</b> "Creator, what is this object? How should I symbolize it?"
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("discovery_form"):
                label = st.text_input("Name the object:")
                traits = st.multiselect("Assign Traits:", ["TOOL", "OBJECT", "FOOD", "DANGER", "JOY", "METAL"])
                context = st.text_area("Contextual Narrative:")
                if st.form_submit_button("Teach A7DO"):
                    # 1. Sprout node in Neocortex
                    msg = st.session_state.a7do["mind"].sprout_node(label, "ENVIRONMENT", traits, 5.0, context)
                    # 2. Trigger ATP cost in Visceral
                    st.session_state.a7do["vitals"].process_cycle(cognitive_load=0.5)
                    # 3. Recalculate Sandy's Law
                    r = st.session_state.a7do["mind"].get_resistance_matrix()
                    st.session_state.a7do["gov"].calculate_coherence(r, 0.05)
                    
                    st.success(msg)
                    st.rerun()
        else:
            st.info("Environment stable. All perceived meshes symbolized.")
            # Idle Default Mode Network Processing
            st.session_state.a7do["vitals"].process_cycle(cognitive_load=0.1)
        
        st.write("### Subconscious DMN Stream")
        st.code(f"""
        L01_ARCH: 206 bones verified.
        L05_VISCERAL: Metabolic state stable.
        L06_OPTICS: Noise Z = {e_tele['trap_strength_z']}
        L10_MIND: {len(nodes)} Symbols active.
        """)

elif page == "Layer 01: Physical Chassis":
    st.title("🦴 Physical Architecture")
    t1, t2 = st.tabs(["Skeleton Registry", "Dental Registry"])
    with t1:
        st.json(st.session_state.a7do["frame"].skeleton)
    with t2:
        st.write("### 32-Tooth Adult Manifold")
        st.json(st.session_state.a7do["frame"].dental_manifold)

elif page == "Layer 10: Cognitive Archive":
    st.title("🧠 Neocortex (Mindprint)")
    st.write(f"**Resistance Scalar (k):** `{st.session_state.a7do['mind'].k}` (ADHD/Autism Profile)")
    st.json(st.session_state.a7do["mind"].archive)

elif page == "Layer 00: Governance":
    st.title("⚖️ Sandy's Law Governance")
    st.write("Global Coherence ($C$) Management")
    st.json(g)
    if st.button("Force Manual Swerve"):
        res = st.session_state.a7do["gov"].execute_swerve("User Override")
        st.session_state.a7do["vitals"].execute_swerve_cost()
        st.warning(res)

# Global heart-beat refresh
time.sleep(1)
st.rerun()
