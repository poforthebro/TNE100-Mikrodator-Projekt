import cv2




class face_tracking():

    # Define and initilize each use of the class with these settings
    def __init__(self, MLresWidth, MLresHeight, Q):
        print("Initilizing ML model")

        # Load the built-in face detector in cv2. It is called YuNet
        self.detector = cv2.FaceDetectorYN.create(
        model='face_detection_yunet.onnx',
        config='',
        input_size=(MLresWidth, MLresHeight),
        score_threshold=Q
        )
        print("ML model has been loaded")



    # Function to run the model on a certain frame
    def get_faces(self, frame):
        status, faces = self.detector.detect(frame)

        if faces is None:
            return None, 0

        if status != 1:
            print("There was an issue processing this frame")

        quality = []

        for face in faces:
            q = get_quality_score(face)
            quality.append(q)

        faces = sorted(faces, key=get_quality_score, reverse=True)

        return faces, quality


# Function to calculate the quality score for a single face
def get_quality_score(face):
    width = face[2]
    height = face[3]
    confidence = face[14]

    area = height * width
    q = area * confidence

    return q

