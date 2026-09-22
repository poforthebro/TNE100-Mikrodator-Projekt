from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

# Initialize the factory and servo
factory = PiGPIOFactory()
servo = Servo(18, pin_factory=factory)

current_servo_pos = 0.0 
servo.value = current_servo_pos

Kp = 0.002
DEADZONE = 15
if abs(delta_y) > DEADZONE:
    adjustment = Kp * delta_y
    ls
    current_servo_pos = max(-1.0, min(1.0, current_servo_pos))
    servo.value = current_servo_pos
    
try:
    print("Sweeping servo... Press Ctrl+C to stop.")
    
    # This loop runs forever until interrupted
    while True:
        servo.min()
        sleep(1)
        servo.max()
        sleep(1)

except KeyboardInterrupt:
    # Catches the Ctrl+C command silently without throwing an ugly error
    print("\nStopping the servo.")
    
finally:
    # Guarantees the pin is released when the script ends
    servo.close()