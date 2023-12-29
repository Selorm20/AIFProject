import RiccardoWorkSpace.AlgorithmLibrary as AL

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
    def __CalculateRiskPathMonsters(self, Path, MonsterPositions, SuccessorFunction):
            
        RiskCost = 0
        
        #For each monster
        for StartPoint in MonsterPositions:
            
            ActualPoints = set()
            ActualPoints.add(StartPoint)
            
            #For each step of path, calculate position where monster can be
            for StepPath in Path:
                
                KnewPoints = set()
                
                for Point in ActualPoints:
                    for NewPoint in SuccessorFunction(Point):
                        KnewPoints.add(NewPoint)
                
                ActualPoints = KnewPoints
                
                #If monster can be in this step of path
                if(StepPath in ActualPoints): RiskCost += 1
                
        return RiskCost
    
    #Calculate next optimal point to choose
    def Calculate(self, ActualPosition, MonsterPositions):
        
        #Calculate all solutions from actual point (adding also)
        Solutions = self.__Calculator.CalculatePath(ActualPosition, [self.ActualGoal])[self.ActualGoal]
        if(self.__ActualPath not in Solutions and self.__ActualPath != []): Solutions = [self.__ActualPath] + Solutions
        
        Solutions.sort(key=lambda x: (self.__CalculateRiskPathMonsters(x, MonsterPositions, self.__SuccessorFunction), len(x)))
        
        self.__ActualPath = Solutions[0]
            
        return self.__ActualPath[1]