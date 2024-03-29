from RiccardoWorkSpace.Path import Path
from RiccardoWorkSpace.AlgorithmLibrary import SearchNode
import random

import RiccardoWorkSpace.AlgorithmLibrary as AL
from itertools import product

class Strategy:
    def __init__(self, CalculatePathsFunction, CalculateRiskFunction):
        self._CalculatorRiskFunctionPath = CalculateRiskFunction
        self._CalculatorPaths = CalculatePathsFunction
        
        self._ActualPath = Path([], 0)
        self.ActualGoal = None
        
    def GetActualPath(self):
        return self._ActualPath

class LessRiskPathStrategy(Strategy):
    def __init__(self, SuccessorFunction, CalculatePathsFunction, CalculateRiskFunction, version):
        
        super().__init__(CalculatePathsFunction, CalculateRiskFunction)
        
        self.__SuccessorFunction = SuccessorFunction
        self.__version = version-1
    
    #Ridà una lista di caselle (ogni index è il numero di step) che sono occupate dai mostri
    def __NotSafePositions(self, MonsterPositions, steps):
        
        DangerCellsForStep = [MonsterPositions]
        
        StartPoints = MonsterPositions
        
        for _ in range(steps):
            
            for StartPoint in StartPoints:
                
                NewStartPoints = set()
                NewStartPoints.union(set(self.__SuccessorFunction(StartPoint)))
                
            DangerCellsForStep.append(StartPoints)
            
        return DangerCellsForStep

    def Calculate(self, ActualPosition, MonsterPositions):
        
        StartPoints = [SearchNode(ActualPosition, None)]
        
        NotSafePositions = self.__NotSafePositions(MonsterPositions, self.__version)
        
        for i in range(self.__version):
            
            #Calculate new points (already filtered)
            NewStartPoints = []
            for StartPoint in StartPoints:
                
                #New points (already filtered)
                NextPointsValues = list(set(self.__SuccessorFunction(StartPoint.GetElement())).difference(set(NotSafePositions[i+1])))
                
                #If on 1 iteration there is only one choice, choose it without continue with computing (shortcut of computing)
                if(i == 0 and len(NextPointsValues) == 1):
                    self._ActualPath = Path([ActualPosition, NextPointsValues[0]], float("inf"))
                    return NextPointsValues[0]

                #For each new point calculate new path to that new point
                for k in NextPointsValues: NewStartPoints.append(SearchNode(k, StartPoint))
                
            StartPoints = NewStartPoints
        
        #Get all start paths
        StartPaths = list(map(lambda x: x.GetPath(), StartPoints))
        
        Paths = []
        
        for StartPath in StartPaths:
            for NewPath in self._CalculatorPaths(StartPath[-1], self.ActualGoal):  
                Paths.append(StartPath + NewPath[1:])
        
        Paths = [Path(x, self._CalculatorRiskFunctionPath(x, MonsterPositions)) for x in Paths]
        Paths.sort(key=lambda x: (x.GetRiskCost(), len(x.GetPath())))
        
        print("Paths calculated: ")
        for i in Paths: print(i)
        
        try: self._ActualPath = Paths[0]
        except: self._ActualPath = Path([ActualPosition, random.choice(self.__SuccessorFunction(ActualPosition))], float("inf"))
        
        return self._ActualPath[1]

