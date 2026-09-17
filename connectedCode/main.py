import threading
import queue
from action import run_motor_worker
from face_tracking import run_tracker

if __name__ == "__main__":
    # Create a Queue with a max size of 1. 
    # This is critical: if the motor is slow, we don't want a backlog 
    # of old coordinates. We only care about the most recent face location.
    target_queue = queue.Queue(maxsize=1)
    
    # Start the motor worker in a background thread
    # daemon=True means this thread will safely die when we close the camera
    motor_thread = threading.Thread(target=run_motor_worker, args=(target_queue,), daemon=True)
    motor_thread.start()
    
    # Create our ultra-fast callback function
    def send_to_queue(delta_x, delta_y):
        # If the motor is still busy with the last coordinate, throw the old one away
        if target_queue.full():
            try:
                target_queue.get_nowait()
            except queue.Empty:
                pass
        
        # Put the newest coordinate into the queue
        target_queue.put((delta_x, delta_y))

    print("Starting camera and motor threads...")
    
    # Run the tracker, passing our fast queue-updating function
    run_tracker(on_target_update=send_to_queue)