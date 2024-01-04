class RiskCostProbabyilityFunction:
    def __init__(self, SuccessorFunction):
        self.__SuccessorFunction = SuccessorFunction
    
    def __call__(self, Path, MonsterPositions):
        return self.__CalculateRiskPathMonsters(Path, MonsterPositions)   
   
    def __ProbabilityMonsterToStep(self, MonsterPosition, GoalPosition, StepNumber):
        
        #Actual step
        KnowSteps = dict()
        KnowSteps[MonsterPosition] = 1
        
        for _ in range(StepNumber):
            
            #New step to calculate
            NewKnowSteps = dict()
            
            #Dictionary for calculating all successor steps from actual steps
            SuccessorStepsDict = dict()
            for Step in KnowSteps: SuccessorStepsDict[Step] = self.__SuccessorFunction(Step)
            
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
    def __CalculateRiskPathMonsters(self, Path, MonsterPositions):
            
        StepRiskList = [[]]*len(Path)
        
        #For each step of our path, calculate total risk cost
        for i, Step in enumerate(Path):
            
            for MonsterPosition in MonsterPositions:
                StepRiskList[i].append(self.__ProbabilityMonsterToStep(MonsterPosition, Step, i))
        
        #Apply formula for each step taking probability (for each monster) to be in i step
        for i in range(len(StepRiskList)):
            
            #Formula start here
            AllNotP = 1
            for p in StepRiskList[i]: AllNotP *= 1-p
            StepRiskList[i] = 1 - AllNotP
        
        #Give like result mean of all probabilities of steps
        return sum(StepRiskList) / len(Path)
    
    
    
    
    
    
class RiskCostWorstCaseFunction:
    def __init__(self, SuccessorFunction):
        
        self.__SuccessorFunction = SuccessorFunction
        
    def __call__(self, Path, MonsterPositions, step):
        RiskCost = 0
        if step==0:
            for i in range(len(Path)-1):
                if i==0:
                    RiskCost += 1000 * self.__n_monsters_there(Path[1],MonsterPositions,0)
                if i==1:
                    RiskCost += 10 * self.__n_monsters_there(Path[2],MonsterPositions,1)
                elif i==2:
                    RiskCost += 5 * self.__n_monsters_there(Path[3],MonsterPositions,2)
                else:
                    RiskCost += 1 * self.__n_monsters_there(Path[i+1],MonsterPositions,i)
        else :
            for i in range(len(Path)-1):
                if i==0:
                    RiskCost += 1000 * self.__n_monsters_there(Path[1],MonsterPositions,1)
                if i==1:
                    RiskCost += 10 * self.__n_monsters_there(Path[2],MonsterPositions,2)
                elif i==2:
                    RiskCost += 5 * self.__n_monsters_there(Path[3],MonsterPositions,3)
                else:
                    RiskCost += 1 * self.__n_monsters_there(Path[i+1],MonsterPositions,i+1)
                    
        return RiskCost
    
    def __n_monsters_there(self, Position, MonsterPositions, n_steps):
        n_monsters = 0
        for StartPoint in MonsterPositions:
            ActualPoints = set()
            ActualPoints.add(StartPoint)
            for i in range(n_steps):
                KnewPoints = set()
                for Point in ActualPoints:
                    for NewPoint in self.__SuccessorFunction(Point):
                        KnewPoints.add(NewPoint)
                ActualPoints = KnewPoints
            if Position in ActualPoints:
                n_monsters += 1
        return n_monsters

