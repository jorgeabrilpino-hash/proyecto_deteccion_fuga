from __future__ import annotations

from models.events import Anomaly, TankSample


def detect_anomalies(samples: list[TankSample]) -> list[Anomaly]:
    anomalies: list[Anomaly] = []

    for sample in samples:
        if sample.pressure_kpa < 35:
            anomalies.append(
                Anomaly(
                    timestamp_s=sample.timestamp_s,
                    cycle_id=sample.cycle_id,
                    kind="pressure_drop",
                    severity="high",
                    value=sample.pressure_kpa,
                    message="Caída anómala de presión detectada",
                )
            )

        if sample.leak_score > 0.7:
            anomalies.append(
                Anomaly(
                    timestamp_s=sample.timestamp_s,
                    cycle_id=sample.cycle_id,
                    kind="possible_leak",
                    severity="critical",
                    value=sample.leak_score,
                    message="Posible fuga detectada por comportamiento anómalo",
                )
            )

    return anomalies
