from gpiozero import Servo
from time import sleep

# Initialize outside the try block
servo = Servo(25)

try:
    # Your servo control code goes here
    servo.min()
    sleep(1000)
    servo.max()
    sleep(1000)
    
finally:
    # This executes no matter what, freeing the pin
    servo.close()