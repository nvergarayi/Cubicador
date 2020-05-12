# -*- coding: utf-8 -*-
from geometry.controller.geometry_2d.segment_2d import Segment2D
from geometry.controller.geometry_3d.segment_3d import Segment3d
from geometry.controller.geometry_2d.point_2d import Point2D
from geometry.controller.geometry_3d.point_3d import Point3d
import math

class Triangle3d(object):

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

    def distanceToPlane(self,p0,p1):

        AB = [self.p1.x-self.p0.x,self.p1.y-self.p0.y,self.p1.z-self.p0.z]
        AC = [self.p2.x-self.p0.x,self.p2.y-self.p0.y,self.p2.z-self.p0.z]

        #print ('AB = ',AB,' AC = ',AC)

        a = AB[1]*AC[2]-AB[2]*AC[1]
        b = AB[0]*AC[2]-AB[2]*AC[0]
        c = AB[0]*AC[1]-AB[1]*AC[0]

        #d = -ax - by - cz
        d = -a*self.p2.x - b*self.p2.y - c*self.p2.z
                                    
        d1 = abs(a*p0.x+b*p0.y+c*p0.z+d)/math.sqrt(a**2+b**2+c**2)
        d2 = abs(a*p1.x+b*p1.y+c*p1.z+d)/math.sqrt(a**2+b**2+c**2)
        #print ('abcd = ',a,b,c,d,p0.z,p1.z,c*p0.z,c*p1.z)
        #print ('d1 = ',a*p0.x+b*p0.y+c*p0.z+d,abs(a*p0.x+b*p0.y+c*p0.z+d))
        #print ('d2 = ',abs(a*p1.x+b*p1.y+c*p1.z+d),a*p1.x+b*p1.y+c*p1.z+d)
        #print ('d1 = ',d1)
        #print ('d2 = ',d2)

        if (d1 != 0 and d2 != 0):
            d1_new = d1/(d1+d2); d2_new = d2/(d1+d2)
            return Point3d(p0.x + (p1.x-p0.x)*d1_new,p0.y + (p1.y-p0.y)*d1_new,p0.z + (p1.z-p0.z)*d1_new)
        else:
            return False

        #  Ecuacion del plano: ax + by + cz + d = 0
        #  AB = (b-a)
        #  AC = (c-a)                                                                                                           
                         
        #|      x         y         z       |
        #|    AB(0)      AB(1)     AB(2)    |
        #|    AC(0)      AC(1)     AC(2)    |

        #new_p.append(Point3d(p0.x + (p1.x-p0.x)*d1_new,p0.y + (p1.y-p0.y)*d1_new,p0.z + (p1.z-p0.z)*d1_new)      
        #print ('triangulo 3 = ',t)
        #new_p.append(Point3d((p1.x+p0.x)/2,(p1.y+p0.y)/2,(p1.z+p0.z)/2))

    '''
    Obtener los segmentos del triangulo.
    '''
    def get_segments(self):
        return [Segment3d(self.p0,self.p1),Segment3d(self.p1,self.p2),Segment3d(self.p2,self.p0)]

    def getReducedCoordinates(self,plane):
        '''
        Funcion que entrega la abscisa y la ordenada de un triangulo segun el plano de referencia.
        Los valores de las coordenadas estan divididos por 1000.
        @param plane: Indica el plano de referencia empleado para obtener la abscisa y ordenada del
                      triangulo. 
        '''

        if (plane == 'xy'):
            reduced_coords = [[self.p0.x/1000,self.p1.x/1000,self.p2.x/1000],[self.p0.y/1000,self.p1.y/1000,self.p2.y/1000]]
        if (plane == 'yz'):
            reduced_coords = [[self.p0.y/1000,self.p1.y/1000,self.p2.y/1000],[self.p0.z/1000,self.p1.z/1000,self.p2.z/1000]]
        if (plane == 'zx'):
            reduced_coords = [[self.p0.z/1000,self.p1.z/1000,self.p2.z/1000],[self.p0.x/1000,self.p1.x/1000,self.p2.x/1000]]

        return reduced_coords

    def getTriangleIntersections(self,consts_curve1,reduced_coords,plane):
        '''
        Funcion que obtiene los puntos de interseccion de un triangulo con respecto a una recta, indicando plano de referencia.
        @param consts_curve1 : Lista de constantes de la recta con la cual intersecta el triangulo.
        @param reduced_coords: Abscisas y ordenadas reducidas para cada punto del triangulo.
        @param plane         : Indica el plano de referencia para realizar los calculos.
        '''
        from geometry.controller.geometry_3d.polygon_3d import Polygon3d
        intersect_points = []
        pts = [self.p0,self.p1,self.p2]

        '''
        Recorrer para cada punto del triangulo.
        '''
        for i in range(3):
            p1 = Point2D(reduced_coords[0][i-1], reduced_coords[1][i-1])
            p2 = Point2D(reduced_coords[0][i], reduced_coords[1][i])
            '''
            Generar un segmento del triangulo y verificar si existe interseccion con la curva.
            '''
            state,p_int = Segment2D(p1,p2).obtainIntersection(consts_curve1,self.p0,Point3d(10*self.p0.x,10*self.p0.y,10*self.p0.z))
            if (state != -1):
                if (plane == 'xy'):
                    consts_curve2 = Polygon3d([pts[i-1],pts[i]]).obtainConsts(3)
                    p_int.append(consts_curve2[0]*p_int[0]+consts_curve2[1])
                    p_int = Point3d(p_int[0]*1000,p_int[1]*1000,p_int[2]*1000)
                if (plane == 'yz'):
                    consts_curve2 = Polygon3d([Point3d(pts[i-1].y,pts[i-1].z,pts[i-1].x), \
                     Point3d(pts[i].y,pts[i].z,pts[i].x)]).obtainConsts(3)
                    p_int.append(consts_curve2[0]*p_int[0]+consts_curve2[1])
                    p_int = Point3d(p_int[2]*1000,p_int[0]*1000,p_int[1]*1000)
                if (plane == 'zx'):
                    consts_curve2 = Polygon3d([Point3d(pts[i-1].z,pts[i-1].x,pts[i-1].y), \
                     Point3d(pts[i].z,pts[i].x,pts[i].y)]).obtainConsts(3)
                    p_int.append(consts_curve2[0]*p_int[0]+consts_curve2[1])
                    p_int = Point3d(p_int[1]*1000,p_int[2]*1000,p_int[0]*1000)
                intersect_points.append([i,state,p_int])

        return intersect_points
