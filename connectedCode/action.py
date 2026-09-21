import queue
import time

def run_motor_worker(data_queue):
    while True:
        try:
            # Wait for coordinates to appear in the queue
            delta_x, delta_y = data_queue.get(timeout=1)
            
            print(f"Starting motor movement to X:{delta_x} Y:{delta_y}...")
            
            # Simulate a slow motor movement (e.g., takes 2 seconds)
             time.sleep(2) 
            
            print("Motor movement complete!")
            
        except queue.Empty:
            # If the queue is empty, just loop back and keep waiting
            continue