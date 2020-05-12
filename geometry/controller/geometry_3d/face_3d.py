# -*- coding: utf-8 -*-
from geometry.controller.geometry_3d.point_3d import Point3d

class Face3d(object):

    def __init__(self, p0, p1, p2, p3):
        '''
        @param p0: instancia de Point3d
        @param p1: instancia de Point3d
        @param p2: instancia de Point3d
        @param p3: instancia de Point3d
        '''
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def Triangulate(self):
        '''
        Metodo que se encarga de triangular una cara en el espacio 3D.
        '''
        '''
        Caso en que la coordenada "y" es igual a cero. 
        '''
        if (self.y == 0):
            '''
            Caso en que la coordenada "x" es mayor que cero. 
            '''
            if (checkSign(self.x) == 2):
                return 0
                '''
                Caso en que la coordenada "x" es menor que cero. 
                '''
            elif (checkSign(self.x) == 1):
                return 180
            '''
            Caso en que la coordenada "x" es igual a cero. 
            '''
        elif (self.x == 0):
            '''
            Caso en que la coordenada "y" es mayor que cero. 
            '''
            if (checkSign(self.y) == 2):
                return 90
                '''
                Caso en que la coordenada "y" es menor que cero. 
                '''
            elif (checkSign(self.y) == 1):
                return 270
            '''
            Caso en que la coordenada "y" es mayor que cero y la coordenada "x" es mayor que cero. 
            '''
        elif (checkSign(self.y) == 2 and checkSign(self.x) == 2):
            return math.degrees(math.atan(self.y/self.x))
            '''
            Caso en que la coordenada "y" es mayor que cero y la coordenada "x" es menor que cero. 
            '''
        elif (checkSign(self.y) == 2 and checkSign(self.x) == 1):
            return 180-math.degrees(math.atan(self.y/-self.x))
            '''
            Caso en que la coordenada "y" es menor que cero y la coordenada "x" es menor que cero. 
            '''
        elif (checkSign(self.y) == 1 and checkSign(self.x) == 1):
            return 180+math.degrees(math.atan(-self.y/-self.x))
            '''
            Caso en que la coordenada "y" es menor que cero y la coordenada "x" es mayor que cero. 
            '''
        elif (checkSign(self.y) == 1 and checkSign(self.x) == 2):
            return 360-math.degrees(math.atan(-self.y/self.x))

    def checkposition(self,pointcomp,side):
        '''
	    Metodo para determinar si el punto 'pointcomp' pertenece al lado 'side'
	    del rectangulo que intersecta al poligono, indicado como parametro.
	    '''
        if (side == 1):
            if (self.x < pointcomp.x): 
                return 0
            elif (self.x > pointcomp.x): 
                return 1
            else:
                return 2
        if (side == 2):
            if (self.y > pointcomp.y): 
                return 0
            elif (self.y < pointcomp.y): 
                return 1
            else:
                return 2
        if (side == 3):
            if (self.x > pointcomp.x): 
                return 0
            elif (self.x < pointcomp.x): 
                return 1
            else:
                return 2
        if (side == 4):
            if (self.y < pointcomp.y): 
                return 0
            elif (self.y > pointcomp.y): 
                return 1
            else:
                return 2