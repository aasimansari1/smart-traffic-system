"""Tests for the Traffic Density Analyzer."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.density_analyzer import TrafficDensityAnalyzer, DensityLevel


def test_classify_density():
    analyzer = TrafficDensityAnalyzer()

    assert analyzer.classify_density(0) == DensityLevel.LOW
    assert analyzer.classify_density(3) == DensityLevel.LOW
    assert analyzer.classify_density(5) == DensityLevel.LOW
    assert analyzer.classify_density(10) == DensityLevel.MEDIUM
    assert analyzer.classify_density(15) == DensityLevel.MEDIUM
    assert analyzer.classify_density(20) == DensityLevel.HIGH
    assert analyzer.classify_density(25) == DensityLevel.HIGH
    assert analyzer.classify_density(30) == DensityLevel.CRITICAL
    print("PASSED: test_classify_density")


def test_analyze():
    analyzer = TrafficDensityAnalyzer()

    counts = {"North": 20, "South": 5, "East": 12, "West": 30}
    result = analyzer.analyze(counts)

    assert result["busiest_lane"] == "West"
    assert result["total_vehicles"] == 67
    assert result["priority_order"][0] == "West"
    assert result["lane_density"]["North"]["density_level"] == DensityLevel.HIGH
    assert result["lane_density"]["South"]["density_level"] == DensityLevel.LOW
    print("PASSED: test_analyze")


def test_smoothing():
    analyzer = TrafficDensityAnalyzer()

    # Feed multiple readings
    for _ in range(5):
        analyzer.analyze({"North": 10, "South": 10, "East": 10, "West": 10})

    # Now one spike - smoothed should dampen it
    result = analyzer.analyze({"North": 50, "South": 10, "East": 10, "West": 10})
    smoothed = result["lane_density"]["North"]["smoothed_count"]
    assert smoothed < 50, f"Smoothed ({smoothed}) should be less than spike (50)"
    assert smoothed > 10, f"Smoothed ({smoothed}) should be more than base (10)"
    print("PASSED: test_smoothing")


def test_density_score():
    analyzer = TrafficDensityAnalyzer()

    analyzer.analyze({"North": 25, "South": 0, "East": 12, "West": 5})
    north_score = analyzer.get_density_score("North")
    south_score = analyzer.get_density_score("South")

    assert north_score == 100.0
    assert south_score == 0.0
    print("PASSED: test_density_score")


if __name__ == "__main__":
    test_classify_density()
    test_analyze()
    test_smoothing()
    test_density_score()
    print("\nAll density analyzer tests passed!")
