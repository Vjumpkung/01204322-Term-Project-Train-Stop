class Lookouts:

    def __init__(
        self,
        mqtt_client,
        west_far_topic,
        west_near_topic,
        east_near_topic,
        east_far_topic,
    ):
        self._west_far = 0
        self._west_near = 0
        self._east_near = 0
        self._east_far = 0
        self._mqtt_client = mqtt_client
        self._west_far_topic = west_far_topic
        self._west_near_topic = west_near_topic
        self._east_near_topic = east_near_topic
        self._east_far_topic = east_far_topic
        self._publish_west_far()
        self._publish_west_near()
        self._publish_east_near()
        self._publish_east_far()

    @property
    def west_far(self):
        return self._west_far

    @west_far.setter
    def west_far(self, status):
        status = int(status)
        if status not in [0, 1]:
            print("Lookouts.west_far.setter: invalid status")
            return
        self._west_far = status
        print(f"Lookouts.west_far.setter: set status to {status}")

    @property
    def west_near(self):
        return self._west_near

    @west_near.setter
    def west_near(self, status):
        status = int(status)
        if status not in [0, 1]:
            print("Lookouts.west_near.setter: invalid status")
            return
        self._west_near = status
        print(f"Lookouts.west_near.setter: set status to {status}")

    @property
    def east_near(self):
        return self._east_near

    @east_near.setter
    def east_near(self, status):
        status = int(status)
        if status not in [0, 1]:
            print("Lookouts.east_near.setter: invalid status")
            return
        self._east_near = status
        print(f"Lookouts.east_near.setter: set status to {status}")

    @property
    def east_far(self):
        return self._east_far

    @east_far.setter
    def east_far(self, status):
        status = int(status)
        if status not in [0, 1]:
            print("Lookouts.east_far.setter: invalid status")
            return
        self._east_far = status
        print(f"Lookouts.east_far.setter: set status to {status}")

    def __str__(self):
        return f"{self._west_far}{self._west_near}{self._east_near}{self._east_far}"

    def _publish_west_far(self):
        self._mqtt_client.publish(
            self._west_far_topic.encode(), str(self._west_far).encode(), retain=True
        )

    def _publish_west_near(self):
        self._mqtt_client.publish(
            self._west_near_topic.encode(), str(self._west_near).encode(), retain=True
        )

    def _publish_east_near(self):
        self._mqtt_client.publish(
            self._east_near_topic.encode(), str(self._east_near).encode(), retain=True
        )

    def _publish_east_far(self):
        self._mqtt_client.publish(
            self._east_far_topic.encode(), str(self._east_far).encode(), retain=True
        )
