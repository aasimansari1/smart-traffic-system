"""
Traffic Simulation Module.

Generates simulated traffic frames for testing when no camera
or video feed is available.
"""

import cv2
import numpy as np
import random

from config.settings import LANE_NAMES


class TrafficSimulator:
    """Generates simulated traffic frames with random vehicles."""

    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.frame_count = 0

    def generate_frame(self, lane_name, num_vehicles=None):
        """
        Generate a simulated traffic frame with drawn vehicles.

        Args:
            lane_name: name of the lane (for display)
            num_vehicles: number of vehicles to draw (random if None)

        Returns:
            BGR frame (numpy array) with simulated vehicles
        """
        if num_vehicles is None:
            num_vehicles = random.randint(2, 30)

        # Create road background
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        frame[:] = (50, 50, 50)  # dark gray road

        # Draw road lines
        cv2.line(frame, (self.width // 2, 0), (self.width // 2, self.height),
                 (0, 200, 200), 2)  # center line
        for y in range(0, self.height, 40):
            cv2.line(frame, (self.width // 4, y), (self.width // 4, y + 20),
                     (255, 255, 255), 1)
            cv2.line(frame, (3 * self.width // 4, y), (3 * self.width // 4, y + 20),
                     (255, 255, 255), 1)

        # Draw vehicles as colored rectangles
        vehicle_colors = [
            (0, 0, 200),    # red car
            (200, 200, 200),  # white car
            (200, 0, 0),    # blue car
            (0, 200, 0),    # green car
            (0, 150, 255),  # orange truck
        ]

        for i in range(num_vehicles):
            x = random.randint(30, self.width - 80)
            y = random.randint(30, self.height - 60)
            w = random.randint(40, 70)
            h = random.randint(25, 45)
            color = random.choice(vehicle_colors)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, -1)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), 1)

        # Lane label
        cv2.putText(
            frame, f"Lane: {lane_name} | Simulated: {num_vehicles} vehicles",
            (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2,
        )

        self.frame_count += 1
        return frame

    def generate_all_lanes(self, vehicle_counts=None):
        """
        Generate frames for all lanes.

        Args:
            vehicle_counts: dict mapping lane name to vehicle count.
                            If None, random counts are used.

        Returns:
            dict mapping lane name to frame.
        """
        frames = {}
        for lane in LANE_NAMES:
            count = vehicle_counts.get(lane) if vehicle_counts else None
            frames[lane] = self.generate_frame(lane, count)
        return frames
