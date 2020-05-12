'''
Created on Apr 23, 2015

@author: fapablaza
'''
import numpy 

from PyQt4.QtOpenGL import QGLWidget
from PyQt4.Qt import QApplication
from outlier.raster.GraphicsDevice import GraphicsDevice, Primitive
from OpenGL.GL.exceptional import glBegin, glEnd
from OpenGL.raw.GL.ARB.tessellation_shader import GL_TRIANGLES
from OpenGL.raw.GL.VERSION.GL_1_0 import glVertex3f, glColor3f

class MyGLWidget(QGLWidget):
    
    def __init__(self, parent):
        QGLWidget.__init__(self, parent)
        
        self.setMinimumSize(400, 300)
        self.angle = 0.0
        self.graphicsDevice = None
        self.meshSubset = None
    
    def initializeGL(self):
        self.graphicsDevice = GraphicsDevice()
        
        vertices = numpy.array(
            [[0.0, 1.0, 0.0,    0.0, 0.0, 1.0,     0.0, 0.0],
            [-1.0, -1.0, 0.0,    0.0, 0.0, 1.0,     0.0, 0.0],
            [1.0, -1.0, 0.0,     0.0, 0.0, 1.0,     0.0, 0.0]], 
            numpy.float32)
        
        self.meshSubset = self.graphicsDevice.createMeshSubset(Primitive.TRIANGLE_LIST, vertices, None)
    
    def paintGL(self):
        color = numpy.array([0.0, 0.0, 1.0, 0.0], numpy.float32)
        
        self.graphicsDevice.beginFrame(color)
        
        self.graphicsDevice.setTransformLookAt([0.0, 2.5, 1.0], [0.0, 0.0, 0.0], [0.0, 1.0, 0.0])
        self.graphicsDevice.render(self.meshSubset)
        
        self.graphicsDevice.endFrame()
        
    def resizeGL(self, w, h):
        if h == 0:
            h = 1
                
        self.graphicsDevice.setViewport(0, 0, w, h)
        self.graphicsDevice.setTransformPerspective(60.0, float(w)/float(h), 0.1, 100.0)

if __name__ == '__main__':
    app = QApplication(['Triangle Demo'])
    
    window = MyGLWidget(None)
    window.show()
    
    app.exec_()
