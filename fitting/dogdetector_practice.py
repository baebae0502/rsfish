# %%
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
1. load image
'''
img = cv2.imread("/home/baejs/rsfish-project/rsfish/resources/TestGauss2d_image.tif", -1)
#img = cv2.imread("/home/baejs/rsfish-project/rsfish/resources/multiple_dots_2D.tif", -1)
#img = cv2.imread("/home/baejs/rsfish-project/rsfish/resources/multiple_dots.tif", -1)


######################### display ########################
plt.imshow(img, cmap = plt.cm.gray)
plt.title('img')
plt.show()
##########################################################


'''
2. set parameter for DoG filter (default)
'''
sigma1 = 1.5
sigma2 = 1.5*( 2**(1/4) )
threshold = 0.007


'''
3. apply DoG filter
'''
blur1 = cv2.GaussianBlur(img, (0, 0), sigma1)
blur2 = cv2.GaussianBlur(img, (0, 0), sigma2)
dog = blur1 - blur2


'''
4. find local maxima coordinates
'''
kernel_size = 3
dilated = cv2.dilate(dog, np.ones((kernel_size, kernel_size), np.uint8))
local_max = (dog == dilated) & (dog > threshold)
max_coords = np.argwhere(local_max)

############################ display ###########################
img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
for coord in max_coords:
    cv2.circle(img_color, tuple(coord[::-1]), 5, (0, 0, 255), 2)
    
plt.imshow(img_color, cmap = plt.cm.gray)
plt.title('Local Maxima')
plt.show()
################################################################

peaks = []
for i in range(len(max_coords)) :
    peaks.append( [ max_coords[i,1].item(), max_coords[i,0].item() ] )

print(len(peaks))


'''
5. add a global gradient 
'''
derivative = GradientPreCompute(img)

######################### display ########################
plt.imshow(derivative.gradient[0,:,:], cmap = plt.cm.gray)
plt.title('derivative0')
plt.show()

plt.imshow(derivative.gradient[1,:,:], cmap = plt.cm.gray)
plt.title('derivative1')
plt.show()
##########################################################

ng = NormalizedGradientAvearge(derivative)

SupportRange = [6, 6] # => SupportRadius = 3

#spot = Spot.extractSpot(image, peaks[0], derivative, ng, SupportRange)
spots = Spot.extractSpots(img, peaks, derivative, ng, SupportRange)


'''
6. ransac on all spots
'''
Spot.ransac1(spots, 100, 0.15, 10.0/100.0, 0, False, 0.0, 0.0, None, None, None, None, None)
#interval = [[0,0], [255,255]]
#Spot.ransac1(spots, 100, 1.5, 10.0/100.0, 20, True, 8.0, 6.0, interval, derivative, None, SupportRange, None)


'''
7. print localizations
'''
c = 0
goodspots = []  # Spot() list

for spot in spots :
    spot.computeAverageCost(spot.inliers)
    if len(spot.inliers) > 10 and math.dist(spot.localize(), spot.loc) < 0.7 :
        goodspots.append(spot)
    
print(len(spots), len(goodspots))  

############################# display #############################
XY = np.array([(goodspot.center.xc, goodspot.center.yc) for goodspot in goodspots])
plt.imshow(img, cmap = plt.cm.gray)
plt.scatter(*XY.T, s=2.5, c='#FF0000')
plt.title('detected spots')
plt.show()
###################################################################

for goodspot in goodspots :
    result = goodspot.toString()
    print(result)



# %%
