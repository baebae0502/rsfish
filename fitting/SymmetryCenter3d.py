import random
import numpy as np
import math

from AbstractModel import *
from Points import *

class SymmetryCenter3D(AbstractModel) :
    
    minNumPoints = 2
    
    def __init__(self, xc = None, yc = None, zc = None) :
        self.xc = xc
        self.yc = yc
        self.zc = zc
        
        self.cost = sys.float_info.max
    
    
    # Fit the function to a list of OrientedPoints
    # Override
    def fitFunction(self, points) :
        numPoints = len(points)
        if numPoints < self.minNumPoints :
            raise Exception("Not enough points, at least " + str(self.minNumPoints) + " are necessary.")
        
        # Compute matrices
        delta = np.zeros(shape = (3, 3))
        theta = np.zeros(shape = 3)
        
        for point in points :
            
            xk = point.getW()[0]
            yk = point.getW()[1]
            zk = point.getW()[2]
            
            ak = point.getOW()[0]
            bk = point.getOW()[1]    
            ck = point.getOW()[2]
            
            if ak == 0 and bk == 0 and ck == 0 :
                continue
            
            ak2 = ak * ak
            bk2 = bk * bk
            ck2 = ck * ck
            
            mk2 = ak2 + bk2 + ck2
            ab = (ak * bk) / mk2
            ac = (ak * ck) / mk2
            bc = (bk * ck) / mk2
            
            delta[0, 0] += 1 - ak2 / mk2
            delta[0, 1] -= ab
            delta[0, 2] -= ac
            
            delta[1, 0] -= ab
            delta[1, 1] += 1 - bk2 / mk2
            delta[1, 2] -= bc
            
            delta[2, 0] -= ac
            delta[2, 1] -= bc
            delta[2, 2] += 1 - ck2 / mk2
            
            theta[0] += xk * (1 - (ak * ak)/mk2) - (ak * ck * zk)/mk2 - (ak * bk * yk)/mk2
            theta[1] += yk * (1 - (bk * bk )/mk2) - (ak * bk * xk)/mk2 - (bk * ck * zk)/mk2
            theta[2] += zk * (1 - (ck * ck)/mk2) - (ak * ck * xk)/mk2 - (bk * ck * yk)/mk2
            
        try :
            delta = np.linalg.inv(delta)
        except :
            self.xc = self.yc = self.zc = float("NaN")    
        self.xc = delta[0, 0] * theta[0] + delta[0, 1] * theta[1] + delta[0, 2] * theta[2]
        self.yc = delta[1, 0] * theta[0] + delta[1, 1] * theta[1] + delta[1, 2] * theta[2]
        self.zc = delta[2, 0] * theta[0] + delta[2, 1] * theta[1] + delta[2, 2] * theta[2]
    
    
    # Compute the distance between a line defined by OrientedPoint and SymmetryCenter3D
    # Override
    def distanceTo(self, point) :
        xk = point.getW()[0]
        yk = point.getW()[1]
        zk = point.getW()[2]
        
        ak = point.getOW()[0]
        bk = point.getOW()[1]
        ck = point.getOW()[2]
        
        dx = xk - self.xc
        dy = yk - self.yc
        dz = zk - self.zc
        
        tmp1 = ak * dx + bk * dy + ck * dz
        
        # numerical instabilities can lead to negative square distances
        return math.sqrt( max( 0, (dx*dx + dy*dy + dz*dz) - ( (tmp1*tmp1)/(ak*ak + bk*bk + ck*ck) ) ) )
    
    
    # Override
    def setSymmetryCenter(self, center, d) :
        if d == 0 :
            self.xc = center
        elif d == 1 :
            self.yc = center
        elif d == 2 :
            self.zc = center
    

    def getSymmetryCenter(self, d) :
        if d == 0 :
            return self.xc
        elif d == 1 :
            return self.yc
        else :
            return self.zc
         
    
    
    
#main 
if __name__ == '__main__' :
    rnd = random.Random(345)
    list = []
    c = [rnd.uniform(0, 1) * 2 - 1, rnd.uniform(0, 1) * 2 -1, rnd.uniform(0, 1) * 2 - 1]
    print("Center should be : " + str(c))
    
    for i in range(10) :
        v = [rnd.uniform(0, 1) * 2 - 1, rnd.uniform(0, 1) * 2 -1, rnd.uniform(0, 1) * 2 - 1]
        p = [c[0] - v[0] * 2.3, c[1] - v[1] * 2.3, c[2] - v[2] * 2.3 ]
        
        list.append(OrientedPoint(p, v, 1))
    
    center = SymmetryCenter3D()
    
    center.fitFunction(list)
    
    print("center :", center.xc, center.yc, center.zc)
    
    for l in list :
        print("Distance :", center.distanceTo(l))
    
    center.setSymmetryCenter(0, 0)
    center.setSymmetryCenter(0, 1)
    center.setSymmetryCenter(2, 2)
    op = OrientedPoint([-10, 0, 0], [1, 0, 0], 1)
    print("Test Distance :", center.distanceTo(op))