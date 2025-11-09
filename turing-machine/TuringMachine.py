#!/usr/bin/python3

class TuringMachine:
    def __init__(self, state=None, max_iterations=100):
        self.set_max_iterations(max_iterations)
        self.state_rules = StateRules()
        self.tape = TapeRecorder()
        self.from_states = set()
        self.to_states = set()
        self.configurable = True
        self.set_state(state)
        self.current_step = 0
        self.halted = False

    def set_max_iterations(self, max_iterations):
        self.max_iterations = max_iterations

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
        if self.current_step > self.max_iterations:
            self.halted = True
        next = self.state_rules.check_rule(self.state, self.tape.read())
        if not next:
            self.halted = True
        if next.instructions[0] == 'H':
            self.halted = True
        if self.halted:
            return False
        self.apply_state(next)
        self.current_step += 1

    def run(self, max_iterations=None, print=False):
        while not self.halted:
            self.next()

    def finalise(self):
        self.check()
        self.configurable = False

    def add_state_rule(self, state, characters, new_state, instructions):
        if not self.configurable:
            raise RuntimeError("Machine configuration already finalised")
        self.state_rules.add_rule(state, characters, new_state, instructions)
        if not self.state:
            self.state = state
        self.from_states.add(state)
        self.to_states.add(new_state)

    def check(self):
        undef_states = ''.join(self.from_states - self.to_states)
        if undef_states:
            raise RuntimeError(f"Machine configuration error: state(s) used but not defined [{undef_states}]")

    def next_state(self):
        return self.state_rules.check_rule(self.state, self.tape.read)

    def apply_state(self, next):
        self.state = next.state
        for instruction in next.instructions:
            if instruction == 'L':
                self.tape.L()
            elif instruction == 'R':
                self.tape.R()
            elif instruction.startswith('P') and len(instruction) == 2:
                self.tape.write(instruction[1])
            else:
                raise RuntimeError(f"Undefined instruction {instruction}")

class Action:
    def __init__(self, state, instructions):
        self.state = state
        self.instructions = instructions

class StateRules:
    def __init__(self):
        self.rules = {}

    def add_rule(self, state, characters, new_state, instructions):
        if not state in self.rules:
            self.rules[state] = {}
        if len(characters) > 0:
            for char in characters:
                self.rules[state][char] = Action(new_state, instructions)
        else:
            self.rules[state][''] = Action(new_state, instructions)

    def check_rule(self, state, character):
        if not state in self.rules:
            raise RuntimeError(f"Undefined state {state}")
        if '' in self.rules[state]:
            return self.rules[state]['']
        if character in self.rules[state]:
            return self.rules[state][character]
        else:
            raise RuntimeError(f"Undefined character {character} in state {state}")

class TapeRecorder:
    def __init__(self, window=5):
        self.tpos = 0
        self.window = window
        self.tape = [' ']

    def __str__(self):
        start = self.tpos - self.window
        if start < 0:
            self._extend_l(-start)
            start = 0
        end = self.tpos + self.window + 1
        if end > len(self.tape):
            self._extend_r(end - len(self.tape))
        frag = self.tape[start: end]
        return ''.join([f"[{x}]" for x in frag])

    def set_window(self, w):
        self.window = w

    def _extend_l(self, c):
        self.tape = [' '] * c + self.tape
        self.tpos += c

    def _extend_r(self, c):
        self.tape = self.tape + [' '] * c

    def __repr__(self):
        return f"Tape of length {len(self.tape)} at position {self.tpos}"

    def len(self):
        return len(self.tape)

    def pos(self):
        return self.tpos

    def move_tape(self, steps):
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
        self.move_tape(-steps)
        return self

    def R(self, steps=1):
        self.move_tape(steps)
        return self
