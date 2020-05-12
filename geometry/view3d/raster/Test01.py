'''
Created on Apr 23, 2015

Ejemplo del triangulo rotante

@author: fapablaza 
'''

from PyQt4.QtOpenGL import QGLWidget
from OpenGL.raw.GL.VERSION.GL_1_1 import GL_COLOR_BUFFER_BIT,\
    GL_DEPTH_BUFFER_BIT, GL_PROJECTION, GL_MODELVIEW
from OpenGL.GL.VERSION.GL_1_1 import GL_DEPTH_BUFFER
from OpenGL.raw.GL.VERSION.GL_1_0 import glLoadIdentity, glClear, glFlush,\
    glColor3f, glClearColor, glVertex3f, glRotatef, glPushMatrix, glPopMatrix,\
    glClearDepth, glMatrixMode, glViewport
from OpenGL.GL.exceptional import glEnd, glBegin
from OpenGL.raw.GL.ARB.tessellation_shader import GL_TRIANGLES
from OpenGL.raw.GLU import gluPerspective, gluLookAt
from PyQt4.Qt import QApplication

class MyGLWidget(QGLWidget):
    
    def __init__(self, parent):
        QGLWidget.__init__(self, parent)
        self.setMinimumSize(400, 300)
        self.angle = 0.0
    
    def initializeGL(self):
        glClearColor(0.0, 0.0, 1.0, 0.0)
        glClearDepth(1.0)
    
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        
        gluLookAt(0.0, 2.5, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
        
        glRotatef(self.angle, 0.0, 1.0, 0.0)
        
        glBegin(GL_TRIANGLES)
        glColor3f(1.0, 1.0, 0.0)
        glVertex3f(0.0, 1.0, 0.0)
        glVertex3f(-1.0, -1.0, 0.0)
        glVertex3f(1.0, -1.0, 0.0)
        glEnd()
        
        glPopMatrix()
        
        glFlush()
        
    def resizeGL(self, w, h):
        if h <= 0:
            h = 1
        
        glViewport(0, 0, w, h)
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60.0, float(w)/float(h), 0.1, 100)
        

if __name__ == '__main__':
    app = QApplication(['Triangle Demo'])
    
    window = MyGLWidget(None)
    window.show()
    
    app.exec_()
