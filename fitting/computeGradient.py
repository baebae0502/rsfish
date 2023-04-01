

class Gradient :
    
    def __init__(self, numDimensions = None) :
        self.numDimensions = numDimensions

    def gradientAt(self, location, derivativeVector) :
        pass


class ComputeGradient :
    
    '''
    Compute the n-dimensional 1st derivative vector in center of a 2x2x2...x2 environment for a certain location
    defined by the position of the RandomAccess
    - param location :  the top-left-front position for which to compute the derivative
    - param derivativeVector : where to put the derivative vector [3]
    '''    
    def gradientAt(self, location, derivativeVector) :
        pass
    

class ComputeGradient2d(ComputeGradient) :
    
    def __init__(self, image) :
        self.image = image
    
    def gradientAt(self, location, derivativeVector) :
        # location = [x,y]
        # image[y,x]
        
        #p0 = self.image[ location[0], location[1] ]
        #p1 = self.image[ location[0], location[1] + 1 ]
        #p2 = self.image[ location[0] + 1, location[1] ]
        #p3 = self.image[ location[0] + 1, location[1] + 1 ]
        p0 = self.image[ location[1], location[0] ]
        p1 = self.image[ location[1], location[0] + 1 ]
        p2 = self.image[ location[1] + 1, location[0] ]
        p3 = self.image[ location[1] + 1, location[0] + 1 ]
        
        
        
        derivativeVector.append( ((p1+p3) - (p0+p2)) / 2.0 )
        derivativeVector.append( ((p2+p3) - (p0+p1)) / 2.0 )
        
        return derivativeVector
    

class ComputeGradient3d(ComputeGradient) :
    
    def __init__(self, image) :
        self.image = image
    
    def gradientAt(self, location, derivativeVector):
        # image[y,x,z]
        p0 = self.image[ location[0], location[1], location[2] ]
        p1 = self.image[ location[0], location[1] + 1, location[2] ]
        p2 = self.image[ location[0] + 1, location[1], location[2] ]
        p3 = self.image[ location[0] + 1, location[1] + 1, location[2] ]
        p4 = self.image[ location[0], location[1], location[2] + 1 ]
        p5 = self.image[ location[0], location[1] + 1, location[2] + 1]
        p6 = self.image[ location[0] + 1, location[1], location[2] + 1]
        p7 = self.image[ location[0] + 1, location[1] + 1, location[2] + 1]
        
        derivativeVector.append( ((p1+p3+p5+p7) - (p0+p2+p4+p6)) / 4.0 )
        derivativeVector.append( ((p2+p3+p6+p7) - (p0+p1+p4+p5)) / 4.0 )
        derivativeVector.append( ((p4+p5+p6+p7) - (p0+p1+p2+p3)) / 4.0 )
        
        return derivativeVector

        
class GradientOnDemand(Gradient) :
    
    def __init__(self, image, numDimensions = None) :
        self.image = image
        self.numDimensions = len(image.shape) 
    
        if self.numDimensions == 2 :
            self.computeGradient = ComputeGradient2d(image)
        elif numDimensions == 3 :
            self.computeGradient = ComputeGradient3d(image)

    def gradientAt(self, location, derivativeVector):
        # location = [x,y]
        return self.computeGradient.gradientAt(location, derivativeVector)
        
    

class GradientPreCompute(Gradient) :
    
    def __init__(self, image) :
        self.n1 = image.ndim
        self.n2 = self.n1 + 1
        self.minIterate = []
        self.maxIterate = []
        self.tmp = []
        self.gradient = self.preCompute(image)
        
        
    def preCompute(self, image) :
        
        import numpy as np
    
        # 2-dimensional 의 경우. 3d의 경우 if문으로 추가해야됨.  
        derivatives = np.zeros((2, image.shape[0] - 1, image.shape[1] - 1))
        god = GradientOnDemand(image)
        dv = []
    
        for y in range(image.shape[0] - 1) :
            for x in range(image.shape[1] - 1 ) :
                for z in range(2) :
                    derivatives[z, y, x] = god.gradientAt([x, y],dv)[z]
                    dv=[]
                    
        
        return derivatives





if __name__ == '__main__' :

    import cv2
    image_path = '/home/baejs/rsfish-project/resources/TestGauss2d_image.tif'

    image = cv2.imread(image_path, -1)

    god = GradientOnDemand(image)
    print(god.numDimensions)
    print(god.computeGradient)
    dv = []

    
    '''
    # IndexError: index 256 is out of bounds for axis 1 with size 256
    
    for i in range(256) :
        for j in range(256) :
            god.gradientAt([i,j],dv)
    '''        
    import numpy as np
    
    derivativeVector = np.zeros((2, image.shape[0] - 1, image.shape[1] - 1))
    print(derivativeVector[1,0:9,0:10])

    for y in range(image.shape[0] - 1) :
        for x in range(image.shape[1] - 1 ) :
            for z in range(2) :
                derivativeVector[z, y, x] = god.gradientAt([x, y],dv)[z]
                dv=[]
            
    print(god.gradientAt([0,58],dv))
    print(derivativeVector[0,0,:80])
    
    
  

