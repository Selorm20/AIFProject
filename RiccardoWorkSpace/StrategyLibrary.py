import AlgorithmLibrary as AL

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
    
    def __ProbabilityMonsterToStep(self, MonsterPosition, GoalPosition, StepNumber, SuccessorFunction):
        
        #Actual step
        KnowSteps = dict()
        KnowSteps[MonsterPosition] = 1
        
        #for i in range(max(StepGoals)):
        for _ in range(StepNumber):
            
            #New step to calculate
            NewKnowSteps = dict()
            
            #Dictionary for calculating all successor steps from actual steps
            SuccessorStepsDict = dict()
            for Step in KnowSteps: SuccessorStepsDict[Step] = SuccessorFunction(Step)
            
            #For each Actual step
            for ActualStep in KnowSteps:
                
                #For each next step from actual step
                for SuccessorStep in SuccessorStepsDict[ActualStep]:
                    
                    #Add value of actual step to value of next step
                    try: NewKnowSteps[SuccessorStep] += KnowSteps[ActualStep]
                    except KeyError: NewKnowSteps[SuccessorStep] = KnowSteps[ActualStep]
                    
            KnowSteps = NewKnowSteps
            
        #Calculate number of all paths to goal paths StepNumber steps
        try: AllGoalPathsNumber = KnowSteps[GoalPosition]
        except KeyError: AllGoalPathsNumber = 0
            
        #Calculate all paths aviable with StepNumber steps
        AllPathsNumber = sum(list(map(lambda x: KnowSteps[x], KnowSteps)))
    
        return AllGoalPathsNumber / AllPathsNumber 
    
    #This method represents calculate risk for a path
    def __CalculateRiskPathMonsters(self, Path, MonsterPositions, SuccessorFunction):
            
        StepRiskList = [[]]*len(Path)
        
        #For each step of our path, calculate total risk cost
        for i, Step in enumerate(Path):
            
            for MonsterPosition in MonsterPositions:
                StepRiskList[i].append(self.__ProbabilityMonsterToStep(MonsterPosition, Step, i, SuccessorFunction))
        
        #Apply formula for each step taking probability (for each monster) to be in i step   
        for i in range(len(StepRiskList)):
            
            #Formula start here
            AllNotP = 1
            for p in StepRiskList[i]: AllNotP *= 1-p
            StepRiskList[i] = 1 - AllNotP
        
        #Give like result sum of all risk cost of all steps
        return sum(StepRiskList)
    
    #Calculate next optimal point to choose
    def Calculate(self, ActualPosition, MonsterPositions):

        #Calculate all solutions from actual point (adding also)
        Solutions = self.__Calculator.CalculatePath(ActualPosition, [self.ActualGoal])[self.ActualGoal]
        if(self.__ActualPath not in Solutions and self.__ActualPath != []): Solutions = [self.__ActualPath] + Solutions
        
        Solutions.sort(key=lambda x: (self.__CalculateRiskPathMonsters(x, MonsterPositions, self.__SuccessorFunction), len(x)))
        
        self.__ActualPath = Solutions[0]
            
        return self.__ActualPath[1]