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
        def __lt__(self, other):
            return self.__Count < other.__Count


class BFSPathSearch(__PathSearch):
    def __init__(self, GetNeighbourPointsFunction):
        super().__init__(GetNeighbourPointsFunction)


    # This is simple BFS that returns the shortest num_paths paths
    def CalculatePath_base(self, StartPoint, FinishPoint, num_paths):
        Target = FinishPoint
        
        SearchLeafs = [self._SearchNode(StartPoint, None)]
        self._VisitedElements.clear()
        
        Result = []
        i = 0
        # While there are leaf nodes to consider
        while len(SearchLeafs) > 0 and len(Result) < num_paths:
            # Find index of the minimum element
            MinimumPoint = SearchLeafs[0]
        
            self._VisitedElements.append(MinimumPoint.GetElement())
            
            # Check if the current node is the target
            if MinimumPoint.GetElement() == Target:
                Result.append(MinimumPoint.GetPath())

            # Calculate neighbor points of the minimum point
            NearPoints = self._GetNeighbourPointsFunction(MinimumPoint.GetElement())
            

            # Create new SearchNode instances for the safe neighbor points
            NearNodes = [self._SearchNode(point, MinimumPoint) for point in NearPoints]
            
            # Delete the minimum point previously explored
            del SearchLeafs[0]
                
            # Concatenate new points to the list of leaf nodes to explore    
            SearchLeafs += NearNodes
            i += 1
        return Result