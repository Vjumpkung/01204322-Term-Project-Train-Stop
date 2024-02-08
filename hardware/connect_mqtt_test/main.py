# example

from machine import reset
import mqtt_setup as mqtt


def func(topic, msg):
    print(msg)


def main():
    client = mqtt.setup("192.168.1.66", 1883)
    client.set_callback(func)


if __name__ == "__main__":
    try:
        main()
    except OSError as e:
        print("Error: " + str(e))
        reset()
