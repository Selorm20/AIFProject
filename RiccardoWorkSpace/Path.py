class Path:
    def __init__(self, Path, RiskCost):
        self.__Path = Path
        self.__RiskCost = RiskCost
        
    def GetPath(self): return self.__Path
    def GetRiskCost(self): return self.__RiskCost
    
    def __getitem__(self, key):
        return self.__Path[key]
    
    def __iter__(self):
        self.__i = 0
        return self

    def __next__(self):
        if(self.__i < len(self.__Path)):
            self.__i += 1
            return self.__Path[self.__i-1]
        else:
            del self.__i
            return StopIteration
    
    def __str__(self):
        return f"{self.__RiskCost} {self.__Path}"