# -*- coding: utf-8 -*-
from geometry.controller.common.common import checkIntervalOpen
from geometry.controller.geometry_2d.segment_2d import Segment2D
from geometry.controller.geometry_2d.point_2d import Point2D
from geometry.controller.geometry_3d.point_3d import Point3d

class Rectangle2D(object):
    
    def __init__(self, centerx=None, centery=None, centerz=None, lenx=None, leny=None, lenz=None,\
        data=None, rect=None, listpoints=None):
        '''
        Caso en que se genera un objeto rectangulo a partir del archivo CSV.
        '''
        if (rect is None and listpoints is None):
            self.centerx = centerx
            self.centery = centery
            self.centerz = centerz
            self.lenx = lenx
            self.leny = leny
            self.lenz = lenz
            self.data = data

            '''
            Caso en que se genera un objeto rectangulo con los puntos de este.
            '''
        elif (rect is not None and listpoints is None):
            self.p0 = Point2D(rect.centerx-rect.lenx/2, rect.centery+rect.leny/2)
            self.p1 = Point2D(rect.centerx+rect.lenx/2, rect.centery+rect.leny/2)
            self.p2 = Point2D(rect.centerx+rect.lenx/2, rect.centery-rect.leny/2)
            self.p3 = Point2D(rect.centerx-rect.lenx/2, rect.centery-rect.leny/2)

            '''
		    Caso en que se genera un objeto rectangulo con los lados de este.
		 '''
        elif (rect is None and listpoints is not None):
            self.s0 = Segment2D(listpoints.p0,listpoints.p1)
            self.s1 = Segment2D(listpoints.p1,listpoints.p2)
            self.s2 = Segment2D(listpoints.p2,listpoints.p3)
            self.s3 = Segment2D(listpoints.p3,listpoints.p0)

    '''
    Metodo que devuelve una lista con los puntos del rectangulo.
    '''
    def getPoints(self):
        return [self.p0,self.p1,self.p2,self.p3]

    '''
    Metodo para determinar si el punto se encuentra dentro o fuera del rectangulo.
    Devuelve 0 si esta dentro, 2 si esta fuera y 1 si esta en el borde.
    '''
    def checkinsert(self,point):
        if (self.checkxrange(point) == True and self.checkyrange(point) == True):
            return 0
        elif (self.checkxrangeb(point) == True or self.checkyrangeb(point) == True):
            return 2
        else:
            return 1

    '''
    Metodo para determinar si el punto se encuentra dentro de la coordenada x
    del rectangulo (intervalo abierto).
    '''
    def checkxrange(self,point):
        if (point.x > self.p0.x and point.x < self.p1.x):
            return True
        else:
            return False

    '''
    Metodo para determinar si el punto se encuentra fuera de la coordenada x
    del rectangulo.
    '''
    def checkxrangeb(self,point):
        if (point.x < self.p0.x or point.x > self.p1.x):
            return True
        else:
            return False

    '''
    Metodo para determinar si el punto se encuentra dentro de la coordenada x
    del rectangulo (intervalo cerrado).
    '''    
    def checkxrangec(self,point):
        if (point.x >= self.p0.x and point.x <= self.p1.x):
            return True
        else:
            return False

    '''
    Metodo para determinar si el punto se encuentra dentro de la coordenada y
    del rectangulo (intervalo abierto).
    '''
    def checkyrange(self,point):
        if (point.y > self.p2.y and point.y < self.p1.y):
            return True
        else:
            return False

    '''
    Metodo para determinar si el punto se encuentra fuera de la coordenada y
    del rectangulo (intervalo abierto).
    '''
    def checkyrangeb(self,point):
        if (point.y < self.p2.y or point.y > self.p1.y):
            return True
        else:
            return False

    '''
    Metodo para determinar si el punto se encuentra dentro de la coordenada y
    del rectangulo (intervalo cerrado).
    '''
    def checkyrangec(self,point):
        if (point.y >= self.p2.y and point.y <= self.p1.y):
            return True
        else:
            return False

    '''
    Metodo para determinar si el punto se encuentra dentro del lado superior
    del rectangulo.
    '''
    def checkborder1(self,point):
        if (point.y == self.p0.y and self.checkxrangec(point) == True):
            return True
        else:
            return False
	
    '''
    Metodo para determinar si el punto se encuentra dentro del lado derecho
    del rectangulo.
    '''
    def checkborder2(self,point):
        if (point.x == self.p1.x and self.checkyrange(point) == True):
            return True
        else:
            return False

    '''
    Metodo para determinar si el punto se encuentra dentro el lado inferior
    del rectangulo.
    '''
    def checkborder3(self,point):
        if (point.y == self.p2.y and self.checkxrangec(point) == True):
            return True
        else:
            return False

    '''
    Metodo para determinar si el punto se encuentra dentro el lado izquierdo
    del rectangulo.
    '''
    def checkborder4(self,point):
        if (point.x == self.p0.x and self.checkyrange(point) == True):
            return True
        else:
            return False

    '''
    Metodo que devuelve en que lado del rectangulo se encuentra el punto.
    Devuelve 0 si no esta en ninguno de los lados.
    '''
    def checkborder(self,point):
        if (self.checkborder1(point) == True):
            return 1
        elif (self.checkborder2(point) == True):
            return 2
        elif (self.checkborder3(point) == True):
            return 3
        elif (self.checkborder4(point) == True):
            return 4
        else:
            return 0

    '''
    Metodo que devuelve los puntos de interseccion del lado del polígono con el
    rectangulo se encuentra el punto.
    '''
    def checkintersections(self,segment2):
        intersections = []
        segment1 = Rectangle2D(None,None,None,None,None,None,None,None,self)
        flag,x = segment1.s0.solve1(segment2)
        if (flag == True):
            intersections.append(x)
            intersections.append(1)    
        flag,x = segment1.s1.solve2(segment2)
        if (flag == True):
            intersections.append(x)
            intersections.append(2)
        flag,x = segment1.s2.solve1(segment2)
        if (flag == True):
            intersections.append(x)
            intersections.append(3)
        flag,x = segment1.s3.solve2(segment2)
        if (flag == True):
            intersections.append(x)
            intersections.append(4)
        return intersections

    '''
    Metodo que agrega al rectangulo el o los puntos de interseccion 
    con el poligono.
    '''
    def genborder(self,sections):
        pointsborder = self.getPoints()
        for p in sections:
            for i in range(len(pointsborder)):
                if (self.inborder(pointsborder[i-1],pointsborder[i],p[0]) == 0):
                    pointsborder.insert(i,p[0])
                    break
            for j in range(len(pointsborder)):
                if (self.inborder(pointsborder[j-1],pointsborder[j],p[len(p)-1]) == 0):
                    pointsborder.insert(j,p[len(p)-1])
                    break
        return pointsborder

    '''
    Metodo que determina si se debe agregar el punto en cuestion al poligono de
    interseccion, en la ubicacion definida por el metodo "genborder".
    '''
    def inborder(self,point1,point2,pointn):
        ind1 = self.checkborder(point1)
        ind2 = self.checkborder(point2)
        ind3 = self.checkborder(pointn)
        if (ind1 == ind2 and ind1 == ind3): 
            if (pointn.checkposition(point1,ind1) == 1 and pointn.checkposition(point2,ind2) == 0):
                return 0
            else:
                return 1
        if (ind1 == 1 and ind2 == 3 and ind3 == 2):
            return 0
        if (ind1 == 3 and ind2 == 1 and ind3 == 4):
            return 0
        if (ind1 == 1 and ind2 == 2 and ind3 == 2):
            if (pointn.checkposition(point2,ind2) == 0):
                return 0
            else:
                return 1
        if (ind1 == 2 and ind2 == 3 and ind3 == 2):
            if (pointn.checkposition(point1,ind1) == 1):
                return 0
            else:
                return 1
        if (ind1 == 3 and ind2 == 4 and ind3 == 4):
            if (pointn.checkposition(point2,ind2) == 0):
                return 0
            else:
                return 1
        if (ind1 == 4 and ind2 == 1 and ind3 == 4):
            if (pointn.checkposition(point1,ind1) == 1):
                return 0
            else:
                return 1
        else:
            return 1

    '''
    Metodo que determina si el segmento cruza el area del rectangulo o no.
    '''
    def crossrectangle(self,segment):
        if (self.crosssegmentsx(segment) == True and self.crosssegmentsy(segment) == True):
            return True
        else:
            return False

    '''
    Metodo que determina si el segmento cruza la coordenada x del area del rectangulo o no.
    '''
    def crosssegmentsx(self,segment):
        if (checkIntervalOpen(segment.p0.x,segment.p1.x,self.p0.x) == True or \
          checkIntervalOpen(segment.p0.x,segment.p1.x,self.p1.x) == True or \
          checkIntervalOpen(self.p0.x,self.p1.x,segment.p0.x) == True):
            return True
        else:
            return False

    '''
    Metodo que determina si el segmento cruza la coordenada y del area del rectangulo o no.
    '''
    def crosssegmentsy(self,segment):
        if (checkIntervalOpen(segment.p0.y,segment.p1.y,self.p1.y) == True or \
          checkIntervalOpen(segment.p0.y,segment.p1.y,self.p2.y) == True or \
          checkIntervalOpen(self.p1.y,self.p2.y,segment.p0.y) == True):
            return True
        else:
            return False

    '''
    Metodo que extrae los rectangulos del archivo CSV y los convierte en objetos
    Rectangle2D.
    '''
    @staticmethod
    def getRectangles2DFromCSV(path, centerx, centery, centerz, lenx, leny, lenz, data=None):
        infile = open(path, 'r')
        headers = infile.readline().replace('\n', '').replace('\r', '').replace(' ', '').split(',')
        headers = dict([(headers[i], i) for i in range(len(headers))])
        
        result = []
        for line in infile:
            line = line.replace('\n', '').replace('\r', '').replace(' ', '').split(',')
            cx = float(line[headers[centerx]]); cy = float(line[headers[centery]]); cz = float(line[headers[centerz]])
            lx = float(line[headers[lenx]]); ly = float(line[headers[leny]]); lz = float(line[headers[lenz]])
            result.append(Rectangle2D(cx, cy, cz, lx, ly, lz, None if not(data) else line[headers[data]],None,None))
        return result

