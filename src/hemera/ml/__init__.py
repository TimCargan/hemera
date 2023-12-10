import math

import numpy as np

# Constants
HOUR_SECONDS = 60 * 60
DAY_SECONDS = 24 * 60 * 60  # seconds in a day
YEAR_SECONDS = 365.2425 * DAY_SECONDS  # seconds in a day year


def scale_cord(cord, o_range, t_range):
    """
    Scale from cords with variable range to a 0 ... t_range
    :param cord: value to convert
    :param o_range: a tuple (min, max) of cord range
    :param t_range: max value in zero based target range
    :return: Scaled cord value
    """
    _range = o_range[1] - o_range[0]
    scale = t_range / _range
    s_cord = (cord - o_range[0]) * scale
    return int(s_cord)



def vectorize(speed, dir_deg=None, dir_rad=None):
    """
    Convert as speed and direction into its component vectors
    Args:
        speed: magnitude of vector
        dir_deg: direction in degrees
        dir_rad: direction in radians

    Returns: A tuple of (x_component, y_component)
    """
    # Convert to radians.
    if dir_rad is None:
        dir_rad = dir_deg * math.pi / 180

    # Calculate the x and y components.
    x_comp = speed * np.cos(dir_rad)
    y_comp = speed * np.sin(dir_rad)
    return x_comp, y_comp


def sin_cos_scale(col: np.ndarray, scale: float) -> (np.ndarray, np.ndarray):
    """
    Scale a cyclical value e.g. day of year, to a sin and cos function
    Args:
        col: The raw cyclic value to be transformed e.g. timestamps
        scale: periodicity of the raw cyclic value (in the same unit) e.g. for a daily cycle and hour of the day, 24, or 365 for a day of year.

    Returns: a tuple of (sin_component, cos_component)
    """
    sin = np.sin(col * (2 * math.pi / scale))
    cos = np.cos(col * (2 * math.pi / scale))
    return sin, cos

