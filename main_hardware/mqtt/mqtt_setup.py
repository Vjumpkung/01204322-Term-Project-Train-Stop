import ubinascii
from umqtt.simple import MQTTClient
import machine
from load_config import MQTT_BROKER, PORT, USERNAME, PASS


def setup():
    CLIENT_ID = ubinascii.hexlify(machine.unique_id())
    mqttClient = MQTTClient(
        CLIENT_ID, MQTT_BROKER, PORT, user=USERNAME, password=PASS, keepalive=60
    )
    mqttClient.connect()
    print("MQTT : Connected to %s:%s" % (MQTT_BROKER, PORT))
    return mqttClient
