class GatesController:

    def __init__(self, mqtt_client, gates_north_topic, gates_south_topic):
        self.mqtt_client = mqtt_client
        self.gates_north_topic = gates_north_topic
        self.gates_south_topic = gates_south_topic

    def set_status(self, status):
        if status == "open":
            n = "1"
        elif status == "close":
            n = "0"
        else:
            print("GatesController.set_status: status is invalid")
            return
        self.mqtt_client.publish(self.gates_north_topic.encode(), n.encode())
        self.mqtt_client.publish(self.gates_south_topic.encode(), n.encode())
