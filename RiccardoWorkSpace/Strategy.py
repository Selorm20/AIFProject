from RiccardoWorkSpace.Path import Path
import random

class Strategy:
    def __init__(self, SuccessorFunction, CalculatePathsFunction, CalculateRiskFunction):
        
        self.__SuccessorFunction = SuccessorFunction
        self.__CalculatorRiskFunctionPath = CalculateRiskFunction
        self.__CalculatorPaths = CalculatePathsFunction
    
        self.__ActualPath = []
        self.ActualGoal = None
        
    def GetActualPath(self):
        return self.__ActualPath
        
    def Calculate(self, ActualPosition, MonsterPositions):
        
        #Calculate all paths, with own risks
        Paths = self.__CalculatorPaths(ActualPosition, self.ActualGoal)
        
        Paths = [Path(x, self.__CalculatorRiskFunctionPath(x, MonsterPositions)) for x in Paths]
        Paths.sort(key=lambda x: (x.GetRiskCost(), len(x.GetPath())))
        
        print("Paths calculated: ")
        for i in Paths: print(i)
        
        #Extract all paths with 0 risk cost
        PathsRiskZero = list(filter(lambda x: x.GetRiskCost() == 0, Paths))
        
        #If exists 1 or more paths with 0 risk cost, choose one
        if(len(PathsRiskZero) > 0):
            self.__ActualPath = PathsRiskZero[0]
            return self.__ActualPath[1]
        
        #Otherwise try with other strategy
        
        #Calculate possible position of monster for next and next next moves
        NextMovePositionMonsters = set() #Next move
        NextMoveDangerPoints = set() #Next next move
        
        for MonsterPosition in MonsterPositions:
            NextMovePositionMonsters.union(set(self.__SuccessorFunction(MonsterPosition)))
        
        for NextMovePositionMonster in NextMovePositionMonsters: 
            NextMoveDangerPoints.union(set(self.__SuccessorFunction(NextMovePositionMonster)))
        
        #Associated value to every possible next step       
        PossibleChoices = self.__SuccessorFunction(ActualPosition)
        
        print(f"NextMovePositionMonsters: {NextMovePositionMonsters}")
        print(f"NextMoveDangerPoints: {NextMoveDangerPoints}")
        
        UtilityList = [0]*len(PossibleChoices)
        
        for i in PossibleChoices:
            UtilityList.append(len(set(self.__SuccessorFunction(i)).difference(NextMoveDangerPoints).difference(NextMovePositionMonsters)))
        
        #Choose the best step to consider
        StepsToConsider = []
        
        for i, value in enumerate(UtilityList):
            if(value == min(UtilityList)): StepsToConsider.append(PossibleChoices[i])
            
        print("Possible choices to consider:")
        for i in PossibleChoices: print(i)
         
        #Choose the best path cosidering best steps already choosed (list is already sorted by risk cost)
        PathsToConsider = list(filter(lambda x: x[1] in StepsToConsider, Paths))
        
        print(f"Paths to consider:")
        for i in PathsToConsider: print(i)
        
        try: self.__ActualPath = PathsToConsider[0]
        except: self.__ActualPath = [ActualPosition, random.choice(PossibleChoices)]
        
        return self.__ActualPath[1]