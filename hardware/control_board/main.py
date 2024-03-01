import time
import _thread
from machine import reset

import cfg_topics
import cfg_dfa
import cfg_pins

from mqtt_setup import setup

from lookouts import Lookouts
from gates import Gates
from control import Control
from button import Button
from display import Display


# global variables used by operations in sub_cb
lookouts = None
gates = None
control = None


def sub_cb(topic, msg):
    topic = topic.decode()
    msg = msg.decode()
    print("sub_cb: received a msg: " + f"{topic}: {msg}")
    # do not do anything that publishes back to the same topic
    # otherwise, this will cause an infinite loop of msg exchanges
    if topic == cfg_topics.LOOKOUT_WEST_FAR:
        sub_lookout_west_far_cb(msg)
    elif topic == cfg_topics.LOOKOUT_WEST_NEAR:
        sub_lookout_west_near_cb(msg)
    elif topic == cfg_topics.LOOKOUT_EAST_NEAR:
        sub_lookout_east_near_cb(msg)
    elif topic == cfg_topics.LOOKOUT_EAST_FAR:
        sub_lookout_east_far_cb(msg)
    elif topic == cfg_topics.GATES_NORTH:
        sub_gate_north_cb(msg)
    elif topic == cfg_topics.GATES_SOUTH:
        sub_gate_south_cb(msg)
    elif topic == cfg_topics.MODE:
        sub_mode_cb(msg)
    else:
        print("sub_cb: no actions for this topic")


def sub_lookout_west_far_cb(msg):

    msg = int(msg)
    if msg not in [0, 1]:
        print("sub_lookout_west_far_cb: invalid received west_far lookout status")
        return
    if lookouts.west_far == msg:
        print("sub_lookout_west_far_cb: no change in received west_far lookout status")
        return
    lookouts.west_far = msg
    control.transition(str(lookouts))


def sub_lookout_west_near_cb(msg):
    msg = int(msg)
    if msg not in [0, 1]:
        print("sub_lookout_west_near_cb: invalid received west_near lookout status")
        return
    if lookouts.west_near == msg:
        print(
            "sub_lookout_west_near_cb: no change in received west_near lookout status"
        )
        return
    lookouts.west_near = msg
    control.transition(str(lookouts))


def sub_lookout_east_near_cb(msg):
    msg = int(msg)
    if msg not in [0, 1]:
        print("sub_lookout_east_near_cb: invalid received east_near lookout status")
        return
    if lookouts.east_near == msg:
        print(
            "sub_lookout_east_near_cb: no change in received east_near lookout status"
        )
        return
    lookouts.east_near = msg
    control.transition(str(lookouts))


def sub_lookout_east_far_cb(msg):
    msg = int(msg)
    if msg not in [0, 1]:
        print("sub_lookout_east_far_cb: invalid received east_far lookout status")
        return
    if lookouts.east_far == msg:
        print("sub_lookout_east_far_cb: no change in received east_far lookout status")
        return
    lookouts.east_far = msg
    control.transition(str(lookouts))


def sub_gate_north_cb(msg):
    msg = int(msg)
    if msg not in [0, 1]:
        print("sub_gate_north_cb: invalid received north gate status")
        return
    if gates.north == msg:
        print("sub_gate_north_cb: no change in received north gate status")
        return
    gates.north = msg


def sub_gate_south_cb(msg):
    msg = int(msg)
    if msg not in [0, 1]:
        print("sub_gate_south_cb: invalid received south gate status")
        return
    if gates.south == msg:
        print("sub_gate_south_cb: no change in received south gate status")
        return
    gates.south = msg


def sub_mode_cb(msg):
    if msg not in ["A", "M"]:
        print("sub_mode_cb: invalid mode")
        return
    if control.mode == msg:
        print("sub_mode_cb: no change in mode")
        return
    control.mode = msg


def button_thread():
    mode_toggle_button = Button(cfg_pins.MODE_TOGGLE, control.toggle_mode)
    gate_north_toggle_button = Button(cfg_pins.GATE_NORTH_TOGGLE, gates.toggle_north)
    gate_south_toggle_button = Button(cfg_pins.GATE_SOUTH_TOGGLE, gates.toggle_south)

    while True:
        mode_toggle_button.read_toggle()
        if control.mode == "M":
            gate_north_toggle_button.read_toggle()
            gate_south_toggle_button.read_toggle()
        time.sleep(0.01)


def display_thread():
    display = Display(control, gates)
    while True:
        display.update()
        time.sleep(0.01)


def main():
    global lookouts
    global gates
    global control

    mqtt_client = setup()

    lookouts = Lookouts(
        mqtt_client,
        cfg_topics.LOOKOUT_WEST_FAR,
        cfg_topics.LOOKOUT_WEST_NEAR,
        cfg_topics.LOOKOUT_EAST_NEAR,
        cfg_topics.LOOKOUT_EAST_FAR,
    )

    gates = Gates(mqtt_client, cfg_topics.GATES_NORTH, cfg_topics.GATES_SOUTH)

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

    control = Control(
        states=cfg_dfa.STATES,
        inputs=cfg_dfa.INPUTS,
        transitions=cfg_dfa.TRANSITIONS,
        state_actions=state_actions,
        initial_state="0",
        mqtt_client=mqtt_client,
        state_topic=cfg_topics.STATE,
        mode_topic=cfg_topics.MODE,
    )

    # do not subscribe to any topics until all the global variables needed by operations in sub_cb are set,
    # otherwise operations on these global variables will raise a nonetype error when a msg is received

    mqtt_client.set_callback(sub_cb)

    mqtt_client.subscribe(cfg_topics.LOOKOUT_WEST_FAR)
    mqtt_client.subscribe(cfg_topics.LOOKOUT_WEST_NEAR)
    mqtt_client.subscribe(cfg_topics.LOOKOUT_EAST_NEAR)
    mqtt_client.subscribe(cfg_topics.LOOKOUT_EAST_FAR)
    mqtt_client.subscribe(cfg_topics.GATES_NORTH)
    mqtt_client.subscribe(cfg_topics.GATES_SOUTH)
    mqtt_client.subscribe(cfg_topics.MODE)

    _thread.start_new_thread(display_thread, ())
    _thread.start_new_thread(button_thread, ())

    print("main: begin listening for msg...")
    last_ping = time.time()
    while True:
        mqtt_client.check_msg()
        # ping the broker every 60 seconds to keep the connection alive
        if time.time() - last_ping > 60:
            mqtt_client.ping()
            last_ping = time.time()
        time.sleep(0.01)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Exception: " + str(e))
        reset()
