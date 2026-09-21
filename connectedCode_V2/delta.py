
class delta():
    def __init__(self, ML_width, ML_height):
        self.middle_width = ML_width // 2
        self.middle_height = ML_height // 2

        print("Middle_width = ", self.middle_width, "Middle_Height = ", self.middle_height)

    def get_delta(self, face):
        x = face[0] + ( face[2] // 2 ) # Center of face
        y = face[1] + ( face[3] // 2 ) # Center of face
        
        delta = (int(self.middle_width - x), int(self.middle_height - y))

        return delta