'''
Created on Apr 23, 2015

@author: fapablaza
'''

import numpy 

def createVertexArrayFromTriangles(triangles):
    '''
    Convierte una lista de triangulos en un arreglo numpy de vertices
    '''
    vertices = numpy.zeros([3*len(triangles), 8])
    
    trianglePoints = numpy.array([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]], numpy.float32)
    
    i = 0
    
    for t in triangles:
        trianglePoints[0, ] = (t.p0.x, t.p0.y, t.p0.z)
        trianglePoints[1, ] = (t.p1.x, t.p1.y, t.p1.z)
        trianglePoints[2, ] = (t.p2.x, t.p2.y, t.p2.z)  
        
        v1 = trianglePoints[1, ] - trianglePoints[0, ]
        v2 = trianglePoints[2, ] - trianglePoints[0, ] 
        
        n = numpy.cross(v1, v2)
        n /= numpy.linalg.norm(n) 
        
        for p in [t.p0, t.p1, t.p2]:
            vertices[i, ] = (p.x, p.y, p.z, 
                             n[0], n[1], n[2], 
                             0.0, 0.0)
            i += 1
    
    return vertices
    
