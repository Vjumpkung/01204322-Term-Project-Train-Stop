class Control:
    def __init__(
        self,
        states,
        inputs,
        transitions,
        state_actions,
        initial_state,
        mqtt_client,
        state_topic,
        mode_topic,
        debug=False,
    ):
        self._states = states
        self._inputs = inputs
        self._transitions = transitions
        self._state_actions = state_actions
        self._initial_state = initial_state
        self._mqtt_client = mqtt_client
        self._state_topic = state_topic
        self._mode_topic = mode_topic
        self._debug = debug
        self._current_state = initial_state
        self._mode = "A"
        self._publish_state()
        self._publish_mode()

    @property
    def current_state(self):
        return self._current_state

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        mode = str(mode)
        if mode not in ["A", "M"]:
            if self._debug:
                print("Control.mode.setter: invalid mode")
            return
        self._mode = mode
        if self._debug:
            print(f"Control.mode.setter: set mode to {self._mode}")

    def _publish_state(self):
        self._mqtt_client.publish(
            self._state_topic.encode(), self._current_state.encode(), retain=True
        )
        if self._debug:
            print(f"Control._publish_state: published state {self._current_state}")

    def _publish_mode(self):
        self._mqtt_client.publish(
            self._mode_topic.encode(), self._mode.encode(), retain=True
        )
        if self._debug:
            print(f"Control._publish_mode: published mode {self._mode}")

    def toggle_mode(self):
        if self._mode == "A":
            self._mode = "M"
        else:
            self._mode = "A"
        self._publish_mode()
        if self._debug:
            print(f"Control.toggle_mode: set mode to {self._mode}")

    def transition(self, _input):
        _input = str(_input)

        if _input not in self._inputs:
            if self._debug:
                print("Control.transition: invalid input")
            return

        if (self._current_state, _input) not in self._transitions:
            if self._debug:
                print("Control.transition: no state change")
            return

        self._current_state = self._transitions[(self._current_state, _input)]
        if self._debug:
            print(f"Control.transition: changed state to {self._current_state}")
        self._publish_state()

        if self._mode == "M":
            if self._debug:
                print(
                    "Control.transition: mode is manual, no state action will be executed"
                )
            return

        if self._current_state in self._state_actions:
            f = self._state_actions[self._current_state]
            if self._debug:
                print(f"Control.transition: executing state action {f.__name__}")
            f()
