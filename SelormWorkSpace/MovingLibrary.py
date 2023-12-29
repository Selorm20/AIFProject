class Moving:
    def __init__(self, env):
        self.__env = env
        
    
    #Do next position to enviroment
    
    def Move(self, ActualPosition, NextPosition):
        Moves = {
            0: (-1, 0), #moveUp
            1: (1, 0),  #moveDown
            2: (0, -1), #moveLeft
            3: (0, 1)   #moveRight
        } 

        if NextPosition in Moves:
            coordinates = Moves[NextPosition]
            new_position = (ActualPosition[0] + coordinates[0], ActualPosition[1] + coordinates[1])
            
            #return True if move is done
            if self.move_is_valid(new_position):
                ActualPosition = new_position
                print("Moved to {ActualPosition}")
                return True
            
            #return False if move is not done after call this method
            else:
                print("Move invalid. Try another")
            
            return False
        
        #Defining the move_valid variable to make sure agent stays in environment
        def move_is_valid(self, new_position):
            return 0 <= new_position[0] < len(self.__env) and 0 <= new_position[1] < len(self.__env[0])
        
        
    



    
    