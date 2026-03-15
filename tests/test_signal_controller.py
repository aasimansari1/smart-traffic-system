"""Tests for the Traffic Signal Controller."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.signal_controller import SignalController, SignalState
from models.density_analyzer import TrafficDensityAnalyzer


def test_green_time_calculation():
    controller = SignalController()

    assert controller.calculate_green_time(0) == 10   # min
    assert controller.calculate_green_time(5) == 18   # 10 + 7.5
    assert controller.calculate_green_time(10) == 25  # 10 + 15
    assert controller.calculate_green_time(100) == 60  # capped at max
    print("PASSED: test_green_time_calculation")


def test_activate_green():
    controller = SignalController()
    controller.activate_green("North", 30)

    status = controller.get_status()
    assert status["North"]["state"] == SignalState.GREEN
    assert status["South"]["state"] == SignalState.RED
    assert status["East"]["state"] == SignalState.RED
    assert status["West"]["state"] == SignalState.RED
    print("PASSED: test_activate_green")


def test_signal_cycle():
    controller = SignalController()
    analyzer = TrafficDensityAnalyzer()

    counts = {"North": 20, "South": 5, "East": 12, "West": 30}
    density = analyzer.analyze(counts)
    result = controller.run_cycle(density)

    # West has highest count, should get green first
    assert result["current_green"] == "West"
    assert result["status"] == "cycle_started"
    print("PASSED: test_signal_cycle")


def test_emergency_override():
    controller = SignalController()
    controller.activate_green("North", 30)

    result = controller.emergency_override("East")
    status = controller.get_status()

    assert result["emergency"] is True
    assert status["East"]["state"] == SignalState.GREEN
    assert status["North"]["state"] == SignalState.RED
    print("PASSED: test_emergency_override")


def test_all_red():
    controller = SignalController()
    controller.activate_green("North", 30)
    controller.all_red()

    status = controller.get_status()
    for lane, data in status.items():
        assert data["state"] == SignalState.RED
    print("PASSED: test_all_red")


if __name__ == "__main__":
    test_green_time_calculation()
    test_activate_green()
    test_signal_cycle()
    test_emergency_override()
    test_all_red()
    print("\nAll signal controller tests passed!")
