from enum import Enum
import statistics
import sys
from Points import *
from AbstractModel import *



class Center(AbstractModel) :
    
    class CenterMethod(Enum) :
        MEAN = 1
        MEDIAN = 2
    
    minNumPoints = 1

    
    def __init__(self, method, mean = None, p = 0, cost = sys.float_info.max) :
        
        self.method = method
        if method == Center.CenterMethod.MEAN :
            self.mean = True
        else :
            self.mean = False
            
        self.p = p
        self.cost = cost
    
    
    def fitFunction(self, points) :
        
        numPoints = len(points)
        if numPoints < self.minNumPoints :
            raise Exception("Not enough points, at least " + str(self.minNumPoints) + " are necessary.")
        
        
        if self.mean :
            sum = 0
            for p in points :
                sum += p.p1.w[0]
            self.p = sum / len(points)
        else :
            values = []
            i = 0
            for p in points :
                values[i] = p.p1.w[0]
                i += 1
            self.p = statistics.median(values)

        return self.p
    
    
    def distanceTo(self, point) :
        return abs(point.w[0] - self.p)
    
    
# main
if __name__ == '__main__' :
    
    points = []
    points.append(Point([1.0]))
    points.append(Point([3.0]))
    points.append(Point([1.5]))
    points.append(Point([0.8]))
    
    candidates = []
    inliers = []
    
    for p in points :
        candidates.append(PointFunctionMatch(p))
    
    l = Center(Center.CenterMethod.MEAN)
    
    
    l, inliers = l.ransac( candidates, inliers, 500, 1, 0.1) # 500 == RadialSymmetry.bsNumIterations
        
    print(len(inliers))
    print("p = " + str(l.p))
    for p in inliers :
        print(str(p.p1.l[0]),str(l.distanceTo(p.p1)))
        
    
    
    
        
        