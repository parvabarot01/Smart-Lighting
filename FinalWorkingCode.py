import sys
sys.path.append('/home/parva-barot/miniforge3/lib/python3.12/site-packages')
import RPi.GPIO as GPIO
import time
import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


LDR_PIN = 18
PIR_PIN = 17
LED_PIN = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(LDR_PIN, GPIO.IN)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)


client = AWSIoTMQTTClient("SmartLightPi")
client.configureEndpoint("atogo4f7776z2-ats.iot.us-east-2.amazonaws.com", 8883)
client.configureCredentials("AmazonRootCA1.pem", "private.key", "device.cert.pem")
client.connect()

log_file = open("led_log.txt", "a")

led_on = False
motion_timer_start = None
last_log_time = 0
manual_override = False  


def log_status(light_status, motion_status, led_status):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp} | Light: {light_status} | Motion: {motion_status} | LED: {led_status}\n"
    print(log_entry.strip())
    log_file.write(log_entry)
    log_file.flush()

    payload = {
        "timestamp": timestamp,
        "light_status": light_status,
        "motion_status": motion_status,
        "led_status": led_status
    }
    client.publish("smart/lightmotion/status", json.dumps(payload), 1)


def take_reading_now():
    light = GPIO.input(LDR_PIN)
    motion = GPIO.input(PIR_PIN)
    is_dark = light == 1
    motion_detected = motion == 1
    light_status = "Dark" if is_dark else "Bright"
    motion_status = "Yes" if motion_detected else "No"
    led_status = "ON" if GPIO.input(LED_PIN) else "OFF"
    log_status(light_status, motion_status, led_status)
               
def custom_callback(client, userdata, message):
    global led_on, manual_override
    command = message.payload.decode().strip().lower()
    print(f"Received command: {command}")

   
    if command == "turn on led":
        GPIO.output(LED_PIN, GPIO.HIGH)
        led_on = True
        manual_override = True
        print("LED turned ON (manual override)")
    elif command == "turn off led":
        GPIO.output(LED_PIN, GPIO.LOW)
        led_on = False
        manual_override = True
        print("LED turned OFF (manual override)")
    elif command == "resume":
        manual_override = False
        print("Resumed sensor-based automatic")
       
client.subscribe("smart/lightmotion/command", 1, custom_callback)

print("Running: Monitoring sensors + listening for commands...")

try:
    while True:
        if manual_override:
            time.sleep(1)
            continue

        light = GPIO.input(LDR_PIN)
        motion = GPIO.input(PIR_PIN)

        is_dark = light == 1
        motion_detected = motion == 1
        light_status = "Dark" if is_dark else "Bright"
        motion_status = "Yes" if motion_detected else "No"

        if not is_dark:
            if led_on:
                GPIO.output(LED_PIN, GPIO.LOW)
                log_status(light_status, motion_status, "OFF")
            led_on = False
            motion_timer_start = None

        elif is_dark and motion_detected:
            if not led_on:
                GPIO.output(LED_PIN, GPIO.HIGH)
                log_status(light_status, motion_status, "ON")
            led_on = True
            motion_timer_start = None

        elif is_dark and not motion_detected:
            if led_on:
                if motion_timer_start is None:
                    motion_timer_start = time.time()
                elif time.time() - motion_timer_start >= 60:
                    GPIO.output(LED_PIN, GPIO.LOW)
                    log_status(light_status, motion_status, "OFF")
                    led_on = False
                    motion_timer_start = None
            else:
                motion_timer_start = None
               
               
        current_time = time.time()
        if current_time - last_log_time >= 10:
            led_status = "ON" if GPIO.input(LED_PIN) else "OFF"
            log_status(light_status, motion_status, led_status)
            last_log_time = current_time

        time.sleep(1)

except KeyboardInterrupt:
    print("Shutting down...")
    log_file.close()
    GPIO.cleanup()