class SafetyFirstStrategy(Strategy):
    def __init__(self, SuccessorFunction, CalculatePathsFunction, CalculateRiskCostPathFunction):
        
        super().__init__(CalculatePathsFunction, CalculateRiskCostPathFunction)
        
        self.SuccessorFunction = SuccessorFunction
 
    # def CalculateRiskPathMonsters(self, Path, MonsterPositions, step):
    #     RiskCost = 0
    #     if step==0:
    #         for i in range(len(Path)-1):
    #             if i==0:
    #                 RiskCost += 1000 * self.n_monsters_there(Path[1],MonsterPositions,0)
    #             if i==1:
    #                 RiskCost += 10 * self.n_monsters_there(Path[2],MonsterPositions,1)
    #             elif i==2:
    #                 RiskCost += 5 * self.n_monsters_there(Path[3],MonsterPositions,2)
    #             else:
    #                 RiskCost += 1 * self.n_monsters_there(Path[i+1],MonsterPositions,i)
    #     else :
    #         for i in range(len(Path)-1):
    #             if i==0:
    #                 RiskCost += 1000 * self.n_monsters_there(Path[1],MonsterPositions,1)
    #             if i==1:
    #                 RiskCost += 10 * self.n_monsters_there(Path[2],MonsterPositions,2)
    #             elif i==2:
    #                 RiskCost += 5 * self.n_monsters_there(Path[3],MonsterPositions,3)
    #             else:
    #                 RiskCost += 1 * self.n_monsters_there(Path[i+1],MonsterPositions,i+1)
                    
    #     return RiskCost

    # Given a version of CalculatePath, returns the lowest-risk path and its risk
    def Calculate(self, ActualPosition, MonsterPositions, n_paths, version, step):
        vers = {"v2":self.CalculatePath_v2, "v3":self.CalculatePath_v3}
        Solutions = vers[version](ActualPosition, self.ActualGoal, n_paths, MonsterPositions)

        Solutions.sort(key=lambda x: (self._CalculatorRiskFunctionPath(x, MonsterPositions, step), len(x)))

        print("The 5 best paths calculated by strategy " + version + " are:")
        for i in Solutions[:5]:
            print(i, self._CalculatorRiskFunctionPath(i, MonsterPositions, step))

        self._ActualPath = Solutions[0]
        
        return self._ActualPath, self._CalculatorRiskFunctionPath(Solutions[0],MonsterPositions,step)

    # Given the position of monsters, returns the numbers of monsters that can be in a certain position within n_steps
    def n_monsters_there(self, Position,MonsterPositions,n_steps):
        n_monsters = 0
        for StartPoint in MonsterPositions:
            ActualPoints = set()
            ActualPoints.add(StartPoint)
            for i in range(n_steps):
                KnewPoints = set()
                for Point in ActualPoints:
                    for NewPoint in self.SuccessorFunction(Point):
                        KnewPoints.add(NewPoint)
                ActualPoints = KnewPoints
            if Position in ActualPoints:
                n_monsters += 1
        return n_monsters
    
    # Given a position that represent the first step I do and the actual MonsterPositions, the fun considers all the possible combinations of monster moves,
    # then returns the number of possible moves from Position at the next step in the worst case
    def worst_case(self,Position,MonsterPositions):
        next_positions = [x for x in self.SuccessorFunction(Position)]
        set_monster_positions = []
        for StartPoint in MonsterPositions:
            Step_1 = set()
            for NewPoint in self.SuccessorFunction(StartPoint):
                Step_1.add(NewPoint)
            set_monster_positions.append(Step_1)
        result = [list(combination) for combination in product(*set_monster_positions)]
        res = []
        for possible_monster_positions in result:
            count = 0
            for next_pos in next_positions:
                count += self.is_safe(next_pos,possible_monster_positions,1)
            res.append(count)
        return min(res)

    # Given the position of monsters, returns if a position is safe or not in n_steps, i.e. if a position can be occupied by at least one of the monster in n_steps
    def is_safe(self, Position,MonsterPositions,n_steps):
        if Position in MonsterPositions: return False
        return self.n_monsters_there(Position,MonsterPositions,n_steps)==0

    # Our more euristhic strategy. The idea is: from the position where I am I call the CalculatePath_v1/2/3, and if I try a path with risk 0 I choose that path.
    # If not, for each NearPoints where I can go with one move, I check how many moves, at least, I will can do from that position at the next step.
    # I choose to step to the position that gives me more choices to move at the next step.
    # If there are multiples with same num of choices, we calculated again with CalculatePath_v1/2/3 starting from each of these position and choose the safest one
    def Safety_first(self, StartPoint, num_paths, MonsterPositions, version, i):
        if i == 0:
            l = -1
        else:
            l = 0
        path, risk = self.Calculate(StartPoint, MonsterPositions, num_paths, version, i)
        if risk==0:
            return path
        
        NearPoints=self.SuccessorFunction(StartPoint)
        NearPoints=[point for point in NearPoints if self.is_safe(point,MonsterPositions,1+l)]
        possible_choices=[]
        for nearpoint in NearPoints:
            possible_choices.append(self.worst_case(nearpoint, MonsterPositions))
        print("The NearPoints are:", NearPoints)
        print("The numbers of possible moves from each of them at the next step are:",possible_choices)
        max_val = max(possible_choices)
        print("The max is", max_val)
        max_indexes = [index for index, value in enumerate(possible_choices) if value == max_val]
        print("Belonging to these moves", [NearPoints[i] for i in max_indexes])
        if(path[1] in [NearPoints[i] for i in max_indexes]):
            print("We chose the move ", path[1], " because it was the lowest_risk solution and is among the selected moves")
            nextpoint = path[1]
        elif len(max_indexes)==1:
            print("We chose the only best move that is ", NearPoints[max_indexes[0]])
            nextpoint = NearPoints[max_indexes[0]]
        else:
            arr_risks = []
            for index in max_indexes:
                risk = self.Calculate(NearPoints[index], MonsterPositions, num_paths, version, i)[1]
                arr_risks.append(risk)
            min_risk = min(arr_risks)
            min_risk_indexes = [index for index,value in enumerate(arr_risks) if value==min_risk]
            if len(min_risk_indexes)==1:
                nextpoint = NearPoints[max_indexes[min_risk_indexes[0]]]
                print("From these moves we chose the move ", nextpoint, " because has the lowest-risk path (among the calculated ones)")
            else:
                nextpoint = NearPoints[max_indexes[random.choice(min_risk_indexes)]]
                print("From these moves we chose randomly the move ", nextpoint)
        result = [StartPoint,nextpoint]
        return result


    # # Our simplest strategy: 
    # def CalculatePath_v1(self, StartPoint, FinishPoint, num_paths, MonsterPositions):
    #     Target = FinishPoint
    #     Result = []
    #     NearPoints = self.SuccessorFunction(StartPoint)
    #     NearPoints = [point for point in NearPoints if self.is_safe(point,MonsterPositions,1)]
    #     if(len(NearPoints)==0):
    #         NearPoints = self.SuccessorFunction(StartPoint)
    #     elif len(NearPoints)==1:
    #         Result = [[StartPoint,NearPoints[0]]]
    #         return Result
    #     for possible_nearpoint in NearPoints:
    #         Result = self.Calculator.CalculatePath_base(possible_nearpoint, Target, num_paths)
    #     return Result
    
    # Searching the top num_paths/num_safe_directions paths by BFS from all possible safe directions
    def CalculatePath_v2(self, StartPoint, FinishPoint, num_paths, MonsterPositions):
        Target = FinishPoint
        Result = []
        NearPoints = self.SuccessorFunction(StartPoint)
        NearPoints = [point for point in NearPoints if self.is_safe(point,MonsterPositions,1)]
        if(len(NearPoints)==0):
            NearPoints = self.SuccessorFunction(StartPoint)
        elif len(NearPoints)==1:
            Result = [[StartPoint,NearPoints[0]]]
            return Result
        for possible_nearpoint in NearPoints:
            for result in self._CalculatorPaths.CalculatePath_base(possible_nearpoint, Target, int(num_paths/len(NearPoints))):
                    result.insert(0, StartPoint)
                    Result.append(result)
        return Result

    # The same as v2, but now we are forcing to search in all possible first and second step directions. Now are excluded the paths that have in the first two moves the possibility to meet a monster
    def CalculatePath_v3(self, StartPoint, FinishPoint, num_paths, MonsterPositions):
        Target = FinishPoint
        Result = []
        NearPoints = self.SuccessorFunction(StartPoint)
        NearPoints = [point for point in NearPoints if self.is_safe(point,MonsterPositions,1)]
        if(len(NearPoints)==0):
            NearPoints = self.SuccessorFunction(StartPoint)
        elif len(NearPoints)==1:
            Result = [[StartPoint,NearPoints[0]]]
            return Result
        for possible_nearpoint in NearPoints:
            NearPoints2 = self.SuccessorFunction(possible_nearpoint)
            NearPoints2 = [point for point in NearPoints2 if self.is_safe(point,MonsterPositions,2)]
            for possible_nearpoint2 in NearPoints2:
                for result in self._CalculatorPaths.CalculatePath_base(possible_nearpoint2, Target, int(num_paths/len(NearPoints2))):
                    result.insert(0, possible_nearpoint)
                    result.insert(0, StartPoint)
                    Result.append(result)
        return Result
