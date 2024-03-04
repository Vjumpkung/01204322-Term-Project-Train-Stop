class Gates:

    def __init__(self, mqtt_client, gates_north_topic, gates_south_topic, debug=False):
        self._mqtt_client = mqtt_client
        self._gates_north_topic = gates_north_topic
        self._gates_south_topic = gates_south_topic
        self._north = 1
        self._south = 1
        self.open_all()
        self._debug = debug

    @property
    def north(self):
        return self._north

    @north.setter
    def north(self, status):
        status = int(status)
        if status not in [0, 1]:
            if self._debug:
                print("Gates.north.setter: invalid status")
            return
        self._north = status
        if self._debug:
            print(f"Gates.north.setter: set status to {self._north}")

    @property
    def south(self):
        return self._south

    @south.setter
    def south(self, status):
        status = int(status)
        if status not in [0, 1]:
            if self._debug:
                print("Gates.south.setter: invalid status")
            return
        self._south = status
        if self._debug:
            print(f"Gates.south.setter: set status to {self._south}")

    def _publish_north(self):
        self._mqtt_client.publish(
            self._gates_north_topic.encode(), str(self._north).encode(), retain=True
        )
        if self._debug:
            print(f"Gates._publish_north: published status {self._north}")

    def _publish_south(self):
        self._mqtt_client.publish(
            self._gates_south_topic.encode(), str(self._south).encode(), retain=True
        )
        if self._debug:
            print(f"Gates._publish_south: published status {self._south}")

    def _open_north(self):
        self._north = 1
        self._publish_north()
        if self._debug:
            print(f"Gates._open_north: set status to {self._north}")

    def _close_north(self):
        self._north = 0
        self._publish_north()
        if self._debug:
            print(f"Gates._close_north: set status to {self._north}")

    def _open_south(self):
        self._south = 1
        self._publish_south()
        if self._debug:
            print(f"Gates._open_south: set status to {self._south}")

    def _close_south(self):
        self._south = 0
        self._publish_south()
        if self._debug:
            print(f"Gates._close_south: set status to {self._south}")

    def open_all(self):
        self._open_north()
        self._open_south()

    def close_all(self):
        self._close_north()
        self._close_south()

    def toggle_north(self):
        if self._north == 1:
            self._close_north()
        else:
            self._open_north()

    def toggle_south(self):
        if self._south == 1:
            self._close_south()
        else:
            self._open_south()
