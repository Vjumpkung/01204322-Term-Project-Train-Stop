import machine
from machine import Pin
import mqtt_setup as mqtt
from time import sleep
from servo import Servo
from load_config import CROSSINGID

GATE_DIRECTION = "north"
GATES_TOPIC = f"{CROSSINGID}/gates/{GATE_DIRECTION}"
GATE_OPEN_COMMAND = "1"
GATE_CLOSE_COMMAND = "0"
GATE_OPEN_STATUS = 90
GATE_CLOSE_STATUS = 0

BUZZER_GPIO_PIN = 21
SERVO_GPIO_PIN = 22
gate_status = -1 # 

count = -1 # count number of command got



motor = Servo(pin=SERVO_GPIO_PIN)
motor.update_settings(
    servo_pwm_freq=50,
    min_u10_duty=26,
    max_u10_duty=123,
    min_angle=0,
    max_angle=180,
    pin=SERVO_GPIO_PIN,
)


buzzer = Pin( BUZZER_GPIO_PIN, Pin.OUT )

def func(topic, msg):
    global gate_status,count
    msg2 = msg.decode()
    
    count +=1
    if count == 0: ## i don't know bug fix
        print(f" first {topic.decode()} command: {msg2}, angle:{gate_status}")
        return
    
    if topic.decode() == GATES_TOPIC:
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
        
    print(f"{topic.decode()} command: {msg2}, angle:{gate_status}")



def move_servo_test():
    while 1:
        for i in range(91):
            motor.move(i)
            sleep(0.01)
        for i in range(90, 0, -1):
            motor.move(i)
            sleep(0.01)


def main():
    client = mqtt.setup()
    client.set_callback(func)
    client.subscribe(GATES_TOPIC)
    global gate_status
    # client.publish(GATES_TOPIC.encode(), GATE_OPEN_COMMAND.encode(), retain=True)
    while(1):
        # print("running")
        client.check_msg()
        if gate_status == GATE_CLOSE_STATUS: # gate close , sound the buzzer
            buzzer.value(not buzzer.value())
        elif buzzer.value() != 0: # 
            buzzer.value(0)
            
        sleep(0.5)
        
    


    


if __name__ == "__main__":
    try:
        main()
    except OSError as e:
        print("Error: " + str(e))
        machine.reset()


