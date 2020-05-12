'''
Created on Apr 23, 2015

@author: fapablaza
'''
import numpy 

from PyQt4.QtOpenGL import QGLWidget
from PyQt4.Qt import QApplication, QPoint
from GraphicsDevice import GraphicsDevice, Primitive, Transform
from Util import createVertexArrayFromTriangles
#from geometry.view3d.raster.GraphicsDevice import GraphicsDevice, Primitive, Transform
#from geometry.view3d.raster.Util import createVertexArrayFromTriangles

class View3D(QGLWidget):
    
    def __init__(self, parent, triangles):
        '''
        @param triangles: Lista de triangulos a mostrar en pantalla. 
        La inicializacion de la malla de OpenGL se hace en el metodo 'initializeGL'
        '''
        QGLWidget.__init__(self, parent)
        
        self.setMinimumSize(400, 300)
        # self.__angle = 0.0
        self.__graphicsDevice = None    # Dispositivo grafico
        self.__meshSubset = None        # Objeto a visualizar
        self.__triangles = triangles    # Lista temporal de triangulos usada para inicializar el objeto
        
        self.__lastMousePosition = None
        
        self.__yaw = 0.0
        self.__pitch = 0.0
    
    def initializeGL(self):
        self.__graphicsDevice = GraphicsDevice()
        
        vertices = createVertexArrayFromTriangles(self.__triangles)
        
        self.__meshSubset = self.__graphicsDevice.createMeshSubset(Primitive.TRIANGLE_LIST, vertices, None)
        self.__triangles = None
    
    def paintGL(self):
        color = numpy.array([0.0, 0.0, 0.0, 0.0], numpy.float32)
        
        self.__graphicsDevice.beginFrame(color)
        
        self.__graphicsDevice.setTransformLookAt([0.0, 5.5, 3.0], [0.0, 0.0, 0.0], [0.0, 1.0, 0.0])
        self.__graphicsDevice.appendRotationXTransform(self.__yaw)
        self.__graphicsDevice.appendRotationYTransform(self.__pitch)
        self.__graphicsDevice.render(self.__meshSubset)
        
        self.__graphicsDevice.endFrame()
        
    def resizeGL(self, w, h):
        if h == 0:
            h = 1
                
        self.__graphicsDevice.setViewport(0, 0, w, h)
        self.__graphicsDevice.setTransformPerspective(60.0, float(w)/float(h), 1, 100.0)
    
    def mouseMoveEvent(self, event):
        mousePosition = event.posF()
        
        if self.__lastMousePosition is None:
            self.__lastMousePosition = mousePosition
        
        delta = self.__lastMousePosition - mousePosition
        self.__lastMousePosition = mousePosition
        
        self.__pitch += float(delta.x())
        self.__yaw += float(delta.y())
        
        self.repaint()
    
