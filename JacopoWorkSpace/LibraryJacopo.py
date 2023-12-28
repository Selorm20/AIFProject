import numpy as np

def remove_black_border(image):
    rows = np.any(image != [0, 0, 0], axis=2).any(axis=1)
    cols = np.any(image != [0, 0, 0], axis=2).any(axis=0)

    image_without_borders = image[rows][:, cols, :]

    return image_without_borders
