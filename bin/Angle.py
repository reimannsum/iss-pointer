class HalfAngle:
    def __init__(self, measure=0.0):
        if measure > 180:
            self.angle = measure - 360
        else:
            self.angle = measure

    def __add__(self, other):  # Define the  + function
        other = float(other)
        total = self.angle + other
        if total > 180:
            return total - 360
        elif total < -180:
            return total + 360
        else:
            return total

    def __sub__(self, other):  # Define the - function
        other = float(other)
        total = self.angle - other
        if total > 180:
            return total - 360
        elif total < -180:
            return total + 360
        else:
            return total

    def __repr__(self):  # Define what is displayed when printed
        return str(self.angle)

    def __iadd__(self, other):  # Define the += function
        return HalfAngle(self + float(other))

    def __float__(self):
        return self.angle


class Angle:

    def __float__(self):
        return self.angle

    def __init__(self, measure=0.0):
        self.angle = measure

    def __add__(self, other):  # Define the  + function
        other = float(other)
        total = self.angle + other
        if total > 360:
            return total - 360
        elif total < 0:
            return total + 360
        else:
            return total

    def __sub__(self, other):  # Define the - function
        other = float(other)
        total = self.angle - other
        if total > 360:
            return total - 360
        elif total < 0:
            return total + 360
        else:
            return total

    def __repr__(self):  # Define what is displayed when printed
        if self.angle > 180:
            return str(self.angle - 360)
        else:
            return str(self.angle)

    def __iadd__(self, other):  # Define the += function
        return Angle(self + float(other))
