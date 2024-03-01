from machine import Pin


class Button:

    def __init__(self, pin_number, control):
        self._last_reading = 1
        self._last_state = 1
        self._current_state = 1
        self._steady_count = 0
        self._pin = Pin(pin_number, Pin.IN, Pin.PULL_UP)
        self._control = control

    def read_toggle_mode(self):
        reading = self._pin.value()
        if reading == self._last_reading:
            self._steady_count += 1
            self._last_reading = reading
        else:
            self._steady_count = 0
            self._last_reading = reading
            return
        if self._steady_count == 5:
            self._steady_count = 0
            self._last_state = self._current_state
            self._current_state = reading
            if self._last_state == 1 and self._current_state == 0:
                self._control.toggle_mode()
