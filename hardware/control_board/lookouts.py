class Lookouts:

    def __init__(self):
        # 0 => not detected
        # 1 => detected
        self.west_far = 0
        self.west_near = 0
        self.east_near = 0
        self.east_far = 0

    def to_str(self):
        return str(self.west_far) + str(self.west_near) + str(self.east_near) + str(self.east_far)
