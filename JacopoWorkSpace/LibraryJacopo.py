import numpy as np
from typing import Tuple
import matplotlib.pyplot as plt
import gym
import minihack

class Map:
    def __init__(self, state):
        self.__state = state
        
    def get_map_image(self):
        # Rimuovi il bordo nero
        image = self.__state['pixel']

        rows = np.any(image != [0, 0, 0], axis=2).any(axis=1)
        cols = np.any(image != [0, 0, 0], axis=2).any(axis=0)

        image_without_borders = image[rows][:, cols, :]
        
        return image_without_borders

    def view_map(self):
        # Ottieni l'immagine della mappa
        image = self.get_map_image()

        # Mostra la mappa
        plt.imshow(image)
        plt.show()


    
    def get_position_symbol(self, x, y):
        return chr(self.__state["chars"][x][y])

    def get_player_location(self, symbol : str = "@") -> Tuple[int, int]:
        x, y = np.where(self.__state["chars"] == ord(symbol))
        return (x[0], y[0])

    def get_monsters_location(self, symbol : str = "d"):
        x, y = np.where(self.__state["chars"] == ord(symbol))
        arr_returned = []
        for i in range(len(x)):
            position = (x[i], y[i])
            arr_returned.append(position)
        return arr_returned
    
def CreateLevel1():

    new_level = minihack.LevelGenerator(w = 11, h = 11)
    new_level.set_start_pos((5, 5))

    new_level.fill_terrain(type='fillrect',flag='L', x1 = 1, y1 = 1, x2 = 4, y2 = 4)
    new_level.fill_terrain(type='fillrect',flag='L', x1 = 6, y1 = 1, x2 = 9, y2 = 4)
    new_level.fill_terrain(type='fillrect',flag='L', x1 = 1, y1 = 6, x2 = 4, y2 = 9)
    new_level.fill_terrain(type='fillrect',flag='L', x1 = 6, y1 = 6, x2 = 9, y2 = 9)

    new_level.fill_terrain(type='fillrect',flag='.', x1 = 2, y1 = 2, x2 = 8, y2 = 8)

    new_level.add_monster(name='coyote',symbol='d', place=(0,0))
    # new_level.add_monster(name='wolf',symbol='d', place=(10,10))
    
    Enviroment = gym.make("MiniHack-Skill-Custom-v0", des_file = new_level.get_des(), observation_keys=("chars", "pixel"))

    state = Enviroment.reset()

    MapGame = Map(state)
    MapGame.view_map()
    
    return MapGame, Enviroment

def CreateLevel2():

    w=11
    h=11
    new_level = minihack.LevelGenerator(w = w, h = h)
    new_level.set_start_pos((6, 6))

    new_level.fill_terrain(type='fillrect',flag='.', x1 = 0, y1 = 0, x2 = w-1, y2 = h-1)
    for i in range(1,w,2):
        for j in range (1,w,2):    
            new_level.fill_terrain(type='fillrect',flag='L', x1=i, y1=j, x2=i, y2=j)

    new_level.add_monster(name='coyote',symbol='d', place=(0,0))
    # new_level.add_monster(name='wolf',symbol='d', place=(10,10))
    
    Enviroment = gym.make("MiniHack-Skill-Custom-v0", des_file = new_level.get_des(), observation_keys=("chars", "pixel"))

    state = Enviroment.reset()

    MapGame = Map(state)
    MapGame.view_map()
    
    return MapGame, Enviroment

def CreateLevel3():

    w=11
    h=11
    new_level = minihack.LevelGenerator(w = w, h = h)
    new_level.set_start_pos((6, 6))

    new_level.fill_terrain(type='fillrect',flag='.', x1 = 0, y1 = 0, x2 = w-1, y2 = h-1)    
    new_level.fill_terrain(type='fillrect',flag='L', x1=1, y1=6, x2=5, y2=6)
    new_level.fill_terrain(type='fillrect',flag='L', x1=5, y1=5, x2=9, y2=5)

    new_level.add_monster(name='coyote',symbol='d', place=(0,0))
    # new_level.add_monster(name='wolf',symbol='d', place=(10,10))
    
    Enviroment = gym.make("MiniHack-Skill-Custom-v0", des_file = new_level.get_des(), observation_keys=("chars", "pixel"))

    state = Enviroment.reset()

    MapGame = Map(state)
    MapGame.view_map()
    
    return MapGame, Enviroment