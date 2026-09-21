
class delta():
    def __init__(self, ML_width, ML_height):
        self.middle_width = ML_width // 2
        self.middle_height = ML_height // 2

    def get_delta(self, x, y):
        delta = (self.middle_width - x, self.middle_height - y)

        return delta