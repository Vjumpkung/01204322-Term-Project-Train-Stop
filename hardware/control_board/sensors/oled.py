from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

i2c = I2C(1, scl=Pin(22), sda=Pin(21), freq=100000)
display = SSD1306_I2C(128, 64, i2c)


def init_display():
    display.fill(0)
    display.text("ESP32 Started...", 0, 0)
    display.show()
