import copy
import numpy as np
from itertools import product
import random
import turns
from turns import Cube

# applies the sequence "moves" onto the cube "cb"
def seq(cb, moves):
    for mv in moves:
        #if the move contains M, then deal with it separately
        if "M" in mv:
            if mv == "M\'":
                cb.move("R", 0, -1)
                cb.move("L", 0, 1)
                cb.turn("L", 1)
            elif mv == "M":
                cb.move("L", 0, -1)
                cb.move("R", 0, 1)
                cb.turn("R", 1)
            else:
                cb.move("L", 0, 2)
                cb.move("R", 0, 2)
                cb.turn("R", 2)
        else:
            dir = 1
            if len(mv) != 1:
                dir = 2 if mv[1] == "2" else 1 if "\'" not in mv[1] else -1
            cb.move(mv[0], 0, dir)

    return cb

# list of moves
moves = [
    'M', 'M\'', 'M2',
    'U', 'U\'', 'U2',
    'D', 'D\'', 'D2',
    'L', 'L\'', 'L2',  
    'R', 'R\'', 'R2',
    'F', 'F\'', 'F2',
    'B', 'B\'', 'B2'
]


# defines cubes
c = Cube(3)
temp = Cube(3)

# stores initial state (H perm) and the solved state
solved = temp.stickers

# defines h perm algorithm
alg = ["M2", "U\'", "M2", "U2", "M2", "U\'", "M2"]

# applies the h perm to a cube
hperm = seq(Cube(3), alg)

# initializes array of working sequences
works = []

# gets all length 7 permutations of moves
combos = product(moves, repeat=7)

# iterates over all sequences
for sequence in combos:
    c = copy.deepcopy(hperm)

    #generates the new state resulting from applying sequence on the cube
    newstate = seq(c, sequence)

    #if the newstate is the solved state, add it to works
    if np.array_equal(newstate.stickers, solved):
        works.append(sequence)

print("Final working solution:", works)
