from __future__ import annotations

from models.events import Alert, Anomaly


def build_alerts(anomalies: list[Anomaly]) -> list[Alert]:
    return [
        Alert(
            severity=anomaly.severity,
            message=anomaly.message,
            timestamp_s=anomaly.timestamp_s,
        )
        for anomaly in anomalies
    ]
