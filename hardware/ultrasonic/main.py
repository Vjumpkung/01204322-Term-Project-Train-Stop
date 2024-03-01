import time
from ultra import Ultra
from machine import reset
from mqtt_setup import setup

def main():
    mqtt_client = setup()
    
    print("main: begin listening for msg...")
    
    CROSSING_ID = "crossing1"
    LOOKOUT_WEST_FAR_TOPIC = f"{CROSSING_ID}/lookouts/west/far"
    
    ultra = Ultra(mqtt_client, LOOKOUT_WEST_FAR_TOPIC)
    
    i = 0
    while True:
        print(f"fetch {i}")
        ultra.read_and_publish()
        time.sleep(0.25)
        i += 1
        


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Exception: " + str(e))
        reset()
