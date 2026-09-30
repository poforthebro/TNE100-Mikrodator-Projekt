from gpiozero import PhaseEnableMotor
from time import sleep 

motor = PhaseEnableMotor(phase=26,enable=13)


try: 
    print("do this but forwards")
    motor.forward(0.5)
    sleep(3)
    
    print("do this but stop")
    motor.stop()
    sleep(2)
    
    print("do this bro but backwards")
    motor.backward(0.5)
    sleep(3)
    
    
    
    
    
    
except KeyboardInterrupt:
    motor.stop()
    print("I STOPPED CHILL")
