"""
Traffic Density Analyzer Module.

Analyzes vehicle counts from each lane and classifies traffic density
as low, medium, or high. Provides density data to the signal controller.
"""

from config.settings import (
    LOW_DENSITY_THRESHOLD,
    MEDIUM_DENSITY_THRESHOLD,
    HIGH_DENSITY_THRESHOLD,
    LANE_NAMES,
)


class DensityLevel:
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class TrafficDensityAnalyzer:
    """Analyzes traffic density across multiple lanes at an intersection."""

    def __init__(self):
        self.history = {lane: [] for lane in LANE_NAMES}
        self.history_size = 10  # rolling window for smoothing

    def classify_density(self, vehicle_count):
        """Classify density level based on vehicle count."""
        if vehicle_count <= LOW_DENSITY_THRESHOLD:
            return DensityLevel.LOW
        elif vehicle_count <= MEDIUM_DENSITY_THRESHOLD:
            return DensityLevel.MEDIUM
        elif vehicle_count <= HIGH_DENSITY_THRESHOLD:
            return DensityLevel.HIGH
        else:
            return DensityLevel.CRITICAL

    def analyze(self, lane_vehicle_counts):
        """
        Analyze traffic density for all lanes.

        Args:
            lane_vehicle_counts: dict mapping lane name to vehicle count.
                e.g. {"North": 12, "South": 5, "East": 20, "West": 8}

        Returns:
            dict with keys:
                - "lane_density": dict mapping lane to density info
                - "priority_order": lanes sorted by density (highest first)
                - "busiest_lane": name of the lane with highest density
                - "total_vehicles": total across all lanes
        """
        lane_density = {}

        for lane_name in LANE_NAMES:
            count = lane_vehicle_counts.get(lane_name, 0)

            # Update rolling history
            self.history[lane_name].append(count)
            if len(self.history[lane_name]) > self.history_size:
                self.history[lane_name].pop(0)

            # Smoothed count (average of recent readings)
            smoothed_count = sum(self.history[lane_name]) / len(self.history[lane_name])

            density_level = self.classify_density(smoothed_count)

            lane_density[lane_name] = {
                "raw_count": count,
                "smoothed_count": round(smoothed_count, 1),
                "density_level": density_level,
            }

        # Sort lanes by smoothed count (highest first)
        priority_order = sorted(
            lane_density.keys(),
            key=lambda l: lane_density[l]["smoothed_count"],
            reverse=True,
        )

        total_vehicles = sum(lane_vehicle_counts.get(l, 0) for l in LANE_NAMES)

        return {
            "lane_density": lane_density,
            "priority_order": priority_order,
            "busiest_lane": priority_order[0],
            "total_vehicles": total_vehicles,
        }

    def get_density_score(self, lane_name):
        """Get a 0-100 density score for a lane based on history."""
        if not self.history[lane_name]:
            return 0
        avg = sum(self.history[lane_name]) / len(self.history[lane_name])
        score = min(100, (avg / HIGH_DENSITY_THRESHOLD) * 100)
        return round(score, 1)

    def reset(self):
        """Clear all history."""
        self.history = {lane: [] for lane in LANE_NAMES}
