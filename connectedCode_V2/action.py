import queue
import time
from gpiozero import Servo, PhaseEnableMotor
from gpiozero.pins.pigpio import PiGPIOFactory

class PIDController: 
    def __init__(it, kp, ki, kd, max_integral=500):
        it.kp = kp
        it.ki = ki
        it.kd = kd
        it.max_integral = max_integral
        it.prev_error = 0
        it.integral = 0
        it.last_time = time.time()

    def compute(it, error):
        current_time = time.time()
        dt = current_time - it.last_time
        if dt <= 0.0: 
            dt = 0.01 

        P = it.kp * error
        it.integral += error * dt
        it.integral = max(-it.max_integral, min(it.max_integral, it.integral))
        I = it.ki * it.integral
        D = it.kd * (error - it.prev_error) / dt
        
        it.prev_error = error
        it.last_time = current_time
        return P + I + D

    def reset(it):
        it.integral = 0
        it.prev_error = 0
        it.last_time = time.time()

def run_motor_worker(data_queue):
    print("Initializing Servo Hardware")
    factory = PiGPIOFactory()
    
    servo_y = Servo(18, pin_factory=factory)
    motor_x = PhaseEnableMotor(phase=26, enable=13, pin_factory=factory)
    
    Kp_servo = 0.002                 
    Kp_motor = 0.0015    
    Ki_motor = 0.0001
    Kd_motor = 0.0000
    
    DEADZONE = 15 
    current_servo_pos_y = 1
    MAX_MOTOR_SPEED = 0.75
    MIN_MOTOR_SPEED = 0.20
    
    # Center the servo on startup
    servo_y.value = current_servo_pos_y
    
    # Implement an x based pid controller
    PID_motor = PIDController(kp=Kp_motor, ki=Ki_motor, kd=Kd_motor)
    
    while True:
        try:
            delta_x, delta_y = data_queue.get(timeout=0.2) 
            '''
            if abs(delta_y) > DEADZONE:
                adjustment = delta_y * Kp_servo
                current_servo_pos_y = current_servo_pos_y + adjustment
                current_servo_pos_y = max(-1.0, min(1.0, current_servo_pos_y))
                servo_y.value = current_servo_pos_y
            '''   
            if abs(delta_x) > DEADZONE:
                u = PID_motor.compute(delta_x)
                rspeed = abs(u)
                pspeed = max(MIN_MOTOR_SPEED, min(MAX_MOTOR_SPEED, rspeed)) 
                
                
                if u < 0:
                    motor_x.forward(pspeed)
                else:
                    motor_x.backward(pspeed)
            else:
                motor_x.stop()
                PID_motor.reset() 
                
        except queue.Empty:
            motor_x.stop()
            PID_motor.reset() 
