import RiccardoWorkSpace.AlgorithmLibrary as AL
import RiccardoWorkSpace.functions as FUN

def ExtractSubPath(Path, Point1, Point2):
    try:
        i1 = Path.index(Point1)
        i2 = Path.index(Point2)
    except: return None
    
    if(i1 == i2): return Path[i1]
    if(i1 < i2): return Path[i1: i2]
    if(i1 > i2): return Path[i2: i1: -1]

#Considering that all monsters can move only with step for each turn
#Considering that all monsters has same damage points
class Strategy:
    def __init__(self, SuccessorFunction):   
        
        self.__SuccessorFunction = SuccessorFunction

        self.__Calculator = AL.BFSPathSearch(SuccessorFunction)
                
        self.__ActualPath = []
        self.ActualGoal = None
        
    def GetSuccessorFunction(self):
        return self.__SuccessorFunction
        
    def GetActualPath(self):
        return list(self.__ActualPath)
    
    #This method represents calculate risk for a path
    def __CalculateRiskPathMonsters(self, Path, MonsterPositions, SuccessorFunction, step):
        RiskCost = 0
        if step==0:
            for i in range(len(Path)-1):
                if i==0:
                    RiskCost += 1000 * FUN.n_monsters_there(Path[1],MonsterPositions,SuccessorFunction,0)
                if i==1:
                    RiskCost += 10 * FUN.n_monsters_there(Path[2],MonsterPositions,SuccessorFunction,1)
                elif i==2:
                    RiskCost += 5 * FUN.n_monsters_there(Path[3],MonsterPositions,SuccessorFunction,2)
                else:
                    RiskCost += 1 * FUN.n_monsters_there(Path[i+1],MonsterPositions,SuccessorFunction,i)
        else :
            for i in range(len(Path)-1):
                if i==0:
                    RiskCost += 1000 * FUN.n_monsters_there(Path[1],MonsterPositions,SuccessorFunction,1)
                if i==1:
                    RiskCost += 10 * FUN.n_monsters_there(Path[2],MonsterPositions,SuccessorFunction,2)
                elif i==2:
                    RiskCost += 5 * FUN.n_monsters_there(Path[3],MonsterPositions,SuccessorFunction,3)
                else:
                    RiskCost += 1 * FUN.n_monsters_there(Path[i+1],MonsterPositions,SuccessorFunction,i+1)
                    
        return RiskCost
    
    #Calculate next optimal point to choose
    def Calculate(self, ActualPosition, MonsterPositions, n_paths, version, step):
        vers = {"v1":self.__Calculator.CalculatePath_v1, "v2":self.__Calculator.CalculatePath_v2, "v3":self.__Calculator.CalculatePath_v3 }
        Solutions = vers[version](ActualPosition, self.ActualGoal, n_paths, MonsterPositions, self.__SuccessorFunction)
        Solutions.sort(key=lambda x: (self.__CalculateRiskPathMonsters(x, MonsterPositions, self.__SuccessorFunction, step), len(x)))
        for i in Solutions:
            print(i, self.__CalculateRiskPathMonsters(i, MonsterPositions, self.__SuccessorFunction, step))

        self.__ActualPath = Solutions[0]
            
        return self.__ActualPath[1], self.__CalculateRiskPathMonsters(Solutions[0],MonsterPositions,self.__SuccessorFunction,step)
    
    def where_will_wolf_go(self, WolfPositions,CharacterPosition):
        Solution = []
        for i in WolfPositions:
            Solution.append(self.__Calculator.CalculatePath_base(i, CharacterPosition, 1))
        return Solution