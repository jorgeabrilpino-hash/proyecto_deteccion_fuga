from __future__ import annotations

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from dashboard.scene import build_tank_scene_html
from detection.rules import detect_anomalies
from simulator.engine import run_simulation

st.set_page_config(page_title="Tank Leak Prototype 3D", layout="wide")
st.title("Tank Leak Prototype 3D")
st.caption("Demo inicial con simulación 3D web del tanque, sensores y cámaras")

samples = run_simulation(total_cycles=4, cycle_length_s=24)
anomalies = detect_anomalies(samples)
df = pd.DataFrame([sample.__dict__ for sample in samples])

with st.sidebar:
    st.header("Control de simulación")
    selected_time = st.slider("Tiempo", min_value=int(df.timestamp_s.min()), max_value=int(df.timestamp_s.max()), value=10)
    selected_sample = df[df.timestamp_s == selected_time].iloc[0].to_dict()
    force_leak = st.toggle("Forzar fuga visual", value=bool(selected_sample["leak_score"] > 0.7))
    show_anomaly_band = st.toggle("Mostrar foco de riesgo", value=True)

sample_state = {
    "timestamp_s": int(selected_sample["timestamp_s"]),
    "cycle_id": int(selected_sample["cycle_id"]),
    "level_pct": float(selected_sample["level_pct"]),
    "pressure_kpa": float(selected_sample["pressure_kpa"]),
    "flow_left_lpm": float(selected_sample["flow_left_lpm"]),
    "flow_right_lpm": float(selected_sample["flow_right_lpm"]),
    "leak_score": float(selected_sample["leak_score"]),
    "leak_detected": bool(force_leak),
    "status_label": "Fuga detectada" if force_leak else ("Advertencia" if selected_sample["pressure_kpa"] < 35 else "Normal"),
    "show_anomaly_band": bool(show_anomaly_band),
}

left, right = st.columns([1.7, 1])
with left:
    components.html(build_tank_scene_html(sample_state), height=720)

with right:
    st.subheader("Estado actual")
    st.metric("Ciclo", sample_state["cycle_id"])
    st.metric("Nivel", f"{sample_state['level_pct']}%")
    st.metric("Presión", f"{sample_state['pressure_kpa']} kPa")
    st.metric("Flujo izquierdo", f"{sample_state['flow_left_lpm']} L/min")
    st.metric("Flujo derecho", f"{sample_state['flow_right_lpm']} L/min")
    st.metric("Leak score", sample_state["leak_score"])
    st.write("El modelo 3D representa el tanque, el líquido, las tuberías laterales, un sensor superior de presión y dos cámaras externas.")

st.subheader("Curvas del prototipo")
st.line_chart(df.set_index("timestamp_s")[["pressure_kpa", "level_pct", "leak_score"]])

st.subheader("Anomalías detectadas")
st.dataframe(pd.DataFrame([anomaly.__dict__ for anomaly in anomalies]), use_container_width=True)
