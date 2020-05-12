
'''
Created on Apr 22, 2015

@author: fapablaza
'''
from Material import Material
#from geometry.view3d.raster.Material import Material
from OpenGL.GL import *

class MeshSubset(object):
    '''
    Porcion elemental de geometria
    '''
    def __init__(self, primitive, vertices, indices):
        '''
        @param vertices: Arreglo numpy unidimensional con los datos de vertices, en el formato (X, Y, Z, NX, NY, NZ, TU, TV), todos
        de tipo numpy.float32. 
        @param indices: Arreglo numpy unidimencional con la informacion de indexacion de la geometria. 
        '''
        self.__material = Material(None)
        self.__vertices = vertices
        self.__indices = indices
        self.__primitive = primitive
        
        # inicializa el buffer de vertices
        size = vertices.size*4
        
        bufferId  = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, bufferId)
        glBufferData(GL_ARRAY_BUFFER, vertices.size*4, vertices, GL_STATIC_DRAW)
        
        # inicializa el buffer de indices
        if indices is None:
            ibufferId = 0
        else:
            ibufferId = glGenBuffers(1)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibufferId)
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.size*4, indices, GL_STATIC_DRAW) 
        
        self.__bufferId = bufferId
        self.__ibufferId = ibufferId
    
    def getMaterial(self):
        return self.__material
    
    def getVertices(self):
        return self.__vertices
    
    def getIndices(self):
        return self.__indices
    
    def getBufferId(self):
        return self.__bufferId
    
    def getIBufferId(self):
        return self.__ibufferId
    
    def getPrimitive(self):
        return self.__primitive
