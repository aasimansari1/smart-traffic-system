"""
Traffic System Logger.

Provides formatted logging for traffic events, signal changes,
and density analysis.
"""

import time
from datetime import datetime


class TrafficLogger:
    """Logs traffic system events to console and optionally to file."""

    def __init__(self, log_file=None):
        self.log_file = log_file
        self.logs = []

    def _timestamp(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _log(self, level, module, message):
        entry = f"[{self._timestamp()}] [{level}] [{module}] {message}"
        print(entry)
        self.logs.append(entry)

        if self.log_file:
            with open(self.log_file, "a") as f:
                f.write(entry + "\n")

    def info(self, module, message):
        self._log("INFO", module, message)

    def warning(self, module, message):
        self._log("WARN", module, message)

    def error(self, module, message):
        self._log("ERROR", module, message)

    def log_detection(self, lane_name, result):
        """Log vehicle detection results."""
        count = result["vehicle_count"]
        types = result["count_by_type"]
        type_str = ", ".join(f"{k}:{v}" for k, v in types.items() if v > 0)
        self.info("Detector", f"{lane_name}: {count} vehicles ({type_str})")

    def log_density(self, analysis):
        """Log density analysis results."""
        for lane, data in analysis["lane_density"].items():
            self.info(
                "Density",
                f"{lane}: {data['raw_count']} vehicles | "
                f"Smoothed: {data['smoothed_count']} | "
                f"Level: {data['density_level']}",
            )
        self.info("Density", f"Busiest lane: {analysis['busiest_lane']}")

    def log_signal(self, cycle_result):
        """Log signal control decisions."""
        self.info(
            "Signal",
            f"Green -> {cycle_result['current_green']} "
            f"for {cycle_result['green_time']}s",
        )
        for lane, status in cycle_result["signals"].items():
            self.info("Signal", f"  {lane}: {status['state']}")
