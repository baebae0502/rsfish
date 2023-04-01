import numpy as np
import random
import sys
import copy
import statistics
from Points import *


 
class AbstractModel :

    rnd = random.Random(69997)
 
    def __init__(self, cost = sys.float_info.max) :
        self.cost = cost
    
    
    def betterThan(self, m) :
        if self.cost < 0 : return False
        else : return self.cost < m.cost
        

    def set() :
        pass
    
    # inliers를 parameter로 받긴하는데 사용안하고 global variable만 사용함(tempInlier).. 다른 해결책 없나?
    def test(self, candidates, inliers, epsilon, minInlierRatio, minNumInliers = None) :
        
        if not minNumInliers :
            minNumInliers = self.minNumPoints
        
        global tempInliers
        tempInliers.clear()
        
        for m in candidates :
            m.apply(self)
            if m.distance < epsilon :
                tempInliers.append(m)
        
        ir = len(tempInliers) / len(candidates)
        self.cost = max(0, min(1, 1 - ir))
        
        return (( len(tempInliers) >= minNumInliers ) and ( ir > minInlierRatio ))


    def test_for_test(self, candidates, inliers, epsilon, minInlierRatio, minNumInliers = None) :
            
            if not minNumInliers :
                minNumInliers = self.minNumPoints
            
            
            inliers.clear()
            
            for m in candidates :
                m.apply(self)
                if m.distance < epsilon :
                    inliers.append(m)
            
            ir = len(inliers) / len(candidates)
            self.cost = max(0, min(1, 1 - ir))
            
            return (( len(inliers) >= minNumInliers ) and ( ir > minInlierRatio ))



    def filter(self, candidates, inliers, maxTrust, minNumInliers) :
        
        if len(candidates) < self.minNumPoints :
            raise Exception(str(len(candidates)) + " data points are not enough to solve the Model, at least " + str(self.minNumPoints) + " data points required." )
        
        # copy1, self = SymmetryCenter2D object
        copy1 = copy.deepcopy(self)
        
        # inliers, temp = PointFunctionMatch object list
        inliers.clear()
        inliers = copy.deepcopy(candidates)
        temp = []
        numInliers = None
        
        while True :
            temp.clear()
            temp = copy.deepcopy(inliers)
            numInliers = len(inliers)
            
            try :
                # copy1.xc & copy1.yc 값을 선택된 inliers를 사용해 갱신
                copy1.fitFunction(inliers)
            except : 
                return False
            
            
            observer = []
            
            for m in temp :
                # temp.distance 값을, 갱신된 copy1.xc & copy1.xc 값을 이용해 갱신
                # m = PointFunctionMatch object
                m.apply(copy1)
                observer.append(m.distance)
                
            inliers.clear()
            #t = observer.getMedian() * maxTrust
            t = statistics.median(observer) * maxTrust
            for m in temp : 
                if m.distance <= t :
                    inliers.append(m)
                    
            
            copy1.cost = statistics.mean(observer)
            
            # break. like do-while
            if numInliers <= len(inliers) :
                break
           
            
        if numInliers < self.minNumPoints :
            return False
        
        self = copy.deepcopy(copy1)
        
        return self, inliers
    
            

    def ransac(self, 
               candidates = None,
               inliers = None,
               iterations = None,
               epsilon = None,
               minInlierRatio = None,
               minNumInliers = None) :
        
        cost = sys.float_info.max
        
        copy1 = copy.deepcopy(self)
        m1 = copy.deepcopy(self)
        
        if minNumInliers == None :
            minNumInliers = self.minNumPoints
        
        if len(candidates) < self.minNumPoints :
            raise Exception(str(len(candidates)) + " data points are not enough to solve the Model, at least " + str(self.minNumPoints) + " data points required." )

                
        inliers.clear()
        i = 0
        minMatches = set()
        
        while i < iterations :
            
            
            # goto
            x=0
            
            # PointMatch p를 minNumInliers 만큼 중복되지않게 뽑기
            minMatches.clear()
            for j in range(self.minNumPoints) :
                
                while True :
                    # random index 생성
                    idx = np.random.uniform(0, len(candidates), 1)
                    idx = int(idx)
                   
                    p = candidates[idx]
                    
                    if p in minMatches :
                        continue
                    else :
                        minMatches.add(p)
                        break
                        
            try : 
                '''
                minMatches_list = list(minMatches)
                x1 = np.array([mM.p1.w[0] for mM in minMatches_list])
                y1 = np.array([mM.p1.w[1] for mM in minMatches_list])
                m1.m, m1.n = np.polyfit(x1, y1, 1).tolist()
                '''
                minMatches_list = list(minMatches)
                
                m1.fitFunction(minMatches_list)
            except : 
                i += 1
                continue
            
            
            global tempInliers 
            tempInliers = []
            
            numInliers = 0
            
            isGood = m1.test(candidates, tempInliers, epsilon, minInlierRatio) # test() --> 보류. 구현해야됨
            
            while isGood and ( numInliers < len(tempInliers) ) :
                
                numInliers = len(tempInliers)
                try : 
                    m1.fitFunction(tempInliers)
                except :
                    # goto
                    i += 1
                    x = 'GoToFirstWhile'
                    break
                
                isGood = m1.test(candidates, tempInliers, epsilon, minInlierRatio, minNumInliers)  
            # goto
            if x == 'GotoFirstWhile' :
                continue
            
                
            if isGood and m1.betterThan(copy1) and ( len(tempInliers) >= minNumInliers ) :
               
                copy1 = copy.deepcopy(m1)
                inliers.clear()
                inliers = copy.deepcopy(tempInliers)
            
            i += 1  
        
        if len(inliers) == 0 :
            return False          

        self = copy.deepcopy(copy1)
        return self, inliers

    
    def filterRansac(self,
                     candidates = None,
                     inliers = None,
                     iterations = None,
                     maxEpsilon = None,
                     minInlierRatio = None,
                     minNumInliers = None,
                     maxTrust = 4) :
        
        temp = []
        
        self_inliers = self.ransac(candidates,
                                    temp,
                                    iterations,
                                    maxEpsilon,
                                    minInlierRatio,
                                    minNumInliers)
        
        if not self_inliers : return False
        
        self = self_inliers[0]
        temp = self_inliers[1]
        
        self_inliers = self.filter(temp, inliers, maxTrust, minNumInliers)
        
        if not self_inliers : return False
        
        return self_inliers
            




if __name__ == '__main__' :
    
    from Center import *
    
    points = []
    points.append(Point([1.0]))
    points.append(Point([3.0]))
    points.append(Point([1.5]))
    points.append(Point([0.8]))
    
    candidates = []
    inliers = []
    inliers2 = []
    
    for p in points :
        candidates.append(PointFunctionMatch(p))
    
    l = Center(Center.CenterMethod.MEAN)
    
    
    l, inliers = l.ransac(candidates, inliers, 500, 1, 0.1) # 500 == RadialSymmetry.bsNumIterations
    
    print(len(inliers))
    print("p = " + str(l.p))
    for p in inliers :
        print(str(p.p1.l[0]),str(l.distanceTo(p.p1)))
     
        
    
    
   
        