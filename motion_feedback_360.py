import RPi.GPIO as GPIO
import time

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Define motion sensors GPIO pins
motion_pins = [17, 27, 22]  # Example GPIO pins for motion sensors m1, m2, and m3

# Define vibration motors GPIO pins
vibration_pins = [18, 23, 24]  # Example GPIO pins for vibration motors v1, v2, and v3

# Setup GPIO pins
for pin in motion_pins:
    GPIO.setup(pin, GPIO.IN)

for pin in vibration_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

try:
    while True:
        for motion_pin, vibration_pin in zip(motion_pins, vibration_pins):
            if GPIO.input(motion_pin) == GPIO.HIGH:
                print(f"Motion detected on motion sensor {motion_pin}")
                GPIO.output(vibration_pin, GPIO.HIGH)
                print(f"Vibration motor {vibration_pin}  turned on")

        time.sleep(1)  # Check motion sensors every 1 second

        for vibration_pin in vibration_pins:
            GPIO.output(vibration_pin, GPIO.LOW)

except KeyboardInterrupt:
    GPIO.cleanup()