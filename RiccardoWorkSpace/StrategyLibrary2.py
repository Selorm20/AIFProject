import RiccardoWorkSpace.AlgorithmLibrary as AL
import RiccardoWorkSpace.functions as FUN
import random


class Strategy:
    def __init__(self, SuccessorFunction):   
        
        self.SuccessorFunction = SuccessorFunction

        self.Calculator = AL.BFSPathSearch(SuccessorFunction)
                
        self.__ActualPath = []
        self.ActualGoal = None
        
    def GetActualPath(self):
        return list(self.__ActualPath)
    
    def CalculateRiskPathMonsters(self, Path, MonsterPositions, step):
        RiskCost = 0
        if step==0:
            for i in range(len(Path)-1):
                if i==0:
                    RiskCost += 1000 * self.n_monsters_there(Path[1],MonsterPositions,0)
                if i==1:
                    RiskCost += 10 * self.n_monsters_there(Path[2],MonsterPositions,1)
                elif i==2:
                    RiskCost += 5 * self.n_monsters_there(Path[3],MonsterPositions,2)
                else:
                    RiskCost += 1 * self.n_monsters_there(Path[i+1],MonsterPositions,i)
        else :
            for i in range(len(Path)-1):
                if i==0:
                    RiskCost += 1000 * self.n_monsters_there(Path[1],MonsterPositions,1)
                if i==1:
                    RiskCost += 10 * self.n_monsters_there(Path[2],MonsterPositions,2)
                elif i==2:
                    RiskCost += 5 * self.n_monsters_there(Path[3],MonsterPositions,3)
                else:
                    RiskCost += 1 * self.n_monsters_there(Path[i+1],MonsterPositions,i+1)
                    
        return RiskCost

    # Given a version of CalculatePath, returns the lowest-risk path and its risk
    def Calculate(self, ActualPosition, MonsterPositions, n_paths, version, step):
        vers = {"v1":self.CalculatePath_v1, "v2":self.CalculatePath_v2, "v3":self.CalculatePath_v3}
        Solutions = vers[version](ActualPosition, self.ActualGoal, n_paths, MonsterPositions)

        Solutions.sort(key=lambda x: (self.CalculateRiskPathMonsters(x, MonsterPositions, step), len(x)))

        print("The 5 best paths calculated by strategy " + version + " are:")
        for i in Solutions[:5]:
            print(i, self.CalculateRiskPathMonsters(i, MonsterPositions, step))

        self.__ActualPath = Solutions[0]
        
        return self.__ActualPath, self.CalculateRiskPathMonsters(Solutions[0],MonsterPositions,step)

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

    # Given the position of monsters, returns if a position is safe or not in n_steps, i.e. if a position can be occupied by at least one of the monster in n_steps
    def is_safe(self, Position,MonsterPositions,n_steps):
        if Position in MonsterPositions:
            return False
        if self.n_monsters_there(Position,MonsterPositions,n_steps)==0:
            return True
        else:
            return False

    # Our more euristhic strategy. The idea is: from the position where I am I call the CalculatePath_v1/2/3, and if I try a path with risk 0 I choose that path.
    # If not, for each NearPoints where I can go with one move, I check how many moves, at least, I will can do from that position at the next step.
    # I choose to step to the position that gives me more choices to move at the next step.
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
            NearPoints2=self.SuccessorFunction(nearpoint)
            NearPoints2=[point for point in NearPoints2 if self.is_safe(point,MonsterPositions,2+l) and self.is_safe(point,MonsterPositions,1+l)]
            possible_choices.append(len(NearPoints2))
        print("The NearPoints are:", NearPoints)
        print("The numbers of possible moves from each of them at the next step are:",possible_choices)
        max_val = max(possible_choices)
        print("The max is", max_val)
        max_indexes = [index for index, value in enumerate(possible_choices) if value == max_val]
        print("Belonging to these moves", [NearPoints[i] for i in max_indexes])
        if len(max_indexes)==1:
            print("We chose the only best move that is ", NearPoints[max_indexes[0]])
            result = [StartPoint,NearPoints[0]]
        if path[1] in [NearPoints[i] for i in max_indexes]:
            print("From these moves we chose the move ", path[1], " beacuse it is the move suggested by the lowest-risk path")
            result = [StartPoint,path[1]]
        else:
            nextpoint = NearPoints[random.choice(max_indexes)]
            result = [StartPoint,nextpoint]
            print("From these moves we chose randomly the move ", nextpoint)
        return result


    # Our simplest strategy: top num_paths paths by BFS excluding paths that begin with a move toward a non-safe position
    def CalculatePath_v1(self, StartPoint, FinishPoint, num_paths, MonsterPositions):
        Target = FinishPoint
        Result = []
        NearPoints = self.SuccessorFunction(StartPoint)
        NearPoints = [point for point in NearPoints if self.is_safe(point,MonsterPositions,1)]
        if(len(NearPoints)==0):
            NearPoints = self.SuccessorFunction(StartPoint)
        elif len(NearPoints)==1:
            Result = [[StartPoint,NearPoints[0]]]
            return Result
        Result = self.Calculator.CalculatePath_base(StartPoint, Target, num_paths)
        return Result
    
    # The same as v1, but now we are forcing to search in all possible first-step directions
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
            for result in self.Calculator.CalculatePath_base(possible_nearpoint, Target, int(num_paths/len(NearPoints))):
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
            if len(NearPoints2)==1:
                Result.append([StartPoint,possible_nearpoint,NearPoints2[0]])
            for possible_nearpoint2 in NearPoints2:
                for result in self.Calculator.CalculatePath_base(possible_nearpoint2, Target, int(num_paths/len(NearPoints2))):
                    result.insert(0, possible_nearpoint)
                    result.insert(0, StartPoint)
                    Result.append(result)
        return Result
