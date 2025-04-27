import RPi.GPIO as GPIO
import time

# Servo pin settings.
servo_pin = 11  # GPIO pin 11
angle_increment = 0  # Angle increment in degrees.

# Set the pin numbering mode.
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)  # Disable warnings.
GPIO.setup(servo_pin, GPIO.OUT)

# Set up PWM on the servo pin.
pwm = GPIO.PWM(servo_pin, 50)  # 50 Hz (20 ms period).
pwm.start(0)  # Initialize with a 0% duty cycle.

def set_servo_angle(angle):
    # Calculate the duty cycle based on the angle.
    duty = max(min(angle / 18 + 2, 12), 2)  # Limit between 2% and 12%
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.09)  # Adjust the time if necessary for smoother movements.
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)

def get_current_angle():
    try:
        with open('servo_down.txt', 'r') as file:
            angle = float(file.read().strip())
    except (FileNotFoundError, ValueError):
        angle = 0.0  # Default angle if file is not found or has invalid content
    return angle

def save_current_angle(angle):
    with open('servo_down.txt', 'w') as file:
        file.write(f"{angle:.2f}")

try:
    current_angle = get_current_angle()
    new_angle = current_angle + angle_increment
    if new_angle > 180:
        new_angle = 180  # Limit the angle to 180 degrees.
    set_servo_angle(new_angle)
    save_current_angle(new_angle)
    print(f"Movido para {new_angle} graus.")

except KeyboardInterrupt:
    # Stop the PWM and clean up the GPIO settings.
    pwm.stop()
    GPIO.cleanup()
