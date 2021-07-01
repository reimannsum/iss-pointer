import math

class Angle:

    def __float__(self):
        return self.angle

    def __init__(self, measure=0.0, max_angle=360):
        self.max = float(Angle(max_angle))   # this keeps things within 360 degrees
        self.angle = self.correct_angle_size(measure)



    def __add__(self, other):  # Define the  + function
        other = float(other)
        total = self.angle + other
        return self.correct_angle_size(total)

    def __sub__(self, other):  # Define the - function
        other = float(other)
        total = self.angle - other
        return self.correct_angle_size(total)

    def __repr__(self):  # Define what is displayed when printed
        if self.angle > 180:
            return str(self.angle - 360)
        else:
            return str(self.angle)

    def __iadd__(self, other):  # Define the += function
        return Angle(self + float(other))

    def correct_angle_size(self, angle):
        while math.abs(angle) > 360:
            if angle > 360:
                angle -= 360
            if angle < -360:
                angle += 360

        if angle > self.max:
            return angle - 360
        elif angle < self.max - 360:
            return angle + 360
        else:
            return angle
