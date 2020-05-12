'''
Created on Apr 23, 2015

@author: fapablaza
'''
from OpenGL.GL.exceptional import glGenTextures
from OpenGL.raw.GL import *
#from OpenGL.raw.GL.VERSION.GL_1_1 import glBindTexture, GL_RGBA,\
#    GL_TEXTURE_MAG_FILTER, GL_LINEAR, GL_TEXTURE_MIN_FILTER
from OpenGL.raw.GL.ARB.internalformat_query2 import GL_TEXTURE_2D
from OpenGL.arrays._arrayconstants import GL_UNSIGNED_BYTE
from OpenGL.GL.images import glTexImage2D
#from OpenGL.raw.GL.VERSION.GL_1_0 import glTexParameteri

class Texture(object):
    def __init__(self, width, height, data):
        '''
        Inicializa una textura a partir de los datos en bruto de una imagen en formato RGBA
        '''
        
        textureId = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, textureId)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        
        self.__textureId = textureId
    
    def getTextureId(self):
        return self.__textureId
    
