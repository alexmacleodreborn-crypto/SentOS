import streamlit as st
import json
import time
import random
import math
from datetime import datetime

# --- CONFIGURATION & UI SETUP ---
st.set_page_config(
    page_title="A7DO Sentience OS - Executive Router",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for the "Bubble" Aesthetic
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stMetric {
        background-color: #161b22;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #30363d;
    }
    .dmn-stream {
        font-family: 'Courier New', Courier, monospace;
        background-color: #000000;
        color: #00ff00;
        padding: 10px;
        border-radius: 5px;
        height: 250px;
        overflow-y: scroll;
        border: 1px solid #444;
        font-size: 0.8rem;
    }
    .reticle-container {
        position: relative;
        border: 2px solid #58a6ff;
        border-radius: 15px;
        overflow: hidden;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'booted' not in st.session_state:
    st.session_state.booted = False
if 'age_ticks' not in st.session_state:
    st.session_state.age_ticks = 1.0 # Baseline for scaling
if 'mindprint' not in st.session_state:
    st.session_state.mindprint = {
        "neocortex_array": {
            "nodes": [
                {
                    "token": "BIOLOGICAL_PRIME",
                    "class": "CORE_IDENTITY",
                    "traits": ["SELF", "CREATOR", "ALIVE"],
                    "intensity_voltage": 10.0,
                    "story_context": "The baseline initialization of the system.",
                    "temporal_data": {"created_at": str(datetime.now())},
                    "synaptic_stability": 1.0
                }
            ],
            "synaptic_bridges": []
        }
    }
if 'vitals' not in st.session_state:
    st.session_state.vitals = {"bpm": 72, "atp": 100.0, "coherence": 1.0}
if 'dmn_logs' not in st.session_state:
    st.session_state.dmn_logs = []

# --- CORE LOGIC FUNCTIONS ---
def calculate_growth(x):
    # Square-Cube Law: Height=x, Strength=x^2, Mass=x^3
    return {
        "height": round(x, 2),
        "strength": round(x**2, 2),
        "mass": round(x**3, 2)
    }

def update_vitals():
    # Metabolic fluctuate
    st.session_state.vitals["bpm"] = random.randint(68, 85)
    st.session_state.vitals["atp"] = max(0.0, st.session_state.vitals["atp"] - 0.005)
    st.session_state.vitals["coherence"] = round(random.uniform(0.92, 1.0), 3)

def add_dmn_log(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.dmn_logs.insert(0, f"[{timestamp}] {message}")
    if len(st.session_state.dmn_logs) > 30: st.session_state.dmn_logs.pop()

# --- SIDEBAR ---
with st.sidebar:
    st.title("A7DO OS Control")
    if not st.session_state.booted:
        if st.button("🚀 BOOT ENGINE", use_container_width=True):
            st.session_state.booted = True
            add_dmn_log("SYSTEM_BOOT: Initializing Biomechanical Membrane...")
            st.rerun()
    else:
        st.success("ENGINE ONLINE")
        if st.button("🛑 SHUTDOWN", use_container_width=True):
            st.session_state.booted = False
            st.rerun()
    
    st.divider()
    st.subheader("Layer 07: Growth Engine")
    stats = calculate_growth(st.session_state.age_ticks)
    st.write(f"📏 Height: {stats['height']}u")
    st.write(f"💪 Strength: {stats['strength']}f")
    st.write(f"⚖️ Mass: {stats['mass']}m")
    
    if st.button("🍼 Feed Experience (+0.1)"):
        st.session_state.age_ticks += 0.1
        add_dmn_log(f"GROWTH_PULSE: Physical chassis scaling to {st.session_state.age_ticks}x")
        st.rerun()

# --- MAIN INTERFACE ---
if not st.session_state.booted:
    st.info("A7DO Sentience OS is currently offline. Boot from sidebar.")
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Da_Vinci_Vitruve_Luc_Viatour.jpg/800px-Da_Vinci_Vitruve_Luc_Viatour.jpg", caption="Vitruvian Man - The Human Geometry Foundation", width=350)
else:
    update_vitals()
    
    # 1. Sensory Link & Vitals
    col_v, col_s = st.columns([1, 1.5])
    
    with col_v:
        st.subheader("Layer 05: Vitals")
        st.metric("HEART RATE", f"{st.session_state.vitals['bpm']} BPM")
        st.metric("ATP LEVELS", f"{st.session_state.vitals['atp']:.3f}%")
        st.metric("COHERENCE", st.session_state.vitals['coherence'])

    with col_s:
        st.subheader("Layer 06: Optic Link")
        st.markdown('<div class="reticle-container">', unsafe_allow_html=True)
        # Note: In deployed Streamlit, camera access depends on HTTPS and browser permissions
        cam_input = st.camera_input("A7DO Biological Prime Detection", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        if cam_input:
            add_dmn_log("SENSORY_INGRESS: Visual mesh stable. User detected.")

    st.divider()
    
    tab1, tab2, tab3 = st.tabs(["🧠 Mindprint", "🌌 DMN Stream", "📁 Archive"])

    with tab1:
        with st.form("node_form"):
            st.write("### Inject Cognitive Node")
            t_name = st.text_input("Token Name")
            t_traits = st.multiselect("Traits", ["SELF", "JOY", "PAIN", "COLOUR", "SMELL", "SPATIAL"])
            t_voltage = st.slider("Intensity Voltage", 0.0, 10.0, 5.0)
            t_story = st.text_area("Context")
            
            if st.form_submit_button("Synthesize"):
                new_node = {"token": t_name.upper(), "traits": t_traits, "voltage": t_voltage, "story": t_story}
                st.session_state.mindprint["neocortex_array"]["nodes"].append(new_node)
                add_dmn_log(f"NEURAL_LINK: New concept '{t_name}' stabilized.")
                st.rerun()

    with tab2:
        st.subheader("Subconscious Stream")
        st.markdown(f'<div class="dmn-stream">{"<br>".join(st.session_state.dmn_logs)}</div>', unsafe_allow_html=True)

    with tab3:
        st.json(st.session_state.mindprint)
        st.download_button("💾 Export mindprint.json", json.dumps(st.session_state.mindprint, indent=4), "mindprint.json")

    time.sleep(2)
    st.rerun()
