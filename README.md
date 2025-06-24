# 💡 Smart Lighting System using Raspberry Pi + AWS IoT

This project is a **motion and light-based smart LED control system** powered by a Raspberry Pi and integrated with **AWS IoT Core**. It allows real-time monitoring and two-way control via MQTT commands like `turn on led`, `turn off led`, and `resume`.

---

## 🛠️ Features

- Detects ambient light and motion to control an LED automatically.
- Sends real-time logs to AWS IoT (topic: `smart/lightmotion/status`).
- Accepts MQTT commands to override or resume sensor-based automation.
- Logs all LED states with timestamps in `led_log.txt`.

---
