class Gates:

    def __init__(self, mqtt_client, gates_north_topic, gates_south_topic):
        self._mqtt_client = mqtt_client
        self._gates_north_topic = gates_north_topic
        self._gates_south_topic = gates_south_topic
        self._north = 1
        self._south = 1
        self.open_all()

    @property
    def north(self):
        return self._north

    @north.setter
    def north(self, status):
        status = int(status)
        if status not in [0, 1]:
            print("Gates.north.setter: status is invalid")
            return
        if self._north == status:
            print("Gates.north.setter: no change in status")
            return
        self._north = status
        print(f"Gates.north.setter: status set to {self._north}")

    @property
    def south(self):
        return self._south

    @south.setter
    def south(self, status):
        status = int(status)
        if status not in [0, 1]:
            print("Gates.south.setter: status is invalid")
            return
        if self._south == status:
            print("Gates.south.setter: no change in status")
            return
        self._south = status
        print(f"Gates.south.setter: status set to {self._south}")

    def _publish_north(self):
        self._mqtt_client.publish(
            self._gates_north_topic.encode(), str(self._north).encode()
        )

    def _publish_south(self):
        self._mqtt_client.publish(
            self._gates_south_topic.encode(), str(self._south).encode()
        )

    def open_north(self):
        self._north = 1
        self._publish_north()
        print(f"Gates.open_north: published and set status to {self._north}")

    def close_north(self):
        self._north = 0
        self._publish_north()
        print(f"Gates.close_north: published and set status to {self._north}")

    def open_south(self):
        self._south = 1
        self._publish_south()
        print(f"Gates.open_south: published and set status to {self._south}")

    def close_south(self):
        self._south = 0
        self._publish_south()
        print(f"Gates.close_south: published and set status to {self._south}")

    def open_all(self):
        self.open_north()
        self.open_south()

    def close_all(self):
        self.close_north()
        self.close_south()
