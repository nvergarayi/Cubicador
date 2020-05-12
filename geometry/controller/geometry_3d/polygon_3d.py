# -*- coding: utf-8 -*-
from geometry.controller.common.common import checkIntervalSemiopen, checkIntervalSemiopen2, checkIntervalClosed, checkIntervalOpen, gaussianElimination
from geometry.controller.geometry_2d.rectangle_2d import Rectangle2D
from geometry.controller.geometry_3d.triangle_3d import Triangle3d
from geometry.controller.geometry_2d.segment_2d import Segment2D
from geometry.controller.geometry_3d.segment_3d import Segment3d
from geometry.controller.geometry_2d.point_2d import Point2D
from geometry.controller.geometry_3d.point_3d import Point3d
from geometry.controller.geometry_3d.curve_3d import Curve3d
#from geometry.view3d.view3d.View3D import View3D
#from PyQt4.Qt import QApplication
import matplotlib.pyplot as plt
import math
from geometry.controller.geometry_3d.set_of_point_3d import SetOfPoint3d

class Polygon3d(object):
   
    def __init__(self, points, name='', rowid=-1):
        self.points = points
        self.rowid = rowid
        self.name = name

    @staticmethod
    def getPolygons3DFromDXF(path):
        '''
	Funcion que lee el archivo DXF y devuelve un conjunto de puntos que integran un
        poligono.
	'''
        infile = open(path, 'r')
        lines = [line.replace('\n', '').replace('\r', '').replace(' ', '') for line in infile]
       
        i = 0
        flag = False
        polygon = Polygon3d([])
        while i < len(lines):
            if lines[i] == 'VERTEX':
                flag = True
            if flag is True:
                if lines[i] == '10' and lines[i+2] == '20' and lines[i+4] == '30':
                    x, y, z = float(lines[i+1]), float(lines[i+3]), float(lines[i+5])
                    polygon.points.append(Point3d(x, y, z))
                    flag = False
                    i += 5 
            i += 1
   
        return polygon
 
    def __str__(self, ):
        return str([(p.x, p.y, p.z) for p in self.points])
    
    def getIntersectionSolid(self,left_curve,right_curve,left_crown,right_crown):
        '''
        Funcion para generar el solido de interseccion.
        @param left_curve : Curva que intersecta a la cancha en la parte posterior.  
        @param right_curve: Curva que intersecta a la cancha en la parte anterior. 
        @param left_crown : Corona posterior.    
        @param right_crown: Corona anterior.  
        '''

        '''
        Ordenar las curvas. Dejar las curvas y las coronas orientadas de acuerdo al movimento de las manecillas del
        reloj. La cancha contra las manecillas del reloj.
        '''
        self.checkOrientation([left_curve,right_curve,left_crown,right_crown])
        #chart ([self.points,left_curve.points,right_curve.points,left_crown.points,right_crown.points],['b','r','g','k','y'])
        '''
        Obtener la suma de las coordenadas en el eje z, tanto para las curvas al nivel de la cancha, como para
        el nivel superior. 
        '''
        sum_curves1 = sum([p.z for p in left_curve.points])           
        sum_curves2 = sum([p.z for p in right_curve.points]) 
        sum_crowns1 = sum([p.z for p in left_crown.points])           
        sum_crowns2 = sum([p.z for p in right_crown.points])
        
        '''
        Calcular el rango en z que se debe elevar la cancha para obtener el poligono superior
        del solido.
        '''
        diff = ((sum_crowns1/len(left_crown.points))+(sum_crowns2/len(right_crown.points)))/2-\
         ((sum_curves1/len(left_curve.points))+(sum_curves2/len(right_curve.points)))/2

        '''
        Generar el poligono superior.
        '''
        polygon_sup = Polygon3d([])
        for p in self.points:
            polygon_sup.points.append(Point3d(p.x,p.y,p.z+diff))
        
        '''
        Generar el poligono de interseccion de la cancha y obtener sus esquinas.
        '''
        polygon_intermediate,polygon3,p1,p2 = self.subPolygons(right_curve,None)
        polygon1,polygon2,p1,p2,p3,p4 = polygon_intermediate.subPolygons(left_curve,[p1,p2])
        intersect_points_polygon2 = [p1,p2,p3,p4]

        '''
        Generar el poligono de interseccion superior y obtener sus esquinas.
        '''
        polygon_intermediate,polygon6,p5,p6 = polygon_sup.subPolygons(right_crown,None)
        polygon4,polygon5,p5,p6,p7,p8 = polygon_intermediate.subPolygons(left_crown,[p5,p6])
        intersect_points_polygon5 = [p5,p6,p7,p8]

        '''
        Triangular el solido.
        '''
        intersection_solid = \
         polygon2.triangulateSolid(polygon5,intersect_points_polygon2,intersect_points_polygon5)
        #chart([polygon2.points,polygon5.points],['b','r'])

        '''
        Generar la curva de interseccion para el solido.
        '''
        mn_x = min([min(t.p0.x,t.p1.x,t.p2.x) for t in intersection_solid.triangles])
        mn_y = min([min(t.p0.y,t.p1.y,t.p2.y) for t in intersection_solid.triangles])
        mn_z = min([min(t.p0.z,t.p1.z,t.p2.z) for t in intersection_solid.triangles])

        mx_x = max([max(t.p0.x,t.p1.x,t.p2.x) for t in intersection_solid.triangles])
        mx_y = max([max(t.p0.y,t.p1.y,t.p2.y) for t in intersection_solid.triangles])
        mx_z = max([max(t.p0.z,t.p1.z,t.p2.z) for t in intersection_solid.triangles])

        curve2 = Curve3d([Point3d(x, y, z) for x, y, z in [(0.0, (mn_y+mx_y)/2, mn_z), (0.0, (mn_y+mx_y)/2, mx_z)]])
        curve3 = Curve3d([Point3d(x, y, z) for x, y, z in [((mn_x+mx_x)/2, mn_y, 0.0), ((mn_x+mx_x)/2, mx_y, 0.0)]])

        '''
        Obtener los subsolidos, el poligono de interseccion y calcular el volumen y las alturas tanto
        del solido original como de los subsolidos.
        '''
        subsolids = intersection_solid.subSolids(curve3,'xy')
        intersection_pols = intersection_solid.obtainPolygons('xy',(mn_x+mx_x)/2)

        #app = QApplication(['Intersection Solid'])
        #window = View3D(None, intersection_solid.triangles)
        #window.show()
        #app.exec_()
        
        #print intersection_solid.checkPointInSolid(Point3d((mn_x+mx_x)/2,(mn_y+mx_y)/2,(mn_z+mx_z)/2))
        volume_solid = intersection_solid.volume
        heights = intersection_solid.obtainHeightsSolid()
        print ('solid_heights =',heights)
        for s in subsolids:
             chart3(s.triangles)
             print ('position_sub_solid =',s.getPositionSolid(curve3,'xy'))
             print ('sub_solid_volume =',s.volume)
             print ('sub_solid_heights =',s.obtainHeightsSolid())
        
        return intersection_solid,volume_solid,subsolids,heights

    def getIntersectionRectangles(self,rectangles):
        #xs = []; ys = []
        #for point in polygon:
        #  xs.append(point.x); ys.append(point.y)
        #for i in range(len(xs)-1):
        #  plt.plot(xs[i:i+2], ys[i:i+2], 'b')
        #plt.plot([xs[len(xs)-1], xs[0]], [ys[len(xs)-1], ys[0]], 'b')

        i = 0
        output = []; prov = []; cpoints = []; cpoints2 = []; newpolygons = []

        '''
        Evaluar para cada rectangulo.
        '''
        for rect in rectangles:
            countintersect = 0
            borderrect = Rectangle2D(None,None,None,None,None,None,None,rect,None)
            #xs = []; ys = []
            #for point in borderrect.getPoints():
            #  xs.append(point.x); ys.append(point.y)
            #for d in range(len(xs)-1):
            #  plt.plot(xs[d:d+2], ys[d:d+2], 'g')
            #plt.plot([xs[len(xs)-1], xs[0]], [ys[len(xs)-1], ys[0]], 'g')

            '''
            Evaluar para cada segmento del poligono.
            '''
            for j in range(len(self.points)):
                '''
  	            Verificar si el segmento intersecta el rectangulo. Si es asi,
                se evaluan los cuatro casos posibles.
  	            '''
                if (borderrect.crossrectangle(Segment3d(self.points[j-1],self.points[j])) == False):
                    continue

                flaginsert1 = borderrect.checkinsert(self.points[j-1])
                flaginsert2 = borderrect.checkinsert(self.points[j])
                if (flaginsert1 == 0 and flaginsert2 == 0):
                    '''
  	                Caso en que el segmento esta dentro del rectangulo.
  	                '''
                    prov.append(self.points[j-1])
                    prov.append(self.points[j])
                    continue
                elif (flaginsert1 == 0 and flaginsert2 != 0):
                    '''
  	                Caso en que el segmento sale del rectangulo.
  	                '''
                    prov.append(self.points[j-1])
                    if (flaginsert2 == 1):
                        '''
		                Caso en que el punto j del segmento se halla en el borde del rectangulo.
  	                    '''
                        prov.append(self.points[j])
                    else:
                        '''
		                Caso en que el punto j del segmento se halla fuera del rectangulo.
  	                    '''
                        p = borderrect.checkintersections(Segment2D(Point2D(self.points[j-1].x,self.points[j-1].y),\
                         Point2D(self.points[j].x,self.points[j].y)))
                        prov.append(p[0])
                    continue
                elif (flaginsert1 != 0 and flaginsert2 == 0):
                    '''
  	                Caso en que el segmento entra al rectangulo.
  	                '''
                    if (flaginsert1 == 1):
                        '''
		                Caso en que el punto j-1 del segmento se halla en el borde del rectangulo.
  	                    '''
                        prov.append(self.points[j-1])
                    else:
                        '''
		                Caso en que el punto j-1 del segmento se halla fuera del rectangulo.
  	                    '''
                        p = borderrect.checkintersections(Segment2D(Point2D(self.points[j-1].x,self.points[j-1].y),\
                         Point2D(self.points[j].x,self.points[j].y)))
                        prov.append(p[0])
                    prov.append(self.points[j])
                    continue
                else:
                    '''
  	                Caso en que el segmento cruza el rectangulo.
  	                '''
                    side1 = borderrect.checkborder(self.points[j-1])
                    side2 = borderrect.checkborder(self.points[j])
                    if (flaginsert1 == 1 and flaginsert2 == 1 and side1 != side2):
                        '''
		                Caso en que ambos puntos del segmento se hallan en los bordes del rectangulo.
  	                    '''
                        prov.append(self.points[j-1])
                        prov.append(self.points[j])
                        continue
                    elif (flaginsert1 == 1 and flaginsert2 == 2):
                        '''
		                Caso en que el punto j-1 del segmento se halla en un borde del rectangulo,
                        y el punto j se encuentra fuera del rectangulo. El segmento cruza uno de los lados.
  	                    '''
                        p = borderrect.checkintersections(Segment2D(Point2D(self.points[j-1].x,self.points[j-1].y),\
                         Point2D(self.points[j].x,self.points[j].y)))
                        if (len(p) > 2):
                            prov.append(self.points[j-1])
                            if (p[1] == side1):
                                prov.append(p[2])
                            else:
                                prov.append(p[0])
                            continue
                    elif (flaginsert1 == 2 and flaginsert2 == 1):
                        '''
		                Caso en que el punto j del segmento se halla en un borde del rectangulo,
                        y el punto j-1 se encuentra fuera del rectangulo. El segmento cruza uno de los lados.
  	                    '''
                        p = borderrect.checkintersections(Segment2D(Point2D(self.points[j-1].x,self.points[j-1].y),\
                         Point2D(self.points[j].x,self.points[j].y)))
                        if (len(p) > 2):
                            if (p[1] == side2):
                                prov.append(p[2])
                            else:
                                prov.append(p[0])
                            prov.append(self.points[j])
                            continue
                    else:
                        '''
		                Caso en que ambos puntos del segmento se ubican fuera del rectangulo. El segmento
                        cruza dos lados del rectangulo.
  	                    '''
                        p = borderrect.checkintersections(Segment2D(Point2D(self.points[j-1].x,self.points[j-1].y),\
                         Point2D(self.points[j].x,self.points[j].y)))
                        if (len(p) == 4):
                            p1 = p[0]
                            p2 = p[2]
                            d1 = Segment2D(Point2D(self.points[j-1].x,self.points[j-1].y),p1).distance()
                            d2 = Segment2D(Point2D(self.points[j-1].x,self.points[j-1].y),p2).distance()
                            if(d1 < d2):
                                prov.append(p[0])
                                prov.append(p[2])
                            else:
                                prov.append(p[2])
                                prov.append(p[0])
                            continue

            '''
            Generar las secciones del poligono de interseccion que estan dentro
            del rectangulo.
            '''
            k = 0
            l = 0
            sections = []
            while (l < len(prov)):
                sections.append([prov[l]])
                l += 1
                if (l < len(prov) - 1) : 
                    while (prov[l].x == prov[l+1].x and prov[l].y == prov[l+1].y):
                        sections[k].append(prov[l])
                        l += 2
                        if (l > len(prov) - 2) : break 
                sections[k].append(prov[l])
                l += 1
                k += 1

            prov = []

            '''
	        Se agregan al rectangulo el o los puntos de interseccion con el 
            poligono.
	        '''
            borderrect2 = borderrect.genborder(sections)
            countnewpolygons = 0

            '''
            Cerrar el poligono de interseccion incluyendo las partes del rectangulo
            que queden entre los bordes de los segmentos internos.
  	        '''
            while (len(sections) > 0):
                provborder = sections.pop(0)
                j = -1
                flag = False
                while True:
                    j += 1
                    if (j == len(borderrect2)): 
                        j = 0
                    if (provborder[len(provborder)-1].x == borderrect2[j].x and \
                     provborder[len(provborder)-1].y == borderrect2[j].y and flag == False):
                        flag = True
                    if (len(sections) > 0):
                        if (sections[0][0].x == borderrect2[j].x and sections[0][0].y == borderrect2[j].y and flag == True):
                            provborder.extend(sections.pop(0))
                            flag = False
                            continue
                    if (provborder[0].x == borderrect2[j].x and provborder[0].y == borderrect2[j].y and flag == True):
                        countnewpolygons += 1
                        newpolygons.append(provborder)
                        provborder = []
                        break
                    if (provborder[0].x == provborder[len(provborder)-1].x and \
                     provborder[0].y == provborder[len(provborder)-1].y and flag == False):
                        del provborder[len(provborder)-1]
                        countnewpolygons += 1
                        newpolygons.append(provborder)
                        provborder = []
                        break
                    if (flag == True):
                        provborder.append(borderrect2[j])
                        continue

            '''
            Determinar el rectangulo completo como poligono de interseccion en el caso
            de que quede dentro de los bordes del poligono.
  	        '''
            if (countnewpolygons == 0):
                if (self.checkPointInPolygon(Point2D(rect.centerx,rect.centery,0),'xy') == True):
                    newpolygons.append(Rectangle2D(None,None,None,None,None,None,None,rect,None).getPoints())

        #chart(newpolygons,['r']*len(newpolygons))
        return newpolygons

    def get_intersection_triangles(self):
        '''
        Funcion para triangular los poligonos de interseccion obtenidos a partir
        de los triangulos.
        '''
        xy_max = [0,0]; yz_max = [0,0]
        for p in self.points:
            if (p.x > xy_max[0]):
                xy_max[0] = p.x
                xy_max[1] = p.y
            if (p.y > yz_max[0]):
                yz_max[0] = p.y
                yz_max[1] = p.z
        xy_min = [xy_max[0],xy_max[1]]; yz_min = [yz_max[0],yz_max[1]] 
        for p in self.points:
            if (p.x < xy_min[0]):
                xy_min[0] = p.x
                xy_min[1] = p.y
            if (p.y < yz_min[0]):
                yz_min[0] = p.y
                yz_min[1] = p.z

        m = Segment2D(Point2D(xy_min[0],xy_min[1]),Point2D(xy_max[0],xy_max[1])).getSlope()
        xy_isline = True
        if (m is None):
            for p in self.points:
                if (round(p.x,8) != round(xy_min[0],8)):
                    xy_isline = False
        else:
            b = -m*xy_min[0] + xy_min[1] 
            for p in self.points:
                if (round(p.y,8) != round(m*p.x+b,8)):
                    xy_isline = False

        m = Segment2D(Point2D(yz_min[0],yz_min[1]),Point2D(yz_max[0],yz_max[1])).getSlope()
        yz_isline = True
        if (m is None):
            for p in self.points:
                if (round(p.x,8) != round(yz_min[0],8)):
                    yz_isline = False
        else:
            b = -m*yz_min[0] + yz_min[1]
            for p in self.points:
                if (round(p.y,8) != round(m*p.x+b,8)):
                    yz_isline = False

        if (xy_isline == False):
            #print ('caso 1')
            return self.get_intersection_triangles_with_case(1)
        elif (yz_isline == False):
            #print ('caso 2')
            return self.get_intersection_triangles_with_case(2)
        else:
            #print ('caso 3')
            return self.get_intersection_triangles_with_case(3)

    def get_intersection_triangles_with_case(self,case):
        '''
        Funcion para triangular los poligonos de interseccion obtenidos a partir
        de los triangulos, indicando el caso, cuando ya se conoce el plano de
        referencia.
        '''

        triangulate_polygon = []

        if (case == 1):
            '''
            Caso en que el plano de referencia es 'xy'.
            '''
            list_with_types,list_with_types_red = self.defTypes([])
            newpolygons = list_with_types.processPolygon()
            for new_pol in newpolygons:
                triangulate_polygon.extend(self.triangulate(new_pol,case))
        elif (case == 2):
            '''
            Caso en que el plano de referencia es 'yz'.
            '''
            transformed_polygon = Polygon3d([])
            for pol in self.points:
                transformed_polygon.points.append(Point3d(pol.y,pol.z,pol.x))
            list_with_types,list_with_types_red = transformed_polygon.defTypes([])
            newpolygons = list_with_types.processPolygon()
            for new_pol in newpolygons:
                triangulate_polygon.extend(self.triangulate(new_pol,case))
        else:
            '''
            Caso en que el plano de referencia es 'xz'.
            '''
            transformed_polygon = Polygon3d([])
            for pol in self.points:
                transformed_polygon.points.append(Point3d(pol.x,pol.z,pol.y))
            list_with_types,list_with_types_red = transformed_polygon.defTypes([])
            newpolygons = list_with_types.processPolygon()
            for new_pol in newpolygons:
                triangulate_polygon.extend(self.triangulate(new_pol,case))

        return triangulate_polygon

    def triangulateSolid(self,polygon2,intersects1,intersects2):
        from geometry.controller.geometry_3d.solid_3d import Solid3d
        '''
        Funcion para triangular solido.
        @param polygon_sup : Poligono superior del solido.  
        @param intersects1 : Lista de puntos correspondientes a las esquinas del poligono inferior del solido.
        @param intersects2 : Lista de puntos correspondientes a las esquinas del poligono superior del solido.
        '''
        
        '''
        Determinar el tipo de vertices que contiene cada poligono inferior
        y el central superior.
        '''
        polygon_with_types1,red_list1 = self.defTypes(intersects1)
        polygon_with_types2,red_list2 = polygon2.defTypes(intersects2)

        '''
        Convertir las coordenadas de los vertices de los poligonos centrales de
        rectangulares a polares y utilizar el angulo, empleando sus vertices
        anteriormente identificados.
        '''
        newcoord1 = self.replaceCoord(red_list1,intersects1)
        newcoord2 = polygon2.replaceCoord(red_list2,intersects2)

        '''
        Invertir poligono central superior.
        '''
        polygon2.points.reverse()
        newcoord2.points.reverse()
        polygon_with_types2,red_list2 = polygon2.defTypes(intersects2)

        '''
        Obtener los subpoligonos dentro de cada poligono.
        '''
        newpolygons1 = polygon_with_types1.processPolygon()
        newpolygons2 = polygon_with_types2.processPolygon()

        '''
        Triangular los poligonos y construir el solido.
        '''
        intersection_solid = Solid3d([])
        for new_pol in newpolygons1:
            intersection_solid.triangles.extend(self.triangulate(new_pol,1))
        for new_pol in newpolygons2:
            intersection_solid.triangles.extend(polygon2.triangulate(new_pol,1))
        #chart3(intersection_solid.triangles)

        '''
        Añadir los triangulos laterales del cuerpo.
        '''
        if (intersects1 == [] and intersects2 == []):
            prov = self.obtainLateralPolygons(polygon2,newcoord1,newcoord2,'n')
        else:
            prov = self.obtainLateralPolygons(polygon2,newcoord1,newcoord2,'y')
        intersection_solid.triangles.extend(prov)
        #chart3(prov)

        return intersection_solid

    def obtainHeights(self,polygon_sup):
        '''
        Funcion para obtener las alturas entre dos poligonos de un solido.
        @param polygon_sup : Poligono superior del solido.
        '''

        '''
        Obtener los dos puntos del poligono superior con el valor minimo y el valor maximo en el eje "y".
        '''
        p_int4 = Point3d(0,0,0)
        for p in polygon_sup.points:
            if (p.y > p_int4.y):
               p_int4 = p
        p_int3 = p_int4
        for p in polygon_sup.points:
            if (p.y < p_int3.y):
               p_int3 = p

        '''
        Generar dos nuevos puntos para el poligono superior, en reemplazo de los anteriormente obtenidos,
        conservando las coordenadas "x" e "y". Para calcular la coordenada "z" se divide el poligono en
        dos secciones, una para cada punto. Se promedian los valores en "z" y se asigna el resultado a
        cada uno de los dos puntos.
        '''
        value_y = (min([p.y for p in polygon_sup.points])+max([p.y for p in polygon_sup.points]))/2
        z_sup1 = []; z_sup2 = []
        for p in polygon_sup.points:
            if (p.y >= value_y):
                z_sup2.append(p.z)
            else:
                z_sup1.append(p.z)

        p_int3 = Point3d(p_int3.x,p_int3.y,sum(z_sup1)/len(z_sup1))
        p_int4 = Point3d(p_int4.x,p_int4.y,sum(z_sup2)/len(z_sup2))

        '''
        Crear la curva con los dos puntos reconstruidos generados a partir del poligono superior, con 
        extrapolaciones para que intersecte al poligono inferior.
        '''
        curve = Curve3d([Point3d(x, y, z) for x, y, z in [(2*p_int3.x-p_int4.x, 2*p_int3.y-p_int4.y, \
         2*p_int3.z-p_int4.z), (p_int3.x,p_int3.y,p_int3.z), ((3*p_int3.x+p_int4.x)/4, (3*p_int3.y+p_int4.y)/4, \
         (3*p_int3.z+p_int4.z)/4), ((p_int3.x+p_int4.x)/2, (p_int3.y+p_int4.y)/2, (p_int3.z+p_int4.z)/2), \
         ((p_int3.x+3*p_int4.x)/4, (p_int3.y+3*p_int4.y)/4, (p_int3.z+3*p_int4.z)/4), \
         (p_int4.x, p_int4.y, p_int4.z), (2*p_int4.x-p_int3.x, 2*p_int4.y-p_int3.y, 2*p_int4.z-p_int3.z)]])

        '''
        Identificar los puntos de la recta inferior de interseccion, que tambien se emplean para calcular las alturas.
        '''
        polygon_inf = Polygon3d(self.points[0:len(self.points)])
        polygon_inf.checkOrientation([])
        p_int1,p_int2 = self.intersectCurve(curve,1)
        xrange_inf = [min([p.x for p in self.points]),max([p.x for p in self.points])]
        yrange_inf = [min([p.y for p in self.points]),max([p.y for p in self.points])]

        '''
        Casos en que no se pueden obtener puntos correctos para la recta de interseccion inferior 
        (se salen del rango espacial del poligono inferior o no se pueden calcular). Se seleccionan
        los dos puntos del poligono inferior con el valor minimo y el valor maximo en el eje "y".
        '''
        found = False
        if (p_int1 is None or p_int2 is None):
            found = False
        else:
            if (checkIntervalClosed(xrange_inf[0],xrange_inf[1],p_int1.x) is False):
                found = False
            if (checkIntervalClosed(xrange_inf[0],xrange_inf[1],p_int2.x) is False):
                found = False
            if (checkIntervalClosed(yrange_inf[0],yrange_inf[1],p_int1.y) is False):
                found = False
            if (checkIntervalClosed(yrange_inf[0],yrange_inf[1],p_int2.y) is False):
                found = False
        if (found is False):
            p_int2 = Point3d(0,0,0)
            for p in self.points:
                if (p.y > p_int2.y):
                    p_int2 = p
            p_int1 = p_int2
            for p in self.points:
                if (p.y < p_int1.y):
                   p_int1 = p

        '''
        Generar dos nuevos puntos para el poligono inferior, en reemplazo de los anteriormente obtenidos,
        conservando las coordenadas "x" e "y". Para calcular la coordenada "z" se divide el poligono en
        dos secciones, una para cada punto. Se promedian los valores en "z" y se asigna el resultado a
        cada uno de lo dos puntos.
        '''
        value_y = (min([p.y for p in self.points])+max([p.y for p in self.points]))/2
        z_inf1 = []; z_inf2 = []
        for p in self.points:
            if (p.y >= value_y):
                z_inf2.append(p.z)
            else:
                z_inf1.append(p.z)

        #p_int1 = Point3d(p_int1.x,p_int1.y,min(z_inf1))
        #p_int2 = Point3d(p_int2.x,p_int2.y,min(z_inf2))
        p_int1 = Point3d(p_int1.x,p_int1.y,sum(z_inf1)/len(z_inf1))
        p_int2 = Point3d(p_int2.x,p_int2.y,sum(z_inf2)/len(z_inf2))

        '''
        Se construyen las rectas de interseccion inferior y superior.
        '''
        init_curve1 = Curve3d([p_int1,p_int3])
        init_curve2 = Curve3d([p_int2,p_int4])
        curve_inf = Curve3d([Point3d(init_curve1.points[0].x,init_curve1.points[0].y,p_int1.z),\
         Point3d(init_curve2.points[0].x,init_curve2.points[0].y,p_int2.z)])
        curve_sup = Curve3d([Point3d(init_curve1.points[0].x,init_curve1.points[0].y,p_int3.z),\
         Point3d(init_curve2.points[0].x,init_curve2.points[0].y,p_int4.z)])
        #chart ([self.points,polygon_sup.points,curve_inf.points,curve_sup.points,curve.points],['b','r','g','k','y'])

        '''
        Calcular las alturas.
        '''
        zdiff2 = curve_sup.points[1].z-curve_inf.points[1].z
        zdiff1 = curve_sup.points[0].z-curve_inf.points[0].z
        dz = (zdiff2-zdiff1)/7
        heights = []
        for i in range(7):
            heights.append(zdiff1+dz*i)
        heights.append(zdiff2)

        return heights

    def intersectCurve(self,curve,case):
        '''
        Funcion para obtener los puntos de interseccion entre una curva o corona y el poligono.
        @param curve : Objeto tipo Curve3d que corresponde a una curva o corona de interseccion.  
        @param case  : Opcion de como se debe interpolar para generar las intersecciones. Si es "0",
                       se interpola de manera cuadratica para obtener la coordenada "z". 
                       Si es "1", se interpola con el valor minimo del eje "z". 
                       Por ultimo, si es "2", se interpola con el valor maximo del eje "z".
        '''

        lim_inf = 0
        lim_sup = len(curve.points)
        enter = False
        leave = False
        
        '''
        Obtener el indice inferior de la lista de la curva para la extraccion de la subcurva que esta dentro
        del poligono.
        '''
        for i in range(len(curve.points)):
            enter = self.checkPointInPolygon(curve.points[i],'xy')

            if(enter == True):
                lim_inf = i
                break
        
        '''
        Obtener el indice superior de la lista de la curva para la extraccion de la subcurva que esta dentro
        del poligono.
        '''
        i = len(curve.points)-1
        while i >= 0:
            leave = self.checkPointInPolygon(curve.points[i],'xy')
            
            if(leave == True):
                lim_sup = i+1
                break
            i -= 1

        '''
        Devolver un aviso si la curva no intersecta al poligono.
        '''
        if (enter == False or leave == False):
            return None,None

        '''
        Generar las contantes de las rectas de interpolacion lineal para obtener las intersecciones
        de los dos extremos de la subcurva con el poligono, para la coordenada "y".
        '''
        const_pol11 = Polygon3d([curve.points[lim_inf],curve.points[lim_inf+2]]).obtainConsts(0)
        const_pol12 = Polygon3d([curve.points[lim_sup-3],curve.points[lim_sup-1]]).obtainConsts(0)

        '''
        Obtener los puntos de interseccion de la curva con el poligono.
        '''
        state1 = -1
        state2 = -1
        index1 = 0
        index2 = 0
        
        '''
        Recorrer el poligono punto por punto, viendo si existen puntos validos de interseccion
        con las dos rectas de interpolacion. Si "state" es "-1", significa que no hay punto valido.
        En caso de que "state" sea "0", quiere decir que corresponde a un punto del poligono. Mientras
        que si "state" es "1", el punto esta entre dos puntos del poligono y se debe interpolar
        nuevamente con el fin de generar la coordenada "z". 
        '''
        for i in range(len(self.points)):
            if ((state1 != -1) and (state2 != -1)):
                break
            if (state1 == -1):
                p1 = Point2D(self.points[i-1].x/1000, self.points[i-1].y/1000)
                p2 = Point2D(self.points[i].x/1000, self.points[i].y/1000) 
                state1,p_int1 = Segment2D(p1,p2).obtainIntersection(const_pol11,curve.points[lim_inf],curve.points[lim_inf+2])
                index1 = i
            if (state2 == -1):
                p1 = Point2D(self.points[i-1].x/1000, self.points[i-1].y/1000)
                p2 = Point2D(self.points[i].x/1000, self.points[i].y/1000)
                state2,p_int2 = Segment2D(p1,p2).obtainIntersection(const_pol12,curve.points[lim_sup-1],curve.points[lim_sup-3])
                index2 = i

        '''
        En caso que "case" sea "0", se interpola de forma cuadratica para generar la coordenada "z". En otro
        caso, se interpola de forma empleando el minimo o el maximo. 
        '''
        if (case == 0):
            const_pol21 = Polygon3d([self.points[index1-2],self.points[index1-1],self.points[index1]]).obtainConsts(1)
            const_pol22 = Polygon3d([self.points[index2-2],self.points[index2-1],self.points[index2]]).obtainConsts(1)
            p_int1.append(const_pol21[0]*(p_int1[0]**2)+const_pol21[1]*p_int1[0]+const_pol21[2])
            p_int2.append(const_pol22[0]*(p_int2[0]**2)+const_pol22[1]*p_int2[0]+const_pol22[2])
        else:
            const_pol21 = Polygon3d([self.points[index1-1],self.points[index1]]).obtainConsts(1+case)
            const_pol22 = Polygon3d([self.points[index2-1],self.points[index2]]).obtainConsts(1+case)
            p_int1.append(const_pol21[0]*p_int1[0]+const_pol21[1])
            p_int2.append(const_pol22[0]*p_int2[0]+const_pol22[1])
        p_int1 = Point3d(p_int1[0]*1000,p_int1[1]*1000,p_int1[2]*1000)
        p_int2 = Point3d(p_int2[0]*1000,p_int2[1]*1000,p_int2[2]*1000)

        if (case == 0):
            return lim_inf,lim_sup,state1,state2,index1,index2,p_int1,p_int2
        else:
            return p_int1,p_int2

    def subPolygons(self,curve,points):
        '''
        Funcion para generar dos subpoligonos a partir de una curva o corona de interseccion y el  
        poligono.
        @param curve : Objeto tipo Curve3d que corresponde a una curva o corona de interseccion.
        @param points: Lista de dos esquinas izquierdas que se pasa como parametro si el poligono
                       esta preprocesado y se va a obtener el poligono de interseccion al invocarse
                       esta funcion. Si el poligono se va a dividir por primera vez, tiene valor
                       "None".
                       
        '''

        '''
        Obtener los puntos de interseccion.
        '''
        lim_inf,lim_sup,state1,state2,index1,index2,p_int1,p_int2 = self.intersectCurve(curve,0)

        '''
        Cortar el poligono en dos partes.
        '''
        if (index1 < index2):
            index1 += len(self.points)
        
        index1 -= index2
        polygon_max = Polygon3d([])
        
        if (state2 == 1):
            polygon_max.points.append(p_int2)
            index1 += 1
        polygon_max.points.extend(self.points[index2:])
        polygon_max.points.extend(self.points[:index2])
        if (state2 == 1):
            polygon_max.points.append(p_int2)
        else:
            polygon_max.points.append(self.points[index2])
        
        polygon_min = Polygon3d([])
        polygon_min.points.extend(polygon_max.points[:index1])
        del polygon_max.points[:index1]

        '''
        Cerrar los subpoligonos.
        '''
        new_curve = Polygon3d([])
        new_curve.points.extend(curve.points[lim_inf:lim_sup])
        new_curve.points.reverse()
        polygon_max.points.extend(new_curve.points)
        
        if (state1 == 1):
            polygon_min.points.append(p_int1)
            polygon_max.points.append(p_int1)
        else:
            polygon_min.points.append(polygon_max.points[0])
        
        polygon_min.points.extend(curve.points[lim_inf:lim_sup])

        '''
        Si el subpoligono obtenido se trata del poligono de interseccion, se chequea si no se ha perdido alguna esquina
        izquierda obtenida en el corte anterior.
        '''
        if (points is not None):
            pp = {}
            for i in range(len(polygon_max.points)):
                pp[round(polygon_max.points[i].x,8),round(polygon_max.points[i].y,8),round(polygon_max.points[i].z,8)] = i

            '''
            Obtener del poligono de interseccion los puntos con el valor minimo y maximo de la coordenada "y".
            '''
            p2 = Point3d(0,0,0)
            for p in polygon_max.points:
                if (p.y > p2.y):
                    p2 = p
            p1 = p2
            for p in polygon_max.points:
                if (p.y < p1.y):
                    p1 = p
            
            '''
            Determinar si alguna de las dos esquinas izquierdas (o ambas) del poligono de interseccion obtenidas en el corte anterior
            se perdieron o no. Si ese es el caso, se repone(n) con el o los puntos con el valor de la coordenada "y" minimo o maximo,
            segun corresponda.
            '''
            if ((round(points[0].x,8),round(points[0].y,8),round(points[0].z,8)) in pp):
                p1 = points[0]
            if ((round(points[1].x,8),round(points[1].y,8),round(points[1].z,8)) in pp):
                p2 = points[1]
   
            return polygon_min,polygon_max,p1,p2,p_int1,p_int2
        else:
            '''
            Si el subpoligono obtenido aun no se trata del poligono de interseccion, se devuelve junto a las dos esquinas
            izquierdas de interseccion.
            '''
            return polygon_min,polygon_max,p_int1,p_int2

    def defTypes(self,intersect_points_polygon):
        '''
        Funcion que determina el tipo de cada vertice del poligono, con el fin de dividirlo
        en subpoligonos monotonos.
        @param intersect_points_polygon : Lista de puntos que corresponden a las esquinas del
                                          poligono.  
        '''
        polygon_with_types = SetOfPoint3d([])
        polygon_with_types_red = []
        indexes_intersect_polygon = []
        p_polygon = {}

        '''
        Determinar los indices del poligono a los cuales corresponden las esquinas de este.
        '''
        for i in range(len(self.points)):
            p_polygon[round(self.points[i].x,8),round(self.points[i].y,8),round(self.points[i].z,8)] = i
        for ip in intersect_points_polygon:
            if ((round(ip.x,8),round(ip.y,8),round(ip.z,8)) in p_polygon):
                indexes_intersect_polygon.append(p_polygon[round(ip.x,8),round(ip.y,8),round(ip.z,8)])

        '''
        Recorrer el poligono.
        '''
        for i in range(len(self.points)):
            point1 = self.points[i-1]
            if (i == (len(self.points)-1)):
                point2 = self.points[0]
            else: 
                point2 = self.points[i+1]
            
            '''
            Determinar si se trata de un vertice de inicio o division. Si el angulo es menor de 180 grados,
            es un vertice de inicio y se identificara como "1". Si el angulo es mayor, es de division y se
            identificara como "4". Indicar si se trata de una esquina o no.
            '''
            if (point1.x > self.points[i].x and point2.x > self.points[i].x):
                res = self.checkAngle(self.points[i],point1,point2)
                polygon_with_types.points.append([self.points[i].x,self.points[i].y,1+res,i])
                if (i in indexes_intersect_polygon):
                    polygon_with_types_red.append(7)
                else:
                    polygon_with_types_red.append(1+res)
                '''
                Determinar si se trata de un vertice final o de combinacion. Si el angulo es menor de 180 grados,
                es un vertice final y se identificara como "2". Si el angulo es mayor, es de combinacion y se
                identificara como "4". Indicar si trata de una esquina o no.
                '''
            elif(point1.x < self.points[i].x and point2.x < self.points[i].x):
                res = self.checkAngle(self.points[i],point1,point2)
                polygon_with_types.points.append([self.points[i].x,self.points[i].y,2+res,i])
                if (i in indexes_intersect_polygon):
                    polygon_with_types_red.append(7)
                else:
                    polygon_with_types_red.append(2+res)
                '''
                Determinar si se trata de un vertice regular.
                '''
            else:
                polygon_with_types.points.append([self.points[i].x,self.points[i].y,3,i])
                '''
                Verificar si el vertice es una esquina del poligono. 
                '''
                if (i in indexes_intersect_polygon):
                    polygon_with_types_red.append(7)
                    continue
                '''
                Si el vertice no es una esquina del poligono y es regular, determinar si es un vertice
                puntiagudo.
                '''
                d1 = math.sqrt(((point1.x-self.points[i].x)**2)+((point1.y-self.points[i].y)**2)+((point1.z-self.points[i].z)**2))
                d2 = math.sqrt(((self.points[i].x-point2.x)**2)+((self.points[i].y-point2.y)**2)+((self.points[i].z-point2.z)**2))
                if (d1 < d2):
                    point2 = Point3d(((d2-d1)*self.points[i].x+d1*point2.x)/d2,((d2-d1)*self.points[i].y+d1*point2.y)/d2,\
                     ((d2-d1)*self.points[i].z+d1*point2.z)/d2)
                if (d2 < d1):
                    point1 = Point3d(((d1-d2)*self.points[i].x+d2*point1.x)/d1,((d1-d2)*self.points[i].y+d2*point1.y)/d1,\
                     ((d1-d2)*self.points[i].z+d2*point1.z)/d1)
                d3 = math.sqrt(((point1.x-point2.x)**2)+((point1.y-point2.y)**2)+((point1.z-point2.z)**2))
                if (d3 <= d1*math.sqrt(2)):
                    polygon_with_types_red.append(6+self.checkAngle(self.points[i],point1,point2))
                else:
                    polygon_with_types_red.append(3)
                
        polygon_with_types.points.sort()
        return polygon_with_types,polygon_with_types_red

    def checkAngle(self,point0,point1,point2):
        '''
        Funcion que determina si el angulo entre dos puntos dados es igual o menor a 180 grados.
        @param point0 : Objeto Point3d correspondiente al vertice del angulo.
        @param point1 : Objeto Point3d correspondiente a uno de los lados del angulo.  
        @param point2 : Objeto Point3d correspondiente a otro de los lados del angulo.
        '''
        '''
        Calcular un punto entre los dos puntos del angulo.
        '''
        pm = Point2D((18*point0.x+point1.x+point2.x)/20,(18*point0.y+point1.y+point2.y)/20)

        '''
        Verificar si el punto medio esta dentro del poligono. Si esta dentro, el angulo es menor a 180 grados.
        Si esta afuera, el angulo es mayor a 180 grados.
        '''
        in_polygon = self.checkPointInPolygon(pm,'xy')

        if(in_polygon == True):
            return 0
        else:
            return 3
 
    def transformCoord(self,red_list):
        '''
        Funcion para convertir las coordenadas de los vertices de un poligono, de rectangulares a polares
        y generar una lista con ellas.
        @param red_list : Lista de indentificadores para cada vertice del poligono, indicando su tipo.
        '''

        '''
        Separar coordenadas x e y.
        '''
        xcoord = [p.x for p in self.points]
        ycoord = [p.y for p in self.points]

        '''
        Ajustar las coordenadas x e y de los puntos de los poligonos dentro del rango [-1,1]. 
        '''
        xmed = (min(xcoord)+max(xcoord))/2
        ymed = (min(ycoord)+max(ycoord))/2
        xinterval = (max(xcoord)-min(xcoord))/2
        yinterval = (max(ycoord)-min(ycoord))/2
        output_pol = SetOfPoint3d([])

        '''
        Obtener el angulo en grados, de la coordenada polar de cada punto. 
        '''
        for i in range(len(self.points)):
            output_pol.points.append([Point2D((self.points[i].x-xmed)/xinterval,\
             (self.points[i].y-ymed)/yinterval).polarCoordinate(),red_list[i]])

        return output_pol

    def replaceCoord(self,red_list,intersections):
        '''
        Funcion para convertir las coordenadas de los vertices de un poligono, de rectangulares a polares
        y generar una lista con ellas, empleando sus vertices anteriormente identificados.
        @param red_list     : Lista de indentificadores para cada vertice del poligono, indicando su tipo.
        @param intersections: Lista de objetos Point3d que corresponden a las esquinas del poligono.
        '''

        p_polygon = {}
        indexes_intersections = []
        output_pol = SetOfPoint3d([])

        '''
        Determinar los indices del poligono a los cuales corresponden las esquinas de este.
        '''
        for i in range(len(self.points)):
            p_polygon[round(self.points[i].x,8),round(self.points[i].y,8),round(self.points[i].z,8)] = i
        for ip in intersections:
            if ((round(ip.x,8),round(ip.y,8),round(ip.z,8)) in p_polygon):
                indexes_intersections.append(p_polygon[round(ip.x,8),round(ip.y,8),round(ip.z,8)])
        indexes_intersections.sort()

        '''
        Determinar los limites para cada uno de los cuatro intervalos generados por los vertices del poligono. 
        '''
        range_i = [[0,indexes_intersections[0]+1],[indexes_intersections[0]+1,indexes_intersections[1]+1], \
        [indexes_intersections[1]+1,indexes_intersections[2]+1],[indexes_intersections[2]+1,indexes_intersections[3]+1]]

        '''
        Calcular la coordenada polar para cada uno de los puntos del poligono, segun el intervalo en que se encuentre.
        '''
        for i in range(4):  
            if (i in [0,2]):
                x_range = [self.points[indexes_intersections[i-1]].x,self.points[indexes_intersections[i]].x]
                if (x_range[0] != x_range[1]):
                    for j in range(range_i[i][0],range_i[i][1]):
                        output_pol.points.append([((self.points[j].x-x_range[0])/(x_range[1]-x_range[0]))*90+90*i,red_list[j]])
                else:
                    y_range = [self.points[indexes_intersections[i-1]].y,self.points[indexes_intersections[i]].y]
                    for j in range(range_i[i][0],range_i[i][1]):
                        output_pol.points.append([((self.points[j].y-y_range[0])/(y_range[1]-y_range[0]))*90+90*i,red_list[j]])    
            else:
                y_range = [self.points[indexes_intersections[i-1]].y,self.points[indexes_intersections[i]].y]
                if (y_range[0] != y_range[1]):
                    for j in range(range_i[i][0],range_i[i][1]):
                        output_pol.points.append([((self.points[j].y-y_range[0])/(y_range[1]-y_range[0]))*90+90*i,red_list[j]])
                else:
                    x_range = [self.points[indexes_intersections[i-1]].x,self.points[indexes_intersections[i]].x]
                    for j in range(range_i[i][0],range_i[i][1]):
                        output_pol.points.append([((self.points[j].x-x_range[0])/(x_range[1]-x_range[0]))*90+90*i,red_list[j]])    

        return output_pol

    def checkOrientation(self,curves):
        '''
        Funcion para dejar orientado un poligono de forma contraria a las manecillas del reloj, y a favor
        de las manecillas del reloj a las otras curvas.
        @param curves : Lista de objetos Curve3d que se deben orientar.
        '''

        '''
        Separar coordenadas x e y.
        '''
        xcoord = [p.x for p in self.points]
        ycoord = [p.y for p in self.points]

        '''
        Ajustar las coordenadas x e y de los puntos del poligono dentro del rango [-1,1]. 
        '''
        xmed = (max(xcoord)+min(xcoord))/2
        ymed = (max(ycoord)+min(ycoord))/2
        xinterval = (max(xcoord)-min(xcoord))/2
        yinterval = (max(ycoord)-min(ycoord))/2
        output_pol = []

        '''
        Obtener el angulo en grados, de la coordenada polar de cada punto. 
        '''
        for p in self.points:
            output_pol.append(Point2D((p.x-xmed)/xinterval,(p.y-ymed)/yinterval).polarCoordinate())
        
        '''
        Determinar si se debe invertir el poligono o no. 
        '''
        cases = 0
        for i in range(len(output_pol)):
            if (output_pol[i-1] < output_pol[i]):
                cases += 1
        if (cases < len(output_pol)/2):
            self.points.reverse()
        
        '''
        Obtener el punto mas a la derecha del poligono.
        '''
        points_candidates = []
        for i in range(len(self.points)):
            if (self.points[i].x >= xmed):
                points_candidates.append([math.sqrt(((xmed-self.points[i].x)**2)+((ymed-self.points[i].y)**2)),i])
        points_candidates.sort()
        
        '''
        Recorrer cada una de las otras curvas.
        '''
        for curve in curves:
            output_pol = []
            xdiff = []
            ydiff = []
            
            '''
            Generar las coordenadas polares para los puntos de cada curva con respecto al extremo derecho
            del poligono.
            '''
            for p in curve.points:
                xdiff.append(abs(self.points[points_candidates[len(points_candidates)-1][1]].x-p.x))
                ydiff.append(abs(self.points[points_candidates[len(points_candidates)-1][1]].y-p.y))
            xinterval = max(xdiff)
            yinterval = min(ydiff)

            for p in curve.points:
                output_pol.append(Point2D((p.x-self.points[points_candidates[len(points_candidates)-1][1]].x)/xinterval,\
                 (p.y-self.points[points_candidates[len(points_candidates)-1][1]].y)/yinterval).polarCoordinate())
            '''
            Determinar si se debe invertir la curva o no.
            '''
            if (output_pol[len(output_pol)-1] > output_pol[0]):
                curve.points.reverse()
            
    def obtainLateralPolygons(self,polygon2,newcoord1,newcoord2,precheck):
        '''
        Funcion para obtener los poligonos laterales del cuerpo.
        @param polygon2 : Objeto Polygon3d que corresponde al poligono superior del solido a construir.
        @param newcoord1: Objeto ListPoints3d que contiene las coordenadas polares y los indices del poligono inferior.
        @param newcoord2: Objeto ListPoints3d que contiene las coordenadas polares y los indices del poligono superior.
        @param precheck : Indica si se debe hacer prebusqueda o no. Si es "y", significa que se debe hacer, ya
                          que estan identificadas las esquinas de los poligonos, producto de lo cual se deben generar
                          subtramos iniciales de busqueda. Si es "n", no se debe hacer porque las esquinas de los poligonos
                          no estan identificadas.
        '''

        lateral_polygons = []
        special_corners_pol1 = SetOfPoint3d([])
        special_corners_pol2 = SetOfPoint3d([])
        indexes_special_corners1 = []
        indexes_special_corners2 = []
        limit_corners = []
        limit_corners2 = []

        '''
        En el caso que las esquinas esten identificadas, obtener los limites de los subtramos iniciales de busqueda
        (prebusqueda).
        '''
        if (precheck == 'y'):
            for i in range(len(newcoord1.points)):
                if (newcoord1.points[i][1] == 7):
                    special_corners_pol1.points.append(newcoord1.points[i])
                    indexes_special_corners1.append(i)
            for i in range(len(newcoord2.points)):
                if (newcoord2.points[i][1] == 7):
                    special_corners_pol2.points.append(newcoord2.points[i])
                    indexes_special_corners2.append(i)

            subdivision = special_corners_pol1.obtainSegments(special_corners_pol2,None,0)
            for i in range(len(subdivision)):
                limit_corners.append([indexes_special_corners1[i],indexes_special_corners2[subdivision[i]]])

            limit_corners.sort()
            special_corners_pol1 = SetOfPoint3d([])
            special_corners_pol2 = SetOfPoint3d([])
            indexes_special_corners1 = []
            indexes_special_corners2 = []

        '''
        Obtener los subtramos de busqueda definitivos.
        '''        
        for i in range(len(newcoord1.points)):
            if (newcoord1.points[i][1] in [1,2,4,5,6,7,9]):
                special_corners_pol1.points.append(newcoord1.points[i])
                indexes_special_corners1.append(i)
        for i in range(len(newcoord2.points)):
            if (newcoord2.points[i][1] in [1,2,4,5,6,7,9]):
                special_corners_pol2.points.append(newcoord2.points[i])
                indexes_special_corners2.append(i)
    
        if (precheck == 'y'):
            if (len(special_corners_pol1.points) <= len(special_corners_pol2.points)):
                subdivision = special_corners_pol1.obtainSegments(special_corners_pol2,limit_corners,0)
                for i in range(len(subdivision)):
                    limit_corners2.append([indexes_special_corners1[i],indexes_special_corners2[subdivision[i]]])
            else:
                for lc in limit_corners:
                    lc.reverse()
                limit_corners.reverse()
                limit_corners.sort()
                subdivision = special_corners_pol2.obtainSegments(special_corners_pol1,limit_corners,0)
                for i in range(len(subdivision)):
                    limit_corners2.append([indexes_special_corners1[subdivision[i]],indexes_special_corners2[i]])
            limit_corners2.extend(limit_corners)
        else:
            if (len(special_corners_pol1.points) <= len(special_corners_pol2.points)):
                subdivision = special_corners_pol1.obtainSegments(special_corners_pol2,None,0)
                for i in range(len(subdivision)):
                    limit_corners2.append([indexes_special_corners1[i],indexes_special_corners2[subdivision[i]]])
            else:
                subdivision = special_corners_pol2.obtainSegments(special_corners_pol1,None,0)
                for i in range(len(subdivision)):
                    limit_corners2.append([indexes_special_corners1[subdivision[i]],indexes_special_corners2[i]])
        limit_corners2.sort()

        '''
        Determinar el orden para evaluar los subpoligonos laterales y triangular.
        '''
        if (len(newcoord1.points) >= len(newcoord2.points)):
            segments = newcoord1.obtainSegments(newcoord2,limit_corners2,1)
            for i in range(len(segments)):
                if(segments[i-1] == segments[i]):
                    lateral_polygons.append(Triangle3d(self.points[i-1],polygon2.points[segments[i]],self.points[i]))
                else:
                    if (segments[i-1] > segments[i]):
                        indexes = range(segments[i],segments[i-1]+1)
                    else:
                        indexes = range(segments[i],len(newcoord2.points))
                        indexes.extend(range(segments[i-1]+1))
                    diff = len(indexes)
                    lateral_polygons.append(Triangle3d(self.points[i-1],polygon2.points[indexes[diff-diff//2]],self.points[i]))
                    for j in range(1,diff//2):
                        lateral_polygons.append(Triangle3d(self.points[i-1],polygon2.points[indexes[len(indexes)-j]], \
                         polygon2.points[indexes[len(indexes)-j-1]]))
                    for j in range(1,diff-diff//2+1):
                        lateral_polygons.append(Triangle3d(self.points[i],polygon2.points[indexes[j]],polygon2.points[indexes[j-1]]))
            return lateral_polygons
        else:
            for lc in limit_corners2:
                lc.reverse()
            limit_corners2.reverse()
            limit_corners2.sort()
            segments = newcoord2.obtainSegments(newcoord1,limit_corners2,1)
            for i in range(len(segments)):
                if(segments[i-1] == segments[i]):
                    lateral_polygons.append(Triangle3d(polygon2.points[i-1],self.points[segments[i]],polygon2.points[i]))
                else:
                    if (segments[i-1] > segments[i]):
                        indexes = list(range(segments[i],segments[i-1]+1))
                    else:
                        indexes = list(range(segments[i],len(newcoord1.points)))
                        indexes.extend(list(range(segments[i-1]+1)))
                    diff = len(indexes)
                    lateral_polygons.append(Triangle3d(polygon2.points[i-1],self.points[indexes[diff-diff//2]],polygon2.points[i]))
                    for j in range(1,diff//2):
                        lateral_polygons.append(Triangle3d(polygon2.points[i-1],self.points[indexes[len(indexes)-j]], \
                         self.points[indexes[len(indexes)-j-1]]))
                    for j in range(1,diff-diff//2+1):
                        lateral_polygons.append(Triangle3d(polygon2.points[i],self.points[indexes[j]],self.points[indexes[j-1]]))
            return lateral_polygons

    def orientPolygon(self,cube,num_face):
        '''
        Funcion que orienta un poligono en la direccion del movimiento de las
        manecillas del reloj.
        '''

        '''
        Transformar el poligono a orientar de tres dimensiones a dos dimensiones.
        '''
        new_polygon = []
        for num_point in range(0,len(self.points)):
            if (num_face in [0,1]):
                cube_xmin = cube.ymin; cube_xmax = cube.ymax; cube_ymin = cube.zmin; cube_ymax = cube.zmax
                new_polygon.append([self.points[num_point].y,self.points[num_point].z,10,num_point])
            if (num_face in [2,3]):
                cube_xmin = cube.xmin; cube_xmax = cube.xmax; cube_ymin = cube.zmin; cube_ymax = cube.zmax
                new_polygon.append([self.points[num_point].x,self.points[num_point].z,10,num_point])
            if (num_face in [4,5]):
                cube_xmin = cube.xmin; cube_xmax = cube.xmax; cube_ymin = cube.ymin; cube_ymax = cube.ymax
                new_polygon.append([self.points[num_point].x,self.points[num_point].y,10,num_point])

        '''
        Calcular el centro del poligono, maximo y minimo en dos dimensiones.
        '''
        centroide_x = 0; centroide_y = 0;
        x_min = 1000000; x_max = 0
        y_min = 1000000; y_max = 0

        for point in new_polygon:
            centroide_x += point[0]
            centroide_y += point[1]
            x_min = min(x_min,point[0])
            x_max = max(x_max,point[0])
            y_min = min(y_min,point[1])
            y_max = max(y_max,point[1])

        centroide_x /= len(new_polygon)
        centroide_y /= len(new_polygon)
        #x_min -= centroide_x
        #x_max -= centroide_x
        #y_min -= centroide_y
        #y_max -= centroide_y
        
        #print ('x_min = ',x_min)
        #print ('x_max = ',x_max)
        #print ('y_min = ',y_min)
        #print ('y_max = ',y_max)
        #print ('centroide_x = ',centroide_x)
        #print ('centroide_y = ',centroide_y)

        #print ('polygon points = ',len(self.points))

        '''
        Separar los puntos del poligono a orientar que estan en el borde del cubo, para cada lado de este.
        '''
        segment_xl_yh_xh_yh = []
        segment_xh_yh_xh_yl = []
        segment_xh_yl_xl_yl = []
        segment_xl_yl_xl_yh = []

        index_new_polygon = 0

        while (index_new_polygon < len(new_polygon)):
            if(new_polygon[index_new_polygon][1] == cube_ymax):
                segment_xl_yh_xh_yh.append(new_polygon[index_new_polygon])
                del new_polygon[index_new_polygon]
                continue
            if(new_polygon[index_new_polygon][0] == cube_xmax):
                segment_xh_yh_xh_yl.append(new_polygon[index_new_polygon])
                del new_polygon[index_new_polygon]
                continue
            if(new_polygon[index_new_polygon][1] == cube_ymin):
                segment_xh_yl_xl_yl.append(new_polygon[index_new_polygon])
                del new_polygon[index_new_polygon]
                continue
            if(new_polygon[index_new_polygon][0] == cube_xmin):
                segment_xl_yl_xl_yh.append(new_polygon[index_new_polygon])
                del new_polygon[index_new_polygon]
                continue
            
            index_new_polygon += 1 
            
        segment_xl_yh_xh_yh.sort()
        segment_xh_yh_xh_yl.sort(key=lambda x:x[1])
        segment_xh_yh_xh_yl.reverse()
        segment_xh_yl_xl_yl.sort()
        segment_xh_yl_xl_yl.reverse()
        segment_xl_yl_xl_yh.sort(key=lambda x:x[1])

        #segment_xl_yh_xh_yh.sort()
        #segment_xl_yh_xh_yh.reverse()
        #segment_xh_yh_xh_yl.sort(key=lambda x:x[1])
        #segment_xh_yl_xl_yl.sort()
        #segment_xl_yl_xl_yh.sort(key=lambda x:x[1])
        #segment_xl_yl_xl_yh.reverse()
       
        list_segments = [segment_xl_yh_xh_yh,segment_xh_yh_xh_yl,segment_xh_yl_xl_yl,segment_xl_yl_xl_yh]
        #print ('agregar0 = ',list_segments)
        for i in range(0,4):
            if(list_segments[i] != []):
                list_segments[i][0].append(i)
                #print ('segment[',i,'] =',list_segments[i])
                #print ('agregar = ',list_segments[i][0])
                new_polygon.append(list_segments[i][0])

        '''
        Modificar rango de coordenadas.
        '''
        x_min = 1000000; x_max = 0
        y_min = 1000000; y_max = 0

        for point in new_polygon:     
            point[0] -= centroide_x
            point[1] -= centroide_y
            #print ('point 0 = ',point[0])
            #print ('point 1 = ',point[1])
            x_min = min(x_min,point[0])
            x_max = max(x_max,point[0])
            y_min = min(y_min,point[1])
            y_max = max(y_max,point[1])

        #x_min = min(new_polygon[:][0])
        #x_max = max(new_polygon[:][0])
        #y_min = min(new_polygon[:][1])
        #y_max = max(new_polygon[:][1])

        #print ('x_min = ',x_min)
        #print ('x_max = ',x_max)
        #print ('y_min = ',y_min)
        #print ('y_max = ',y_max)

        for point in new_polygon:
            if (point[0] < 0):
                point[0] /= -x_min
            else:
                point[0] /= x_max

            if (point[1] < 0):
                point[1] /= -y_min
            else:
                point[1] /= y_max

            point[2] = math.atan2(point[1],point[0])
            #print ('new_p0 = ',point[0])
            #print ('new_p1 = ',point[1])
            #print ('new_point2 = ',point[2])
                   
        '''
        Ordenar los puntos de acuerdo a la transformacion de coordenadas realizada.
        '''
        oriented_polygon = Polygon3d([])
        
        new_polygon.sort(key=lambda x:x[2])
        #print ('new_pol = ',new_polygon)
        for point in new_polygon:
            #print ('new_point2 = ',point[2])
            if (len(point) == 5):
                segment = list_segments[point[4]]
                segment.reverse()
                for p in segment:
                    oriented_polygon.points.append(self.points[p[3]])
            else:
                oriented_polygon.points.append(self.points[point[3]])

        '''
        Invertir orientacion de los poligonos para las caras 1, 2 y 5.
        '''
        if num_face in [1,2,5]:
            oriented_polygon.points.reverse()
            
        return oriented_polygon

    def triangulate(self,indexes_pol,option):
      '''
      Funcion para triangular cada subpoligono monotono, con la correspondiente orientacion.
      @param indexes_pol : Lista de indices que corresponden a las posiciones reales de los puntos del poligono.
      @param option      : Indice que indica que plano se utilizara como referencia para la triangulacion del
                           poligono. Si es "1", se empleara el plano "xy". Si es "2", el plano "yz". Si es "3",
                           el plano "xz".
      '''

      '''
      Devolver el mismo poligono generando un solo triangulo si contiene tres puntos. 
      '''
      if (len(self.points) == 3):
        return [Triangle3d(self.points[0],self.points[1],self.points[2])]

      triangles = []
      pts = {}
      '''
      Generar diccionario con los vecinos de cada punto empleando plano "xy".
      '''
      if (option == 1):
        for i in range(len(indexes_pol)-1):
          pts[self.points[indexes_pol[i]].x,self.points[indexes_pol[i]].y,self.points[indexes_pol[i]].z] =\
           [self.points[indexes_pol[i-1]].x,self.points[indexes_pol[i-1]].y,self.points[indexes_pol[i-1]].z,\
           self.points[indexes_pol[i+1]].x,self.points[indexes_pol[i+1]].y,self.points[indexes_pol[i+1]].z]
        pts[self.points[indexes_pol[len(indexes_pol)-1]].x,self.points[indexes_pol[len(indexes_pol)-1]].y,\
         self.points[indexes_pol[len(indexes_pol)-1]].z] = [self.points[indexes_pol[len(indexes_pol)-2]].x,\
         self.points[indexes_pol[len(indexes_pol)-2]].y,self.points[indexes_pol[len(indexes_pol)-2]].z,\
         self.points[indexes_pol[0]].x,self.points[indexes_pol[0]].y,self.points[indexes_pol[0]].z]
        '''
        Generar diccionario con los vecinos de cada punto empleando plano "yz".
        '''
      elif (option == 2):
        for i in range(len(indexes_pol)-1):
          pts[self.points[indexes_pol[i]].y,self.points[indexes_pol[i]].z,self.points[indexes_pol[i]].x] =\
           [self.points[indexes_pol[i-1]].y,self.points[indexes_pol[i-1]].z,self.points[indexes_pol[i-1]].x,\
           self.points[indexes_pol[i+1]].y,self.points[indexes_pol[i+1]].z,self.points[indexes_pol[i+1]].x]
        pts[self.points[indexes_pol[len(indexes_pol)-1]].y,self.points[indexes_pol[len(indexes_pol)-1]].z,\
         self.points[indexes_pol[len(indexes_pol)-1]].x] = [self.points[indexes_pol[len(indexes_pol)-2]].y,\
         self.points[indexes_pol[len(indexes_pol)-2]].z,self.points[indexes_pol[len(indexes_pol)-2]].x,\
         self.points[indexes_pol[0]].y,self.points[indexes_pol[0]].z,self.points[indexes_pol[0]].x]
      else:
        '''
        Generar diccionario con los vecinos de cada punto empleando plano "xz".
        '''
        for i in range(len(indexes_pol)-1):
          pts[self.points[indexes_pol[i]].x,self.points[indexes_pol[i]].z,self.points[indexes_pol[i]].y] =\
           [self.points[indexes_pol[i-1]].x,self.points[indexes_pol[i-1]].z,self.points[indexes_pol[i-1]].y,\
           self.points[indexes_pol[i+1]].x,self.points[indexes_pol[i+1]].z,self.points[indexes_pol[i+1]].y]
        pts[self.points[indexes_pol[len(indexes_pol)-1]].x,self.points[indexes_pol[len(indexes_pol)-1]].z,\
         self.points[indexes_pol[len(indexes_pol)-1]].y] = [self.points[indexes_pol[len(indexes_pol)-2]].x,\
         self.points[indexes_pol[len(indexes_pol)-2]].z,self.points[indexes_pol[len(indexes_pol)-2]].y,\
         self.points[indexes_pol[0]].x,self.points[indexes_pol[0]].z,self.points[indexes_pol[0]].y]

      '''
      Obtener las coordenadas de los puntos del poligono y ordenarlas de izquierda a derecha.
      '''
      ks = sorted(pts)

      index = 1
      '''
      Recorrer cada punto del poligono de izquierda a derecha.
      '''
      while (len(ks) > 2):

        i = 0
        while (i < index):
          '''
          Verificar si existe un vertice hacia atras con el cual triangular.
          '''
          if (pts[ks[i][0],ks[i][1],ks[i][2]][0] == pts[ks[index][0],ks[index][1],ks[index][2]][3] and \
           pts[ks[i][0],ks[i][1],ks[i][2]][1] == pts[ks[index][0],ks[index][1],ks[index][2]][4]):
            '''
            Generar un nuevo triangulo para el plano "xy".
            '''
            if (option == 1):
              triangles.append(Triangle3d(Point3d(ks[index][0],ks[index][1],ks[index][2]),Point3d(pts[ks[index][0],ks[index][1],\
               ks[index][2]][3],pts[ks[index][0],ks[index][1],ks[index][2]][4],pts[ks[index][0],ks[index][1],\
               ks[index][2]][5]),Point3d(ks[i][0],ks[i][1],ks[i][2])))
              '''
              Generar un nuevo triangulo para el plano "yz".
              '''
            elif (option == 2):
              triangles.append(Triangle3d(Point3d(ks[index][2],ks[index][0],ks[index][1]),Point3d(pts[ks[index][0],ks[index][1],\
               ks[index][2]][5],pts[ks[index][0],ks[index][1],ks[index][2]][3],pts[ks[index][0],ks[index][1],\
               ks[index][2]][4]),Point3d(ks[i][2],ks[i][0],ks[i][1])))
              '''
              Generar un nuevo triangulo para el plano "xz".
              '''
            else:
              triangles.append(Triangle3d(Point3d(ks[index][0],ks[index][2],ks[index][1]),Point3d(pts[ks[index][0],ks[index][1],\
               ks[index][2]][3],pts[ks[index][0],ks[index][1],ks[index][2]][5],pts[ks[index][0],ks[index][1],\
               ks[index][2]][4]),Point3d(ks[i][0],ks[i][2],ks[i][1])))
            '''
            Actualizar el diccionario con los puntos del resto de poligono que queda. 
            '''
            del pts[pts[ks[index][0],ks[index][1],ks[index][2]][3],pts[ks[index][0],ks[index][1],ks[index][2]][4],\
             pts[ks[index][0],ks[index][1],ks[index][2]][5]]
            pts[ks[index][0],ks[index][1],ks[index][2]] = [pts[ks[index][0],ks[index][1],ks[index][2]][0],\
             pts[ks[index][0],ks[index][1],ks[index][2]][1],pts[ks[index][0],ks[index][1],ks[index][2]][2],ks[i][0],ks[i][1],ks[i][2]]
            pts[ks[i][0],ks[i][1],ks[i][2]] = [ks[index][0],ks[index][1],ks[index][2],pts[ks[i][0],ks[i][1],\
             ks[i][2]][3],pts[ks[i][0],ks[i][1],ks[i][2]][4],pts[ks[i][0],ks[i][1],ks[i][2]][5]]
            ks = []
            ks = sorted(pts)

            i = index
            index = 0
          '''
          if (pts[ks[i][0],ks[i][1]][2] == pts[ks[index][0],ks[index][1]][0] and \
           pts[ks[i][0],ks[i][1]][3] == pts[ks[index][0],ks[index][1]][1]):
            triangles.append([Point2D(ks[index][0],ks[index][1]),Point2D(ks[i][0],ks[i][1]),Point2D(pts[ks[index][0],ks[index][1]][0],\
             pts[ks[index][0],ks[index][1]][1])])
            del pts[pts[ks[index][0],ks[index][1]][0],pts[ks[index][0],ks[index][1]][1]]
            pts[ks[index][0],ks[index][1]] = [ks[i][0],ks[i][1],pts[ks[index][0],ks[index][1]][2],pts[ks[index][0],ks[index][1]][3]]
            pts[ks[i][0],ks[i][1]] = [pts[ks[i][0],ks[i][1]][0],pts[ks[i][0],ks[i][1]][1],ks[index][0],ks[index][1]]
            ks = []
            ks = pts.keys()
            ks.sort()
            i = index
            index = 0
          '''
          i += 1
        index += 1
      return triangles

    def obtainConsts(self,case):
        '''
        Funcion para obtener las constantes del polinomio lineal o cuadratico de interpolacion,
        que se necesita para generar las intersecciones entre la curva y el poligono.
        @param case: Opcion de interpolacion.
        '''

        a = []
        u = []
        
        '''
        case igual a "0": Se interpola de forma lineal para la coordenada "y".
        '''
        if (case == 0):
            m = Segment2D(Point2D(self.points[0].x/1000,self.points[0].y/1000),\
             Point2D(self.points[1].x/1000,self.points[1].y/1000)).getSlope()
            if (m is None):
                return [None,Point2D(self.points[0].x/1000,self.points[0].y/1000),\
                 Point2D(self.points[1].x/1000,self.points[1].y/1000)]
            else:
                return [m,(self.points[0].y/1000)-m*self.points[0].x/1000]
            '''
            case igual a "1": Se interpola de forma cuadratica para la coordenada "z".
            '''
        elif (case == 1):
            for i in range(3):
                a.append([(self.points[i].x/1000)**2,self.points[i].x/1000,1])
                u.append(self.points[i].z/1000)
            return gaussianElimination(a,u)
        else:
            m = Segment2D(Point2D(self.points[0].x/1000,self.points[0].z/1000),\
             Point2D(self.points[1].x/1000,self.points[1].z/1000)).getSlope()
            if (m is None):
                '''
                case igual a "2": Se interpola con el valor minimo de la coordenada "z".
                '''
                if (case == 2):
                    return [0,min(self.points[0].z/1000,self.points[1].z/1000)]
                    '''
                    case igual a "3": Se interpola con el valor maximo de la coordenada "z".
                    '''
                else:
                    return [0,max(self.points[0].z/1000,self.points[1].z/1000)]
            else: 
                return [m,(self.points[0].z/1000)-m*self.points[0].x/1000]

    def getDivisionPolygon(self,plane):
        '''
        Funcion que entrega un poligono de division a partir de una secuencia de puntos, eliminando los repetidos.
        @param plane: Indica el plano de referencia empleado para comparar si dos puntos tienen las
                      mismas coordenadas o no. 
        '''

        '''
        Eliminar puntos repetidos del poligono de division.
        '''
        points_polygon2 = Polygon3d([])
        points_polygon3 = Polygon3d([])
        pp = {}

        for p1 in self.points:
            if ((round(p1.x,8),round(p1.y,8),round(p1.z,8)) not in pp):
                pp[(round(p1.x,8),round(p1.y,8),round(p1.z,8))] = (0,0,0)
                points_polygon2.points.append(p1)
                if (plane == 'xy'):
                    points_polygon3.points.append(Point2D(p1.y,p1.z))
                if (plane == 'yz'):
                    points_polygon3.points.append(Point2D(p1.z,p1.x))
                if (plane == 'zx'):
                    points_polygon3.points.append(Point2D(p1.x,p1.y))

        '''
        Si no es posible generar el poligono de division, entregar un mensaje.
        '''
        if (len(points_polygon2.points) < 3):
            return None
        else:
            '''
            Ordenar los puntos del poligono de division construido y generar objeto Polygon3d.
            '''
            pol_coord = points_polygon3.transformCoord(range(len(points_polygon3.points)))
            pol_coord.points.sort()
            cut_pol = Polygon3d([])
            for pol in pol_coord.points:
                cut_pol.points.append(points_polygon2.points[pol[1]])
            #chart([self.points,cut_pol.points],['g','b'])
            '''
            points_polygon2 = Polygon3d([])
            points_polygon2.points.extend(cut_pol.points)
            cut_pol = Polygon3d([])
            point = points_polygon2.points[0]
            cut_pol.points.append(point)
            del points_polygon2.points[0]
            while (len(points_polygon2.points) > 0):
                distance = 0
                for i in range(len(points_polygon2.points)):
                    distance = max(Segment3d(point,points_polygon2.points[i]).checkdistance(),distance)
                for i in range(len(points_polygon2.points)):
                    newdistance = Segment3d(point,points_polygon2.points[i]).checkdistance()
                    if (newdistance <= distance):
                        newpoint = [points_polygon2.points[i],i]
                point = newpoint[0]
                cut_pol.points.append(point)
                del points_polygon2.points[newpoint[1]]
            #chart2([cut_pol.points,points_polygon2.points],['k','b'])
            '''
            return cut_pol

    def checkPointInPolygon(self,point,plane):
        '''
        Funcion que indica si un punto esta dentro de un poligono o no. Devuelve "True" en caso afirmativo
        y "False" en caso negativo.
        @param point: Objeto Point3d para el cual se debe indicar si esta dentro del poligono o no.
        '''

        '''
        Recorrer para cada segmento del poligono.
        '''
        countintersect = 0
        if (plane == 'xy'):
            for i in range(len(self.points)):
                '''
                Construir una semirrecta con el punto pasado como parametro y examinar si intersecta el segmento o no.
                En caso positivo, se incrementa el contador de intersecciones en 1.
                '''
                if (checkIntervalSemiopen(self.points[i-1].x,self.points[i].x,point.x) == True):
                    if(min(self.points[i-1].y,self.points[i].y) > point.y):
                        countintersect += 1
                    elif((min(self.points[i-1].y,self.points[i].y) < point.y) and \
                     (max(self.points[i-1].y,self.points[i].y) > point.y)):
                        m = Segment2D(Point2D(self.points[i-1].x,self.points[i-1].y), Point2D(self.points[i].x,self.points[i].y)).getSlope() 
                        if m is not None and (point.y < m*(point.x-self.points[i-1].x)+self.points[i-1].y):
                            countintersect += 1

        elif (plane == 'yz'):
            for i in range(len(self.points)):
                '''
                Construir una semirrecta con el punto pasado como parametro y examinar si intersecta el segmento o no.
                En caso positivo, se incrementa el contador de intersecciones en 1.
                '''
                if (checkIntervalSemiopen(self.points[i-1].y,self.points[i].y,point.y) == True):
                    if(min(self.points[i-1].z,self.points[i].z) > point.z):
                        countintersect += 1
                    elif((min(self.points[i-1].z,self.points[i].z) < point.z) and \
                     (max(self.points[i-1].z,self.points[i].z) > point.z)):
                        m = Segment2D(Point2D(self.points[i-1].y,self.points[i-1].z), Point2D(self.points[i].y,self.points[i].z)).getSlope() 
                        if m is not None and (point.z < m*(point.y-self.points[i-1].y)+self.points[i-1].z):
                            countintersect += 1

        elif (plane == 'xz'):
            for i in range(len(self.points)):
                '''
                Construir una semirrecta con el punto pasado como parametro y examinar si intersecta el segmento o no.
                En caso positivo, se incrementa el contador de intersecciones en 1.
                '''
                if (checkIntervalSemiopen(self.points[i-1].x,self.points[i].x,point.x) == True):
                    if(min(self.points[i-1].z,self.points[i].z) > point.z):
                        countintersect += 1
                    elif((min(self.points[i-1].z,self.points[i].z) < point.z) and \
                     (max(self.points[i-1].z,self.points[i].z) > point.z)):
                        m = Segment2D(Point2D(self.points[i-1].x,self.points[i-1].z), Point2D(self.points[i].x,self.points[i].z)).getSlope() 
                        if m is not None and (point.z < m*(point.x-self.points[i-1].x)+self.points[i-1].z):
                            countintersect += 1

        else:
            return None

        '''
        Si el numero de intersecciones de la semirrecta con el poligono es impar, el punto esta dentro de este.
        '''
        if(countintersect%2 == 1):
            return True
        else:
            return False

'''
Funcion graficadora del resultado de la triangulacion.
'''
def chart(polygons,colors):
  fig = plt.figure(figsize=(8,6))
  ax = fig.add_subplot(1, 1, 1, projection='3d')
  for i in range(len(polygons)):
    xs = []; ys = []; zs = []
    for point in polygons[i]:
      xs.append(point.x); ys.append(point.y); zs.append(point.z)
    for j in range(len(xs)-1):
      plt.plot(xs[j:j+2], ys[j:j+2], zs[j:j+2], colors[i])
    plt.plot([xs[len(xs)-1], xs[0]], [ys[len(xs)-1], ys[0]], [zs[len(xs)-1], zs[0]], colors[i])
  plt.show()

def chart2(polygons,colors):
  fig = plt.figure(figsize=(8,6))
  ax = fig.add_subplot(1, 1, 1, projection='3d')
  for i in range(len(polygons)):
    xs = []; ys = []; zs = [] 
    for point in polygons[i]:
      xs.append(point.x); ys.append(point.y); zs.append(point.z)
    for j in range(len(xs)-1):
      plt.plot(xs[j:j+2], ys[j:j+2], zs[j:j+2], colors[i])
    #plt.plot([xs[len(xs)-1], xs[0]], [ys[len(xs)-1], ys[0]], [zs[len(xs)-1], zs[0]], colors[i])
  plt.show()

def chart3(triangles):
  fig = plt.figure(figsize=(8,6))
  ax = fig.add_subplot(1, 1, 1, projection='3d')
  for triangle in triangles:
    xs = []; ys = []; zs = []
    xs.append(triangle.p0.x)
    xs.append(triangle.p1.x)
    xs.append(triangle.p2.x)
    ys.append(triangle.p0.y)
    ys.append(triangle.p1.y)
    ys.append(triangle.p2.y)
    zs.append(triangle.p0.z)
    zs.append(triangle.p1.z)
    zs.append(triangle.p2.z)
    for i in range(len(xs)-1):
      plt.plot(xs[i:i+2], ys[i:i+2], zs[i:i+2], 'r')
    plt.plot([xs[len(xs)-1], xs[0]], [ys[len(xs)-1], ys[0]],  [zs[len(xs)-1], zs[0]], 'r')
  plt.show()

def chart6(polygons,triangles_solid):
  fig = plt.figure(figsize=(8,6))
  ax = fig.add_subplot(1, 1, 1, projection='3d')
  for triangle in triangles_solid:
    xs = []; ys = []; zs = []
    xs.append(triangle.p0.x)
    xs.append(triangle.p1.x)
    xs.append(triangle.p2.x)
    ys.append(triangle.p0.y)
    ys.append(triangle.p1.y)
    ys.append(triangle.p2.y)
    zs.append(triangle.p0.z)
    zs.append(triangle.p1.z)
    zs.append(triangle.p2.z)
    for i in range(len(xs)-1):
      plt.plot(xs[i:i+2], ys[i:i+2], zs[i:i+2], 'y')
    plt.plot([xs[len(xs)-1], xs[0]], [ys[len(xs)-1], ys[0]],  [zs[len(xs)-1], zs[0]], 'y')
  #for i in range(len(polygons)):
  #for i in range(len(polygons)):
  xs = []; ys = []; zs = []
  #for point in polygons[i].points:
  for point in polygons.points:
    xs.append(point.x); ys.append(point.y); zs.append(point.z)
  colours = ['r','k','b','c','m','g','r','k','b','c','m','g','r','k','b','c','m','g']
  for j in range(len(xs)-1):
    #plt.plot(xs[j:j+2], ys[j:j+2], zs[j:j+2], colours[j])
    plt.plot(xs[j:j+2], ys[j:j+2], zs[j:j+2], 'r')
    if (xs != []):
      #plt.plot([xs[len(xs)-1], xs[0]], [ys[len(xs)-1], ys[0]], [zs[len(xs)-1], zs[0]], 'g')
      plt.plot([xs[len(xs)-1], xs[0]], [ys[len(xs)-1], ys[0]], [zs[len(xs)-1], zs[0]], 'r')
  plt.show()
