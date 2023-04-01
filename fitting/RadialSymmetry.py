from enum import Enum
from computeGradient import GradientOnDemand
import RadialSymParams


class RadialSymmetry : 
    
    class Ransac(Enum) :
        NONE = 1
        SIMPLE = 2
        MULTICONSENSU = 3
        
    bsNumIterations = 500   # not a parameter, can be changed through Beanshell 
    numIterations = 250     # not a parameter, can be changed through Beanshell

    peaks = None
    spots = None
    derivative = None
    ng = None
    
    img = None
    params = None
    globalInterval = None   # we need to know where to cut off gradients at image borders
    computeInterval = None
    
    def __init__(self, img, globalInterval, computeInterval, params) :
        self.img = img    
        self.params = params
        self.globalInterval = globalInterval
        self.computeInterval = computeInterval
    
    
    def compute(rs, pImg, globalInterval, computeInterval, p) :
        
        # perform DOG    
        print( "Computing DoG..." )
        
        rs.peaks = RadialSymmetry.computeDog(pImg, computeInterval, p.sigma, p.threshold, p.anisotropyCoefficient, p.useAnisotropyForDoG) # p.numThreads는 일단 생략
    
        print( "DoG pre-detected spots : " + str(len(rs.peaks)) )
    
        # calculate (normalized) derivatives
        rs.derivative = GradientOnDemand(pImg)
        rs.ng = RadialSymmetry.calculateNormalizedGradient(rs.derivative, RadialSymParams.bsMethods[p.bsMethod])

        
        print( "Computing Radial Symmetry..." )
        
        rs.spots = computeRadialSymmetry(
            globalInterval,
            rs.ng,
            rs.derivative,
            rs.peaks,
            [p.supportRadius, pImg.ndim],
            p.inlierRatio,
            p.maxError,
            p.anisotropyCoefficient,
            p.RANSAC(),
            p.minNumInliers,
            p.nTimesStDev1,
            p.nTimesStDev2)
    
        ##########################################
        
            
            
            
        
    
    
    def computeDog(pImg, interval, pSigma, pThreshold, anisotropy, useAnisotropy, numThreads) :
        
        pSigma2 = pSigma * ( pow(2, 1 / RadialSymParams.defaultSensitivity) )
        
        calibration = [0] * pImg.ndim
        calibration[0] = 1.0
        calibration[1] = 1.0
        if len(calibration) == 3 :
            calibration[2] = 1.0 / anisotropy if useAnisotropy else 1.0
        
        ##########################################333
        
    
    def calculateNormalizedGradient() :
        pass
    
    def computeRadialSymmetry() :
        pass