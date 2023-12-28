# Create a class of character actions and define them
from typing import List, Tuple

class CharacterActions:
    def __init__(self, env):
        self.env = env
        self.actions = []

    def move(self, direction):
       
     self.actions.append(self.env.actions.move(direction))

    def attack(self, target):
        
     self.actions.append(self.env.actions.attack(target))

    def wait(self):
       
     self.actions.append(self.env.actions.wait())

    def skill_use(self, skill_name, target):
        
        
     self.actions.append(self.env.actions.skill_use(skill_name, target))

    def item_use(self, item_name, target):
       
     self.actions.append(self.env.actions.item_use(item_name, target))

    def get_actions(self):
       
        return self.actions

    def clear_actions(self):
        
        self.actions = []
    
   
def actions_from_path(start: Tuple[int, int], path: List[Tuple[int, int]]) -> List[int]:
    action_map = {
        "N": 0,
        "E": 1,
        "S": 2,
        "W": 3
    }
    actions = []
    x_s, y_s = start
    for (x, y) in path:
        if x_s == x:
            if y_s > y:
                actions.append(action_map["W"])
            else:
                actions.append(action_map["E"])
        elif y_s == y:
            if x_s > x:
                actions.append(action_map["N"])
            else:
                actions.append(action_map["S"])
        else:
            raise Exception("x and y can't change at the same time. Oblique moves not allowed!")
        x_s = x
        y_s = y

    return actions