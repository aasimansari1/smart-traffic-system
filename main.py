"""
Smart Traffic Management System - Main Application.

Integrates vehicle detection, density analysis, and signal control
into a complete traffic management pipeline.

Usage:
    python main.py                  # Run in simulation mode
    python main.py --mode video     # Run with video files
    python main.py --mode camera    # Run with live cameras
    python main.py --image path.jpg # Detect vehicles in a single image
"""

import argparse
import random
import time
import sys
import cv2

from config.settings import LANE_NAMES, LANE_SOURCES, SIMULATION_MODE
from models.vehicle_detector import VehicleDetector
from models.density_analyzer import TrafficDensityAnalyzer
from models.signal_controller import SignalController
from models.emergency_detector import EmergencyDetector
from utils.simulator import TrafficSimulator
from utils.logger import TrafficLogger


def run_single_image(image_path):
    """Detect vehicles in a single image and display results."""
    print(f"\n--- Vehicle Detection on: {image_path} ---\n")

    detector = VehicleDetector()
    result = detector.detect_from_file(image_path)

    print(f"Total vehicles detected: {result['vehicle_count']}")
    print(f"By type: {result['count_by_type']}")
    print("\nDetections:")
    for det in result["detections"]:
        print(f"  {det['class_name']} (conf: {det['confidence']}) at {det['bbox']}")

    # Save annotated image
    output_path = image_path.rsplit(".", 1)[0] + "_detected.jpg"
    cv2.imwrite(output_path, result["annotated_frame"])
    print(f"\nAnnotated image saved to: {output_path}")


def run_simulation():
    """Run the full traffic system in simulation mode."""
    print("\n" + "=" * 60)
    print("  SMART TRAFFIC MANAGEMENT SYSTEM")
    print("  Mode: Simulation")
    print("=" * 60 + "\n")

    detector = VehicleDetector()
    analyzer = TrafficDensityAnalyzer()
    controller = SignalController()
    emergency_det = EmergencyDetector()
    simulator = TrafficSimulator()
    logger = TrafficLogger()

    cycle_count = 0

    try:
        while True:
            cycle_count += 1
            print(f"\n{'='*50}")
            print(f"  CYCLE {cycle_count}")
            print(f"{'='*50}")

            lane_counts = {}

            # Step 1: Generate frames and detect vehicles for each lane
            for lane_name in LANE_NAMES:
                # Generate a random vehicle count for simulation
                sim_count = random.randint(2, 35)
                frame = simulator.generate_frame(lane_name, sim_count)

                result = detector.detect(frame)

                # In simulation mode, YOLO won't detect drawn rectangles,
                # so use the simulated count for the pipeline
                actual_count = result["vehicle_count"] if result["vehicle_count"] > 0 else sim_count
                result["vehicle_count"] = actual_count
                logger.log_detection(lane_name, result)
                lane_counts[lane_name] = actual_count

                # Check for emergency vehicles
                emergency = emergency_det.check_emergency(
                    frame, result["detections"]
                )
                if emergency["emergency_detected"]:
                    logger.warning(
                        "Emergency",
                        f"Emergency vehicle detected in {lane_name}!",
                    )
                    override = controller.emergency_override(lane_name)
                    logger.info("Signal", f"Emergency override: {override}")
                    time.sleep(3)
                    controller.clear_emergency()

            # Step 2: Analyze traffic density
            density = analyzer.analyze(lane_counts)
            logger.log_density(density)

            # Step 3: Control signals based on density
            cycle_result = controller.run_cycle(density)
            logger.log_signal(cycle_result)

            # Print signal plan summary
            print(f"\n--- Signal Plan ---")
            for entry in cycle_result["full_plan"]["signal_plan"]:
                print(
                    f"  {entry['lane']}: "
                    f"GREEN {entry['green_time']}s | "
                    f"Vehicles: {entry['vehicle_count']} | "
                    f"Density: {entry['density_level']}"
                )

            # Wait before next cycle
            print(f"\n[Next cycle in 5 seconds...]")
            time.sleep(5)

    except KeyboardInterrupt:
        print("\n\nSystem stopped by user.")
        print(f"Total cycles completed: {cycle_count}")


def run_video_mode():
    """Run with video files as input."""
    print("\n" + "=" * 60)
    print("  SMART TRAFFIC MANAGEMENT SYSTEM")
    print("  Mode: Video")
    print("=" * 60 + "\n")

    detector = VehicleDetector()
    analyzer = TrafficDensityAnalyzer()
    controller = SignalController()
    emergency_det = EmergencyDetector()
    logger = TrafficLogger()

    # Open video captures
    captures = {}
    for lane_name, source in LANE_SOURCES.items():
        cap = cv2.VideoCapture(source)
        if cap.isOpened():
            captures[lane_name] = cap
            logger.info("Video", f"Opened video source for {lane_name}: {source}")
        else:
            logger.warning("Video", f"Cannot open source for {lane_name}: {source}")

    if not captures:
        print("No video sources available. Use --mode simulate or provide valid video paths.")
        return

    cycle_count = 0

    try:
        while True:
            cycle_count += 1
            lane_counts = {}

            for lane_name, cap in captures.items():
                ret, frame = cap.read()
                if not ret:
                    # Loop video
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    ret, frame = cap.read()
                    if not ret:
                        continue

                result = detector.detect(frame)
                logger.log_detection(lane_name, result)
                lane_counts[lane_name] = result["vehicle_count"]

                emergency = emergency_det.check_emergency(frame, result["detections"])
                if emergency["emergency_detected"]:
                    logger.warning("Emergency", f"Emergency vehicle in {lane_name}!")
                    controller.emergency_override(lane_name)
                    time.sleep(2)
                    controller.clear_emergency()

            density = analyzer.analyze(lane_counts)
            logger.log_density(density)

            cycle_result = controller.run_cycle(density)
            logger.log_signal(cycle_result)

            time.sleep(2)

    except KeyboardInterrupt:
        print(f"\nStopped. Cycles: {cycle_count}")
    finally:
        for cap in captures.values():
            cap.release()


def main():
    parser = argparse.ArgumentParser(
        description="Smart Traffic Management System using AI + IoT"
    )
    parser.add_argument(
        "--mode",
        choices=["simulate", "video", "camera"],
        default="simulate",
        help="Running mode (default: simulate)",
    )
    parser.add_argument(
        "--image",
        type=str,
        help="Path to a single image for vehicle detection",
    )
    args = parser.parse_args()

    if args.image:
        run_single_image(args.image)
    elif args.mode == "simulate":
        run_simulation()
    elif args.mode in ("video", "camera"):
        run_video_mode()


if __name__ == "__main__":
    main()
