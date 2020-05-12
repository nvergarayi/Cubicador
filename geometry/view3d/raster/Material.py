'''
Created on Apr 22, 2015

@author: fapablaza
'''

import numpy 

class Material(object):
    '''
    Almacena las componentes de color de un material (modelo gouraud de iluminacion)
    '''
    def __init__(self, texture):
        self.__ambient = numpy.array([0.2, 0.2, 0.2, 1.0], numpy.float32)
        self.__diffuse = numpy.array([0.8, 0.8, 0.8, 1.0], numpy.float32)
        self.__specular = numpy.array([0.0, 0.0, 0.0, 1.0], numpy.float32)
        self.__emissive = numpy.array([0.0, 0.0, 0.0, 1.0], numpy.float32)
        self.__shininess = 0.0
        self.__texture = texture
        
    def getAmbient(self):
        return self.__ambient
    
    def getDiffuse(self):
        return self.__diffuse
    
    def getSpecular(self):
        return self.__specular
    
    def getEmissive(self):
        return self.__emissive
    
    def getShininess(self):
        return self.__shininess
    
    def setShininess(self, value):
        self.__shininess = value
        
    def getTexture(self):
        return self.__texture
    