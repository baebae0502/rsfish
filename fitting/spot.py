#%%
import sys
from SymmetryCenter2d import *
from SymmetryCenter3d import *
from Points import *
import math


class Spot :
   
    
    def __init__(self, loc = None) :
        self.n = len(loc)
        self.loc = loc
        
        if self.n == 2 :
            self.center = SymmetryCenter2D()
        elif self.n == 3 :
            self.center = SymmetryCenter3D()
        else :
            raise ValueError("only 2d and 3d is allowed.")
        
        self.candidates = []
        self.inliers = []
        self.multiConsensusMatches = []
        self.scale = [1,1,1]
        self.numRemoved = -1
        self.avgCost = -1; self.minCost = -1; self.maxCost = -1
        self.intensity = -1
        
        
    def toString(self) :
        result = "center : "
        
        for d in range(self.n) :
            result += str(self.center.getSymmetryCenter(d) / self.scale[d]) + " "
        
        result += " Removed = " + str(self.numRemoved) + "/" + str(len(self.candidates)) + " error = " + str(self.minCost) + ";" + str(self.avgCost) + ';' + str(self.maxCost) + '---' + str(self.loc)            

        return result
    
    
    def computeAverageCost(self, set) :
        # set : PointFunctionMatch object
        if len(set) == 0 :
            self.minCost = sys.float_info.max
            self.maxCost = sys.float_info.max
            self.avgCost = sys.float_info.max

            return self.avgCost

        self.minCost = sys.float_info.max
        self.maxCost = 0
        self.avgCost = 0

        for pm in set :
            pm.apply(self.center)
            d = pm.distance
            
            self.avgCost += d
            self.minCost = min(d, self.minCost)
            self.maxCost = max(d, self.maxCost)
        
        self.avgCost /= len(set)
        
        return self.avgCost
    
    
    def updateScale(self, scale) :
        # candidates : PointFunctionMatch object
        for pm in self.candidates :
            
            # p1 : OrientedPoint object
            p = pm.p1
            
            l = p.l
            w = p.w
            ol = p.ol
            ow = p.ow
            
            for d in range(len(l)) :
                w[d] = l[d] * scale[d]
                ow[d] = ol[d] * scale[d]
            
        for d in range(len(scale)) :
            self.scale[d] = scale[d]
            
    
    def extractSpot(image, peak, derivative, normalizer, spotSize) :
        
        numDimensions = derivative.n1
        # len(min), len(max) = numDimensions
        min_range = []
        max_range = []
        
        gradient = None
        if normalizer == None : 
            # derivative는 Gradient object  
            gradient = derivative
        else :
            # normalizer는 NormalizedGradient object
            gradient = normalizer
        
        spot = Spot(peak)
        
        
        # this part defines the possible values
        for e in range(numDimensions) :
            min_range.append(peak[e] - spotSize[e] / 2)
            max_range.append(min_range[e] + spotSize[e] - 1) 

            # check that it does not exceed bounds of the underlying image
            min_range[e] = int(max(min_range[e], 0))
            # we always compute the location at 0.5,0,5,0.5 - so we cannot compute it at the last entry of each dimension
            # 0 would be the image, -1 is the gradient image as we loose one value computing the gradient
            max_range[e] = int(min(max_range[e], image.shape[e] - 2))    
            
        spotInterval = [min_range, max_range]
        
        if normalizer != None :
            # 이때, gradient는 NormalizedGradient object
            gradient.normalize(spotInterval)

        
        # 2d의 경우. 
         
        y_interval = spotInterval[1][1] - spotInterval[0][1] + 1
        x_interval = spotInterval[1][0] - spotInterval[0][0] + 1
       
        for i in range(y_interval) :
            for j in range(x_interval) :
                
                v = []
                p = []
                y = i + spotInterval[0][1]
                x = j + spotInterval[0][0]
                
                p = [x + 0.5, y + 0.5]

                v = gradient.gradientAt([x,y], v)
                
                
                spot.candidates.append(PointFunctionMatch(OrientedPoint(p, v, 1)))     
        
        return spot
                    
            
    def extractSpots(image, peaks, derivative, normalizer, spotSize) :
        spots = []
        for peak in peaks :
            spots.append(Spot.extractSpot(image, peak, derivative, normalizer, spotSize))
        
        return spots
        

    def ransac1(spots, 
               iterations,
               maxError,
               inlierRatio,
               minNumInliers,
               multiConsensus,  # all variables below are to instantiate new spots
               nTimesStDev1,
               nTimesStDev2,
               interval,
               derivative,
               normalizer,
               spotSize,
               silent) :
        
        additionalSpots = []

        min_num = sys.maxsize
        max_num = - sys.maxsize - 1
        sum_num = 0

        inlierCount = []
        
        
        for spot in spots :
            try :
                Spot.ransac2(spot, iterations, maxError, inlierRatio, multiConsensus, minNumInliers)
            except :
                spot.inliers.clear()
                spot.numRemoved = len(spot.candidates)
            
            if len(spot.inliers) > 0 :
                min_num = min(min_num, len(spot.inliers))
                max_num = max(max_num, len(spot.inliers))
                sum_num += len(spot.inliers)
                
                inlierCount.append( len(spot.inliers) )
                
        if len(inlierCount) > 0 :
            avg = sum_num / len(inlierCount)  
            stdev = 0
            
            for v in inlierCount :
                stdev += (v - avg) * (v - avg)
            
            stdev = math.sqrt( stdev / (len(inlierCount) - 1) )
            
            if not silent :
                print("min #inliers=" + str(min_num))
                print("max #inliers=" + str(max_num))
                print("average #inliers=" + str(avg))
                print("stdev #inliers=" + str(stdev))
            
            # select extra consensus areas that might be spots
            if multiConsensus :
                thr1 = round(avg - nTimesStDev1 * stdev)
                thr2 = round(avg - nTimesStDev2 * stdev)
                
                if not silent :
                    print("Finding additional spots ... ")
                    print("MultiConsensus initial threshold #inliers=" + str(thr1))
                    print("MultiConsensus final threshold #inliers=" + str(thr2))
                
                newSpots = []
                for spot in spots :
                    # list = PointFunctionMatch object list
                    for list in spot.multiConsensusMatches :
                        if len(list) >= thr1 :
                            pos = []
                            
                            try :
                                spot.center.fitFunction(list)
                                for d in range(len(pos)) :
                                    pos[d] = round(spot.center.getSymmetryCenter(d))
                                if not Spot.pointExists(pos, newSpots) :
                                    newSpot = Spot.extractSpot(interval, pos, derivative, normalizer, spotSize)
                                    
                                    minNumInliers = max( minNumInliers, round(len(newSpot.candidates) * inlierRatio) )
                                    
                                    pN = []
                                    
                                    for i in range( len(newSpot.candidates) - 1, -1, -1 ) :
                                        pfN = newSpot.candidates[i]
                                        for d in range(len(pos)) :
                                            pN[d] = round( pfN.p1.l[d] - 0.5 )
                                        foundIdentical = False
                                        
                                        for s in spots :
                                            for p in s.inliers :
                                                same = True
                                                
                                                for d in range(len(pos)) :
                                                    if pN[d] != round( p.p1.l[d] - 0.5 ) :
                                                        same = False
                                                        break
                                                if same == True :
                                                    foundIdentical = True
                                                    break
                                            
                                            if foundIdentical : 
                                                break
                                        
                                        if foundIdentical : 
                                            del newSpot.candidates[i]
                                    
                                    newSpot.updateScale(spot.scale)
                                    
                                    print( "new candidate for : " + str(spot.loc) + "@" + str(pos) + " : " + str(len(list)) )
                                    
                                    Spot.ransac2(newSpot, iterations, maxError, inlierRatio, False, minNumInliers)
                                    
                                    print( str(len(newSpot.inliers)) + " from " + str(len(list)) )
                                    
                                    # Ad-hoc criteria that the inliers either increase by 33% or that they reach the range of the normal spots
                                    if len(newSpot.inliers) >= minNumInliers and len(newSpot.inliers) >= thr2 :
                                        newSpot.center.fitFunction(newSpot.inliers)
                                        additionalSpots.append(newSpot)
                                        print( str(len(newSpot.inliers)) + " -- " + str(newSpot.localize()) ) 
                            except : pass
                            
                            try : 
                                # re-fit as we might have destroyed locations
                                if len(spot.inliers) >= spot.center.minNumPoints :
                                    spot.center.fitFunction(spot.inliers)
                            except : pass
        
        else :
            if not silent :
                print("No spots remaining after RANSAC.")
        
        return additionalSpots                      
                            
                            
                
                            
                    
            
               
    def ransac2(spot, iterations, maxError, inlierRatio, multiConsensus, minNumInliers) :
        
        if multiConsensus :
            spot.numRemoved = len(spot.candidates)
            
            filter = Spot.MultiConsensusFilter(spot, iterations, maxError, inlierRatio, minNumInliers, False)
            # allMatches = PointFunctionMatch object list
            allMatches = filter.filter(spot.candidates)
            
            if allMatches == None or len(allMatches) == 0 :
                spot.inliers = []
            else : 
                spot.inliers = allMatches[0] 
                for i in range( 1, len(allMatches) ) :
                    spot.multiConsensusMatches.append([allMatches[i]])
            
            spot.numRemoved -= len(spot.inliers)
                    
                    
        else : 
            self_inliers = spot.center.filterRansac(spot.candidates, spot.inliers, iterations, maxError, inlierRatio, minNumInliers)
            spot.center = self_inliers[0]
            spot.inliers = self_inliers[1]
            spot.numRemoved = len(spot.candidates) - len(spot.inliers)
        
        if len(spot.inliers) >= spot.center.minNumPoints :
            spot.center.fitFunction(spot.inliers)



    def localize(self) :
        center = []
        
        for d in range(self.n) :  
    
            center.append(self.center.getSymmetryCenter(d) / self.scale[d])
    
        return center
    
    
    # spot들의 loc과 parameter로 받는 loc을 비교 -> 일치하는 loc을 가지는 spot 발견 시 return True
    def pointExists(loc, spots) :
        for spot in spots :
            equal = True
            for d in range(len(spot.loc)) :
                if loc[d] != spot.loc[d] :
                    equal = False
                    break
                
            if equal == True :
                return True
        
        return False
    
                
    

    class MultiConsensusFilter :
        
        def __init__(self, spot, numIterations, maxEpsilon, minInlierRatio, minNumInliers, silent) :
            self.spot = spot
            self.numIterations = numIterations
            self.maxEpsilon = maxEpsilon
            self.minInlierRatio = minInlierRatio
            self.minNumInliers = minNumInliers
            self.silent = silent
         
         
        def filterMultiConsensusSets(self, candidates) :
            
            inliers = []
            modelFound = True
            
            while True :
                modelInliers = []
                try :
                    modelFound = self.spot.center.filterRansac(candidates,
                                                               modelInliers,
                                                               self.numIterations,
                                                               self.maxEpsilon,
                                                               self.minInlierRatio,
                                                               self.minNumInliers,
                                                               4)
                    self.spot.center = modelFound[0]
                    modelInliers = modelFound[1]
                except :
                    modelFound = False
                
                if modelFound :
                    inliers.append(modelInliers)
                    
                    '''
                    for x in candidates :
                        for y in modelInliers :
                            if x.p1.l == y.p1.l :
                                candidates.remove(x)
                                break
                    '''
                    for x in range(len(candidates)-1,-1,-1) :
                        for y in range(len(modelInliers)-1,-1,-1) :
                            if candidates[x].p1.l == modelInliers[y].p1.l :
                                candidates.remove(candidates[x])
                                break
                    
                # break
                if not modelFound :
                    break
                
            return inliers


        def filter(self, candidates) :
            multiConsensusSets = self.filterMultiConsensusSets(candidates)
            
            return multiConsensusSets
        

if __name__ == '__main__' :
    pass
