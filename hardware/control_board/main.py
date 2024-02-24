import time

from machine import reset
from mqtt_setup import setup

from lookouts import Lookouts
from dfa import DFA
from gates_controller import GatesController
from state_announcer import StateAnnouncer


CROSSING_ID = "crossing1"
print(f"{CROSSING_ID}")

LOOKOUT_WEST_FAR_TOPIC = f"{CROSSING_ID}/lookouts/west/far"
LOOKOUT_WEST_NEAR_TOPIC = f"{CROSSING_ID}/lookouts/west/near"
LOOKOUT_EAST_NEAR_TOPIC = f"{CROSSING_ID}/lookouts/east/near"
LOOKOUT_EAST_FAR_TOPIC = f"{CROSSING_ID}/lookouts/east/far"

STATE_TOPIC = f"{CROSSING_ID}/state"

GATES_NORTH_TOPIC = f"{CROSSING_ID}/gates/north"
GATES_SOUTH_TOPIC = f"{CROSSING_ID}/gates/south"

STATES = {
    "0",
    "eb0", "eb1", "eb2", "eb3", "eb4", "eb5",
    "wb0", "wb1", "wb2", "wb3", "wb4", "wb5"
}

# "<west_far><west_near><east_near><east_far>"
INPUTS = {
    "0000", "0001", "0010", "0100", "1000",
    "0011", "0110", "1100",
    "0111", "1110",
    "1111"
}

TRANSITIONS = {
    # westbound #
    # ---------------------- #
    ("0", "0001"): "wb0",  # close gates
    # ---------------------- #
    ("wb0", "0100"): "wb1",
    ("wb0", "0110"): "wb1",
    ("wb0", "0111"): "wb1",
    # ---------------------- #
    ("wb1", "0000"): "wb2",  # open gates
    ("wb2", "1000"): "wb3",
    ("wb3", "0000"): "0",
    # ---------------------- #
    ("wb1", "1100"): "wb4",
    ("wb1", "1110"): "wb4",
    ("wb1", "1111"): "wb4",
    ("wb4", "1000"): "wb5",  # open gates
    ("wb5", "0000"): "0",
    # ---------------------- #

    # eastbound #
    # ---------------------- #
    ("0", "1000"): "eb0",  # close gates
    # ---------------------- #
    ("eb0", "0010"): "eb1",
    ("eb0", "0110"): "eb1",
    ("eb0", "1110"): "eb1",
    # ---------------------- #
    ("eb1", "0000"): "eb2",  # open gates
    ("eb2", "0001"): "eb3",
    ("eb3", "0000"): "0",
    # ---------------------- #
    ("eb1", "0011"): "eb4",
    ("eb1", "0111"): "eb4",
    ("eb1", "1111"): "eb4",
    ("eb4", "0001"): "eb5",  # open gates
    ("eb5", "0000"): "0",
    # ---------------------- #
}

lookouts = None
dfa = None

def sub_cb(topic, msg):
    topic = topic.decode()
    msg = msg.decode()
    print("sub_cb: received a msg: " + f"{topic}: {msg}")
    if topic == LOOKOUT_WEST_FAR_TOPIC:
        if msg != "0" and msg != "1":
            print("sub_cb: lookout status is invalid")
            return
        if lookouts.west_far == int(msg):
            print("sub_cb: lookout status didn't change")
            return
        lookouts.west_far = int(msg)
        print(f"sub_cb: lookouts changed to {lookouts.to_str()}")
        dfa.transition(lookouts.to_str())
    elif topic == LOOKOUT_WEST_NEAR_TOPIC:
        if msg != "0" and msg != "1":
            print("sub_cb: lookout status is invalid")
            return
        if lookouts.west_near == int(msg):
            print("sub_cb: lookout status didn't change")
            return
        lookouts.west_near = int(msg)
        print(f"sub_cb: lookouts changed to {lookouts.to_str()}")
        dfa.transition(lookouts.to_str())
    elif topic == LOOKOUT_EAST_NEAR_TOPIC:
        if msg != "0" and msg != "1":
            print("sub_cb: lookout status is invalid")
            return
        if lookouts.east_near == int(msg):
            print("sub_cb: lookout status didn't change")
            return
        lookouts.east_near = int(msg)
        print(f"sub_cb: lookouts changed to {lookouts.to_str()}")
        dfa.transition(lookouts.to_str())
    elif topic == LOOKOUT_EAST_FAR_TOPIC:
        if msg != "0" and msg != "1":
            print("sub_cb: lookout status is invalid")
            return
        if lookouts.east_far == int(msg):
            print("sub_cb: lookout status didn't change")
            return
        lookouts.east_far = int(msg)
        print(f"sub_cb: lookouts changed to {lookouts.to_str()}")
        dfa.transition(lookouts.to_str())
    else:
        print("sub_cb: topic didn't match")

def main():
    global lookouts
    global dfa

    mqtt_client = setup()
    print("main: done setting up mqtt_client")
    mqtt_client.set_callback(sub_cb)
    print("main: done setting subscribe callback")

    mqtt_client.subscribe(LOOKOUT_WEST_FAR_TOPIC)
    mqtt_client.subscribe(LOOKOUT_WEST_NEAR_TOPIC)
    mqtt_client.subscribe(LOOKOUT_EAST_NEAR_TOPIC)
    mqtt_client.subscribe(LOOKOUT_EAST_FAR_TOPIC)
    print("main: done subscribing to topics")

    state_announcer = StateAnnouncer(mqtt_client, STATE_TOPIC)
    print("main: done creating state_announcer")
    gates_controller = GatesController(mqtt_client, GATES_NORTH_TOPIC, GATES_SOUTH_TOPIC)
    print("main: done creating gates_controller")

    state_actions = {
        "wb0": [
            (gates_controller.set_status, {"status": "close"})
        ],
        "eb0": [
            (gates_controller.set_status, {"status": "close"})
        ],
        "wb2": [
            (gates_controller.set_status, {"status": "open"})
        ],
        "wb5": [
            (gates_controller.set_status, {"status": "open"})
        ],
        "eb2": [
            (gates_controller.set_status, {"status": "open"})
        ],
        "eb5": [
            (gates_controller.set_status, {"status": "open"})
        ],
    }
    print("main: done creating state_actions")

    lookouts = Lookouts()
    print("main: done creating lookouts")

    dfa = DFA(STATES, INPUTS, TRANSITIONS, state_announcer.announce_state, state_actions, "0")
    print("main: done creating dfa")

    print("main: begin listening for msg...")
    last_scheduled_report = time.time()
    while True:
        mqtt_client.check_msg()
        if time.time() - last_scheduled_report > 1:
            state_announcer.announce_state(dfa.current_state)
            last_scheduled_report = time.time()
        time.sleep(0.1)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Exception: " + str(e))
        reset()
