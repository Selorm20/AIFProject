class AstarPathSearch:
    def __init__(self, GetNearPointsFunction):
        self.__GetNearPointsFunction = GetNearPointsFunction
    
    def GetNearPointsFunction(self):
        return self.__GetNearPointsFunction
    
    def CalculatePath(self, StartPoint, FinishPoint):
        
        SearchLeafs = [__SearchNode(StartPoint, None)]
        
        #While there is also 1 leaf to consider
        while(len(SearchLeafs) > 0):
            
            #Find index of minimum element
            MinimumPoint = SearchLeafs[0]
            
            r = 0
            for i in range(len(SearchLeafs)):
                if(SearchLeafs[i].GetCount() < MinimumPoint.GetCount()):
                    MinimumPoint, r = SearchLeafs[i], i
                    
            #Calculate Neighbour points of minimum point
            NearPoints = list(map(lambda x: __SearchNode(x, MinimumPoint),  self.__GetNearPointsFunction(MinimumPoint.GetElement())))
            
            #Check if finish point is found
            for i in NearPoints:
                if(i.GetElement() == FinishPoint): return i.GetPath()
                
            #Concatenate new points to list of leaf to explore    
            SearchLeafs += NearPoints
            
            #Delete minimum point previously explored
            del SearchLeafs[r]  
            
        #In that case, there is no path from start point to finish point 
        return None

class BFSPathSearch:
    def __init__(self, GetNearPointsFunction):
        self.__GetNearPointsFunction = GetNearPointsFunction
    
    def GetNearPointsFunction(self):
        return self.__GetNearPointsFunction
    
    def CalculatePath(self, StartPoint, FinishPoint):
        
        SearchLeafs = [__SearchNode(StartPoint, None)]
        
        #While there is also 1 leaf to consider
        while(len(SearchLeafs) > 0):
            
            #Find index of minimum element
            MinimumPoint = SearchLeafs[0]
                    
            #Calculate Neighbour points of minimum point
            NearPoints = list(map(lambda x: __SearchNode(x, MinimumPoint),  self.__GetNearPointsFunction(MinimumPoint.GetElement())))
            
            #Check if finish point is found
            for i in NearPoints:
                if(i.GetElement() == FinishPoint): return i.GetPath()
                
            #Concatenate new points to list of leaf to explore    
            SearchLeafs += NearPoints
            
            #Delete minimum point previously explored
            del SearchLeafs[0]  
            
        #In that case, there is no path from start point to finish point 
        return None
            
class __SearchNode:
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
        if(self.GetPreviousNode() == None): return self.GetElement()
        return [self.GetPreviousNode().GetPath()] + [self.GetElement()]
    
    def __del__(self):
        return NotImplemented
