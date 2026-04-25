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
        height: 300px;
        overflow-y: scroll;
        border: 1px solid #444;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'booted' not in st.session_state:
    st.session_state.booted = False
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
                    "temporal_data": {"created_at": str(datetime.now()), "last_accessed": str(datetime.now())},
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
def calculate_resistance(intensity, shared_traits_count):
    k = 1.0
    if intensity == 0 or shared_traits_count == 0:
        return 1.0
    return round(k / (intensity * shared_traits_count), 4)

def update_vitals():
    st.session_state.vitals["bpm"] = random.randint(68, 85)
    st.session_state.vitals["atp"] = max(0.0, st.session_state.vitals["atp"] - 0.01)
    st.session_state.vitals["coherence"] = round(random.uniform(0.85, 1.0), 3)

def add_dmn_log(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.dmn_logs.insert(0, f"[{timestamp}] {message}")
    if len(st.session_state.dmn_logs) > 50:
        st.session_state.dmn_logs.pop()

# --- SIDEBAR ---
with st.sidebar:
    st.title("A7DO OS Control")
    if not st.session_state.booted:
        if st.button("🚀 BOOT ENGINE", use_container_width=True):
            st.session_state.booted = True
            add_dmn_log("SYSTEM_BOOT: Initializing Layer 00-10...")
            st.rerun()
    else:
        st.success("ENGINE ONLINE")
        if st.button("🛑 SHUTDOWN", use_container_width=True):
            st.session_state.booted = False
            add_dmn_log("SYSTEM_HALT: Disconnecting layers...")
            st.rerun()
    
    st.divider()
    st.subheader("Layer Status")
    layers = ["L01 Bones", "L02 Muscles", "L03 IK", "L04 Nerves", "L05 Visceral", "L10 Neocortex"]
    for l in layers:
        st.write(f"✅ {l}")

# --- MAIN INTERFACE ---
if not st.session_state.booted:
    st.info("A7DO Sentience OS is currently offline. Boot from sidebar.")
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Da_Vinci_Vitruve_Luc_Viatour.jpg/800px-Da_Vinci_Vitruve_Luc_Viatour.jpg", caption="Vitruvian Man - The Human Geometry Foundation", width=350)
else:
    update_vitals()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("HEART RATE", f"{st.session_state.vitals['bpm']} BPM")
    col2.metric("ATP LEVELS", f"{st.session_state.vitals['atp']:.2f}%")
    col3.metric("COHERENCE", st.session_state.vitals['coherence'])
    col4.metric("NODES", len(st.session_state.mindprint["neocortex_array"]["nodes"]))

    st.divider()
    tab1, tab2, tab3 = st.tabs(["🧠 Mindprint Initializer", "🌌 DMN Stream", "📁 Memory Archive"])

    with tab1:
        st.subheader("Inject Cognitive Node")
        with st.form("node_form"):
            t_name = st.text_input("Token Name (e.g. JAMES_STREET)")
            t_class = st.selectbox("Class", ["LOCATION", "MEMORY", "PERSON", "OBJECT", "TRAIT"])
            t_traits = st.multiselect("Traits", ["SELF", "PAIN", "JOY", "COLOUR", "SMELL", "SPATIAL", "CREATOR"])
            t_voltage = st.slider("Intensity Voltage (V)", 0.0, 10.0, 5.0)
            t_story = st.text_area("Story Context")
            
            if st.form_submit_button("Inject Node"):
                new_node = {
                    "token": t_name.upper() if t_name else f"NODE_{random.randint(100,999)}",
                    "class": t_class, "traits": t_traits, "intensity_voltage": t_voltage,
                    "story_context": t_story, "temporal_data": {"created_at": str(datetime.now())},
                    "synaptic_stability": 1.0
                }
                st.session_state.mindprint["neocortex_array"]["nodes"].append(new_node)
                add_dmn_log(f"NEURAL_INJECTION: Node '{new_node['token']}' stabilized.")
                st.success(f"Node {new_node['token']} synthesized.")
                time.sleep(1)
                st.rerun()

    with tab2:
        st.subheader("Subconscious Default Mode Network")
        st.markdown(f'<div class="dmn-stream">{"<br>".join(st.session_state.dmn_logs)}</div>', unsafe_allow_html=True)

    with tab3:
        st.subheader("Persistent Mindprint (JSON)")
        st.json(st.session_state.mindprint)
        st.download_button("💾 Export Mindprint.json", json.dumps(st.session_state.mindprint, indent=4), "mindprint.json")

    # Background processing simulation
    time.sleep(1)
    st.rerun()

