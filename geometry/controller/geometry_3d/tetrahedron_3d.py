# -*- coding: utf-8 -*-
from geometry.controller.geometry_3d.point_3d import Point3d
from numpy.linalg import det
from numpy import sign

class Tetrahedron3d(object):

    def __init__(self, p0, p1, p2, rowid=-1):
        '''
        @param p0: instancia de Point3d
        @param p1: instancia de Point3d
        @param p2: instancia de Point3d
        '''
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.rowid = rowid
    
    @property
    def tetrahedronVolume(self):
        '''
        Funcion que obtiene el volumen del tetraedro formado entre el
        triangulo exterior y el centro del solido.
        '''
        volume = self.p0.x*(self.p1.z*self.p2.y-self.p1.y*self.p2.z)
        volume += self.p0.y*(self.p1.x*self.p2.z-self.p1.z*self.p2.x)
        volume += self.p0.z*(self.p1.y*self.p2.x-self.p1.x*self.p2.y)
        return volume/6

    def isPointInTetrahedron(self,centroid,point):
        '''
        Funcion que determina si un punto dado se encuentra dentro de
        un tetrahedro o no.
        '''

        D0 = [[centroid.x,centroid.y,centroid.z,1],[self.p0.x,self.p0.y,self.p0.z,1],\
             [self.p1.x,self.p1.y,self.p1.z,1],[self.p2.x,self.p2.y,self.p2.z,1]]

        D1 = [[point.x,point.y,point.z,1],[self.p0.x,self.p0.y,self.p0.z,1],\
             [self.p1.x,self.p1.y,self.p1.z,1],[self.p2.x,self.p2.y,self.p2.z,1]]

        D2 = [[centroid.x,centroid.y,centroid.z,1],[point.x,point.y,point.z,1],\
             [self.p1.x,self.p1.y,self.p1.z,1],[self.p2.x,self.p2.y,self.p2.z,1]]

        D3 = [[centroid.x,centroid.y,centroid.z,1],[self.p0.x,self.p0.y,self.p0.z,1],\
             [point.x,point.y,point.z,1],[self.p2.x,self.p2.y,self.p2.z,1]]

        D4 = [[centroid.x,centroid.y,centroid.z,1],[self.p0.x,self.p0.y,self.p0.z,1],\
             [self.p1.x,self.p1.y,self.p1.z,1],[point.x,point.y,point.z,1]]
        
        '''
        Evaluar si todos los determinantes tienen el mismo signo. Si es asi, el punto esta
        dentro del tetrahedro, en caso contario, esta afuera.
        '''
        determinants = [det(D0),det(D1),det(D2),det(D3),det(D4)]
        sign_det = [0,0,0,0,0]
        for num_det in range(0,5):
            if (determinants[num_det] > 1):
                sign_det[num_det] = 1    
            if (determinants[num_det] < -1):
                sign_det[num_det] = -1
       
        positive_sign = 1 in sign_det
        negative_sign = -1 in sign_det
        
        if (positive_sign == True) and (negative_sign == True):
            return False
        else:
            return True
