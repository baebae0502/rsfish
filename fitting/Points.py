import math
# from Line import *


# Point 관련 class들 모아놓음
class Point :
    
    def __init__(self, l, w = None) :
        
        if len(l) == 2 :
            self.l = l
        else :
            self.l = l*2 

        
        if w == None :
            self.w = self.l.copy()
        else :
            self.w = w
    
    def distance(p1, p2) :
        math.dist([p1 for p1 in p1.w], [p2 for p2 in p2.w])
            


class PointMatch :
    
    def __init__(self, p1, p2 = None, weight = 1, strength = 1) :
        self.p1 = p1
        self.p2 = p2
        
        if isinstance(weight, list) :
            self.weight = 1
            for wi in weight :
                self.weight *= wi 
        else :
            self.weight = weight
            
        self.strength = strength
    
    def getDistance(self) :
        return Point.distance(self.p1, self.p2)

    
 
class PointFunctionMatch(PointMatch) :
    
    def __init__(self, p1, p2 = None, weight = 1, strength = 1, distance = 0) :
        
        self.distance = distance
        super().__init__(p1, p2, weight, strength)
    
    
    def apply(self, l) :
        
        self.distance = l.distanceTo(self.p1)   
    
    
    def getW(self) :
        return self.p1.w
    
    def getOW(self) :
        return self.p1.ow
    
    def getL(self) :
        return self.p1.l
    
    def getOL(self) :
        return self.p1.ol
        
        
class OrientedPoint :
    
    def __init__(self, position, vector, magnitude) :
        
        self.l = position
        
        self.w = self.l.copy()
        
        # Orientation in local coordinates
        self.ol = vector
        
        # Orientation in world coordinates
        self.ow = self.ol.copy()
        
        # gradient magnitude
        self.magnitude = magnitude
        
        # TODO : Multithreading-save
        self.tmp = []       
    
    def getW(self) :
        return self.w
    
    def getOW(self) :
        return self.ow
    
    def getL(self) :
        return self.l
    
    def getOL(self) :
        return self.ol
    
        
        