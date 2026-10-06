import queue
from gpiozero import Servo,PhaseEnableMotor
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep 

def run_motor_worker(data_queue):
    print("Initializing Servo Hardware")
    factory = PiGPIOFactory()
    servo_y = Servo(18, pin_factory=factory)
    motor_x = PhaseEnableMotor(phase=26,enable=13)
    
    Kp_servo = 0.002                 
    Kp_motor = 0.0015         
    DEADZONE = 15 # we have a deadzone of 15 pixels to avoid jittering so it doesnt needlessly move 
    current_servo_pos_y = 1
    MAX_MOTOR_SPEED = 0.75
    MIN_MOTOR_SPEED = 0.20
    
    SAMPLETIME = 0.1 
    
    # Center the servo on startup
    servo_y.value = current_servo_pos_y

    while True:
        try:
            delta_x, delta_y = data_queue.get(timeout=1) #we get our delta values from the camera, checks how far off center the object is, can be applied to a PID controller. 
            if abs(delta_y) > DEADZONE:
                adjustment = delta_y * Kp_servo
                current_servo_pos_y = current_servo_pos_y + adjustment
                current_servo_pos_y = max(-1.0, min(1.0, current_servo_pos_y))
                servo_y.value = current_servo_pos_y
            if abs(delta_x) > DEADZONE:
                rspeed = abs(delta_x) * Kp_motor
                pspeed = max(MIN_MOTOR_SPEED, min(MAX_MOTOR_SPEED, rspeed)) # 
                if delta_x < 0:
                    motor_x.forward(pspeed)
                else:
                    motor_x.backward(pspeed)
            else:
                motor_x.stop() #stop if in deadzone
        except queue.Empty:
            continue # wait
