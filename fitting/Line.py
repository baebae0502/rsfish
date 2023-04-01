import numpy as np
import math
import copy
import sys
from Points import *
from AbstractModel import *



class Line(AbstractModel) :
    
    minNumPoints = 2
    
    def __init__(self, n = None, m = None) :
        self.n = n
        self.m = m
        self.cost = sys.float_info.max
        
        
    def fitFunction(self, points) :
        numPoints = len(points)
        if numPoints < self.minNumPoints :
            raise Exception("Not enough points, at least " + str(self.minNumPoints) + " are necessary.")
        
        # compute matrices
        delta = np.zeros(shape = (2, 2))
        theta = np.zeros(shape = 2)
        
        for p in points :
            
            x = p.p1.w[0]
            y = p.p1.w[1]
            
            xx = x * x
            xy = x * y
            
            delta[0, 0] += xx
            delta[0, 1] += x
            delta[1, 0] += x
            delta[1, 1] += 1
            
            theta[0] += xy
            theta[1] += y
        
        delta = np.linalg.inv(delta)
        
        self.m = delta[0, 0] * theta[0] + delta[0, 1] * theta[1]
        self.n = delta[1, 0] * theta[0] + delta[1, 1] * theta[1]
        
    
    def distanceTo(self, point) :
        x1 = point.w[0] 
        y1 = point.w[1]
        
        return abs(y1 - self.m * x1 - self.n) / (math.sqrt(self.m * self.m + 1))       


     
if __name__ == '__main__' :
    
    points = []
    
    points.append(Point([1, -3.95132]))
    points.append(Point([2, 6.51205]))
    points.append(Point([3, 18.03612]))
    points.append(Point([4, 28.65245]))
    points.append(Point([5, 42.05581]))
    points.append(Point([6, 54.01327]))
    points.append(Point([7, 64.58747]))
    points.append(Point([8, 76.48754]))
    points.append(Point([9, 89.00033]))
    
    candidates = []
    inliers = []
    
    for p in points :
        candidates.append(PointFunctionMatch(p))
        
    l = Line()
    
    
    l, inliers = l.ransac( candidates, inliers, 100, 0.1, 0.5)
    
    print(len(inliers))
    print("y = " + str(l.m) + " x + " + str(l.n))
    for p in inliers :
        print(l.distanceTo(p.p1))
    
