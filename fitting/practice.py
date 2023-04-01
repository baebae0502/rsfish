#%%
from Points import *
from Line import *
import copy
from enum import Enum
from Center import *


x = PointFunctionMatch(Point([4, 28.65]))
print(x.p1.l)

line = Line(n=-16, m=11.66)

x.apply(line)
print(x.distance)
print(x)



a=10
  
def mulx10(x) :
    global a
    a = a*7

mulx10(a)
print(a)

b=None
if not b :
    print('b is None')
    
c = [1,2]
c1 = c.copy()
print(c1)

line2 = copy.deepcopy(line)
print(line2.cost)

##

class CenterMethod(Enum) :
        MEAN = 1
        MEDIAN = 2
        
for CM in CenterMethod :
    print(CM)

method = CenterMethod.MEDIAN
if method == CenterMethod.MEAN :
    print(method)
else :
    print("not MEAN")
    
## 

ct = Center(Center.CenterMethod.MEAN)
print(ct.method, ct.mean, ct.cost)

##

z = [1]
print(z*2)
print(type(z*2))

##

def caffeine(x) :
    return x+2, x+3


coffee = caffeine(10)
print(type(coffee))

##

ll = Line()
print(isinstance(ll, Line))

##

m1 = Line()
if isinstance(m1, Line) :
    m1.m, m1.n = caffeine(10)
elif isinstance(m1, Center) :
    m1.p = 4
    
print(m1.m)

##

coef = []
coef = 1
print(coef)

##

inliers = []
print(type(inliers))

##

a=[]
print(len(a))


class Dept:
    def __init__(self, dname):
        self.dname = dname
    class Prof:
        def __init__(self,pname):
            self.pname = pname
        class Country:
            def __init__(self,cname):
                self.cname = cname
    def call1() :
        spot = Dept.Prof('bae')
        print(spot.pname)

    def call2() :
        Dept.call1()
        print('hi')
    
Dept.call2()
#%%
import RadialSymParams
print(RadialSymParams.defaultBsInlierRatio)
# %%
from enum import Enum
class Shape(Enum):
    SQUARE = 2
    DIAMOND = 1
    CIRCLE = 3
    ALIAS_FOR_SQUARE = 2

# %%
