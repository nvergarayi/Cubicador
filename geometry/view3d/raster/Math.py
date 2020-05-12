'''
Funciones para la construccion de matrices de
@author: fapablaza
'''

import numpy

def createZeroMatrix():
    return numpy.zeros([4, 4], numpy.float32)

def createIdentityMatrix():
    matrix = createZeroMatrix()
    matrix[0, 0] = 1.0
    matrix[1, 1] = 1.0
    matrix[2, 2] = 1.0
    matrix[3, 3] = 1.0
    
    return matrix
    
def createTranslationMatrix(x, y, z):
    matrix = createIdentityMatrix()
    
def createScalingMatrix(x, y, z):
    pass

def createRotationXMatrix(rads):
    pass

def createRotationYMatrix(rads):
    pass

def createRotationZMatrix(rads):
    pass

def createRotationMatrix(rads, x, y, z):
    pass
