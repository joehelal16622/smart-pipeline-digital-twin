import streamlit as st
import pandas as pd
import plotly.express as px

from model import simulate_pipeline


st.set_page_config(
    page_title="Smart Pipeline Digital Twin",
    layout="wide"
)

st.title("Smart Pipeline Elbow Digital Twin")

st.write(
    """
    Interactive physics-based digital twin for a 90-degree steel pipeline elbow
    subjected to pressure surge, thermal expansion, and fatigue loading.
    """
)

# ============================================================
# SIDEBAR INPUTS
# ============================================================

st.sidebar.header("Simulation Inputs")

t_wall_mm = st.sidebar.slider(
    "Pipe wall thickness (mm)",
    min_value=4.0,
    max_value=20.0,
    value=12.0,
    step=0.5
)

closure_duration = st.sidebar.slider(
    "Valve closure time (s)",
    min_value=0.2,
    max_value=8.0,
    value=2.0,
    step=0.1
)

delta_T = st.sidebar.slider(
    "Temperature rise (°C)",
    min_value=0.0,
    max_value=100.0,
    value=30.0,
    step=5.0
)

Kt = st.sidebar.slider(
    "Elbow stress concentration factor",
    min_value=1.0,
    max_value=3.0,
    value=1.5,
    step=0.1
)

P0_MPa = st.sidebar.slider(
    "Operating pressure (MPa)",
    min_value=0.5,
    max_value=5.0,
    value=2.0,
    step=0.1
)

Q0 = st.sidebar.slider(
    "Flow rate (m³/s)",
    min_value=0.02,
    max_value=0.30,
    value=0.10,
    step=0.01
)

# Convert wall thickness from mm to m
t_wall = t_wall_mm / 1000

# Convert pressure from MPa to Pa
P0 = P0_MPa * 1e6


# ============================================================
# RUN SIMULATION
# ============================================================

data, metrics = simulate_pipeline(
    t_wall=t_wall,
    closure_duration=closure_duration,
    delta_T=delta_T,
    Kt=Kt,
    P0=P0,
    Q0=Q0
)


# ============================================================
# TOP METRICS
# ============================================================

st.subheader("Digital Twin Health Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Max Pressure",
    f"{metrics['Max Pressure (MPa)']:.2f} MPa"
)

col2.metric(
    "Max von Mises Stress",
    f"{metrics['Max von Mises Stress (MPa)']:.1f} MPa"
)

col3.metric(
    "Factor of Safety",
    f"{metrics['Factor of Safety']:.2f}"
)

col4.metric(
    "Risk Level",
    metrics["Risk Level"]
)

if metrics["Risk Level"] == "Critical":
    st.error("Critical risk: the simulated elbow is operating in an unsafe stress region.")
elif metrics["Risk Level"] == "Warning":
    st.warning("Warning: the simulated elbow is close to or below the desired design margin.")
elif metrics["Risk Level"] == "Monitor":
    st.info("Monitor: stresses are elevated but not immediately critical.")
else:
    st.success("Safe: the simulated elbow remains within the defined safety limits.")


# ============================================================
# INTERACTIVE GRAPHS
# ============================================================

st.subheader("Live Simulation Outputs")

fig_pressure = px.line(
    data,
    x="Time (s)",
    y="Pressure (MPa)",
    title="Internal Pressure Response"
)

st.plotly_chart(fig_pressure, use_container_width=True)


fig_stress = px.line(
    data,
    x="Time (s)",
    y=[
        "Hoop Stress (MPa)",
        "Longitudinal Stress (MPa)",
        "von Mises Stress (MPa)"
    ],
    title="Pipeline Elbow Stress Response"
)

st.plotly_chart(fig_stress, use_container_width=True)


fig_damage = px.line(
    data,
    x="Time (s)",
    y="Fatigue Damage",
    title="Accumulated Fatigue Damage"
)

st.plotly_chart(fig_damage, use_container_width=True)


fig_health = px.line(
    data,
    x="Time (s)",
    y="Health Index (%)",
    title="Health Index Over Time"
)

st.plotly_chart(fig_health, use_container_width=True)


# ============================================================
# ENGINEERING DETAILS
# ============================================================

st.subheader("Engineering Interpretation")

st.write(
    f"""
    For the selected conditions, the maximum von Mises stress is
    **{metrics['Max von Mises Stress (MPa)']:.1f} MPa**.

    The calculated factor of safety is **{metrics['Factor of Safety']:.2f}**.

    Static safety check: **{metrics['Static Safety Check']}**.

    Risk classification: **{metrics['Risk Level']}**.
    """
)

with st.expander("View raw simulation data"):
    st.dataframe(data, use_container_width=True)