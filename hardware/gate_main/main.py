from machine import Pin, reset
from time import time, sleep
import _thread
from mqtt_setup import setup
from servo import Servo


CROSSING_ID = "crossing1"

GATE_DIRECTION = "north"

GATE_TOPIC = f"{CROSSING_ID}/gates/{GATE_DIRECTION}"

GATE_OPEN_COMMAND = "1"
GATE_CLOSE_COMMAND = "0"

GATE_OPEN_STATUS = 90
GATE_CLOSE_STATUS = 0

BUZZER_GPIO_PIN = 21
SERVO_GPIO_PIN = 22


gate_status = -1  # init
count = 0  # count number of command got

motor = Servo(pin=SERVO_GPIO_PIN)
motor.update_settings(
    servo_pwm_freq=50,
    min_u10_duty=26,
    max_u10_duty=123,
    min_angle=0,
    max_angle=180,
    pin=SERVO_GPIO_PIN,
)


def angle_to_status(angle: int):
    if angle == GATE_OPEN_STATUS:
        return "Open"
    elif angle == GATE_CLOSE_STATUS:
        return "Close"
    return "wrong =ω="


def buzzer_thread():
    buzzer = Pin(BUZZER_GPIO_PIN, Pin.OUT)
    while True:
        if gate_status == GATE_OPEN_STATUS:
            buzzer.value(0)
            sleep(0.01)
            continue
        buzzer.value(1)
        sleep(0.5)
        buzzer.value(0)
        sleep(0.5)


def callback_func(topic, msg):
    global gate_status, count
    msg2 = msg.decode()

    count += 1
    if count == 1:  ## i don't know bug fix
        print(
            f" first not count {topic.decode()} command: {msg2}, angle:{gate_status} {angle_to_status(gate_status)}"
        )
        return

    if topic.decode() == GATE_TOPIC:
        if msg2 == GATE_OPEN_COMMAND:
            gate_status = GATE_OPEN_STATUS
        elif msg2 == GATE_CLOSE_COMMAND:
            gate_status = GATE_CLOSE_STATUS
        else:
            print("wrong gate angle (this should not happened)")
            gate_status = 45
        motor.move(gate_status)
    else:
        print("wrong topic you fool")

    print(
        f"{count}# {topic.decode()} command: {msg2}, angle:{gate_status} {angle_to_status(gate_status)}"
    )


def main():
    global gate_status

    mqtt_client = setup()
    mqtt_client.set_callback(callback_func)
    mqtt_client.subscribe(GATE_TOPIC)
    # client.publish(GATES_TOPIC.encode(), GATE_OPEN_COMMAND.encode(), retain=True)

    _thread.start_new_thread(buzzer_thread, ())

    last_ping = time()
    while True:
        # print("running")
        mqtt_client.check_msg()

        if time() - last_ping > 60:
            # ping the broker every 60 seconds to keep the connection alive
            mqtt_client.ping()
            last_ping = time()

        sleep(0.01)


if __name__ == "__main__":
    try:
        main()
    except OSError as e:
        print("Error: " + str(e))
        reset()
