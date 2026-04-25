from __future__ import annotations

import pandas as pd
import streamlit as st

from detection.rules import detect_anomalies
from simulator.engine import run_simulation

st.set_page_config(page_title="Tank Leak Prototype", layout="wide")
st.title("Tank Leak Prototype")

samples = run_simulation()
anomalies = detect_anomalies(samples)

df = pd.DataFrame([sample.__dict__ for sample in samples])
st.line_chart(df.set_index("timestamp_s")[["pressure_kpa", "level_pct", "leak_score"]])
st.subheader("Anomalías")
st.dataframe(pd.DataFrame([anomaly.__dict__ for anomaly in anomalies]))
