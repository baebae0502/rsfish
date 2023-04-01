#%%
import cv2
import matplotlib.pyplot as plt
from skimage import measure, io
from skimage.morphology import local_maxima
import numpy as np
import imutils
from computeGradient import *
from normalizedGradient import *
from spot import *
from SymmetryCenter2d import *
from AbstractModel import *

'''
1. 이미지 불러오기 & show
'''
# image_path = '/home/baejs/rsfish-project/resources/multiple_dots_2D.tif'
image_path = '/home/baejs/rsfish-project/resources/TestGauss2d_image.tif'

#image = io.imread(image_path)
image = cv2.imread(image_path, -1)


plt.imshow(image, cmap = plt.cm.gray)
plt.title('image')
plt.show()


'''
2. local_maxima value (peak) 찾기
'''
y,x = local_maxima(image, indices = True)
peaks = []
for i in range(len(y)) :
    peaks.append([x[i].item(), y[i].item()])


'''
3. adding a global gradient for testing
'''
derivative = GradientPreCompute(image)

############### visualization of gradients ##############
plt.imshow(derivative.gradient[0,:,:], cmap = plt.cm.gray)
plt.title('derivative0')
plt.show()

plt.imshow(derivative.gradient[1,:,:], cmap = plt.cm.gray)
plt.title('derivative1')
plt.show()
########################################################

ng = NormalizedGradientAvearge(derivative)

range = [10, 10]

#spot = Spot.extractSpot(image, peaks[0], derivative, ng, range)
spots = Spot.extractSpots(image, peaks, derivative, ng, range)


'''
4. ransac on all spots
'''
Spot.ransac1(spots, 100, 0.15, 10.0/100.0, 0, False, 0.0, 0.0, None, None, None, None, None)
#interval = [[0,0], [255,255]]
#Spot.ransac1(spots, 100, 0.15, 10.0/100.0, 0, True, 8.0, 6.0, interval, derivative, None, range, None)


#%%
'''
5. print localizations
'''
c = 0
goodspots = []  # Spot() list

for spot in spots :
    
    spot.computeAverageCost(spot.inliers)
    
    if len(spot.inliers) > 10 and math.dist(spot.localize(), spot.loc) < 0.7 :
        goodspots.append(spot)
    
print(len(spots), len(goodspots))  

################## visualization of localization ##################
XY = np.array([(goodspot.center.xc, goodspot.center.yc) for goodspot in goodspots])
plt.imshow(image, cmap = plt.cm.gray)
plt.scatter(*XY.T, s=2.5, c='#FF0000')
plt.title('image')
plt.show()
###################################################################

#%%
for goodspot in goodspots :
    result = goodspot.toString()
    print(result)


