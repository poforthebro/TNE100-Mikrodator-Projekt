import queue
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import PhaseEnableMotor
from time import sleep 

def run_motor_worker(data_queue):
    print("Initializing Servo Hardware...")
    
    # 1. Hardware Setup (Runs once when the thread starts)
    factory = PiGPIOFactory()
    servo_y = Servo(18, pin_factory=factory) # Make sure this matches your working pin
    motor = PhaseEnableMotor(phase=26,enable=13)
    
    # 2. Control System Parameters
    Kp = 0.002                 # Gain: Fraction of delta_y to move per frame'
    Kp_motor = 0.005           # Gain for motor speed adjustment
    DEADZONE = 15              # Threshold: Ignore tiny pixel movements
    current_servo_pos_y = 1  # Center position   
    
    # Center the servo on startup
    servo_y.value = current_servo_pos_y

    while True:
        try:
            # Wait for the delta coordinates to appear in the queue from main.py
            delta_x, delta_y = data_queue.get(timeout=1)
            
            # 3. Apply the Control Logic to the Y-axis
            if abs(delta_y) > DEADZONE:
                adjustment = delta_y * Kp
                
                # Add adjustment to current position (change to '-' if it moves the wrong way)
                current_servo_pos_y = current_servo_pos_y + adjustment
                
                # Clamp the value between -1.0 and 1.0 so gpiozero doesn't crash
                current_servo_pos_y = max(-1.0, min(1.0, current_servo_pos_y))
                
                # Output the signal to the hardware
                servo_y.value = current_servo_pos_y
            if abs(delta_x) > DEADZONE:
                speed = delta_x * Kp_motor
                speed = max(-0.3, min(0.3, speed))
                if speed > 0:
                    motor.forward(speed)
                elif speed < 0:
                    motor.backward(-speed)
            else:
                motor.stop()
                
        except queue.Empty:
            continue
