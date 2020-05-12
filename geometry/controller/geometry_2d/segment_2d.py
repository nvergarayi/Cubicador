# -*- coding: utf-8 -*-
from geometry.controller.geometry_2d.point_2d import Point2D
from geometry.controller.common.common import checkIntervalOpen, checkIntervalClosed, gaussianElimination
import math

class Segment2D(object):

    def __init__(self, p0, p1, rowid=-1):
        '''
        @param p0: instancia de Point2D
        @param p1: instancia de Point2D
        '''
        self.p0 = p0
        self.p1 = p1
        self.rowid = rowid

    def getSlope(self):
        '''
        Funcion que obtiene la pendiente del segmento, en caso de no ser posible None.
        '''
        try:
            return (self.p1.y-self.p0.y)/(self.p1.x-self.p0.x)
        except ZeroDivisionError:
            return None

    def distance(self):
        '''
        Funcion que obtiene la distancia entre dos puntos del segmento pasado como parametro.
        '''
        return math.sqrt(((self.p1.y-self.p0.y)**2)+((self.p1.x-self.p0.x)**2))

    def obtainIntersection(self,constants,p_close,p_away):
        '''
        Funcion que determina la existencia de un punto de interseccion entre un segmento del borde de la cancha
        y uno de los extremos de la corona, y cual es en caso positivo.
        @param constants: Lista que contiene las dos constantes de la recta de interpolacion de la corona. 
                          Si no se pueden obtener por ser vertical, entrega None. 
        @param p_close  : El primero de los dos Point3d de la corona mas cercanos al segmento.  
        @param p_away   : El segundo de los dos Point3d de la corona mas cercanos al segmento.
        '''
        points = []
        m = self.getSlope()
        '''
        Caso en que existe la recta de interpolacion.
        '''
        if (constants[0] is not None):
            '''
            Caso en que el segmento del borde de la cancha es vertical.
            '''
            if (m is None):
                return self.evaluatePol(constants,self.p0.x,p_close,p_away,None)
                '''
                Caso en que el segmento del borde de la cancha no es vertical.
                '''
            else:
                res = gaussianElimination([[m,-1],[constants[0],-1]],[m*self.p0.x-self.p0.y,-constants[1]])
                return self.evaluatePol(constants,res[0],p_close,p_away,None)
            '''
            Caso en que la recta de interpolacion es vertical.
            '''
        else:
            '''
            Caso en que el segmento del borde de la cancha es vertical.
            '''
            if (m is not None):
                return self.evaluatePol(constants,constants[1].x,p_close,p_away,'x')
                '''
                Caso en que el segmento del borde de la cancha no es vertical.
                '''
            else:
                return -1,[0,0]

    def evaluatePol(self,constants,x,p_close,p_away,axis):
        '''
        Funcion que evalua la interpolacion lineal de la corona en la coordenada "x"
        dada, y chequear si el punto resultante esta en el segmento dado del borde 
        de la cancha o no. En caso positivo, devuelve 1 o 0 y una lista con las
        coordenadas en dos dimensiones del punto. En caso negativo, un -1 y una lista
        "[0,0]".
        @param constants: Lista que contiene las dos constantes de la recta de interpolacion de la corona. 
                          Si no se pueden obtener por ser vertical, entrega None.
        @param x        : Valor de la coordenada x en que se evalua el poligono lineal de interpolacion de la corona.
        @param p_close  : El primero de los dos Point3d de la corona mas cercanos al segmento.  
        @param p_away   : El segundo de los dos Point3d de la corona mas cercanos al segmento.
        @param axis     : Indica si se debe trabajar con la coordenada "x" o "y" del segmento. Si el valor es 'x',
                          se emplea el rango en "x". Si es None, se utiliza el rango en "y".
        '''

        '''
        Caso en que se evalua la recta de interpolacion para obtener la coordenada "y" del punto.
        '''
        if (constants[0] is not None):
            y = constants[0]*x+constants[1]
            '''
            Caso en que no existe la recta de interpolacion, por lo que se calcula la coordenada "y"
            del punto a partir de las coordenadas del segmento del borde de la cancha.
            '''
        else:
            m = self.getSlope()
            y = m*(x-self.p0.x) + self.p0.y

        '''
        Evaluar la distancia de los puntos mas cercanos al segmento, con respecto al punto candidato.
        '''
        dist_pclose = Segment2D(Point2D(p_close.x/1000,p_close.y/1000),Point2D(x,y)).distance()
        dist_paway = Segment2D(Point2D(p_away.x/1000,p_away.y/1000),Point2D(x,y)).distance()
        '''
        Caso en que p_close es el mas cercano al punto candidato. Esto significa que esta dentro o en el
        borde de la cancha.
        '''
        if (dist_pclose < dist_paway):
            '''
            Ver si el candidato coincide con uno de los puntos del segmento del borde de la cancha.
            '''
            if ((round(self.p1.x,8) == round(x,8)) and (round(self.p1.y,8) == round(y,8))):
                return 0,[x,y]
            '''
            En el caso de que la recta de interpolacion no sea vertical, verificar si el punto se halla
            dentro del rango "x" e "y" del segmento del borde de la cancha.
            '''
            if (constants[0] is not None):
                if (checkIntervalOpen(self.p0.x,self.p1.x,x) == True and checkIntervalOpen(self.p0.y,self.p1.y,y) == True):
                    return 1,[x,y]
                else:
                    return -1,[0,0]
                '''
                Caso en que la recta de interpolacion es vertical.
                '''
            else:
                '''
                Caso en que el segmento del borde de la cancha es vertical. Se verfica si la coordenada "x" del
                candidato esta en el rango "x" de dicho segmento.
                '''
                if (axis == 'x'):
                    if (checkIntervalOpen(self.p0.x,self.p1.x,x) == True):
                        return 1,[x,y]
                    else:
                        return -1,[0,0]
                    '''
                    Caso en que el segmento del borde de la cancha no es vertical. Se verfica si la coordenada
                    "y" del candidato esta en el rango "y" de dicho segmento.
                    '''
                else:
                    if (checkIntervalOpen(self.p0.y,self.p1.y,y) == True):
                        return 1,[x,y]
                    else:
                        return -1,[0,0]
            '''
            Caso en que p_away es el mas cercano al punto candidato. Esto significa que fuera de la cancha.
            '''
        else:
            return -1,[0,0]

    '''
    Metodo que calcula la interseccion de un segmento con un lado horizontal de
    un rectangulo.
    '''
    def solve1(self,segment):
        m = segment.getSlope()
        if (m is not None):
            '''    
            Caso en que el segmento deberia intersectar al lado de manera oblicua.
            '''
            if (checkIntervalClosed(segment.p0.y,segment.p1.y,self.p0.y) == False or m == 0):
                '''
		Caso en que el segmento no toca el lado.
		'''
                return False,Point2D(0,0)
            else:
                res = (self.p0.y-segment.p0.y)/m+segment.p0.x
                if (checkIntervalClosed(self.p0.x,self.p1.x,res) == True):
                    '''
                    Caso en que el segmento intersecta el lado y devuelve el punto como resultado.
                    '''
                    return True,Point2D(res,self.p0.y)
                else:
                    '''
                    Caso en que el segmento solo toca el lado (no devuelve punto).
                    '''
                    return False,Point2D(0,0)
        else:
            '''
	    Caso en que el segmento deberia intersectar al lado de manera perpendicular. 
            '''
            if (checkIntervalClosed(self.p0.x,self.p1.x,segment.p0.x) == True and \
              checkIntervalClosed(segment.p0.y,segment.p1.y,self.p0.y) == True):
                '''
		Caso en que el segmento intersecta el lado y devuelve un punto como resultado.
                '''
                return True,Point2D(segment.p0.x,self.p0.y)
            else:
                '''
		Caso en que el segmento no toca el lado.
                '''
                return False,Point2D(0,0)

    '''
    Metodo que calcula la interseccion de un segmento con un lado vertical de
    un rectangulo.
    '''
    def solve2(self,segment):
        m = segment.getSlope()
        if (m is not None):
            if (checkIntervalClosed(segment.p0.x,segment.p1.x,self.p0.x) == False):
                '''
                Caso en que el segmento no toca el lado.
                '''
                return False,Point2D(0,0)
            else:
                '''
		Caso en que el segmento deberia intersectar al lado de manera oblicua.
                '''
                res = m*(self.p0.x-segment.p0.x)+segment.p0.y
                if (checkIntervalClosed(self.p0.y,self.p1.y,res) == True):
                    '''
		    Caso en que el segmento intersecta el lado y devuelve el punto como resultado.
                    '''
                    return True,Point2D(self.p0.x,res)
                else:
                    '''
		    Caso en que el segmento no toca el lado.
                    '''
                    return False,Point2D(0,0)
        else:
            '''
	    Caso en que el segmento es paralelo al lado.
            '''
            return False,Point2D(0,0)

