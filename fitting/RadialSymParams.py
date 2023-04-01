import RadialSymmetry

class RadialSymParams :
    
    modeChoice = [ "Interactive", "Advanced" ]
    ransacChoice = [ "No RANSAC", "RANSAC", "Multiconsensus RANSAC" ]

    bsMethods = [ "No background subtraction", "Mean", "Median", "RANSAC on Mean", "RANSAC on Median" ]
    intensityMethods = [ "Linear Interpolation", "Gaussian fit (on inlier pixels)", "Integrate spot intensities (on candidate pixels)" ]

    defaultAutoMinMax = True
    defaultMin = 0
    defaultMax = 255

    defaultIntensityThreshold = 0
    defaultSigma = 1.5
    defaultThreshold = 0.007

    defaultMaxError = 1.5
    defaultInlierRatio = 10.0 / 100.0
    defaultSupportRadius = 3

    defaultBsInlierRatio = 75.0 / 100.0
    defaultBsMaxError = 0.05
    defaultBsMethodChoice = 0

    defaultRANSACChoice = 1
    defaultAnisotropy = 1
    defaultUseAnisotropyForDoG = True

    defaultIntensityMethod = 0
    # defaultGaussFitLocation = False
    defaultMode = 0
    defaultImg = 0

    defaultAddToROIManager = False

    defaultResultsFilePath = ""

    # only used for DoG
    # numThreads = Runtime.getRuntime().availableProcessors();

    # steps per octave for DoG
    defaultSensitivity = 4

    # multiconsensus options
    defaultMinNumInliers = 20
    defaultNTimesStDev1 = 8.0
    defaultNTimesStDev2 = 6.0

    # min/max
    autoMinMax = defaultAutoMinMax
    min = float('nan')
    max = float('nan')

    # RANSAC parameters
    # current value
    # .. public Ransac RANSAC() { return Ransac.values()[ ransacSelection ]; }
    ransacSelection = defaultRANSACChoice
    def RANSAC(self) :
        return RadialSymmetry.Ransac(self.ransacSelection)
    maxError = defaultMaxError 
    inlierRatio = defaultInlierRatio
    supportRadius = defaultSupportRadius

    # Background Subtraction parameter
    # current values
    bsMaxError = defaultBsMaxError 
    bsInlierRatio = defaultInlierRatio
    bsMethod = defaultBsMethodChoice

    # DoG parameters
    # current
    sigma = defaultSigma 
    threshold = defaultThreshold

    # intensity threshold
    intensityThreshold = defaultIntensityThreshold

    # Z-scaling anisotropy calculation
    anisotropyCoefficient = defaultAnisotropy
    useAnisotropyForDoG = defaultUseAnisotropyForDoG

    # use gauss fit
    intensityMethod = defaultIntensityMethod
    # public boolean gaussFitLocation = defaultGaussFitLocation

    # multiconsensus options
    minNumInliers = defaultMinNumInliers
    nTimesStDev1 = defaultNTimesStDev1 
    nTimesStDev2 = defaultNTimesStDev2

    # ROI manager
    addToROIManager = defaultAddToROIManager

    # advanced output
    resultsFilePath = defaultResultsFilePath

    ''' skip
    public void printParams() { printParams(true); }
    public void printParams( final boolean printIntensityThreshold ) {
        HelperFunctions.log("SigmaDoG               : " + sigma);
        HelperFunctions.log("ThresholdDoG           : " + threshold);
        HelperFunctions.log("anisotropyCoefficient  : " + anisotropyCoefficient);
        HelperFunctions.log("useAnisotropyForDoG    : " + useAnisotropyForDoG);
        HelperFunctions.log("RANSAC                 : " + RANSAC() );
        HelperFunctions.log("MaxError               : " + maxError);
        HelperFunctions.log("InlierRatio            : " + inlierRatio);
        HelperFunctions.log("supportRadius          : " + supportRadius);
        HelperFunctions.log("Intensity computation  : " + intensityMethods[ intensityMethod ]);
        //HelperFunctions.log("GaussFitLocation       : " + gaussFitLocation);
        if ( printIntensityThreshold )
            HelperFunctions.log("intensityThreshold     : " + intensityThreshold);
        HelperFunctions.log("min intensity          : " + min);
        HelperFunctions.log("max intensity          : " + max);
        HelperFunctions.log("autoMinMax             : " + autoMinMax);
        HelperFunctions.log("resultsFilePath        : " + resultsFilePath);

        if ( ransacSelection == 2 )
        {
            HelperFunctions.log("minNumInliers          : " + minNumInliers);
            HelperFunctions.log("nTimesStDev1           : " + nTimesStDev1);
            HelperFunctions.log("nTimesStDe             : " + nTimesStDev2);
        }

        HelperFunctions.log("bsMethod               : " + bsMethods[ bsMethod ]);
        HelperFunctions.log("bsMaxError             : " + bsMaxError);
        HelperFunctions.log("bsInlierRatio          : " + bsInlierRatio);

    }
    '''

