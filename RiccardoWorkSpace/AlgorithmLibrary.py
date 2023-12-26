class __PathSearch:
    def __init__(self, GetNeighbourPointsFunction):
        
        self._VisitedElements = [] 
        self._GetNeighbourPointsFunction = lambda x: list(filter(lambda i: i not in self._VisitedElements, GetNeighbourPointsFunction(x)))
    
    def CalculatePath(self, StartPoint, FinishPoints):
        return NotImplemented
    
    def GetMinimumPointPath(self, Points):
        MinimumPoint, r = Points[0], 0
        
        for i in range(len(Points)):
            if(Points[i].GetCount() < MinimumPoint.GetCount()): MinimumPoint, r = Points[i], i
            
        return MinimumPoint, r
    
    class _SearchNode:
        def __init__(self, Element, PreviousNode):
            self.__PreviousNode = PreviousNode
            self.__Element = Element
            self.__Count = 0 if PreviousNode == None else PreviousNode.GetCount()+1
                
        def GetPreviousNode(self):
            return self.__PreviousNode
            
        def GetElement(self):
            return self.__Element
            
        def GetCount(self):
            return self.__Count
            
        def GetPath(self):
            Result = []
            Step = self
            
            while(Step != None):
                Result.insert(0, Step.GetElement())
                Step = Step.GetPreviousNode()
                
            return Result
        
        def __del__(self):
            return NotImplemented

class AstarPathSearch(__PathSearch):
    def __init__(self, GetNeighbourPointsFunction):
        super().__init__(GetNeighbourPointsFunction)
    
    def CalculatePath(self, StartPoint, FinishPoints):
        
        Targets = list(FinishPoints)
        
        SearchLeafs = [self._SearchNode(StartPoint, None)]
        self._VisitedElements.clear()
        
        Result = dict()
        for i in FinishPoints: Result[i] = None
        
        #While there is also 1 leaf to consider
        while(len(SearchLeafs) > 0 and len(Targets) > 0):
            
            #Find index of minimum element
            PointToAnalyze, r = self.GetMinimumPointPath(SearchLeafs)
                    
            self._VisitedElements.append(PointToAnalyze.GetElement())
            
            #Delete minimum point previously explored
            del SearchLeafs[r]
                    
            #Calculate Neighbour points of minimum point
            NearPoints = list(map(lambda x: self._SearchNode(x, PointToAnalyze),  self._GetNeighbourPointsFunction(PointToAnalyze.GetElement())))
            
            #Check if any finish point is found
            for i in NearPoints:
                if(i.GetElement() in FinishPoints):
                    Result[i.GetElement()] = i.GetPath()
                    del Targets[Targets.index(i.GetElement())]
                
            #Concatenate new points to list of leaf to explore    
            SearchLeafs += NearPoints            
            
        #In that case, there is no path from start point to finish point 
        return Result

class BFSPathSearch(__PathSearch):
    def __init__(self, GetNeighbourPointsFunction):
        super().__init__(GetNeighbourPointsFunction)
    
    def CalculatePath(self, StartPoint, FinishPoints):
        
        Targets = list(FinishPoints)
        
        SearchLeafs = [self._SearchNode(StartPoint, None)]
        self._VisitedElements.clear()
        
        Result = dict()
        for i in FinishPoints: Result[i] = []
        
        #While there is also 1 leaf to consider
        while(len(SearchLeafs) > 0 and len(Targets) > 0):
            
            #Find index of minimum element
            MinimumPoint = SearchLeafs[0]
          
            self._VisitedElements.append(MinimumPoint.GetElement())
            if(MinimumPoint.GetElement() in Targets): del Targets[Targets.index(MinimumPoint.GetElement())]
            
            ElementSearchLeafs = list(map(lambda x: x.GetElement(), SearchLeafs))

            #Calculate Neighbour points of minimum point
            NearPoints = list(filter(lambda x: x not in ElementSearchLeafs or x in FinishPoints, self._GetNeighbourPointsFunction(MinimumPoint.GetElement())))
            NearPoints = list(map(lambda x: self._SearchNode(x, MinimumPoint), NearPoints))
            
            #Check if finish point is found
            for i in NearPoints:
                if(i.GetElement() in FinishPoints):
                    Result[i.GetElement()].append(i.GetPath())
                   
            #Delete minimum point previously explored
            del SearchLeafs[0]
                
            #Concatenate new points to list of leaf to explore    
            SearchLeafs += NearPoints  
            
        for i in Result.keys():
            Result[i].sort(key=lambda x: len(x))       
            
        #In that case, there is no path from start point to finish point 
        return Result