from AlgorithmLibrary import *

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
        
        self.__Calculator = BFSPathSearch(SuccessorFunction)
        
        self.__ActualPath = []
        self.ActualGoal = None
        
    def GetSuccessorFunction(self):
        return self.__SuccessorFunction
        
    def GetActualPath(self):
        return list(self.__ActualPath)
        
    #This method represents calculate risk for a path
    def __CalculateRiskPathMonsters(self, Path, MonsterPositions, SuccessorFunction):
            
        StepRiskList = [0]*len(Path)
        
        #For each step of our path, calculate total risk cost
        for i, Step in enumerate(Path):
            
            #Calculate paths of all monsters
            MonsterPaths = self.__Calculator.CalculatePath(Step, MonsterPositions)
            MonsterPaths = list(map(lambda x: MonsterPaths[x][0], MonsterPaths.keys()))
            
            #For each monster, calculate cost considering our step and our monster
            for MonsterPath in MonsterPaths:
                RiskCost = 1
                
                #If monster has no enough step to take in time this Step, pass to next Path monster
                if(i < len(MonsterPath)): continue
                
                #Calculate risk of this path monster
                for StepMonster in MonsterPath: RiskCost *= 1/len(SuccessorFunction(StepMonster))
                
                #Add Risk cost of monster path to all risk cost of this step
                StepRiskList[i] += RiskCost
        
        #Give like result sum of all risk cost of all steps
        return sum(StepRiskList)
    
    #Calculate next optimal point to choose
    def Calculate(self, ActualPosition, MonsterPositions):

        #Update own actual solution if it is possible
        self.__ActualPath = ExtractSubPath(self.__ActualPath, ActualPosition, self.__ActualPath[-1])
        if(self.__ActualPath == None): self.__ActualPath = []
        
        #If there is no any calculated path
        if(self.__ActualPath == []):
            self.__ActualPath = self.__Calculator.CalculatePath(ActualPosition, [self.__ActualGoal])[self.__ActualGoal][0]
            return self.__ActualPath[0]
        
        #Calculate all solutions from actual point (adding also)
        Solutions = self.__Calculator.CalculatePath(ActualPosition, [self.__ActualGoal])[self.__ActualGoal]
        if(self.__ActualPath not in Solutions): Solutions = [self.__ActualPath] + Solutions
        
        Solutions.sort(key=lambda x: (self.__CalculateRiskPathMonsters(x, MonsterPositions, self.__SuccessorFunction), len(x)))
        
        self.__ActualPath = Solutions[0]
            
        return self.__ActualPath[0]