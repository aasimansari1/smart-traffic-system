<div align="center">

# 🚦 Smart Traffic Management System

### AI-powered traffic signals that adapt in real time — using YOLOv8 computer vision and dynamic timing logic.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-FF4500?style=for-the-badge)](https://ultralytics.com)
[![OpenCV](https://img.shields.io/badge/OpenCV-4-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org)
[![Flask](https://img.shields.io/badge/Flask-Dashboard-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)

</div>

---

> **Traditional traffic lights run on fixed timers — regardless of whether 1 car or 50 cars are waiting.**
> This system uses YOLOv8 to count vehicles per lane in real time and gives the busiest lane the longest green light. Emergency vehicles get an instant override.

---

## ✨ Features

<table>
<tr>
<td width="50%">

**🚗 Vehicle Detection**
- YOLOv8 detects cars, motorcycles, buses & trucks
- Works on live camera, video file, or simulation
- Rolling-average smoothing prevents signal thrashing

</td>
<td width="50%">

**🧠 Dynamic Signal Control**
- Green time scales from 10s → 60s with vehicle count
- Busiest lane always gets priority
- 4 density levels: LOW / MEDIUM / HIGH / CRITICAL

</td>
</tr>
<tr>
<td width="50%">

**🚨 Emergency Override**
- Detects ambulances & fire trucks via color analysis
- Instantly overrides signal to give emergency vehicles a clear path
- Logs all override events

</td>
<td width="50%">

**🖥️ Simulation Mode**
- Run without any camera or hardware
- Synthetic traffic data generator included
- Great for testing and demos

</td>
</tr>
</table>

---

## ⚡ Quick Start

```bash
git clone https://github.com/aasimansari1/smart-traffic-system.git
cd smart-traffic-system

pip install -r requirements.txt

# Run in simulation mode (no camera needed)
python main.py

# Single image detection
python main.py --image path/to/traffic.jpg

# Video file
python main.py --mode video --source path/to/video.mp4

# Live camera
python main.py --mode camera
```

---

## 🏗️ How It Works

```
  📷 Camera / Video / Simulation
          │
          ▼
  ┌──────────────────┐
  │  VehicleDetector │  ← YOLOv8 — counts cars/buses/trucks per lane
  └────────┬─────────┘
           │
           ▼
  ┌──────────────────┐
  │ DensityAnalyzer  │  ← rolling average → LOW/MEDIUM/HIGH/CRITICAL
  └────────┬─────────┘
           │
           ▼
  ┌──────────────────┐     ┌───────────────────┐
  │ SignalController │     │ EmergencyDetector │
  │ (dynamic timing) │◄────│ (color analysis)  │
  └────────┬─────────┘     └───────────────────┘
           │
           ▼
  🟢 Green time: 10s–60s (scales with density)
  🚨 Emergency override: instant green
```

---

## ⏱️ Signal Timing Logic

| Density | Vehicles | Green Time |
|---|:---:|:---:|
| LOW | 0 – 5 | 10 – 18s |
| MEDIUM | 6 – 15 | 19 – 32s |
| HIGH | 16 – 25 | 33 – 47s |
| CRITICAL | 25+ | 48 – 60s |

All thresholds and lane names are configurable in `config/settings.py`.

---

## 🗂️ Project Structure

```
smart-traffic-system/
├── config/
│   └── settings.py              # All tunable params (timing, thresholds, lanes)
├── models/
│   ├── vehicle_detector.py      # YOLOv8 detection pipeline
│   ├── density_analyzer.py      # Density classification + smoothing
│   ├── signal_controller.py     # Green time calculation + priority logic
│   └── emergency_detector.py    # Color-based emergency detection
├── utils/
│   ├── simulator.py             # Synthetic traffic frame generator
│   └── logger.py                # Event logging
├── tests/
│   ├── test_density_analyzer.py
│   └── test_signal_controller.py
├── app.py                       # Flask dashboard (real-time monitoring)
├── main.py                      # CLI entry point
└── yolov8n.pt                   # Pre-trained YOLOv8 nano weights (~6.5MB)
```

---

## 🧪 Tests

```bash
python tests/test_density_analyzer.py
python tests/test_signal_controller.py
```

---

## 🌐 Web Dashboard

```bash
python app.py
# → http://localhost:5000
```

Real-time view of vehicle counts, density levels, and signal state per lane.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Object Detection | YOLOv8 (Ultralytics) |
| Computer Vision | OpenCV |
| Numerical | NumPy |
| Web Dashboard | Flask |
| Pre-trained Model | `yolov8n.pt` (included) |

---

## 🗺️ Roadmap

- [ ] IoT hardware integration (ESP32 / Arduino signal controllers)
- [ ] Accident detection module
- [ ] Google Maps real-time traffic data feed
- [ ] Multi-intersection coordination
- [ ] Mobile app for traffic authority alerts

---

## 🤝 Contributing

```bash
git checkout -b feature/your-feature
git commit -m 'Add your feature'
git push origin feature/your-feature
```

---

## 📄 License

MIT © [Mohd Aasim Ansari](https://github.com/aasimansari1)

---

<div align="center">

**Making roads smarter, one intersection at a time. If this interests you, please ⭐ star the repo!**

</div>
