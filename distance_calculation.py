import RPi.GPIO as GPIO
import time

# Disable warnings related to GPIO operations
GPIO.setwarnings(False)

# Set up GPIO
GPIO.setmode(GPIO.BCM)
TRIG_PIN = 11
ECHO_PIN = 13
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

def measure_distance():
    # Trigger pulse
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    # Measure time of pulse travel
    pulse_start = time.time()
    timeout = pulse_start + 0.1  # Set a timeout of 0.1 seconds
    pulse_end = pulse_start

    # Wait for the ECHO pin to go high
    while GPIO.input(ECHO_PIN) == 0 and pulse_start < timeout:
        pulse_start = time.time()

    # Wait for the ECHO pin to go low
    while GPIO.input(ECHO_PIN) == 1 and pulse_end < timeout:
        pulse_end = time.time()

    # Calculate distance
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound = 343 meters per second (17150 cm/s)
    distance = round(distance / 100, 2)

    return distance

try:

    dist = measure_distance()
    print(f"Distance: {dist} m")
    time.sleep(1)

except KeyboardInterrupt:
    #print("Measurement stopped by the user")
    GPIO.cleanup()