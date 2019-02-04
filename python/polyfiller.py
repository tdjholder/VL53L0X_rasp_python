# coding=utf-8
VL53L0X_BETTER_ACCURACY_MODE = True


class VL53L0X:

    def __init__(self, address):
        self.count = 0.0
        self.address = address
        self.is_ranging = False

    def start_ranging(self, is_ranging):
        """Stub that does nothing."""
        self.is_ranging = is_ranging

    def get_distance(self):
        """Increment by 1 and return."""
        self.count += 1.0
        return self.count
