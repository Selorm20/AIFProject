def n_monsters_there(Position,MonsterPositions,SuccessorFunction,n_steps):
    n_monsters = 0
    for StartPoint in MonsterPositions:
        ActualPoints = set()
        ActualPoints.add(StartPoint)
        for i in range(n_steps):
            KnewPoints = set()
            for Point in ActualPoints:
                for NewPoint in SuccessorFunction(Point):
                    KnewPoints.add(NewPoint)
            ActualPoints = KnewPoints
        if Position in ActualPoints:
            n_monsters += 1
    return n_monsters

def is_safe(Position,MonsterPositions,SuccessorFunction):
    if n_monsters_there(Position,MonsterPositions,SuccessorFunction,1)==0:
        return True
    else:
        return False
    