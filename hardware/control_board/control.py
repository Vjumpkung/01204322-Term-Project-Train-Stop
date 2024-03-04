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
    ):
        self._states = states
        self._inputs = inputs
        self._transitions = transitions
        self._state_actions = state_actions
        self._initial_state = initial_state
        self._mqtt_client = mqtt_client
        self._state_topic = state_topic
        self._mode_topic = mode_topic
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
            print("Control.mode.setter: invalid mode")
            return
        self._mode = mode
        print(f"Control.mode.setter: set mode to {self._mode}")

    def _publish_state(self):
        self._mqtt_client.publish(
            self._state_topic.encode(), self._current_state.encode(), retain=True
        )
        print(f"Control._publish_state: published state {self._current_state}")

    def _publish_mode(self):
        self._mqtt_client.publish(
            self._mode_topic.encode(), self._mode.encode(), retain=True
        )
        print(f"Control._publish_mode: published mode {self._mode}")

    def use_auto_mode(self):
        self.mode = "A"
        self._publish_mode()
        print(f"Control.use_auto_mode: published and set mode to {self._mode}")

    def use_manual_mode(self):
        self.mode = "M"
        self._publish_mode()
        print(f"Control.use_manual_mode: published and set mode to {self._mode}")

    def transition(self, _input):
        _input = str(_input)

        if _input not in self._inputs:
            print("Control.transition: invalid input")
            return

        if (self._current_state, _input) not in self._transitions:
            print("Control.transition: no state change")
            return

        self._current_state = self._transitions[(self._current_state, _input)]
        print(f"Control.transition: changed state to {self._current_state}")
        self._publish_state()

        if self._current_state not in self._state_actions:
            print("Control.transition: no actions for this state")
            return

        for action in self._state_actions[self._current_state]:
            respect_mode = action[0]
            if respect_mode and self._mode == "M":
                continue
            func = action[1]
            kwargs = action[2]
            print(f"Control.transition: calling state action {func.__name__}")
            func(**kwargs)
