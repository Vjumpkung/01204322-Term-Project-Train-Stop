class DFA:
    def __init__(self, states, inputs, transitions, state_publisher, state_actions, initial_state):
        self.states = states
        self.inputs = inputs
        self.transitions = transitions
        self.state_publisher = state_publisher
        self.state_actions = state_actions
        self.initial_state = initial_state
        self.current_state = initial_state

    def transition(self, _input):
        if _input not in self.inputs:
            print("DFA.transition: input is invalid")
            return
        if (self.current_state, _input) not in self.transitions:
            print("DFA.transition: state didn't change")
            return
        self.current_state = self.transitions[(self.current_state, _input)]
        print(f"DFA.transition: state changed to {self.current_state}")
        self.state_publisher(self.current_state)
        if self.current_state not in self.state_actions:
            print("DFA.transition: no actions for this state")
            return
        for action in self.state_actions[self.current_state]:
            func = action[0]
            kwargs = action[1]
            func(**kwargs)

    def reset(self):
        self.current_state = self.initial_state
