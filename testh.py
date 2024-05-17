import numpy as np
from itertools import product
import time
import turns
from turns import Cube

start = time.time()

def seq(cb, moves):
    for mv in moves:
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
                dir = 2 if mv[1] == "2" else 1 if "'" not in mv[0] else -1
            cb.move(mv[0], 0, dir)

        '''
        print(ct + 1)
        ct += 1
        print(cube.stickers)'''
    return cb.stickers

moves = [
    'U', 'U\'', 'U2',
    'D', 'D\'', 'D2',
    'L', 'L\'', 'L2',  
    'R', 'R\'', 'R2',
    'F', 'F\'', 'F2',
    'B', 'B\'', 'B2',
    'M', 'M\'', 'M2'
]

#defines cube
c = Cube(3)
temp = Cube(3)
#stores initial (H perm) and solved state
solved = temp.stickers
h = ["M2", "U\'", "M2", "U2", "M2", "U\'", "M2"]
hperm = seq(Cube(3), h)
works = []

combos = product(moves, repeat=7)

ct = 0
for sequence in combos:
    newstate = seq(c, sequence)
    if np.array_equal(newstate, solved):
        works.append(sequence)
    
    #reset c
    c.stickers = hperm
    if ct % 100000 == 0:
        print(ct)
        print(sequence)
        print(time.time() - start)
    ct += 1

print(works)