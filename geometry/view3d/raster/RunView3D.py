from View3D import View3D
from PyQt4.Qt import QApplication

class Point3D(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        
class Triangle3D(object):
    def __init__(self, p0, p1, p2):
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2

def generateTriangleList():
    p0 = Point3D( 0.0,  1.0, 0.0)
    p1 = Point3D(-1.0, -1.0, 0.0)
    p2 = Point3D( 1.0, -1.0, 0.0)
    
    return [Triangle3D(p0, p1, p2), Triangle3D(p0, p2, p1)]

if __name__ == '__main__':
    triangles = generateTriangleList() 
    
    app = QApplication(['Triangle Demo'])
    window = View3D(None, triangles)
    window.show()
    
    app.exec_()
