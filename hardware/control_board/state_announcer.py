class StateAnnouncer:

    def __init__(self, mqtt_client, topic):
        self.mqtt_client = mqtt_client
        self.topic = topic

    def announce_state(self, state):
        self.mqtt_client.publish(self.topic.encode(), state.encode())
