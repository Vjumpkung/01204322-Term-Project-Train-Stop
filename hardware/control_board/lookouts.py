class Lookouts:

    def __init__(self):
        self._west_far = 0
        self._west_near = 0
        self._east_near = 0
        self._east_far = 0

    @property
    def west_far(self):
        return self._west_far

    @west_far.setter
    def west_far(self, status):
        status = int(status)
        if status not in [0, 1]:
            print("Lookouts.west_far.setter: status is invalid")
            return
        if self._west_far == status:
            print("Lookouts.west_far.setter: no change in status")
            return
        self._west_far = status
        print(f"Lookouts.west_far.setter: status set to {status}")

    @property
    def west_near(self):
        return self._west_near

    @west_near.setter
    def west_near(self, status):
        status = int(status)
        if status not in [0, 1]:
            print("Lookouts.west_near.setter: status is invalid")
            return
        if self._west_near == status:
            print("Lookouts.west_near.setter: no change in status")
            return
        self._west_near = status
        print(f"Lookouts.west_near.setter: status set to {status}")

    @property
    def east_near(self):
        return self._east_near

    @east_near.setter
    def east_near(self, status):
        status = int(status)
        if status not in [0, 1]:
            print("Lookouts.east_near.setter: status is invalid")
            return
        if self._east_near == status:
            print("Lookouts.east_near.setter: no change in status")
            return
        self._east_near = status
        print(f"Lookouts.east_near.setter: status set to {status}")

    @property
    def east_far(self):
        return self._east_far

    @east_far.setter
    def east_far(self, status):
        status = int(status)
        if status not in [0, 1]:
            print("Lookouts.east_far.setter: status is invalid")
            return
        if self._east_far == status:
            print("Lookouts.east_far.setter: no change in status")
            return
        self._east_far = status
        print(f"Lookouts.east_far.setter: status set to {status}")

    def __str__(self):
        return f"{self._west_far}{self._west_near}{self._east_near}{self._east_far}"
