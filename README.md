# Smart Traffic Management System (AI + IoT)

An intelligent traffic control system that automatically manages traffic signals based on real-time vehicle density using **YOLOv8**, **Computer Vision**, and **IoT**.

## Features

- **Vehicle Detection** — Detects cars, motorcycles, buses, trucks using YOLOv8
- **Traffic Density Analysis** — Classifies lanes as LOW / MEDIUM / HIGH / CRITICAL with rolling-average smoothing
- **Dynamic Signal Control** — Green time (10–60s) scales with vehicle count; busiest lane gets priority
- **Emergency Vehicle Detection** — Detects ambulance/fire truck via color analysis; overrides signals instantly
- **Simulation Mode** — Run without cameras using synthetic traffic data

## Project Structure

```
smart-traffic-system/
├── config/
│   └── settings.py              # All configurable parameters
├── models/
│   ├── vehicle_detector.py      # YOLOv8 vehicle detection
│   ├── density_analyzer.py      # Traffic density classification
│   ├── signal_controller.py     # Dynamic signal timing control
│   └── emergency_detector.py    # Emergency vehicle detection
├── utils/
│   ├── simulator.py             # Simulated traffic frame generator
│   └── logger.py                # Event logging
├── tests/
│   ├── test_density_analyzer.py # Density analyzer tests
│   └── test_signal_controller.py# Signal controller tests
├── main.py                      # Main application
└── requirements.txt
```

## Installation

```bash
git clone https://github.com/<your-username>/smart-traffic-system.git
cd smart-traffic-system
pip install -r requirements.txt
```

## Usage

```bash
# Simulation mode (no camera needed)
python main.py

# Single image vehicle detection
python main.py --image path/to/traffic.jpg

# Video file input
python main.py --mode video

# Live camera feed
python main.py --mode camera
```

## How It Works

1. **Camera/Frame Input** → captures traffic from each lane
2. **YOLOv8 Detection** → counts vehicles by type per lane
3. **Density Analysis** → smoothed classification with rolling average
4. **Signal Decision** → busiest lane gets longest green (10–60s)
5. **Emergency Override** → instant green for emergency vehicles

## Signal Timing Logic

| Vehicles | Green Time | Density Level |
|----------|-----------|---------------|
| 0–5      | 10–18s    | LOW           |
| 6–15     | 19–32s    | MEDIUM        |
| 16–25    | 33–47s    | HIGH          |
| 25+      | 48–60s    | CRITICAL      |

## Tech Stack

- **Python**
- **YOLOv8** (Ultralytics) — Object Detection
- **OpenCV** — Computer Vision
- **NumPy** — Data Processing

## Running Tests

```bash
python tests/test_density_analyzer.py
python tests/test_signal_controller.py
```

## Future Enhancements

- Web dashboard for real-time monitoring
- IoT hardware integration (ESP32 / Arduino)
- Accident detection module
- Google Maps traffic data integration
- Mobile app for traffic alerts

## License

MIT
