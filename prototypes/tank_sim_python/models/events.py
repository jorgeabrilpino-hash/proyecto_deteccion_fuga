from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TankSample:
    timestamp_s: int
    cycle_id: int
    level_pct: float
    pressure_kpa: float
    flow_left_lpm: float
    flow_right_lpm: float
    leak_score: float


@dataclass
class Anomaly:
    timestamp_s: int
    cycle_id: int
    kind: str
    severity: str
    value: float
    message: str


@dataclass
class Alert:
    severity: str
    message: str
    timestamp_s: int
