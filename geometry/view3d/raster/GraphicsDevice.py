
'''
Created on Apr 22, 2015

@author: fapablaza
'''

import numpy

from Material import Material
from OpenGL.GL import *
from OpenGL.raw.GL import *
#from OpenGL.GL.VERSION.GL_1_0 import glMaterialfv, glLoadMatrixf, glLightfv
from OpenGL.raw.GL.VERSION.GL_1_1 import GL_AMBIENT, GL_SPECULAR, GL_DIFFUSE,\
    GL_FRONT, GL_EMISSION, GL_SHININESS, GL_MODELVIEW, GL_PROJECTION,\
    GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, glEnableClientState,\
    GL_NORMAL_ARRAY, GL_TEXTURE_COORD_ARRAY, glDisableClientState,\
    GL_PERSPECTIVE_CORRECTION_HINT, glDrawArrays, GL_POINT, GL_POINTS,\
    GL_DEPTH_TEST, GL_LIGHTING, GL_LIGHT0, GL_AUTO_NORMAL, GL_NORMALIZE,\
    GL_POSITION, GL_CULL_FACE
#from OpenGL.raw.GL.VERSION.GL_1_0 import glMatrixMode, glClearColor, glClear,\
#    glFlush, glFinish, glViewport, glLoadIdentity, glTranslatef, glScalef,\
#    glRotatef, glEnable, glClearDepth, glNormal3f, glTexCoord2f, glVertex3f
#from OpenGL.raw.GL.VERSION.GL_1_5 import GL_ARRAY_BUFFER, glBindBuffer,\
#    GL_ELEMENT_ARRAY_BUFFER
#from OpenGL.raw.GL.KHR.debug import GL_VERTEX_ARRAY
from OpenGL.GL.pointers import glVertexPointer, glNormalPointer,\
    glTexCoordPointer, glDrawElements
from OpenGL.arrays import *
#from OpenGL.arrays._arrayconstants import GL_FLOAT
from OpenGL.raw.GLU import gluLookAt, gluPerspective
from MeshSubset import MeshSubset
#from geometry.view3d.raster.MeshSubset import MeshSubset
#from OpenGL.raw.GL.ARB.tessellation_shader import GL_TRIANGLES
#from OpenGL.raw.GL.ARB.internalformat_query2 import GL_TEXTURE_2D
from OpenGL.GL.exceptional import glBegin, glEnd
    
class Transform():
    MODELVIEW = 0
    PROJECTION = 1

class Primitive():
    POINT_LIST = 1
    TRIANGLE_LIST = 4
    
