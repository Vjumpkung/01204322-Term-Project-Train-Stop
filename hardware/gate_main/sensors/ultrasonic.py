from hcsr04 import HCSR04

ultrasonic = HCSR04(trigger_pin=19, echo_pin=18, echo_timeout_us=10000)


def get_ultra_distance():
    return ultrasonic.distance_cm()
