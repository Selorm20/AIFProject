import numpy as np
from typing import Tuple

def remove_black_border(image):
    rows = np.any(image != [0, 0, 0], axis=2).any(axis=1)
    cols = np.any(image != [0, 0, 0], axis=2).any(axis=0)

    image_without_borders = image[rows][:, cols, :]

    return image_without_borders

def get_player_location(game_map: np.ndarray, symbol : str = "@") -> Tuple[int, int]:
    x, y = np.where(game_map == ord(symbol))
    return (x[0], y[0])

def get_target_location(game_map: np.ndarray, symbol : str = ">") -> Tuple[int, int]:
    x, y = np.where(game_map == ord(symbol))
    return (x[0], y[0])

def get_monsters_location(game_map: np.ndarray, symbol : str = "d"):
    x, y = np.where(game_map == ord(symbol))
    arr_returned = []
    for i in range(len(x)):
        position = (x[i],y[i])
        arr_returned.append(position)
    return arr_returned