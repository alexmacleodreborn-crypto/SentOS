import streamlit as st
import pandas as pd

# Load workbook sheets
@st.cache_data
def load_data():
    phases = pd.read_excel('A7DO DNA.xlsx', sheet_name='Prenatal Phases')
    anatomy = pd.read_excel('A7DO DNA.xlsx', sheet_name='Anatomy Growth Engine')
    tick_loop = pd.read_excel('A7DO DNA.xlsx', sheet_name='Tick-Based DNA Loop')
    organs = pd.read_excel('A7DO DNA.xlsx', sheet_name='Organ & System Activation')
    return phases, anatomy, tick_loop, organs

phases, anatomy, tick_loop, organs = load_data()

st.title("A7DO Developmental Engine")

# --- Clean tick IDs for slider ---
tick_ids = pd.to_numeric(tick_loop['Tick ID'], errors='coerce')
tick_ids = tick_ids.dropna().astype(int)
tick_ids = tick_ids.sort_values().unique()

current_tick = st.slider(
    "Simulation Tick",
    min_value=int(tick_ids.min()),
    max_value=int(tick_ids.max()),
    step=500,
    value=int(tick_ids.min())
)

# Find current phase
current_phase_row = tick_loop[tick_loop['Tick ID'] <= current_tick].iloc[-1]
current_phase = current_phase_row['DNA Phase']
current_week = current_phase_row['Week']

st.header(f"Current Phase: {current_phase} (Week {current_week})")
st.write(f"Growth Factor: {current_phase_row['Growth Factor']}, Neural Gain: {current_phase_row['Neural Gain']}, Reflex Gain: {current_phase_row['Reflex Gain']}")

# Anatomy growth table
st.subheader("Anatomy Growth Engine")
anatomy_now = anatomy[anatomy['Current Week'] <= current_week]
st.dataframe(anatomy_now[['Name', 'Category', 'DNA Code', 'Start Week', 'End Week', 'Growth Curve', 'Growth Status', 'Activation %']])

# Organ activation table
st.subheader("Organ & System Activation")
if 'an' in organs.columns:
    organs['an'] = pd.to_numeric(organs['an'], errors='coerce')
    organs_now = organs[organs['an'] <= current_week]
    st.dataframe(organs_now[['Organ/System', 'Activation Event', 'DNA Code', 'Notes']])
else:
    st.info("No 'an' column in Organ & System Activation sheet.")

# Developmental timeline
st.subheader("Prenatal Phases Timeline")
st.dataframe(phases)

# Advance simulation
if st.button("Advance Tick"):
    next_tick = min(current_tick + 500, int(tick_ids.max()))
    st.session_state['current_tick'] = next_tick
    st.experimental_rerun()

st.caption("This starter app loads your workbook, advances ticks, and displays developmental data. Expand with more sheets and features as needed!")
