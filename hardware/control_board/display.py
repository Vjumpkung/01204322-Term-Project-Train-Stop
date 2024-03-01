from machine import Pin, I2C
from ssd1306 import SSD1306_I2C


class Display:

    def __init__(self, control, gates):
        self._control = control
        self._gates = gates
        self._i2c = I2C(1, scl=Pin(22), sda=Pin(21), freq=100000)
        self._oled = SSD1306_I2C(128, 64, self._i2c)
        self._oled.init_display()

    def update(self):
        self._oled.fill(0)
        self._oled.text(
            "Mode: " + ("Auto" if self._control.mode == "A" else "Manual"), 0, 0
        )
        self._oled.text("", 0, 10)
        self._oled.text("Gates", 0, 20)
        self._oled.text(
            "North: " + ("Open" if self._gates.north == 1 else "Closed"), 0, 30
        )
        self._oled.text(
            "South: " + ("Open" if self._gates.south == 1 else "Closed"), 0, 40
        )
        self._oled.show()
