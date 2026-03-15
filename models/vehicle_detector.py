"""
Vehicle Detection Module using YOLOv8.

Detects and counts vehicles (cars, motorcycles, buses, trucks) from
camera frames or images using the YOLO object detection model.
"""

import cv2
import numpy as np
from ultralytics import YOLO

from config.settings import (
    YOLO_MODEL,
    CONFIDENCE_THRESHOLD,
    VEHICLE_CLASSES,
)


class VehicleDetector:
    """Detects vehicles in images/video frames using YOLOv8."""

    def __init__(self, model_path=None):
        model_path = model_path or YOLO_MODEL
        print(f"[VehicleDetector] Loading YOLO model: {model_path}")
        self.model = YOLO(model_path)
        self.vehicle_class_ids = set(VEHICLE_CLASSES.keys())

    def detect(self, frame):
        """
        Detect vehicles in a single frame.

        Args:
            frame: BGR image (numpy array from OpenCV).

        Returns:
            dict with keys:
                - "detections": list of dicts with keys
                    "class_id", "class_name", "confidence", "bbox" (x1,y1,x2,y2)
                - "vehicle_count": total vehicles detected
                - "count_by_type": dict mapping vehicle type to count
                - "annotated_frame": frame with bounding boxes drawn
        """
        results = self.model(frame, verbose=False)[0]

        detections = []
        count_by_type = {name: 0 for name in VEHICLE_CLASSES.values()}

        for box in results.boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            if class_id not in self.vehicle_class_ids:
                continue
            if confidence < CONFIDENCE_THRESHOLD:
                continue

            x1, y1, x2, y2 = box.xyxy[0].tolist()
            class_name = VEHICLE_CLASSES[class_id]

            detections.append({
                "class_id": class_id,
                "class_name": class_name,
                "confidence": round(confidence, 2),
                "bbox": (int(x1), int(y1), int(x2), int(y2)),
            })
            count_by_type[class_name] += 1

        annotated_frame = self._draw_detections(frame.copy(), detections)

        return {
            "detections": detections,
            "vehicle_count": len(detections),
            "count_by_type": count_by_type,
            "annotated_frame": annotated_frame,
        }

    def detect_from_file(self, image_path):
        """Detect vehicles from an image file path."""
        frame = cv2.imread(image_path)
        if frame is None:
            raise FileNotFoundError(f"Cannot read image: {image_path}")
        return self.detect(frame)

    def _draw_detections(self, frame, detections):
        """Draw bounding boxes and labels on the frame."""
        colors = {
            "car": (0, 255, 0),
            "motorcycle": (255, 255, 0),
            "bus": (0, 165, 255),
            "truck": (0, 0, 255),
        }

        for det in detections:
            x1, y1, x2, y2 = det["bbox"]
            color = colors.get(det["class_name"], (255, 255, 255))
            label = f"{det['class_name']} {det['confidence']}"

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(
                frame, label, (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2,
            )

        # Total count overlay
        cv2.putText(
            frame,
            f"Vehicles: {len(detections)}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 255, 255),
            2,
        )
        return frame
