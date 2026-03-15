"""
Emergency Vehicle Detection Module.

Detects emergency vehicles (ambulances, fire trucks) using
color analysis and siren-like visual patterns on detected vehicles.
"""

import cv2
import numpy as np


class EmergencyDetector:
    """
    Detects emergency vehicles by analyzing color patterns
    (red/blue flashing lights, white body with red markings).
    """

    def __init__(self):
        # HSV color ranges for emergency vehicle indicators
        # Red color range (two ranges since red wraps around in HSV)
        self.red_lower1 = np.array([0, 100, 100])
        self.red_upper1 = np.array([10, 255, 255])
        self.red_lower2 = np.array([160, 100, 100])
        self.red_upper2 = np.array([180, 255, 255])

        # Blue color range (police/ambulance lights)
        self.blue_lower = np.array([100, 150, 100])
        self.blue_upper = np.array([130, 255, 255])

        self.red_threshold = 0.15  # 15% of ROI must be red/blue

    def check_emergency(self, frame, detections):
        """
        Check if any detected vehicle is an emergency vehicle.

        Args:
            frame: original BGR frame
            detections: list of detection dicts from VehicleDetector

        Returns:
            dict with:
                - "emergency_detected": bool
                - "emergency_vehicles": list of detections flagged as emergency
                - "lane_hint": suggested lane for priority (if detected)
        """
        emergency_vehicles = []

        for det in detections:
            if det["class_name"] not in ("bus", "truck", "car"):
                continue

            x1, y1, x2, y2 = det["bbox"]

            # Clamp to frame bounds
            h, w = frame.shape[:2]
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)

            roi = frame[y1:y2, x1:x2]
            if roi.size == 0:
                continue

            # Check upper portion of vehicle (where lights/sirens are)
            upper_h = max(1, roi.shape[0] // 3)
            upper_roi = roi[:upper_h, :]

            if self._has_emergency_colors(upper_roi):
                emergency_vehicles.append({
                    **det,
                    "emergency": True,
                })

        return {
            "emergency_detected": len(emergency_vehicles) > 0,
            "emergency_vehicles": emergency_vehicles,
        }

    def _has_emergency_colors(self, roi):
        """Check if ROI contains significant red or blue (emergency lights)."""
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        total_pixels = roi.shape[0] * roi.shape[1]
        if total_pixels == 0:
            return False

        # Red mask
        red_mask1 = cv2.inRange(hsv, self.red_lower1, self.red_upper1)
        red_mask2 = cv2.inRange(hsv, self.red_lower2, self.red_upper2)
        red_mask = red_mask1 | red_mask2
        red_ratio = np.count_nonzero(red_mask) / total_pixels

        # Blue mask
        blue_mask = cv2.inRange(hsv, self.blue_lower, self.blue_upper)
        blue_ratio = np.count_nonzero(blue_mask) / total_pixels

        # Emergency if significant red OR blue
        return (red_ratio > self.red_threshold) or (blue_ratio > self.red_threshold)
