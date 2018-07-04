import objc
from random import random

NSObject = objc.lookUpClass("NSObject")

class Math(NSObject):
    _seed = 0
    def setRandomSeed_(self, nseed):
        _seed = nseed
        seed(_seed)

    def randomFloatBetween_and_(self, nmin, nmax):
        return ((random()%0x7fffffff))*(nmax-nmin)+nmin



