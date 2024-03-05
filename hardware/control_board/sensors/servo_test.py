from time import sleep
from servo import Servo


motor = Servo(pin=22)
motor.update_settings(
    servo_pwm_freq=50,
    min_u10_duty=26,
    max_u10_duty=123,
    min_angle=0,
    max_angle=180,
    pin=22,
)


def move_servo_test():
    while 1:
        for i in range(91):
            print(i)
            motor.move(i)
            sleep(0.01)
        for i in range(90, 0, -1):
            print(i)
            motor.move(i)
            sleep(0.01)
