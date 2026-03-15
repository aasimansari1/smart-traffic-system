"""
Traffic Signal Controller Module.

Dynamically adjusts traffic signal timing based on real-time
vehicle density analysis. Supports emergency vehicle priority.
"""

import time
from config.settings import (
    MIN_GREEN_TIME,
    MAX_GREEN_TIME,
    DEFAULT_GREEN_TIME,
    YELLOW_TIME,
    HIGH_DENSITY_THRESHOLD,
    LANE_NAMES,
)


class SignalState:
    RED = "RED"
    YELLOW = "YELLOW"
    GREEN = "GREEN"


class TrafficSignal:
    """Represents a single traffic signal for one lane."""

    def __init__(self, lane_name):
        self.lane_name = lane_name
        self.state = SignalState.RED
        self.green_duration = DEFAULT_GREEN_TIME
        self.time_remaining = 0
        self.last_change = time.time()

    def set_green(self, duration):
        self.state = SignalState.GREEN
        self.green_duration = duration
        self.time_remaining = duration
        self.last_change = time.time()

    def set_yellow(self):
        self.state = SignalState.YELLOW
        self.time_remaining = YELLOW_TIME
        self.last_change = time.time()

    def set_red(self):
        self.state = SignalState.RED
        self.time_remaining = 0
        self.last_change = time.time()

    def __repr__(self):
        return f"Signal({self.lane_name}: {self.state}, {self.time_remaining}s)"


class SignalController:
    """
    Controls traffic signals at an intersection based on density data.

    Cycle: one lane gets GREEN while others stay RED.
    Transitions: GREEN -> YELLOW -> RED, then next lane goes GREEN.
    """

    def __init__(self):
        self.signals = {lane: TrafficSignal(lane) for lane in LANE_NAMES}
        self.current_green_lane = None
        self.phase = "idle"  # idle, green, yellow
        self.emergency_active = False
        self.cycle_log = []

    def calculate_green_time(self, vehicle_count):
        """
        Calculate green time proportional to vehicle density.

        More vehicles = longer green time, clamped to min/max bounds.
        """
        if vehicle_count <= 0:
            return MIN_GREEN_TIME

        # Linear scaling: each vehicle adds ~1.5 seconds
        green_time = MIN_GREEN_TIME + (vehicle_count * 1.5)
        green_time = max(MIN_GREEN_TIME, min(MAX_GREEN_TIME, green_time))
        return round(green_time)

    def update_cycle(self, density_analysis):
        """
        Determine the next signal cycle based on density analysis.

        Args:
            density_analysis: output from TrafficDensityAnalyzer.analyze()

        Returns:
            dict with the full signal plan for this cycle.
        """
        priority_order = density_analysis["priority_order"]
        lane_density = density_analysis["lane_density"]

        signal_plan = []

        for lane_name in priority_order:
            count = lane_density[lane_name]["smoothed_count"]
            green_time = self.calculate_green_time(count)

            signal_plan.append({
                "lane": lane_name,
                "green_time": green_time,
                "yellow_time": YELLOW_TIME,
                "vehicle_count": lane_density[lane_name]["raw_count"],
                "density_level": lane_density[lane_name]["density_level"],
            })

        self.cycle_log.append({
            "timestamp": time.time(),
            "plan": signal_plan,
            "busiest_lane": density_analysis["busiest_lane"],
            "total_vehicles": density_analysis["total_vehicles"],
        })

        return {
            "signal_plan": signal_plan,
            "cycle_order": priority_order,
            "busiest_lane": density_analysis["busiest_lane"],
        }

    def activate_green(self, lane_name, duration):
        """Set one lane to GREEN and all others to RED."""
        for name, signal in self.signals.items():
            if name == lane_name:
                signal.set_green(duration)
            else:
                signal.set_red()
        self.current_green_lane = lane_name
        self.phase = "green"

    def transition_to_yellow(self):
        """Transition current green signal to yellow."""
        if self.current_green_lane:
            self.signals[self.current_green_lane].set_yellow()
            self.phase = "yellow"

    def all_red(self):
        """Set all signals to RED (safety phase)."""
        for signal in self.signals.values():
            signal.set_red()
        self.current_green_lane = None
        self.phase = "idle"

    def emergency_override(self, lane_name):
        """
        Immediately give green to the specified lane (emergency vehicle detected).
        All other lanes go RED.
        """
        self.emergency_active = True
        print(f"[EMERGENCY] Priority green for lane: {lane_name}")
        self.activate_green(lane_name, MAX_GREEN_TIME)
        return {
            "emergency": True,
            "lane": lane_name,
            "action": "GREEN priority activated",
        }

    def clear_emergency(self):
        """Clear emergency override and return to normal operation."""
        self.emergency_active = False
        self.all_red()

    def get_status(self):
        """Get current status of all signals."""
        return {
            lane: {
                "state": signal.state,
                "time_remaining": signal.time_remaining,
            }
            for lane, signal in self.signals.items()
        }

    def run_cycle(self, density_analysis):
        """
        Execute one full signal cycle (non-blocking plan generation).

        Returns the plan; actual timing is handled by the main loop.
        """
        if self.emergency_active:
            return {"status": "emergency_active", "signals": self.get_status()}

        plan = self.update_cycle(density_analysis)

        # Activate green for the busiest lane first
        first_lane = plan["cycle_order"][0]
        first_green_time = plan["signal_plan"][0]["green_time"]
        self.activate_green(first_lane, first_green_time)

        return {
            "status": "cycle_started",
            "current_green": first_lane,
            "green_time": first_green_time,
            "full_plan": plan,
            "signals": self.get_status(),
        }
