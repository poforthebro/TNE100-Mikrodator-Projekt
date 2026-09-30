import queue
import threading

from action import run_motor_worker

class queue_handler:
    def __init__(self):
        self.target_queue = queue.Queue(maxsize=1)

        self.action_thread = threading.Thread(
            target=run_motor_worker, 
            args=(self.target_queue,), 
            daemon=True)
        
        self.action_thread.start()


    def send_to_queue(self, delta):

        if self.target_queue.full():
            try:
                self.target_queue.get_nowait()
            except queue.Empty:
                pass

        self.target_queue.put(delta)