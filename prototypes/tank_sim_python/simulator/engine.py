from __future__ import annotations

from models.events import TankSample


def run_simulation(total_cycles: int = 3, cycle_length_s: int = 20) -> list[TankSample]:
    samples: list[TankSample] = []
    t = 0

    for cycle in range(1, total_cycles + 1):
        for step in range(cycle_length_s):
            level = max(20.0, 100.0 - (cycle - 1) * 8 - step * 0.6)
            pressure = 45.0 - step * 0.15
            flow_left = 4.0 if 4 <= step <= 10 else 0.4
            flow_right = 4.1 if 11 <= step <= 17 else 0.4
            leak_score = 0.1

            if cycle == 2 and step >= 14:
                pressure -= 8.0
                leak_score = 0.82

            samples.append(
                TankSample(
                    timestamp_s=t,
                    cycle_id=cycle,
                    level_pct=round(level, 3),
                    pressure_kpa=round(pressure, 3),
                    flow_left_lpm=round(flow_left, 3),
                    flow_right_lpm=round(flow_right, 3),
                    leak_score=round(leak_score, 3),
                )
            )
            t += 1

    return samples
