import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.patches import Polygon

class Cube(object):
    facedict = {"U":0, "D":1, "F":2, "B":3, "R":4, "L":5}
    dictface = dict([(v, k) for k, v in facedict.items()])
    normals = [np.array([0., 1., 0.]), np.array([0., -1., 0.]),
               np.array([0., 0., 1.]), np.array([0., 0., -1.]),
               np.array([1., 0., 0.]), np.array([-1., 0., 0.])]
    # this xdirs has to be synchronized with the self.move() function
    xdirs = [np.array([1., 0., 0.]), np.array([1., 0., 0.]),
               np.array([1., 0., 0.]), np.array([-1., 0., 0.]),
               np.array([0., 0., -1.]), np.array([0, 0., 1.])]
    colordict = {"w":0, "y":1, "b":2, "g":3, "o":4, "r":5}
    pltpos = [(0., 1.05), (0., -1.05), (0., 0.), (2.10, 0.), (1.05, 0.), (-1.05, 0.)]

    def __init__(self, N, whiteplastic=False):
        """
        (see above)
        """
        self.N = N
        self.stickers = np.array([np.tile(i, (self.N, self.N)) for i in range(6)])
        self.stickercolors = ["w", "#ffcf00", "#00008f", "#009f0f", "#ff6f00", "#cf0000"]
        self.stickerthickness = 0.001 # sticker thickness in units of total cube size
        self.stickerwidth = 0.9 # sticker size relative to cubie size (must be < 1)
        if whiteplastic:
            self.plasticcolor = "#dfdfdf"
        else:
            self.plasticcolor = "#1f1f1f"
        self.fontsize = 12. * (self.N / 5.)
        return None
    
    def turn(self, f, d):
        """
        Turn whole cube (without making a layer move) around face `f`
        `d` 90-degree turns in the clockwise direction.  Use `d=3` or
        `d=-1` for counter-clockwise.
        """
        for l in range(self.N):
            self.move(f, l, d)
        return None

    def move(self, f, l, d):
        """
        Make a layer move of layer `l` parallel to face `f` through
        `d` 90-degree turns in the clockwise direction.  Layer `0` is
        the face itself, and higher `l` values are for layers deeper
        into the cube.  Use `d=3` or `d=-1` for counter-clockwise
        moves, and `d=2` for a 180-degree move..
        """
        i = self.facedict[f]
        l2 = self.N - 1 - l
        assert l < self.N
        ds = range((d + 4) % 4)
        if f == "U":
            f2 = "D"
            i2 = self.facedict[f2]
            for d in ds:
                self._rotate([(self.facedict["F"], range(self.N), l2),
                              (self.facedict["R"], range(self.N), l2),
                              (self.facedict["B"], range(self.N), l2),
                              (self.facedict["L"], range(self.N), l2)])
        if f == "D":
            return self.move("U", l2, -d)
        if f == "F":
            f2 = "B"
            i2 = self.facedict[f2]
            for d in ds:
                self._rotate([(self.facedict["U"], range(self.N), l),
                              (self.facedict["L"], l2, range(self.N)),
                              (self.facedict["D"], range(self.N)[::-1], l2),
                              (self.facedict["R"], l, range(self.N)[::-1])])
        if f == "B":
            return self.move("F", l2, -d)
        if f == "R":
            f2 = "L"
            i2 = self.facedict[f2]
            for d in ds:
                self._rotate([(self.facedict["U"], l2, range(self.N)),
                              (self.facedict["F"], l2, range(self.N)),
                              (self.facedict["D"], l2, range(self.N)),
                              (self.facedict["B"], l, range(self.N)[::-1])])
        if f == "L":
            return self.move("R", l2, -d)
        for d in ds:
            if l == 0:
                self.stickers[i] = np.rot90(self.stickers[i], 3)
            if l == self.N - 1:
                self.stickers[i2] = np.rot90(self.stickers[i2], 1)
        return None

    def _rotate(self, args):
        """
        Internal function for the `move()` function.
        """
        a0 = args[0]
        foo = self.stickers[a0]
        a = a0
        for b in args[1:]:
            self.stickers[a] = self.stickers[b]
            a = b
        self.stickers[a] = foo
        return None


"""
This file is part of the Magic Cube project.

license
-------
Copyright 2012 David W. Hogg (NYU).

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or (at
your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
02110-1301 USA.

usage
-----
- initialize a solved cube with `c = Cube(N)` where `N` is the side length.
- randomize a cube with `c.randomize(32)` where `32` is the number of random moves to make.
- make cube moves with `c.move()` and turn the whole cube with `c.turn()`.
- make figures with `c.render().savefig(fn)` where `fn` is the filename.
- change sticker colors with, eg, `c.stickercolors[c.colordict["w"]] = "k"`.

conventions
-----------
- This is a model of where the stickers are, not where the solid cubies are.  That's a bug not a feature.
- Cubes are NxNxN in size.
- The faces have integers and one-letter names. The one-letter face names are given by the dictionary `Cube.facedict`.
- The layers of the cube have names that are composed of a face letter and a number, with 0 indicating the outermost face.
- Every layer has two layer names, for instance, (F, 1) and (B, 1) are the same layer of a 3x3x3 cube; (F, 1) and (B, 3) are the same layer of a 5x5x5.
- The colors have integers and one-letter names. The one-letter color names are given by the dictionary `Cube.colordict`.
- Convention is x before y in face arrays, plus an annoying baked-in left-handedness.  Sue me.  Or fork, fix, pull-request.

"""