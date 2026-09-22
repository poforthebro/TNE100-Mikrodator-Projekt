from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

# 1. Initialize the pigpio factory
factory = PiGPIOFactory()

# 2. explicitly assign the factory to the servo
servo = Servo(18, pin_factory=factory)

try:
    servo.min()
    sleep(1)
    servo.max()
    sleep(1)
    
finally:
    # 3. Ensure the pin is always released, even on crash
    servo.close()