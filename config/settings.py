"""
Configuration settings for Smart Traffic Management System.
"""

# YOLO model configuration
YOLO_MODEL = "yolov8n.pt"  # nano model for speed; use yolov8s.pt or yolov8m.pt for accuracy
CONFIDENCE_THRESHOLD = 0.5

# Vehicle class IDs in COCO dataset
VEHICLE_CLASSES = {
    2: "car",
    3: "motorcycle",
    5: "bus",
    7: "truck",
}

# Emergency vehicle detection (via visual cues)
EMERGENCY_CLASSES = {
    5: "bus",  # ambulances often detected as bus; refined with color detection
}

# Traffic signal timing (in seconds)
MIN_GREEN_TIME = 10
MAX_GREEN_TIME = 60
DEFAULT_GREEN_TIME = 30
YELLOW_TIME = 3

# Density thresholds (vehicle count per lane)
LOW_DENSITY_THRESHOLD = 5
MEDIUM_DENSITY_THRESHOLD = 15
HIGH_DENSITY_THRESHOLD = 25

# Number of lanes/directions at intersection
NUM_LANES = 4
LANE_NAMES = ["North", "South", "East", "West"]

# Camera/video source for each lane (index or file path)
# Use 0 for webcam, or provide video file paths
LANE_SOURCES = {
    "North": "data/sample_videos/north.mp4",
    "South": "data/sample_videos/south.mp4",
    "East": "data/sample_videos/east.mp4",
    "West": "data/sample_videos/west.mp4",
}

# Simulation mode (True = use generated frames when no camera/video available)
SIMULATION_MODE = True
