#!/usr/bin/python3

import random
import sys
import TuringMachine

n1 = random.randint(1,10)
n2 = random.randint(1,10)

tape = TuringMachine.Tape(data = ['1'] * n1 + [' '] + ['1'] * n2)
print("Adding", n1, "and", n2)
print("Created tape:", tape)

tm = TuringMachine.TuringMachine()
tm.load(tape)

tm.add_state_rule('A', '1', 'A', 'R')
tm.add_state_rule('A', ' ', 'B', 'P1;R')
tm.add_state_rule('B', '1', 'B', 'R')
tm.add_state_rule('B', ' ', 'C', 'L')
tm.add_state_rule('C', '1', 'D', 'P ;H')
tm.finalise()
tm.run()

print("Result", sum([int(x) for x in tape.data if x == '1']))

print("End tape:", tape)
