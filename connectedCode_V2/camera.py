from picamera2 import Picamera2
import cv2

class camera:

    # Define and initilize each use of the class with these settings
    def __init__(self, streamResWidth, streamResHeight, MLresWidth, MLresHeight):
        print("Initilizing camera hardware")

        self.picam2 = Picamera2() # Connect picamera2() to self.picam2

        # Configure the two different streams and their respective settings
        config = self.picam2.create_video_configuration(
            main = {"format": "BGR88", "size": (streamResWidth, streamResHeight) }, 
            lores = {"format": "YUV420", "size": (MLresWidth, MLresHeight) }
        )

        self.picam2.configure(config) # Is self really needed here?
        
        self.picam2.start()
        print("Camera has started")


    # Functino to retrieve frames color corrected and flipped
    def get_frames(self):
        request = self.picam2.capture_request()
        high_res_frame = request.make_array("main")
        ml_frame = request.make_array("lores")

        #Realease the DSP in the camera to make it available again.
        request.release()

        # Convert the YUV420 hardware stream into a BGR image for OpenCV
        ml_frame = cv2.cvtColor(ml_frame, cv2.COLOR_YUV2BGR_I420)

    # Flip both
        high_res_frame = cv2.flip(high_res_frame, 1)
        ml_frame = cv2.flip(ml_frame, 1)

        return(ml_frame, high_res_frame)


    def stop(self):
        self.picam2.stop()