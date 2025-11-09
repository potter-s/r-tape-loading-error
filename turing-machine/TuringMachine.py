#!/usr/bin/python3

class TuringMachine:
    def __init__(self, state=None, max_iterations=100):
        self.max_iterations = self.set_max_iterations(max_iterations)
        self.state_rules = StateRules()
        self.tape = Tape()
        self.from_states = set()
        self.to_states = set()
        self.configurable = True
        self.set_state(state)
        self.current_step = 0
        self.halted = False

    def set_max_iterations(self, mi):
        self.max_iterations = mi

    def set_state(self, state):
        """
        Sets initial machines state; if not set, the first machine
        state encountered in the M configuration is used
        """
        self.state = state
        if state:
            self.to_states.add(state)

    def read_char(self):
        return self.tape.read()

    def next(self, print=False):
        self.current_step += 1
        if self.current_step > self.max_iterations:
            self.halted = True
        if self.halt:
            return False
        char = self.read_char()
        next = self.state_rules.check_rule(self.state, char)
        if next.action[0] == 'Halt':
            self.halt = True
            return False

    def run(self, max_iterations=None, print=False):
        if max_iterations:
            self.set_max_iterations(max_iterations)
        while not self.halt:
            self.apply_rules(next)

    def finalise(self):
        self.check()
        self.configurable = False

    def add_state_rule(self, state, characters, new_state, actions):
        if not self.configurable:
            raise RuntimeError("Machine configuration already finalised")
        self.state_rules.add_rule(state, characters, new_state, actions)
        if not self.state:
            self.state = state
        self.from_states.add(state)
        self.to_states.add(new_state)

    def check(self):
        undef_states = ''.join(self.from_states - self.to_states)
        if undef_states:
            raise RuntimeError(f"Machine configuration error: state(s) used but not defined [{undef_states}]")

    def apply_state(self, next):
        self.state = next.state
        for action in next.actions:
            pass

#class State:
#def __init__(self, state, character):
#self.state = state
#self.actions = actions

class Next:
    def __init__(self, state, actions):
        self.state = state
        self.actions = actions

class StateRules:
    def __init__(self):
        self.rules = {}

    def add_rule(self, state, characters, new_state, actions):
        if not state in self.rules:
            self.rules[state] = {}
        if len(characters) > 0:
            for char in characters:
                self.rules[state][char] = Next(new_state, actions)
        else:
            self.rules[state][''] = Next(new_state, actions)

    def check_rule(self, state, character):
        if not state in self.rules:
            raise RuntimeError(f"Undefined state {state}")
        if '' in self.rules[state]:
            return self.rules[state]['']
        if character in self.rules[state]:
            return self.rules[state][character]
        else:
            raise RuntimeError(f"Undefined character {character} in state {state}")

class Tape:
    def __init__(self, window=5):
        self.tpos = 0
        self.window = window
        self.tape = [' ']

    def __str__(self):
        start = self.tpos - self.window
        if start < 0:
            self.extend_l(-start)
            start = 0
        end = self.tpos + self.window + 1
        if end > len(self.tape):
            self.extend_r(end - len(self.tape))
        frag = self.tape[start: end]
        return ''.join([f"[{x}]" for x in frag])

    def get_window(self):
        return self.window

    def set_window(self, w):
        self.window = w

    def extend_l(self, c):
        self.tape = [' '] * c + self.tape
        self.tpos += c

    def extend_r(self, c):
        self.tape = self.tape + [' '] * c

    def __repr__(self):
        return f"Tape of length {self.tlen} at position {self.tpos}"

    def len(self):
        return len(self.tape)

    def pos(self):
        return self.tpos

    def move(self, steps):
        if steps > 0:
            if self.tpos + steps >= len(self.tape):
                self.tape = self.tape + [' '] * (self.tpos + steps + 1 - len(self.tape))
        else:
            if self.tpos + steps < 0:
                self.tape = [' '] * (abs(steps) - self.tpos) + self.tape
                self.tpos -= steps
        self.tpos += steps

    def write(self, char):
        self.tape[self.tpos] = char

    def read(self):
        return self.tape[self.tpos]

    def L(self, steps=1):
        self.move(-steps)
        return self

    def R(self, steps=1):
        self.move(steps)
        return self
