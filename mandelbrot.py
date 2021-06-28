import colorsys
import random

from itertools import repeat
from multiprocessing import Pool
from matplotlib import colors
import numpy as np
from numba import jit


@jit
def get_col_with_move(args):
    iy, width, height, max_iterations, ZOOM, move_x, move_y = args
    result = np.zeros((1, width, 3))
    for ix in np.arange(width):
        x0 = ix * 3.0 / width * ZOOM - 2.0 + move_x
        y0 = iy * 2.0 / height * ZOOM - 1.0 + move_y
        x = 0.0
        y = 0.0
        for iteration in range(max_iterations):
            x_new = x * x - y * y + x0
            y = 2 * x * y + y0
            x = x_new

            if x * x + y * y > 4.0:
                # choose color and set
                color = [(iteration % 8) * 40.0, (16 - iteration % 16) * 16.0, (iteration % 16) * 16.0]
                break

        else:
            # failed, set color to black
            color = [0.0, 0.0, 0.0]

        result[0, ix] = color
    return result


@jit
def get_col(args):
    iy, width, height, a, b, max_iterations = args
    pixelX = b.real - a.real
    pixelY = b.imag - a.imag
    result = np.zeros((1, width, 3))
    for ix in np.arange(width):
        x0 = ix * pixelX / width + a.real
        y0 = iy * pixelY / height + a.imag
        x = 0.0
        y = 0.0
        for iteration in range(max_iterations):
            x_new = x * x - y * y + x0
            y = 2 * x * y + y0
            x = x_new

            if x * x + y * y > 4.0:
                color = [(iteration % 8) * 40.0, (16 - iteration % 16) * 16.0, (iteration % 16) * 16.0]
                break

        else:
            # failed, set color to black
            color = [0.0, 0.0, 0.0]

        result[0, ix] = color
    return result
