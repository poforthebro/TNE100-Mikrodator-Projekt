
import argparse

import numpy as np
import cv2 as cv
from mp_handpose import MPHandPose
from mp_palmdet import MPPalmDet

# We need to start the model, feed it a frame of data and then grab the array of values it output. Those values then need to be processed

# Setup all classes
backend_id = backend_target_pairs[args.backend_target][0]
target_id = backend_target_pairs[args.backend_target][1]
# palm detector
palm_detector = MPPalmDet(modelPath=palm_model_path,
                            nmsThreshold=0.3,
                            scoreThreshold=0.6,
                            backendId=backend_id,
                            targetId=target_id)
# handpose detector
handpose_detector = MPHandPose(modelPath=args.model,
                                confThreshold=args.conf_threshold,
                                backendId=backend_id,
                                targetId=target_id)

class MPHandPose:
    def __init__(self, MLresWidth, MLresHeight):
