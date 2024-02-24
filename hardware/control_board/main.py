import time

from machine import reset
from mqtt_setup import setup

from gates import Gates
from lookouts import Lookouts
from control import Control


CROSSING_ID = "crossing1"

LOOKOUT_WEST_FAR_TOPIC = f"{CROSSING_ID}/lookouts/west/far"
LOOKOUT_WEST_NEAR_TOPIC = f"{CROSSING_ID}/lookouts/west/near"
LOOKOUT_EAST_NEAR_TOPIC = f"{CROSSING_ID}/lookouts/east/near"
LOOKOUT_EAST_FAR_TOPIC = f"{CROSSING_ID}/lookouts/east/far"

STATE_TOPIC = f"{CROSSING_ID}/state"

GATES_NORTH_TOPIC = f"{CROSSING_ID}/gates/north"
GATES_SOUTH_TOPIC = f"{CROSSING_ID}/gates/south"

MODE_TOPIC = f"{CROSSING_ID}/mode"

STATES = {
    # "0" => initial state
    # "eb..." train is eastbound
    # "wb..." train is westbound
    "0",
    "eb0",
    "eb1",
    "eb2",
    "eb3",
    "eb4",
    "eb5",
    "wb0",
    "wb1",
    "wb2",
    "wb3",
    "wb4",
    "wb5",
}

INPUTS = {
    # "<west_far><west_near><east_near><east_far>"
    "0000",
    "0001",
    "0010",
    "0100",
    "1000",
    "0011",
    "0110",
    "1100",
    "0111",
    "1110",
    "1111",
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


# global variables used by sub_cb
gates = None
lookouts = None
control = None


def sub_cb(topic, msg):
    topic = topic.decode()
    msg = msg.decode()
    print("sub_cb: received a msg: " + f"{topic}: {msg}")
    if topic == LOOKOUT_WEST_FAR_TOPIC:
        lookouts.west_far = int(msg)
        control.transition(str(lookouts))
    elif topic == LOOKOUT_WEST_NEAR_TOPIC:
        lookouts.west_near = int(msg)
        control.transition(str(lookouts))
    elif topic == LOOKOUT_EAST_NEAR_TOPIC:
        lookouts.east_near = int(msg)
        control.transition(str(lookouts))
    elif topic == LOOKOUT_EAST_FAR_TOPIC:
        lookouts.east_far = int(msg)
        control.transition(str(lookouts))
    elif topic == MODE_TOPIC:
        control.mode = msg
    elif topic == GATES_NORTH_TOPIC:
        gates.north = int(msg)
    elif topic == GATES_SOUTH_TOPIC:
        gates.south = int(msg)
    else:
        print("sub_cb: no action for this topic")


def main():
    global gates
    global lookouts
    global control

    mqtt_client = setup()
    mqtt_client.set_callback(sub_cb)

    mqtt_client.subscribe(LOOKOUT_WEST_FAR_TOPIC)
    mqtt_client.subscribe(LOOKOUT_WEST_NEAR_TOPIC)
    mqtt_client.subscribe(LOOKOUT_EAST_NEAR_TOPIC)
    mqtt_client.subscribe(LOOKOUT_EAST_FAR_TOPIC)

    mqtt_client.subscribe(GATES_NORTH_TOPIC)
    mqtt_client.subscribe(GATES_SOUTH_TOPIC)

    mqtt_client.subscribe(MODE_TOPIC)

    gates = Gates(mqtt_client, GATES_NORTH_TOPIC, GATES_SOUTH_TOPIC)

    state_actions = {
        # "state": [(<respect_mode>, <function>, <kwargs>), ...]
        # if <respect_mode> is True, then the function will only be called if the mode is "A" (automatic)
        # if <respect_mode> is False, then the function will be called regardless of the mode
        "wb0": [(True, gates.close_all, {})],
        "eb0": [(True, gates.close_all, {})],
        "wb2": [(True, gates.open_all, {})],
        "wb5": [(True, gates.open_all, {})],
        "eb2": [(True, gates.open_all, {})],
        "eb5": [(True, gates.open_all, {})],
    }

    lookouts = Lookouts()

    control = Control(
        states=STATES,
        inputs=INPUTS,
        transitions=TRANSITIONS,
        state_actions=state_actions,
        initial_state="0",
        mqtt_client=mqtt_client,
        state_topic=STATE_TOPIC,
        mode_topic=MODE_TOPIC,
    )

    print("main: begin listening for msg...")
    last_ping = time.time()
    while True:
        mqtt_client.check_msg()
        if time.time() - last_ping > 60:
            mqtt_client.ping()
            last_ping = time.time()
        time.sleep(0.1)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Exception: " + str(e))
        reset()
