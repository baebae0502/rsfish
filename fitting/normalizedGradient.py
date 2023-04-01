
from computeGradient import *
from statistics import mean, median


class NormalizedGradient(Gradient) :
    
    def __init__(self, gradient) :
        self.n1 = gradient.numDimensions - 1
        self.gradient = gradient
        self.background = []
    
    
    def computeBackground(self, gradientsPerDim, bkgrnd) :
        pass
    
    
    def isBoundaryPixel(self, l, spotInterval, n) :
        # l = [x,y], spotInterval = [[min x, min y], [max x, max y]]
        for d in range(n) :
            p = l[d]
            # spotInterval[0] = min 좌표, spotInterval[1] = max 좌표 
            if p == spotInterval[0][d] or p == spotInterval[1][d] : 
                return True
        
        return False
    
    
    def gradientAt(self, location, derivativeVector) :
        # location = [x,y]
        # -> location[1] = y , location[0] = x
        # derivativeVector = [Z x Y x X] array      (ex)..[2 x 255 x 255]
        derivativeVector = self.gradient.gradient[ : , location[1], location[0]]
        
        
        for d in range(self.n1) :
            derivativeVector[d] -= self.background[d]
        
        derivativeVector = derivativeVector.tolist()
        
        return derivativeVector
    
        



    # compute the median or mean of the bounding area in all dimensions.
    def normalize(self, spotInterval) :
        # the list of gradients on the boundary separated by dimension
        gradientsPerDim = [ [], [] ]
        
        # define a local region to iterate around the potential detection
        v = []  
        x_interval = spotInterval[1][0] - spotInterval[0][0] + 1
        y_interval = spotInterval[1][1] - spotInterval[0][1] + 1
        
        for i in range(y_interval) :
            for j in range(x_interval) :
                x = j + spotInterval[0][0]
                y = i + spotInterval[0][1]
                
                if self.isBoundaryPixel([x,y], spotInterval, self.n1) :
                    
                    for d in range(self.n1) :
                        v = self.gradient.gradient[d,y,x]
                        gradientsPerDim[d].append(v)

        self.background = []
        
        self.background = self.computeBackground(gradientsPerDim, self.background)

    
    

class NormalizedGradientAvearge(NormalizedGradient) : 
    
    def __init__(self, gradient) :
        self.n1 = gradient.n1
        self.gradient = gradient
        self.background = []
    
    
    def computeBackground(self, gradientsPerDim, bkgrnd) :
        for d in range(self.n1) :
            #bkgrnd[d] = mean(gradientsPerDim[d])
            bkgrnd.append(mean(gradientsPerDim[d]))
        return bkgrnd
    
    
        

    


class NormalizedGradientMedian(NormalizedGradient) :
    
    def __init__(self, gradient) :
        self.n1 = gradient.n1
        self.gradient = gradient
        self.background = []
    
    
    def computeBackground(self, gradientsPerDim, bkgrnd) :
        for d in self.n1 :
            #bkgrnd[d] = median(gradientsPerDim[d])
            bkgrnd.append(median(gradientsPerDim[d]))
        return bkgrnd
    
    


if __name__ == '__main__' :
    pass


