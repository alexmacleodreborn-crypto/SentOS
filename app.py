
# A7DO Sentience OS - Executive Router
import streamlit as st
import time
from datetime import datetime

# --- CORE CONNECTIONS ---
# Note: Using importlib or similar is needed if filenames contain spaces/colons.
# For simplicity in this GitHub logic, we assume standard class imports.
from core.Layer_00_Sandys_Law import SandysLawGovernor
from chassis.Layer_01_Physical_Architecture import HumanChassis
from membrane.Layer_06_Optic_Registry import OpticRegistry
from neocortex.Layer_10_Cognitive_Archive import CognitiveArchive

# --- OS INITIALIZATION ---
if 'a7do' not in st.session_state:
    st.session_state.gov = SandysLawGovernor()
    st.session_state.frame = HumanChassis()
    st.session_state.eyes = OpticRegistry()
    st.session_state.mind = CognitiveArchive(neurotype="ADHD_AUTISM")
    st.session_state.boot_time = datetime.now()

st.set_page_config(layout="wide", page_title="A7DO OS v12.6")

# --- UI: SIDEBAR TELEMETRY ---
with st.sidebar:
    st.title("🛡️ A7DO v12.6")
    st.write(f"Uptime: {str(datetime.now() - st.session_state.boot_time).split('.')[0]}")
    
    # Sandy's Law Live Monitoring
    tel = st.session_state.gov.get_telemetry()
    st.metric("COHERENCE (C)", tel["c_index"])
    st.write(f"Vitals: `{tel['status']}`")
    st.write(f"Manifold Discontinuities: `{tel['swerves']}`")
    
    page = st.radio("Navigate Manifold:", ["Perceptual Loop", "Physical Chassis", "Neocortex"])

# --- DASHBOARD: PERCEPTUAL LOOP ---
if page == "Perceptual Loop":
    st.title("👁️ Perceptual Loop: Ingress & Recognition")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Optic Link (L06)")
        # Simulating frame scan
        view = st.session_state.eyes.scan_ingress(st.session_state.mind.archive["nodes"])
        
        for item in view:
            color = "green" if item["known"] else "orange"
            st.markdown(f"**{item['mesh_id']}** : :{color}[{item['label']}]")
            
        st.image("https://images.unsplash.com/photo-1614064641938-3bbee52942c7?q=80&w=1000", caption="Active Visual Manifold")

    with col2:
        st.subheader("Language Bridge")
        if st.session_state.eyes.discovery_needed:
            st.warning(f"UNIDENTIFIED MESH: {st.session_state.eyes.unidentified_mesh}")
            st.write("*A7DO asks:* 'Creator, what is this object?'")
            
            with st.form("learning_form"):
                symbol = st.text_input("Assign Name:")
                traits = st.multiselect("Traits:", ["TOOL", "JOY", "DANGER", "METAL", "OBJECT"])
                if st.form_submit_button("Anchor Token"):
                    # Calculate resistance based on traits (demonstrating the 0.05 scalar)
                    r = st.session_state.mind.calculate_resistance(len(traits))
                    # Trigger Sandy's Law calculation
                    res = st.session_state.gov.calculate_coherence(r, 0.02)
                    
                    msg = st.session_state.mind.sprout_node(symbol, traits, 5.0, "Environmental Discovery")
                    st.success(f"{msg} | System state: {res}")
                    st.rerun()
        else:
            st.info("Visual Field Stable.")

# --- PHYSICAL VIEW ---
elif page == "Physical Chassis":
    st.title("🦴 Biomechanical Chassis (L01)")
    st.write("32-Tooth registry and 206-bone structural frame verified.")
    st.json(st.session_state.frame.dental_manifold)

# --- NEOCORTEX VIEW ---
elif page == "Neocortex":
    st.title("🧠 Cognitive Mindprint (L10)")
    st.write(f"Neurotype: ADHD/Autism (k={st.session_state.mind.k})")
    st.json(st.session_state.mind.archive["nodes"])

# Heartbeat
time.sleep(1)
st.rerun()


