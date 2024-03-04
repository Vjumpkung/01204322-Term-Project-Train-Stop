from ultrasonic import get_ultra_distance


class Ultra:

    def __init__(
        self, mqtt_client, lookout_topic, threshold=3, count=0, memo=0, prev_dec=0
    ):
        self.mqtt_client = mqtt_client
        self.lookout_topic = lookout_topic
        self.threshold = threshold
        self.count = count
        self.memo = memo
        self.prev_dec = prev_dec

        self.mqtt_client.publish(
            self.lookout_topic.encode(), str(prev_dec).encode(), retain=True
        )
        print(f"Lookouts {self.lookout_topic}: published status {prev_dec}")

    def read_and_publish(self, DEBUG=False):
        dis = get_ultra_distance()
        decision = 0

        if (dis < self.threshold and self.memo < self.threshold) or (
            dis > self.threshold and self.memo > self.threshold
        ):
            self.count += 1
        else:
            self.count = 0

        self.memo = dis

        if DEBUG:
            print(f"dis = {dis} cm")

        if self.count >= 3:
            if dis < self.threshold and dis > 0:
                decision = 1
            else:
                decision = 0

            if decision != self.prev_dec:
                self.mqtt_client.publish(
                    self.lookout_topic.encode(), str(decision).encode(), retain=True
                )
                if DEBUG:
                    print(f"Lookouts {self.lookout_topic}: published status {decision}")

            self.prev_dec = decision
            self.count = 0
