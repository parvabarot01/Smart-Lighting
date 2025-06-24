# 💡 Smart Lighting System using Raspberry Pi + AWS IoT

This project is a **motion and light-based smart LED control system** powered by a Raspberry Pi and integrated with **AWS IoT Core**. It allows real-time monitoring and two-way control via MQTT commands like `turn on led`, `turn off led`, and `resume`.

---

## 🛠️ Features

- Detects ambient light and motion to control an LED automatically.
- Sends real-time logs to AWS IoT (topic: `smart/lightmotion/status`).
- Accepts MQTT commands to override or resume sensor-based automation.
- Logs all LED states with timestamps in `led_log.txt`.

---

---

## 🧾 Requirements

- Raspberry Pi (with RPi.GPIO library)
- AWS IoT Core account & Thing setup
- Python 3.12+
- AWS IoT certificates

---

## 📥 Installation (100% Copy-Paste Safe)

### 🔧 1. Enable GPIO and Install Required Packages

```bash
sudo apt update
sudo apt install python3-pip
pip3 install AWSIoTPythonSDK RPi.GPIO
```

###  2. Clone the Repository and Set Up Certificates
```bash
git clone https://github.com/parvabarot01/Smart-Lighting-System.git
cd Smart-Lighting-System

# Place your AWS IoT certificates here
mkdir certs
mv path/to/AmazonRootCA1.pem certs/
mv path/to/private.key certs/
mv path/to/device.cert.pem certs/
```