class GraphicsDevice(object):
    
    def __init__(self):
        self.__material = Material(None)
        self.__previousMaterial = Material(None)
        
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_AUTO_NORMAL)
        glEnable(GL_NORMALIZE)
        glEnable(GL_CULL_FACE)
        
        glClearDepth(1.0)
    
    def createMeshSubset(self, primitive, vertices, indices):
        return MeshSubset(primitive, vertices, indices)
    
    def setTransform(self, transform, matrix):
        glMatrixMode(self.__convertTransform(transform))
        glLoadMatrixf(matrix)
    
    def setTransformLookAt(self, eye, lookat, up):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(eye[0], eye[1], eye[2], lookat[0], lookat[1], lookat[2], up[0], up[1], up[2])
        
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.8, 0.8, 0.8, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
        glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 0.0, 1.0, 0.0])
        
    def setTransformPerspective(self, fov, aspect, znear, zfar):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(fov, aspect, znear, zfar)
    
    def appendTranslationTransform(self, pos):
        glMatrixMode(GL_MODELVIEW)
        glTranslatef(pos[0], pos[1], pos[2])
    
    def appendScalingTransform(self, scale):
        glMatrixMode(GL_MODELVIEW)
        glScalef(scale[0], scale[1], scale[2])
        
    def appendRotationXTransform(self, rads):
        glMatrixMode(GL_MODELVIEW)
        glRotatef(rads, 1.0, 0.0, 0.0)
        
    def appendRotationYTransform(self, rads):
        glMatrixMode(GL_MODELVIEW)
        glRotatef(rads, 0.0, 1.0, 0.0)
        
    def appendRotationZTransform(self, rads):
        glMatrixMode(GL_MODELVIEW)
        glRotatef(rads, 0.0, 0.0, 1.0)
        
    def appendRotationTransform(self, rads, axis):
        glMatrixMode(GL_MODELVIEW)
        glRotatef(rads, axis[0], axis[1], axis[2])
    
    def setMaterial(self, material):
        self.__previousMaterial = self.getMaterial()
        self.__material = material
    
    def getMaterial(self):
        return self.__material
    
    def beginFrame(self, color):
        glClearColor(color[0], color[1], color[2], color[3])
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
    def endFrame(self):
        glFlush()
        
    def render(self, subset):
        # if self.__previousMaterial != self.getMaterial():
        #     self.__preRenderMaterial(self.getMaterial())
        
        self.__renderMeshSubset(subset)
        
        # if self.__previousMaterial != self.getMaterial():
        #     self.__postRenderMaterial(self.getMaterial())
        
    def setViewport(self, x, y, w, h):
        if h == 0:
            h = 1
            
        glViewport(x, y, w, h)
    
    def __renderMeshSubset(self, subset):
        if subset.getIBufferId() != 0:
            self.__renderIndexedMeshSubset(subset)
        else:
            # self.__renderNonIndexedMeshSubset(subset)
            self.__renderNonIndexedMeshSubsetOld(subset)
    
    def __renderIndexedMeshSubset(self, subset):
        pass
        
    def __renderNonIndexedMeshSubset(self, subset):
        '''
        En reparaciones...
        '''
        vertexStride = 4*(3 + 3 + 2)
        
        glBindBuffer(GL_ARRAY_BUFFER, subset.getBufferId())
        
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        
        glVertexPointer(3, GL_FLOAT, vertexStride, 0)
        glNormalPointer(GL_FLOAT, vertexStride, 3*4)
        glTexCoordPointer(2, GL_FLOAT, vertexStride, 6*4)
        
        glDrawArrays(self.__convertPrimitive(subset.getPrimitive()), 0, subset.getVertices().size/8)
        
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)
        
    def __renderNonIndexedMeshSubsetOld(self, subset):
        '''
        Funcion provisoria mientras se repara la anterior ...
        '''
        vertices = subset.getVertices()
        
        glBegin(self.__convertPrimitive(subset.getPrimitive()))
        for i in range(0, vertices.shape[0]):
            vertex = vertices[i, ]
            
            x, y, z = vertex[0], vertex[1], vertex[2]
            nx, ny, nz = vertex[3], vertex[4], vertex[5]
            u, v = vertex[6], vertex[7]
            
            glNormal3f(nx, ny, nz)
            glTexCoord2f(u, v)
            glVertex3f(x, y, z)
        glEnd()
        
    
    def __renderMaterial(self, material):
        glMaterialfv(GL_FRONT, GL_AMBIENT, material.getAmbient())
        glMaterialfv(GL_FRONT, GL_DIFFUSE , material.getDiffuse())
        glMaterialfv(GL_FRONT, GL_SPECULAR, material.getSpecular())
        glMaterialfv(GL_FRONT, GL_EMISSION, material.getEmissive())
        glMaterialfv(GL_FRONT, GL_SHININESS, numpy.array([material.getShininess()]))
    
    def __preRenderMaterial(self, material):
        self.__previousMaterial = self.getMaterial()
        self.__renderMaterial(material)
    
    def __postRenderMaterial(self, material):
        self.__renderMaterial(self.__previousMaterial)
    
    def __convertPrimitive(self, primitive):
        if primitive == Primitive.POINT_LIST:
            return GL_POINTS
        elif primitive == Primitive.TRIANGLE_LIST:
            return GL_TRIANGLES
        else:
            return 0; 
    
    def __convertTransform(self, transform):    
        if transform == Transform.MODELVIEW:
            return GL_MODELVIEW
        elif transform == Transform.PROJECTION:
            return GL_PROJECTION
        else:
            return 0
    
