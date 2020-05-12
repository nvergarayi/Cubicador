# -*- coding: utf-8 -*-
from geometry.controller.geometry_2d.point_2d import Point2D
from geometry.controller.geometry_3d.point_3d import Point3d
from geometry.controller.geometry_2d.segment_2d import Segment2D
from geometry.controller.geometry_3d.segment_3d import Segment3d
from geometry.controller.geometry_3d.solid_3d import Solid3d
from geometry.controller.geometry_3d.triangle_3d import Triangle3d
from geometry.controller.geometry_3d.polygon_3d import Polygon3d
from geometry.controller.geometry_3d.face_3d import Face3d
import matplotlib.pyplot as plt
import math

class Cube3d(object):
    
    def __init__(self, xmin, xmax, ymin, ymax, zmin, zmax, data=None):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.zmin = zmin
        self.zmax = zmax

    '''
    Metodo que extrae los cubos del archivo CSV y los convierte en objetos Cube3d.
    '''
    @staticmethod
    def getCubes3DFromCSV(path, centerx, centery, centerz, lenx, leny, lenz, data=None):
        infile = open(path, 'r')
        headers = infile.readline().replace('\n', '').replace('\r', '').replace(' ', '').split(',')
        headers = dict([(headers[i], i) for i in range(len(headers))])
        
        result = []
        for line in infile:
            line = line.replace('\n', '').replace('\r', '').replace(' ', '').split(',')
            cx = float(line[headers[centerx]]); cy = float(line[headers[centery]]); cz = float(line[headers[centerz]])
            lx = float(line[headers[lenx]]); ly = float(line[headers[leny]]); lz = float(line[headers[lenz]])
            result.append(Cube3d(cx-lx/2, cx+lx/2, cy-ly/2, cy+ly/2, cz-lz/2, cz+lz/2, None if not(data) else line[headers[data]]))
        return result

    '''
    Metodo que extrae los cubos del archivo CSV y los convierte en objetos Cube3d.
    '''
    @staticmethod
    def getCubes3DFromCSV_2(path, centerx, centery, centerz, lenx, leny, lenz, data=None):
        infile = open(path, 'r')
        headers = infile.readline().replace('\n', '').replace('\r', '').replace(' ', '').split(',')
        headers = dict([(headers[i], i) for i in range(len(headers))])
        
        result = []
        for line in infile:
            line = line.replace('\n', '').replace('\r', '').replace(' ', '').split(',')
            cx = float(line[headers[centerx]]); cy = float(line[headers[centery]]); cz = float(line[headers[centerz]])
            lx = float(line[headers[lenx]]); ly = float(line[headers[leny]]); lz = float(line[headers[lenz]])
            result.append([cx-lx/2, cx+lx/2, cy-ly/2, cy+ly/2, cz-lz/2, cz+lz/2])
        return result

    '''
    Funcion que calcula el volumen de un cubo.
    '''
    def calculateVolumeCube(self):
        return (self.xmax-self.xmin)*(self.ymax-self.ymin)*(self.zmax-self.zmin)

    '''
    Funcion que entrega los puntos a partir de un cubo.
    '''
    def getPointsCube(self):
        
        point_xl_yl_zl = Point3d(self.xmin,self.ymin,self.zmin)
        point_xh_yl_zl = Point3d(self.xmax,self.ymin,self.zmin)
        point_xl_yh_zl = Point3d(self.xmin,self.ymax,self.zmin)
        point_xh_yh_zl = Point3d(self.xmax,self.ymax,self.zmin)
        point_xl_yl_zh = Point3d(self.xmin,self.ymin,self.zmax)
        point_xh_yl_zh = Point3d(self.xmax,self.ymin,self.zmax)
        point_xl_yh_zh = Point3d(self.xmin,self.ymax,self.zmax)
        point_xh_yh_zh = Point3d(self.xmax,self.ymax,self.zmax)
        '''
        point_xl_yl_zl = Point3d(self.xmin,self.zmin,self.ymin)
        point_xh_yl_zl = Point3d(self.xmax,self.zmin,self.ymin)
        point_xl_yh_zl = Point3d(self.xmin,self.zmax,self.ymin)
        point_xh_yh_zl = Point3d(self.xmax,self.zmax,self.ymin)
        point_xl_yl_zh = Point3d(self.xmin,self.zmin,self.ymax)
        point_xh_yl_zh = Point3d(self.xmax,self.zmin,self.ymax)
        point_xl_yh_zh = Point3d(self.xmin,self.zmax,self.ymax)
        point_xh_yh_zh = Point3d(self.xmax,self.zmax,self.ymax)
        '''
        list_points_cube = [point_xl_yl_zl,point_xh_yl_zl,point_xh_yl_zh,point_xl_yl_zh,point_xl_yh_zl,point_xh_yh_zl,point_xh_yh_zh,point_xl_yh_zh]   
        #list_points_cube = [point_xl_yl_zl,point_xh_yl_zl,point_xl_yh_zl,point_xh_yh_zl,point_xl_yl_zh,point_xh_yl_zh,point_xl_yh_zh,point_xh_yh_zh]
        #list_points_cube = [point_xl_yl_zl,point_xh_yl_zl,point_xh_yh_zl,point_xl_yh_zl,point_xl_yl_zh,point_xh_yl_zh,point_xh_yh_zh,point_xl_yh_zh]
        return list_points_cube
    
    '''
    Funcion que elimina los triangulos que coincidan con una de las caras al efectuar la
    primera etapa de la triangulacion de la interseccion del solido con los cubos.
    '''
    def checkTriangles(self,triangles_for_check):
       
        list_to_eliminate = [];

        '''
        Evaluar cada triangulo y comparar si su superficie coincide con alguna cara
        del cubo.        
        '''
        for index in range(0,len(triangles_for_check)):
            if (triangles_for_check[index].p0.x == self.xmin and triangles_for_check[index].p1.x == self.xmin and triangles_for_check[index].p2.x == self.xmin):
                list_to_eliminate.append(index)
                continue
            if (triangles_for_check[index].p0.x == self.xmax and triangles_for_check[index].p1.x == self.xmax and triangles_for_check[index].p2.x == self.xmax):
                list_to_eliminate.append(index)
                continue
            if (triangles_for_check[index].p0.y == self.ymin and triangles_for_check[index].p1.y == self.ymin and triangles_for_check[index].p2.y == self.ymin):
                list_to_eliminate.append(index)
                continue
            if (triangles_for_check[index].p0.y == self.ymax and triangles_for_check[index].p1.y == self.ymax and triangles_for_check[index].p2.y == self.ymax):
                list_to_eliminate.append(index)
                continue
            if (triangles_for_check[index].p0.z == self.zmin and triangles_for_check[index].p1.z == self.zmin and triangles_for_check[index].p2.z == self.zmin):
                list_to_eliminate.append(index)
                continue
            if (triangles_for_check[index].p0.z == self.zmax and triangles_for_check[index].p1.z == self.zmax and triangles_for_check[index].p2.z == self.zmax):
                list_to_eliminate.append(index)

        list_to_eliminate.reverse()

        for index in list_to_eliminate:
            del triangles_for_check[index]

        return triangles_for_check        

    '''
    Funcion que cierra internamente los cubos.
    '''
    def addInternalFaces(self,solid,centroid_father_solid,intersections_cube,collision_triangles):
        '''
        Obtener los poligonos de interseccion para cerrar las caras del bloque
        de interseccion.
        '''
        new_polygons = []
        
        new_polygon1 = []; new_polygon2 = [];
        for point in intersections_cube[0]:
            new_polygon1.append([point.x,point.y,point.z])
        new_polygon1.sort(key=lambda x:x[2])
            
        for point in new_polygon1:
            new_polygon2.append(Point3d(point[0],point[1],point[2]))
        new_polygons.append(new_polygon2)

        new_polygon1 = []; new_polygon2 = [];
        for point in intersections_cube[1]:
            new_polygon1.append([point.x,point.y,point.z])
        new_polygon1.sort(key=lambda x:x[2])
            
        for point in new_polygon1:
            new_polygon2.append(Point3d(point[0],point[1],point[2]))
        new_polygons.append(new_polygon2)

        new_polygon1 = []; new_polygon2 = [];
        for point in intersections_cube[2]:
            new_polygon1.append([point.x,point.y,point.z])
        new_polygon1.sort(key=lambda x:x[2])

        for point in new_polygon1:
            new_polygon2.append(Point3d(point[0],point[1],point[2]))
        new_polygons.append(new_polygon2)

        new_polygon1 = []; new_polygon2 = [];
        for point in intersections_cube[3]:
            new_polygon1.append([point.x,point.y,point.z])
        new_polygon1.sort(key=lambda x:x[2])
            
        for point in new_polygon1:
            new_polygon2.append(Point3d(point[0],point[1],point[2]))
        new_polygons.append(new_polygon2)

        new_polygon1 = []; new_polygon2 = [];
        for point in intersections_cube[4]:
            new_polygon1.append([point.x,point.y,point.z])
        new_polygon1.sort(key=lambda x:x[1])
            
        for point in new_polygon1:
            new_polygon2.append(Point3d(point[0],point[1],point[2]))
        new_polygons.append(new_polygon2)

        new_polygon1 = []; new_polygon2 = [];
        for point in intersections_cube[5]:
            new_polygon1.append([point.x,point.y,point.z])
        new_polygon1.sort(key=lambda x:x[1])
            
        for point in new_polygon1:
            new_polygon2.append(Point3d(point[0],point[1],point[2]))
        new_polygons.append(new_polygon2)

        #print ('nuevos poligonos = ',new_polygons)

        point_xl_yl_zl = Point3d(self.xmin,self.ymin,self.zmin)
        point_xh_yl_zl = Point3d(self.xmax,self.ymin,self.zmin)
        point_xl_yh_zl = Point3d(self.xmin,self.ymax,self.zmin)
        point_xh_yh_zl = Point3d(self.xmax,self.ymax,self.zmin)
        point_xl_yl_zh = Point3d(self.xmin,self.ymin,self.zmax)
        point_xh_yl_zh = Point3d(self.xmax,self.ymin,self.zmax)
        point_xl_yh_zh = Point3d(self.xmin,self.ymax,self.zmax)
        point_xh_yh_zh = Point3d(self.xmax,self.ymax,self.zmax)        

        #face_0 = Face3d(point_xl_yl_zh,point_xl_yl_zl,point_xl_yh_zl,point_xl_yh_zh)
        face_0 = Polygon3d([point_xl_yl_zh,point_xl_yl_zl,point_xl_yh_zl,point_xl_yh_zh])
        face_1 = Polygon3d([point_xh_yl_zl,point_xh_yl_zh,point_xh_yh_zh,point_xh_yh_zl])
        face_2 = Polygon3d([point_xl_yl_zl,point_xl_yl_zh,point_xh_yl_zh,point_xh_yl_zl])
        face_3 = Polygon3d([point_xl_yh_zh,point_xl_yh_zl,point_xh_yh_zl,point_xh_yh_zh])
        face_4 = Polygon3d([point_xl_yh_zl,point_xl_yl_zl,point_xh_yl_zl,point_xh_yh_zl])
        face_5 = Polygon3d([point_xl_yl_zh,point_xl_yh_zh,point_xh_yh_zh,point_xh_yl_zh])
        faces = [face_0,face_1,face_2,face_3,face_4,face_5]
        
        collision_triangles_solid = Solid3d([])
        intersection_triangles = Solid3d([])

        for collision_triangle in collision_triangles:
            collision_triangles_solid.triangles.append(solid.triangles[collision_triangle[6]])

        for num_face in range(0,6):

            #print ('in solid or not polygon [',ind,'] :')
            new_face = Polygon3d([])

            for point in faces[num_face].points:
                #print ('state_point = ',collision_triangles_solid.isPointInSolid(centroid_father_solid,point))
                if (collision_triangles_solid.isPointInSolid(centroid_father_solid,point) == True):
                    new_face.points.append(point)
            
            new_face.points.extend(new_polygons[num_face])
            new_face_oriented = Polygon3d([])

            if (len(new_face.points) < 3): continue

            new_face_oriented = new_face.orientPolygon(self,num_face)
            #chart6(new_face_oriented,solid.triangles)

            if (num_face in [0,1]):
                intersection_triangles.triangles.extend(new_face_oriented.get_intersection_triangles_with_case(2))
            elif (num_face in [4,5]):
                intersection_triangles.triangles.extend(new_face_oriented.get_intersection_triangles_with_case(1))
            else:
                intersection_triangles.triangles.extend(new_face_oriented.get_intersection_triangles_with_case(3))
            
        #print ('nueva cara = ',new_faces)
        #new_polygons.append(new_polygon)
        #bounding_boxes.sort(key=lambda x:x[depth*2+1])

        return intersection_triangles

        #for face_cube_polygon in face_cube_polygons:
        #    if (len(face_cube_polygon.points) >= 3):
        #        print ('cara  = ')
        #        intersect_triangles.extend(face_cube_polygon.get_intersection_triangles())    

        '''

        new_polygons2 = []

        print ('newpol0 = ',new_polygons[0])
        print ('newpol1 = ',new_polygons[1])
        print ('newpol2 = ',new_polygons[2])
        print ('newpol3 = ',new_polygons[3])
        print ('newpol4 = ',new_polygons[4])
        print ('newpol5 = ',new_polygons[5])

        # Cara 0.
        if (new_polygons[0] != []):
            new_polygons2.append(Polygon3d(new_polygons[0] + [point_xl_yl_zh,point_xl_yl_zl]))
            new_polygons2.append(Polygon3d([point_xl_yh_zl,point_xl_yh_zh] + new_polygons[0][::-1]))
        else:
            new_polygons2.append(Polygon3d([point_xl_yh_zl,point_xl_yh_zh,point_xl_yl_zh,point_xl_yl_zl]))
            new_polygons2.append(Polygon3d([point_xl_yh_zl,point_xl_yh_zh,point_xl_yl_zh,point_xl_yl_zl]))

        # Cara 1.
        if (new_polygons[1] != []):
            new_polygons2.append(Polygon3d([point_xh_yl_zl,point_xh_yl_zh] + new_polygons[1][::-1]))
            new_polygons2.append(Polygon3d(new_polygons[1] + [point_xh_yh_zh,point_xh_yh_zl]))
        else:
            new_polygons2.append(Polygon3d([point_xh_yl_zl,point_xh_yl_zh,point_xh_yh_zh,point_xh_yh_zl]))
            new_polygons2.append(Polygon3d([point_xh_yl_zl,point_xh_yl_zh,point_xh_yh_zh,point_xh_yh_zl]))

        # Cara 2.
        if (new_polygons[2] != []):
            new_polygons2.append(Polygon3d([point_xl_yl_zl,point_xl_yl_zh] + new_polygons[2][::-1]))
            new_polygons2.append(Polygon3d(new_polygons[2] + [point_xh_yl_zh,point_xh_yl_zl]))
        else:
            new_polygons2.append(Polygon3d([point_xl_yl_zl,point_xl_yl_zh,point_xh_yl_zh,point_xh_yl_zl]))
            new_polygons2.append(Polygon3d([point_xl_yl_zl,point_xl_yl_zh,point_xh_yl_zh,point_xh_yl_zl]))

        # Cara 3.
        if (new_polygons[3] != []):
            new_polygons2.append(Polygon3d(new_polygons[3] + [point_xl_yh_zh,point_xl_yh_zl]))
            new_polygons2.append(Polygon3d([point_xh_yh_zl,point_xh_yh_zh] + new_polygons[3][::-1]))
        else:
            new_polygons2.append(Polygon3d([point_xh_yh_zl,point_xh_yh_zh,point_xl_yh_zh,point_xl_yh_zl]))
            new_polygons2.append(Polygon3d([point_xh_yh_zl,point_xh_yh_zh,point_xl_yh_zh,point_xl_yh_zl]))

        # Cara 4.
        if (new_polygons[4] != []):
            new_polygons2.append(Polygon3d([point_xl_yh_zl,point_xl_yl_zl] + new_polygons[4]))
            new_polygons2.append(Polygon3d(new_polygons[4][::-1] + [point_xh_yl_zl,point_xh_yh_zl]))
        else:
            new_polygons2.append(Polygon3d([point_xh_yl_zl,point_xh_yh_zl,point_xl_yh_zl,point_xl_yl_zl]))
            new_polygons2.append(Polygon3d([point_xh_yl_zl,point_xh_yh_zl,point_xl_yh_zl,point_xl_yl_zl]))
        
        # Cara 5.
        if (new_polygons[5] != []):
            new_polygons2.append(Polygon3d([point_xl_yl_zh,point_xl_yh_zh] + new_polygons[5]))
            new_polygons2.append(Polygon3d([point_xh_yh_zh,point_xh_yl_zh] + new_polygons[5][::-1]))
        else:
            new_polygons2.append(Polygon3d([point_xl_yl_zh,point_xl_yh_zh,point_xh_yh_zh,point_xh_yl_zh]))
            new_polygons2.append(Polygon3d([point_xl_yl_zh,point_xl_yh_zh,point_xh_yh_zh,point_xh_yl_zh]))

        collision_triangles_solid = Solid3d([])
        for collision_triangle in collision_triangles:
            collision_triangles_solid.triangles.append(solid.triangles[collision_triangle[6]])

        for ind in range(0,12):
            print ('in solid or not polygon [',ind,'] :')
            for point in new_polygons2[ind].points:
                print ('state_point = ',collision_triangles_solid.isPointInSolid(centroid_father_solid,point))
        '''
        #return new_polygons2

    '''
    Funcion que devuelve los triangulos cuyos bounding box colisionan con el cubo.    
    '''
    def obtain_collision_candidates(self,bounding_boxes,max_b_boxes):
      #for i in range(0,len(bounding_boxes)):
      #  print('bounding_box1[',i,'] =',bounding_boxes[i])
      flag,bounding_boxes = search_collisions(self.xmin,self.xmax,bounding_boxes,bounding_boxes[0][0],max_b_boxes,0)
      candidates_polygon = bounding_boxes
      #print 'bbbb1 =',bounding_boxes
      if (flag == False):
        return [],candidates_polygon
      max_b_boxes = 0
      for bb in bounding_boxes:
        max_b_boxes = max(bb[3],max_b_boxes)
      bounding_boxes.sort(key=lambda x:x[2])
      min_b_boxes = bounding_boxes[0][2]
      #for i in range(0,len(bounding_boxes)):
      #  print('bounding_box2[',i,'] =',bounding_boxes[i])
      flag,bounding_boxes = search_collisions(self.ymin,self.ymax,bounding_boxes,min_b_boxes,max_b_boxes,1)
      #print 'bbbb2 =',bounding_boxes
      if (flag == False):
        return [],candidates_polygon
      max_b_boxes = 0
      for bb in bounding_boxes:
        max_b_boxes = max(bb[5],max_b_boxes)
      bounding_boxes.sort(key=lambda x:x[4])
      min_b_boxes = bounding_boxes[0][4]
      flag,bounding_boxes = search_collisions(self.zmin,self.zmax,bounding_boxes,min_b_boxes,max_b_boxes,2)
      #for i in range(0,len(bounding_boxes)):
      #  print('bounding_box3[',i,'] =',bounding_boxes[i])
      #print ('flag =',flag)
      if (flag == False):
        return [],candidates_polygon
      else:
        return bounding_boxes,candidates_polygon

    '''
    Funcion que determina si un triangulo esta dentro del cubo o no.
    '''
    def inner_triangle(self,bounding_box):
      if (checkrange(bounding_box[0],bounding_box[1],self.xmin,self.xmax) == True and \
       checkrange(bounding_box[2],bounding_box[3],self.ymin,self.ymax) == True and \
       checkrange(bounding_box[4],bounding_box[5],self.zmin,self.zmax) == True):
        return bounding_box[6]
      else:
        return -1

    '''
    Funcion para obtener el centro del cubo.
    '''
    def center_point(self):
      return Point3d((self.xmin+self.xmax)/2,(self.ymin+self.ymax)/2,(self.zmin+self.zmax)/2)

    '''
    Funcion para obtener las coordenadas de las aristas del cubo.
    '''
    def get_edges(self):
      edges = [Segment2D(Point2D(self.xmin,self.ymin),Point2D(self.xmax,self.ymin)),\
               Segment2D(Point2D(self.xmin,self.ymax),Point2D(self.xmax,self.ymax)),\
               Segment2D(Point2D(self.xmin,self.ymin),Point2D(self.xmin,self.ymax)),\
               Segment2D(Point2D(self.xmax,self.ymin),Point2D(self.xmax,self.ymax)),\
               Segment2D(Point2D(self.ymin,self.zmin),Point2D(self.ymax,self.zmin)),\
               Segment2D(Point2D(self.ymin,self.zmax),Point2D(self.ymax,self.zmax)),\
               Segment2D(Point2D(self.ymin,self.zmin),Point2D(self.ymin,self.zmax)),\
               Segment2D(Point2D(self.ymax,self.zmin),Point2D(self.ymax,self.zmax)),\
               Segment2D(Point2D(self.xmin,self.zmin),Point2D(self.xmax,self.zmin)),\
               Segment2D(Point2D(self.xmin,self.zmax),Point2D(self.xmax,self.zmax)),\
               Segment2D(Point2D(self.xmin,self.zmin),Point2D(self.xmin,self.zmax)),\
               Segment2D(Point2D(self.xmax,self.zmin),Point2D(self.xmax,self.zmax))]
      new_edges = [[edges[0],edges[2],edges[4],edges[6],edges[8],edges[10]],\
                   [edges[0],edges[3],edges[4],edges[6],edges[8],edges[11]],\
                   [edges[1],edges[2],edges[4],edges[7],edges[8],edges[10]],\
                   [edges[1],edges[3],edges[4],edges[7],edges[8],edges[11]],\
                   [edges[0],edges[2],edges[5],edges[6],edges[9],edges[10]],\
                   [edges[0],edges[3],edges[5],edges[6],edges[9],edges[11]],\
                   [edges[1],edges[2],edges[5],edges[7],edges[9],edges[10]],\
                   [edges[1],edges[3],edges[5],edges[7],edges[9],edges[11]]]
      return new_edges

    '''
    Funcion para triangular un cubo entero.
    '''
    def get_triangulated_cube(self):
      solid = Solid3d([])
      solid.triangles.append(Triangle3d(Point3d(self.xmin,self.ymin,self.zmin),\
       Point3d(self.xmin,self.ymin,self.zmax),Point3d(self.xmax,self.ymin,self.zmax)))
      solid.triangles.append(Triangle3d(Point3d(self.xmin,self.ymin,self.zmin),\
       Point3d(self.xmax,self.ymin,self.zmax),Point3d(self.xmax,self.ymin,self.zmin)))
      solid.triangles.append(Triangle3d(Point3d(self.xmax,self.ymin,self.zmin),\
       Point3d(self.xmax,self.ymin,self.zmax),Point3d(self.xmax,self.ymax,self.zmax)))
      solid.triangles.append(Triangle3d(Point3d(self.xmax,self.ymin,self.zmin),\
       Point3d(self.xmax,self.ymax,self.zmax),Point3d(self.xmax,self.ymax,self.zmin)))   
      solid.triangles.append(Triangle3d(Point3d(self.xmax,self.ymax,self.zmax),\
       Point3d(self.xmin,self.ymax,self.zmax),Point3d(self.xmin,self.ymax,self.zmin)))
      solid.triangles.append(Triangle3d(Point3d(self.xmax,self.ymax,self.zmax),\
       Point3d(self.xmin,self.ymax,self.zmin),Point3d(self.xmax,self.ymax,self.zmin)))
      solid.triangles.append(Triangle3d(Point3d(self.xmin,self.ymax,self.zmax),\
       Point3d(self.xmin,self.ymin,self.zmax),Point3d(self.xmin,self.ymin,self.zmin)))
      solid.triangles.append(Triangle3d(Point3d(self.xmin,self.ymax,self.zmax),\
       Point3d(self.xmin,self.ymin,self.zmin),Point3d(self.xmin,self.ymax,self.zmin)))
      solid.triangles.append(Triangle3d(Point3d(self.xmin,self.ymin,self.zmax),\
       Point3d(self.xmin,self.ymax,self.zmax),Point3d(self.xmax,self.ymax,self.zmax)))
      solid.triangles.append(Triangle3d(Point3d(self.xmin,self.ymin,self.zmax),\
       Point3d(self.xmax,self.ymax,self.zmax),Point3d(self.xmax,self.ymin,self.zmax)))
      solid.triangles.append(Triangle3d(Point3d(self.xmin,self.ymax,self.zmin),\
       Point3d(self.xmin,self.ymin,self.zmin),Point3d(self.xmax,self.ymin,self.zmin)))
      solid.triangles.append(Triangle3d(Point3d(self.xmin,self.ymax,self.zmin),\
       Point3d(self.xmax,self.ymin,self.zmin),Point3d(self.xmax,self.ymax,self.zmin)))
      return solid

    '''
    Funcion que genera el diccionario con la tabla de clasificacion de los cubos de acuerdo
    a los 14 casos en que opera Marching Cubes. 
    '''
    @staticmethod
    def generateMarchingCubesCases():

        casesMarchingCubes = {}

        '''
        Indicar a que caso del algoritmo Marching Cubes corresponde el cubo al cual se le examino las posiciones de los vertices.
        '''
        casesMarchingCubes[(0,0,0,0,0,0,0,0)] = 0
        casesMarchingCubes[(0,0,0,0,0,0,0,1)] = 1
        casesMarchingCubes[(0,0,0,0,0,0,1,0)] = 1
        casesMarchingCubes[(0,0,0,0,0,0,1,1)] = 2
        casesMarchingCubes[(0,0,0,0,0,1,0,0)] = 1
        casesMarchingCubes[(0,0,0,0,0,1,0,1)] = 3
        casesMarchingCubes[(0,0,0,0,0,1,1,0)] = 2
        casesMarchingCubes[(0,0,0,0,0,1,1,1)] = 5
        casesMarchingCubes[(0,0,0,0,1,0,0,0)] = 1
        casesMarchingCubes[(0,0,0,0,1,0,0,1)] = 2
        casesMarchingCubes[(0,0,0,0,1,0,1,0)] = 3
        casesMarchingCubes[(0,0,0,0,1,0,1,1)] = 5
        casesMarchingCubes[(0,0,0,0,1,1,0,0)] = 2
        casesMarchingCubes[(0,0,0,0,1,1,0,1)] = 5
        casesMarchingCubes[(0,0,0,0,1,1,1,0)] = 5
        casesMarchingCubes[(0,0,0,0,1,1,1,1)] = 8
        casesMarchingCubes[(0,0,0,1,0,0,0,0)] = 1
        casesMarchingCubes[(0,0,0,1,0,0,0,1)] = 2
        casesMarchingCubes[(0,0,0,1,0,0,1,0)] = 3
        casesMarchingCubes[(0,0,0,1,0,0,1,1)] = 5
        casesMarchingCubes[(0,0,0,1,0,1,0,0)] = 4
        casesMarchingCubes[(0,0,0,1,0,1,0,1)] = 6
        casesMarchingCubes[(0,0,0,1,0,1,1,0)] = 6
        casesMarchingCubes[(0,0,0,1,0,1,1,1)] = 14
        casesMarchingCubes[(0,0,0,1,1,0,0,0)] = 3
        casesMarchingCubes[(0,0,0,1,1,0,0,1)] = 5
        casesMarchingCubes[(0,0,0,1,1,0,1,0)] = 7
        casesMarchingCubes[(0,0,0,1,1,0,1,1)] = 9
        casesMarchingCubes[(0,0,0,1,1,1,0,0)] = 6
        casesMarchingCubes[(0,0,0,1,1,1,0,1)] = 11
        casesMarchingCubes[(0,0,0,1,1,1,1,0)] = 12
        casesMarchingCubes[(0,0,0,1,1,1,1,1)] = 5
        casesMarchingCubes[(0,0,1,0,0,0,0,0)] = 1
        casesMarchingCubes[(0,0,1,0,0,0,0,1)] = 3
        casesMarchingCubes[(0,0,1,0,0,0,1,0)] = 2
        casesMarchingCubes[(0,0,1,0,0,0,1,1)] = 5
        casesMarchingCubes[(0,0,1,0,0,1,0,0)] = 3
        casesMarchingCubes[(0,0,1,0,0,1,0,1)] = 7
        casesMarchingCubes[(0,0,1,0,0,1,1,0)] = 5
        casesMarchingCubes[(0,0,1,0,0,1,1,1)] = 9
        casesMarchingCubes[(0,0,1,0,1,0,0,0)] = 4
        casesMarchingCubes[(0,0,1,0,1,0,0,1)] = 6
        casesMarchingCubes[(0,0,1,0,1,0,1,0)] = 6
        casesMarchingCubes[(0,0,1,0,1,0,1,1)] = 11
        casesMarchingCubes[(0,0,1,0,1,1,0,0)] = 6
        casesMarchingCubes[(0,0,1,0,1,1,0,1)] = 12
        casesMarchingCubes[(0,0,1,0,1,1,1,0)] = 14
        casesMarchingCubes[(0,0,1,0,1,1,1,1)] = 5
        casesMarchingCubes[(0,0,1,1,0,0,0,0)] = 2
        casesMarchingCubes[(0,0,1,1,0,0,0,1)] = 5
        casesMarchingCubes[(0,0,1,1,0,0,1,0)] = 5
        casesMarchingCubes[(0,0,1,1,0,0,1,1)] = 8
        casesMarchingCubes[(0,0,1,1,0,1,0,0)] = 6
        casesMarchingCubes[(0,0,1,1,0,1,0,1)] = 12
        casesMarchingCubes[(0,0,1,1,0,1,1,0)] = 11
        casesMarchingCubes[(0,0,1,1,0,1,1,1)] = 5
        casesMarchingCubes[(0,0,1,1,1,0,0,0)] = 6
        casesMarchingCubes[(0,0,1,1,1,0,0,1)] = 14
        casesMarchingCubes[(0,0,1,1,1,0,1,0)] = 12
        casesMarchingCubes[(0,0,1,1,1,0,1,1)] = 5
        casesMarchingCubes[(0,0,1,1,1,1,0,0)] = 10
        casesMarchingCubes[(0,0,1,1,1,1,0,1)] = 6
        casesMarchingCubes[(0,0,1,1,1,1,1,0)] = 6
        casesMarchingCubes[(0,0,1,1,1,1,1,1)] = 2
        casesMarchingCubes[(0,1,0,0,0,0,0,0)] = 1
        casesMarchingCubes[(0,1,0,0,0,0,0,1)] = 4
        casesMarchingCubes[(0,1,0,0,0,0,1,0)] = 3
        casesMarchingCubes[(0,1,0,0,0,0,1,1)] = 6
        casesMarchingCubes[(0,1,0,0,0,1,0,0)] = 2
        casesMarchingCubes[(0,1,0,0,0,1,0,1)] = 6
        casesMarchingCubes[(0,1,0,0,0,1,1,0)] = 5
        casesMarchingCubes[(0,1,0,0,0,1,1,1)] = 11
        casesMarchingCubes[(0,1,0,0,1,0,0,0)] = 3
        casesMarchingCubes[(0,1,0,0,1,0,0,1)] = 6
        casesMarchingCubes[(0,1,0,0,1,0,1,0)] = 7
        casesMarchingCubes[(0,1,0,0,1,0,1,1)] = 12
        casesMarchingCubes[(0,1,0,0,1,1,0,0)] = 5
        casesMarchingCubes[(0,1,0,0,1,1,0,1)] = 14
        casesMarchingCubes[(0,1,0,0,1,1,1,0)] = 9
        casesMarchingCubes[(0,1,0,0,1,1,1,1)] = 5
        casesMarchingCubes[(0,1,0,1,0,0,0,0)] = 3
        casesMarchingCubes[(0,1,0,1,0,0,0,1)] = 6
        casesMarchingCubes[(0,1,0,1,0,0,1,0)] = 7
        casesMarchingCubes[(0,1,0,1,0,0,1,1)] = 12
        casesMarchingCubes[(0,1,0,1,0,1,0,0)] = 6
        casesMarchingCubes[(0,1,0,1,0,1,0,1)] = 10
        casesMarchingCubes[(0,1,0,1,0,1,1,0)] = 12
        casesMarchingCubes[(0,1,0,1,0,1,1,1)] = 6
        casesMarchingCubes[(0,1,0,1,1,0,0,0)] = 7
        casesMarchingCubes[(0,1,0,1,1,0,0,1)] = 12
        casesMarchingCubes[(0,1,0,1,1,0,1,0)] = 13
        casesMarchingCubes[(0,1,0,1,1,0,1,1)] = 7
        casesMarchingCubes[(0,1,0,1,1,1,0,0)] = 12
        casesMarchingCubes[(0,1,0,1,1,1,0,1)] = 6
        casesMarchingCubes[(0,1,0,1,1,1,1,0)] = 7
        casesMarchingCubes[(0,1,0,1,1,1,1,1)] = 3
        casesMarchingCubes[(0,1,1,0,0,0,0,0)] = 2
        casesMarchingCubes[(0,1,1,0,0,0,0,1)] = 6
        casesMarchingCubes[(0,1,1,0,0,0,1,0)] = 5
        casesMarchingCubes[(0,1,1,0,0,0,1,1)] = 14
        casesMarchingCubes[(0,1,1,0,0,1,0,0)] = 5
        casesMarchingCubes[(0,1,1,0,0,1,0,1)] = 12
        casesMarchingCubes[(0,1,1,0,0,1,1,0)] = 8
        casesMarchingCubes[(0,1,1,0,0,1,1,1)] = 5
        casesMarchingCubes[(0,1,1,0,1,0,0,0)] = 6
        casesMarchingCubes[(0,1,1,0,1,0,0,1)] = 10
        casesMarchingCubes[(0,1,1,0,1,0,1,0)] = 12
        casesMarchingCubes[(0,1,1,0,1,0,1,1)] = 6
        casesMarchingCubes[(0,1,1,0,1,1,0,0)] = 11
        casesMarchingCubes[(0,1,1,0,1,1,0,1)] = 6
        casesMarchingCubes[(0,1,1,0,1,1,1,0)] = 5
        casesMarchingCubes[(0,1,1,0,1,1,1,1)] = 2
        casesMarchingCubes[(0,1,1,1,0,0,0,0)] = 5
        casesMarchingCubes[(0,1,1,1,0,0,0,1)] = 11
        casesMarchingCubes[(0,1,1,1,0,0,1,0)] = 9
        casesMarchingCubes[(0,1,1,1,0,0,1,1)] = 5
        casesMarchingCubes[(0,1,1,1,0,1,0,0)] = 14
        casesMarchingCubes[(0,1,1,1,0,1,0,1)] = 6
        casesMarchingCubes[(0,1,1,1,0,1,1,0)] = 5
        casesMarchingCubes[(0,1,1,1,0,1,1,1)] = 2
        casesMarchingCubes[(0,1,1,1,1,0,0,0)] = 12
        casesMarchingCubes[(0,1,1,1,1,0,0,1)] = 6
        casesMarchingCubes[(0,1,1,1,1,0,1,0)] = 7
        casesMarchingCubes[(0,1,1,1,1,0,1,1)] = 3
        casesMarchingCubes[(0,1,1,1,1,1,0,0)] = 6
        casesMarchingCubes[(0,1,1,1,1,1,0,1)] = 4
        casesMarchingCubes[(0,1,1,1,1,1,1,0)] = 3
        casesMarchingCubes[(0,1,1,1,1,1,1,1)] = 1
        casesMarchingCubes[(1,0,0,0,0,0,0,0)] = 1
        casesMarchingCubes[(1,0,0,0,0,0,0,1)] = 3
        casesMarchingCubes[(1,0,0,0,0,0,1,0)] = 4
        casesMarchingCubes[(1,0,0,0,0,0,1,1)] = 6
        casesMarchingCubes[(1,0,0,0,0,1,0,0)] = 3
        casesMarchingCubes[(1,0,0,0,0,1,0,1)] = 7
        casesMarchingCubes[(1,0,0,0,0,1,1,0)] = 6
        casesMarchingCubes[(1,0,0,0,0,1,1,1)] = 12
        casesMarchingCubes[(1,0,0,0,1,0,0,0)] = 2
        casesMarchingCubes[(1,0,0,0,1,0,0,1)] = 5
        casesMarchingCubes[(1,0,0,0,1,0,1,0)] = 6
        casesMarchingCubes[(1,0,0,0,1,0,1,1)] = 14
        casesMarchingCubes[(1,0,0,0,1,1,0,0)] = 5
        casesMarchingCubes[(1,0,0,0,1,1,0,1)] = 9
        casesMarchingCubes[(1,0,0,0,1,1,1,0)] = 11
        casesMarchingCubes[(1,0,0,0,1,1,1,1)] = 5
        casesMarchingCubes[(1,0,0,1,0,0,0,0)] = 2
        casesMarchingCubes[(1,0,0,1,0,0,0,1)] = 5
        casesMarchingCubes[(1,0,0,1,0,0,1,0)] = 6
        casesMarchingCubes[(1,0,0,1,0,0,1,1)] = 11
        casesMarchingCubes[(1,0,0,1,0,1,0,0)] = 6
        casesMarchingCubes[(1,0,0,1,0,1,0,1)] = 12
        casesMarchingCubes[(1,0,0,1,0,1,1,0)] = 10
        casesMarchingCubes[(1,0,0,1,0,1,1,1)] = 6
        casesMarchingCubes[(1,0,0,1,1,0,0,0)] = 5
        casesMarchingCubes[(1,0,0,1,1,0,0,1)] = 8
        casesMarchingCubes[(1,0,0,1,1,0,1,0)] = 12
        casesMarchingCubes[(1,0,0,1,1,0,1,1)] = 5
        casesMarchingCubes[(1,0,0,1,1,1,0,0)] = 14
        casesMarchingCubes[(1,0,0,1,1,1,0,1)] = 5
        casesMarchingCubes[(1,0,0,1,1,1,1,0)] = 6
        casesMarchingCubes[(1,0,0,1,1,1,1,1)] = 2
        casesMarchingCubes[(1,0,1,0,0,0,0,0)] = 3
        casesMarchingCubes[(1,0,1,0,0,0,0,1)] = 7
        casesMarchingCubes[(1,0,1,0,0,0,1,0)] = 6
        casesMarchingCubes[(1,0,1,0,0,0,1,1)] = 12
        casesMarchingCubes[(1,0,1,0,0,1,0,0)] = 7
        casesMarchingCubes[(1,0,1,0,0,1,0,1)] = 13
        casesMarchingCubes[(1,0,1,0,0,1,1,0)] = 12
        casesMarchingCubes[(1,0,1,0,0,1,1,1)] = 7
        casesMarchingCubes[(1,0,1,0,1,0,0,0)] = 6
        casesMarchingCubes[(1,0,1,0,1,0,0,1)] = 12
        casesMarchingCubes[(1,0,1,0,1,0,1,0)] = 10
        casesMarchingCubes[(1,0,1,0,1,0,1,1)] = 6
        casesMarchingCubes[(1,0,1,0,1,1,0,0)] = 12
        casesMarchingCubes[(1,0,1,0,1,1,0,1)] = 7
        casesMarchingCubes[(1,0,1,0,1,1,1,0)] = 6
        casesMarchingCubes[(1,0,1,0,1,1,1,1)] = 3
        casesMarchingCubes[(1,0,1,1,0,0,0,0)] = 5
        casesMarchingCubes[(1,0,1,1,0,0,0,1)] = 9
        casesMarchingCubes[(1,0,1,1,0,0,1,0)] = 14
        casesMarchingCubes[(1,0,1,1,0,0,1,1)] = 5
        casesMarchingCubes[(1,0,1,1,0,1,0,0)] = 12
        casesMarchingCubes[(1,0,1,1,0,1,0,1)] = 7
        casesMarchingCubes[(1,0,1,1,0,1,1,0)] = 6
        casesMarchingCubes[(1,0,1,1,0,1,1,1)] = 3
        casesMarchingCubes[(1,0,1,1,1,0,0,0)] = 11
        casesMarchingCubes[(1,0,1,1,1,0,0,1)] = 5
        casesMarchingCubes[(1,0,1,1,1,0,1,0)] = 6
        casesMarchingCubes[(1,0,1,1,1,0,1,1)] = 2
        casesMarchingCubes[(1,0,1,1,1,1,0,0)] = 6
        casesMarchingCubes[(1,0,1,1,1,1,0,1)] = 3
        casesMarchingCubes[(1,0,1,1,1,1,1,0)] = 4
        casesMarchingCubes[(1,0,1,1,1,1,1,1)] = 1
        casesMarchingCubes[(1,1,0,0,0,0,0,0)] = 2
        casesMarchingCubes[(1,1,0,0,0,0,0,1)] = 6
        casesMarchingCubes[(1,1,0,0,0,0,1,0)] = 6
        casesMarchingCubes[(1,1,0,0,0,0,1,1)] = 10
        casesMarchingCubes[(1,1,0,0,0,1,0,0)] = 5
        casesMarchingCubes[(1,1,0,0,0,1,0,1)] = 12
        casesMarchingCubes[(1,1,0,0,0,1,1,0)] = 14
        casesMarchingCubes[(1,1,0,0,0,1,1,1)] = 6
        casesMarchingCubes[(1,1,0,0,1,0,0,0)] = 5
        casesMarchingCubes[(1,1,0,0,1,0,0,1)] = 11
        casesMarchingCubes[(1,1,0,0,1,0,1,0)] = 12
        casesMarchingCubes[(1,1,0,0,1,0,1,1)] = 6
        casesMarchingCubes[(1,1,0,0,1,1,0,0)] = 8
        casesMarchingCubes[(1,1,0,0,1,1,0,1)] = 5
        casesMarchingCubes[(1,1,0,0,1,1,1,0)] = 5
        casesMarchingCubes[(1,1,0,0,1,1,1,1)] = 2
        casesMarchingCubes[(1,1,0,1,0,0,0,0)] = 5
        casesMarchingCubes[(1,1,0,1,0,0,0,1)] = 14
        casesMarchingCubes[(1,1,0,1,0,0,1,0)] = 12
        casesMarchingCubes[(1,1,0,1,0,0,1,1)] = 6
        casesMarchingCubes[(1,1,0,1,0,1,0,0)] = 11
        casesMarchingCubes[(1,1,0,1,0,1,0,1)] = 6
        casesMarchingCubes[(1,1,0,1,0,1,1,0)] = 6
        casesMarchingCubes[(1,1,0,1,0,1,1,1)] = 4
        casesMarchingCubes[(1,1,0,1,1,0,0,0)] = 9
        casesMarchingCubes[(1,1,0,1,1,0,0,1)] = 5
        casesMarchingCubes[(1,1,0,1,1,0,1,0)] = 7
        casesMarchingCubes[(1,1,0,1,1,0,1,1)] = 3
        casesMarchingCubes[(1,1,0,1,1,1,0,0)] = 5
        casesMarchingCubes[(1,1,0,1,1,1,0,1)] = 2
        casesMarchingCubes[(1,1,0,1,1,1,1,0)] = 3
        casesMarchingCubes[(1,1,0,1,1,1,1,1)] = 1
        casesMarchingCubes[(1,1,1,0,0,0,0,0)] = 5
        casesMarchingCubes[(1,1,1,0,0,0,0,1)] = 12
        casesMarchingCubes[(1,1,1,0,0,0,1,0)] = 11
        casesMarchingCubes[(1,1,1,0,0,0,1,1)] = 6
        casesMarchingCubes[(1,1,1,0,0,1,0,0)] = 9
        casesMarchingCubes[(1,1,1,0,0,1,0,1)] = 7
        casesMarchingCubes[(1,1,1,0,0,1,1,0)] = 5
        casesMarchingCubes[(1,1,1,0,0,1,1,1)] = 3
        casesMarchingCubes[(1,1,1,0,1,0,0,0)] = 14
        casesMarchingCubes[(1,1,1,0,1,0,0,1)] = 6
        casesMarchingCubes[(1,1,1,0,1,0,1,0)] = 6
        casesMarchingCubes[(1,1,1,0,1,0,1,1)] = 4
        casesMarchingCubes[(1,1,1,0,1,1,0,0)] = 5
        casesMarchingCubes[(1,1,1,0,1,1,0,1)] = 3
        casesMarchingCubes[(1,1,1,0,1,1,1,0)] = 2
        casesMarchingCubes[(1,1,1,0,1,1,1,1)] = 1
        casesMarchingCubes[(1,1,1,1,0,0,0,0)] = 8
        casesMarchingCubes[(1,1,1,1,0,0,0,1)] = 5
        casesMarchingCubes[(1,1,1,1,0,0,1,0)] = 5
        casesMarchingCubes[(1,1,1,1,0,0,1,1)] = 2
        casesMarchingCubes[(1,1,1,1,0,1,0,0)] = 5
        casesMarchingCubes[(1,1,1,1,0,1,0,1)] = 3
        casesMarchingCubes[(1,1,1,1,0,1,1,0)] = 2
        casesMarchingCubes[(1,1,1,1,0,1,1,1)] = 1
        casesMarchingCubes[(1,1,1,1,1,0,0,0)] = 5
        casesMarchingCubes[(1,1,1,1,1,0,0,1)] = 2
        casesMarchingCubes[(1,1,1,1,1,0,1,0)] = 3
        casesMarchingCubes[(1,1,1,1,1,0,1,1)] = 1
        casesMarchingCubes[(1,1,1,1,1,1,0,0)] = 2
        casesMarchingCubes[(1,1,1,1,1,1,0,1)] = 1
        casesMarchingCubes[(1,1,1,1,1,1,1,0)] = 1
        casesMarchingCubes[(1,1,1,1,1,1,1,1)] = 0

    '''
    Funcion que genera el diccionario con el detalle de los lados que se deben intersectar para cada cubo,
    de acuerdo a los 14 casos en que opera Marching Cubes. 
    '''
    @staticmethod
    def generateMarchingCubesIntersections():

        intersects_for_cases = {}

        '''
        Indicar que lados se deben intersectar del cubo al cual se le examino las posiciones de los vertices.
        '''
        intersects_for_cases[(0,0,0,0,0,0,0,0)] = [[]]
        intersects_for_cases[(0,0,0,0,0,0,0,1)] = [[[6,7,10],[6,19,7],[7,19,10],[10,19,6]]]
        intersects_for_cases[(0,0,0,0,0,0,1,0)] = [[[5,6,11],[5,18,6],[6,18,11],[11,18,5]]]
        intersects_for_cases[(0,0,0,0,0,0,1,1)] = [[[5,7,10],[5,10,11],[5,19,7],[18,19,5],[11,18,5],[7,19,10],[10,18,11],[18,10,19]]]
        intersects_for_cases[(0,0,0,0,0,1,0,0)] = [[[4,5,9],[4,17,5],[5,17,9],[9,17,4]]]
        intersects_for_cases[(0,0,0,0,0,1,0,1)] = [[[6,7,10],[6,19,7],[7,19,10],[10,19,6]],[[9,4,5],[9,17,4],[4,17,5],[5,17,9]]]
        intersects_for_cases[(0,0,0,0,0,1,1,0)] = [[[11,9,4],[11,4,6],[11,17,9],[18,17,11],[6,18,11],[9,17,4],[4,18,6],[18,4,17]]]
        intersects_for_cases[(0,0,0,0,0,1,1,1)] = [[[9,4,7],[9,7,10],[9,10,11],[9,17,4],[11,17,9],[17,11,18],[10,19,11],[11,19,18],[10,7,19],[4,19,7],[19,4,18],[18,4,17]]]
        intersects_for_cases[(0,0,0,0,1,0,0,0)] = [[[7,4,8],[7,16,4],[4,16,8],[8,16,7]]]
        intersects_for_cases[(0,0,0,0,1,0,0,1)] = [[[6,4,8],[6,8,10],[6,16,4],[19,16,6],[10,19,6],[4,16,8],[8,19,10],[19,8,16]]]
        intersects_for_cases[(0,0,0,0,1,0,1,0)] = [[[7,4,8],[7,16,4],[4,16,8],[8,16,7]],[[11,5,6],[11,18,5],[5,18,6],[6,18,11]]]
        intersects_for_cases[(0,0,0,0,1,0,1,1)] = [[[11,5,4],[11,4,8],[11,8,10],[11,18,5],[10,18,11],[18,10,19],[8,16,10],[10,16,19],[8,4,16],[5,16,4],[16,5,19],[19,5,18]]]
        intersects_for_cases[(0,0,0,0,1,1,0,0)] = [[[7,5,9],[7,9,8],[7,17,5],[16,17,7],[8,16,7],[5,17,9],[9,16,8],[16,9,17]]]
        intersects_for_cases[(0,0,0,0,1,1,0,1)] = [[[10,6,5],[10,5,9],[10,9,8],[10,19,6],[8,19,10],[19,8,16],[9,17,8],[8,17,16],[9,5,17],[6,17,5],[17,6,16],[16,6,19]]]
        intersects_for_cases[(0,0,0,0,1,1,1,0)] = [[[8,7,6],[8,6,11],[8,11,9],[8,16,7],[9,16,8],[16,9,17],[11,18,9],[9,18,17],[11,6,18],[7,18,6],[18,7,17],[17,7,16]]]
        intersects_for_cases[(0,0,0,0,1,1,1,1)] = [[[9,8,10],[11,9,10],[11,17,9],[17,11,18],[10,18,11],[18,10,19],[8,16,10],[19,10,16],[9,16,8],[16,9,17],[16,17,18],[16,18,19]]]
        intersects_for_cases[(0,0,0,1,0,0,0,0)] = [[[2,10,3],[2,15,10],[10,15,3],[3,15,2]]]
        intersects_for_cases[(0,0,0,1,0,0,0,1)] = [[[7,3,2],[7,2,6],[7,15,3],[19,15,7],[6,19,7],[3,15,2],[2,19,6],[19,2,15]]]
        intersects_for_cases[(0,0,0,1,0,0,1,0)] = [[[2,10,3],[2,15,10],[10,15,3],[3,15,2]],[[5,6,11],[5,18,6],[6,18,11],[11,18,5]]]
        intersects_for_cases[(0,0,0,1,0,0,1,1)] = [[[3,2,11],[3,11,5],[3,5,7],[3,15,2],[7,15,3],[15,7,19],[5,18,7],[7,18,19],[5,11,18],[2,18,11],[18,2,19],[19,2,15]]]
        intersects_for_cases[(0,0,0,1,0,1,0,0)] = [[[2,10,3],[2,15,10],[10,15,3],[3,15,2]],[[9,4,5],[5,17,9],[4,17,5],[9,17,4]]]
        intersects_for_cases[(0,0,0,1,0,1,0,1)] = [[[7,3,2],[7,2,6],[7,15,3],[19,15,7],[6,19,7],[3,15,2],[2,19,6],[19,2,15]],[[5,9,4],[4,17,5],[9,17,4],[5,17,9]]]
        intersects_for_cases[(0,0,0,1,0,1,1,0)] = [[[11,9,4],[11,4,6],[11,17,9],[18,17,11],[6,18,11],[9,17,4],[4,18,6],[18,4,17]],[[10,3,2],[2,15,10],[3,15,2],[10,15,3]]]
        intersects_for_cases[(0,0,0,1,0,1,1,1)] = [[[2,7,3],[2,11,9],[2,9,7],[7,9,4],[3,15,2],[7,15,3],[15,7,19],[9,17,4],[2,18,11],[18,2,15],[19,18,15],[11,17,9],[17,11,18],[17,18,4],[4,18,7],[19,7,18]]]
        intersects_for_cases[(0,0,0,1,1,0,0,0)] = [[[10,3,2],[10,15,3],[3,15,2],[2,15,10]],[[4,8,7],[4,16,8],[8,16,7],[7,16,4]]]
        intersects_for_cases[(0,0,0,1,1,0,0,1)] = [[[4,8,3],[4,3,2],[4,2,6],[4,16,8],[6,16,4],[16,6,19],[2,15,6],[6,15,19],[2,3,15],[8,15,3],[15,8,19],[19,8,16]]]
        intersects_for_cases[(0,0,0,1,1,0,1,0)] = [[[10,3,2],[10,15,3],[2,15,10],[3,15,2]],[[8,7,4],[8,16,7],[7,16,4],[4,16,8]],[[11,5,6],[6,18,11],[5,18,6],[11,18,5]]]
        intersects_for_cases[(0,0,0,1,1,0,1,1)] = [[[3,4,8],[3,5,4],[3,2,5],[2,11,5],[3,15,2],[11,18,5],[4,16,8],[3,19,15],[8,19,3],[16,19,8],[18,19,5],[5,19,4],[4,19,16],[2,15,19],[2,19,11],[11,19,18]]]
        intersects_for_cases[(0,0,0,1,1,1,0,0)] = [[[7,5,9],[7,9,8],[7,17,5],[16,17,7],[8,16,7],[5,17,9],[9,16,8],[16,9,17]],[[3,2,10],[10,15,3],[2,15,10],[3,15,2]]]
        intersects_for_cases[(0,0,0,1,1,1,0,1)] = [[[3,9,8],[3,6,9],[3,2,6],[6,5,9],[3,15,2],[5,17,9],[9,17,8],[16,8,17],[3,19,15],[8,19,3],[16,19,8],[2,19,6],[19,2,15],[5,6,17],[17,6,19],[17,19,16]]]
        intersects_for_cases[(0,0,0,1,1,1,1,0)] = [[[3,2,10],[10,15,3],[3,15,2],[2,15,10]],[[7,6,8],[8,6,11],[8,11,9],[8,16,7],[9,16,8],[16,9,17],[11,18,9],[9,18,17],[11,6,18],[7,18,6],[18,7,17],[17,7,16]]]
        intersects_for_cases[(0,0,0,1,1,1,1,1)] = [[[3,2,11],[8,3,11],[9,8,11],[11,2,15],[11,15,19],[18,11,19],[9,17,8],[16,8,17],[3,19,15],[8,19,3],[8,16,19],[9,11,18],[18,17,9],[3,15,2],[18,19,16],[16,17,18]]]
        intersects_for_cases[(0,0,1,0,0,0,0,0)] = [[[2,1,11],[2,14,1],[1,14,11],[11,14,2]]]
        intersects_for_cases[(0,0,1,0,0,0,0,1)] = [[[10,6,7],[10,19,6],[6,19,7],[7,19,10]],[[1,11,2],[1,14,11],[11,14,2],[2,14,1]]]
        intersects_for_cases[(0,0,1,0,0,0,1,0)] = [[[6,2,1],[6,1,5],[6,14,2],[18,14,6],[5,18,6],[2,14,1],[1,18,5],[18,1,14]]]
        intersects_for_cases[(0,0,1,0,0,0,1,1)] = [[[7,10,2],[7,2,1],[7,1,5],[7,19,10],[5,19,7],[19,5,18],[1,14,5],[5,14,18],[1,2,14],[10,14,2],[14,10,18],[18,10,19]]]
        intersects_for_cases[(0,0,1,0,0,1,0,0)] = [[[5,9,4],[5,17,9],[9,17,4],[4,17,5]],[[2,1,11],[2,14,1],[1,14,11],[11,14,2]]]
        intersects_for_cases[(0,0,1,0,0,1,0,1)] = [[[11,2,1],[11,14,2],[1,14,11],[2,14,1]],[[10,6,7],[10,19,6],[6,19,7],[7,19,10]],[[9,4,5],[5,17,9],[4,17,5],[9,17,4]]]
        intersects_for_cases[(0,0,1,0,0,1,1,0)] = [[[2,1,9],[2,9,4],[2,4,6],[2,14,1],[6,14,2],[14,6,18],[4,17,6],[6,17,18],[4,9,17],[1,17,9],[17,1,18],[18,1,14]]]
        intersects_for_cases[(0,0,1,0,0,1,1,1)] = [[[2,7,10],[2,4,7],[2,1,4],[1,9,4],[2,14,1],[9,17,4],[7,19,10],[2,18,14],[10,18,2],[19,18,10],[17,18,4],[4,18,7],[7,18,19],[1,14,18],[1,18,9],[9,18,17]]]
        intersects_for_cases[(0,0,1,0,1,0,0,0)] = [[[7,4,8],[7,16,4],[4,16,8],[8,16,7]],[[2,1,11],[11,14,2],[1,14,11],[2,14,1]]]
        intersects_for_cases[(0,0,1,0,1,0,0,1)] = [[[6,4,8],[6,8,10],[6,16,4],[19,16,6],[10,19,6],[4,16,8],[8,19,10],[19,8,16]],[[2,1,11],[11,14,2],[1,14,11],[2,14,1]]]
        intersects_for_cases[(0,0,1,0,1,0,1,0)] = [[[6,2,1],[6,1,5],[6,14,2],[18,14,6],[5,18,6],[2,14,1],[1,18,5],[18,1,14]],[[4,8,7],[7,16,4],[8,16,7],[4,16,8]]]
        intersects_for_cases[(0,0,1,0,1,0,1,1)] = [[[2,8,10],[2,5,8],[2,1,5],[5,4,8],[2,14,1],[4,16,8],[8,16,10],[19,10,16],[2,18,14],[10,18,2],[19,18,10],[1,18,5],[18,1,14],[4,5,16],[16,5,18],[16,18,19]]]
        intersects_for_cases[(0,0,1,0,1,1,0,0)] = [[[9,8,7],[9,7,5],[9,16,8],[17,16,9],[5,17,9],[8,16,7],[7,17,5],[17,7,16]],[[11,2,1],[1,14,11],[2,14,1],[11,14,2]]]
        intersects_for_cases[(0,0,1,0,1,1,0,1)] = [[[2,1,11],[11,14,2],[2,14,1],[1,14,11]],[[6,5,10],[10,5,9],[10,9,8],[10,19,6],[8,19,10],[19,8,16],[9,17,8],[8,17,16],[9,5,17],[6,17,5],[17,6,16],[16,6,19]]]
        intersects_for_cases[(0,0,1,0,1,1,1,0)] = [[[1,6,2],[1,9,8],[1,8,6],[6,8,7],[2,14,1],[6,14,2],[14,6,18],[8,16,7],[1,17,9],[17,1,14],[18,17,14],[9,16,8],[16,9,17],[16,17,7],[7,17,6],[18,6,17]]]
        intersects_for_cases[(0,0,1,0,1,1,1,1)] = [[[2,1,9],[10,2,9],[8,10,9],[9,1,14],[9,14,18],[17,9,18],[8,16,10],[19,10,16],[2,18,14],[10,18,2],[10,19,18],[8,9,17],[17,16,8],[2,14,1],[17,18,19],[19,16,17]]]
        intersects_for_cases[(0,0,1,1,0,0,0,0)] = [[[11,10,3],[11,3,1],[11,15,10],[14,15,11],[1,14,11],[10,15,3],[3,14,1],[14,3,15]]]
        intersects_for_cases[(0,0,1,1,0,0,0,1)] = [[[1,11,6],[1,6,7],[1,7,3],[1,14,11],[3,14,1],[14,3,15],[7,19,3],[3,19,15],[7,6,19],[11,19,6],[19,11,15],[15,11,14]]]
        intersects_for_cases[(0,0,1,1,0,0,1,0)] = [[[5,6,10],[5,10,3],[5,3,1],[5,18,6],[1,18,5],[18,1,14],[3,15,1],[1,15,14],[3,10,15],[6,15,10],[15,6,14],[14,6,18]]]
        intersects_for_cases[(0,0,1,1,0,0,1,1)] = [[[3,1,5],[7,3,5],[7,15,3],[15,7,19],[5,19,7],[19,5,18],[1,14,5],[18,5,14],[3,14,1],[14,3,15],[14,15,19],[14,19,18]]]
        intersects_for_cases[(0,0,1,1,0,1,0,0)] = [[[11,10,3],[11,3,1],[11,15,10],[14,15,11],[1,14,11],[10,15,3],[3,14,1],[14,3,15]],[[9,4,5],[5,17,9],[4,17,5],[9,17,4]]]
        intersects_for_cases[(0,0,1,1,0,1,0,1)] = [[[9,4,5],[5,17,9],[9,17,4],[4,17,5]],[[11,6,1],[1,6,7],[1,7,3],[1,14,11],[3,14,1],[14,3,15],[7,19,3],[3,19,15],[7,6,19],[11,19,6],[19,11,15],[15,11,14]]]
        intersects_for_cases[(0,0,1,1,0,1,1,0)] = [[[10,4,6],[10,1,4],[10,3,1],[1,9,4],[10,15,3],[9,17,4],[4,17,6],[18,6,17],[10,14,15],[6,14,10],[18,14,6],[3,14,1],[14,3,15],[9,1,17],[17,1,14],[17,14,18]]]
        intersects_for_cases[(0,0,1,1,0,1,1,1)] = [[[9,4,7],[1,9,7],[3,1,7],[7,4,17],[7,17,18],[19,7,18],[3,15,1],[14,1,15],[9,18,17],[1,18,9],[1,14,18],[3,7,19],[19,15,3],[9,17,4],[19,18,14],[14,15,19]]]
        intersects_for_cases[(0,0,1,1,1,0,0,0)] = [[[3,1,11],[3,11,10],[3,14,1],[15,14,3],[10,15,3],[1,14,11],[11,15,10],[15,11,14]],[[7,4,8],[8,16,7],[4,16,8],[7,16,4]]]
        intersects_for_cases[(0,0,1,1,1,0,0,1)] = [[[8,6,4],[8,3,1],[8,1,6],[6,1,11],[4,16,8],[6,16,4],[16,6,19],[1,14,11],[8,15,3],[15,8,16],[19,15,16],[3,14,1],[14,3,15],[14,15,11],[11,15,6],[19,6,15]]]
        intersects_for_cases[(0,0,1,1,1,0,1,0)] = [[[4,8,7],[7,16,4],[4,16,8],[8,16,7]],[[6,10,5],[5,10,3],[5,3,1],[5,18,6],[1,18,5],[18,1,14],[3,15,1],[1,15,14],[3,10,15],[6,15,10],[15,6,14],[14,6,18]]]
        intersects_for_cases[(0,0,1,1,1,0,1,1)] = [[[4,8,3],[5,4,3],[1,5,3],[3,8,16],[3,16,19],[15,3,19],[1,14,5],[18,5,14],[4,19,16],[5,19,4],[5,18,19],[1,3,15],[15,14,1],[4,16,8],[15,19,18],[18,14,15]]]
        intersects_for_cases[(0,0,1,1,1,1,0,0)] = [[[3,1,10],[1,11,10],[1,14,11],[10,15,3],[1,15,14],[15,1,3],[11,14,10],[10,14,15]],[[7,5,9],[7,9,8],[5,17,9],[8,16,7],[9,17,8],[16,8,17],[7,17,5],[17,7,16]]]
        intersects_for_cases[(0,0,1,1,1,1,0,1)] = [[[8,3,1],[9,8,1],[11,6,5],[3,15,14],[14,1,3],[19,16,6],[6,16,5],[5,16,17],[3,19,15],[8,19,3],[16,19,8],[1,14,11],[5,1,11],[9,1,5],[5,17,9],[8,13,9],[13,8,12],[6,15,19],[11,15,6],[14,15,11]]]
        intersects_for_cases[(0,0,1,1,1,1,1,0)] = [[[1,9,8],[3,1,8],[7,6,10],[9,17,16],[16,8,9],[18,14,6],[6,14,10],[10,14,15],[9,18,17],[1,18,9],[14,18,1],[8,16,7],[10,8,7],[3,8,10],[10,15,3],[1,12,3],[12,1,13],[6,17,18],[7,17,6],[16,17,7]]]
        intersects_for_cases[(0,0,1,1,1,1,1,1)] = [[[8,3,1],[9,8,1],[3,19,15],[8,19,3],[16,19,8],[14,18,1],[1,18,9],[9,18,17],[3,15,14],[3,14,1],[18,19,16],[16,17,18],[9,16,8],[16,9,17],[14,15,19],[19,18,14]]]
        intersects_for_cases[(0,1,0,0,0,0,0,0)] = [[[0,9,1],[0,13,9],[9,13,1],[1,13,0]]]
        intersects_for_cases[(0,1,0,0,0,0,0,1)] = [[[6,7,10],[6,19,7],[7,19,10],[10,19,6]],[[1,0,9],[9,13,1],[0,13,9],[1,13,0]]]
        intersects_for_cases[(0,1,0,0,0,0,1,0)] = [[[11,5,6],[11,18,5],[5,18,6],[6,18,11]],[[0,9,1],[0,13,9],[9,13,1],[1,13,0]]]
        intersects_for_cases[(0,1,0,0,0,0,1,1)] = [[[5,7,10],[5,10,11],[5,19,7],[18,19,5],[11,18,5],[7,19,10],[10,18,11],[18,10,19]],[[1,0,9],[9,13,1],[0,13,9],[1,13,0]]]
        intersects_for_cases[(0,1,0,0,0,1,0,0)] = [[[0,4,5],[0,5,1],[0,17,4],[13,17,0],[1,13,0],[4,17,5],[5,13,1],[13,5,17]]]
        intersects_for_cases[(0,1,0,0,0,1,0,1)] = [[[5,1,0],[5,0,4],[5,13,1],[17,13,5],[4,17,5],[1,13,0],[0,17,4],[17,0,13]],[[7,10,6],[6,19,7],[10,19,6],[7,19,10]]]
        intersects_for_cases[(0,1,0,0,0,1,1,0)] = [[[6,11,1],[6,1,0],[6,0,4],[6,18,11],[4,18,6],[18,4,17],[0,13,4],[4,13,17],[0,1,13],[11,13,1],[13,11,17],[17,11,18]]]
        intersects_for_cases[(0,1,0,0,0,1,1,1)] = [[[1,10,11],[1,4,10],[1,0,4],[4,7,10],[1,13,0],[7,19,10],[10,19,11],[18,11,19],[1,17,13],[11,17,1],[18,17,11],[0,17,4],[17,0,13],[7,4,19],[19,4,17],[19,17,18]]]
        intersects_for_cases[(0,1,0,0,1,0,0,0)] = [[[0,9,1],[0,13,9],[9,13,1],[1,13,0]],[[7,4,8],[7,16,4],[4,16,8],[8,16,7]]]
        intersects_for_cases[(0,1,0,0,1,0,0,1)] = [[[8,10,6],[8,6,4],[8,19,10],[16,19,8],[4,16,8],[10,19,6],[6,16,4],[16,6,19]],[[9,1,0],[0,13,9],[1,13,0],[9,13,1]]]
        intersects_for_cases[(0,1,0,0,1,0,1,0)] = [[[4,8,7],[4,16,8],[7,16,4],[8,16,7]],[[0,9,1],[0,13,9],[9,13,1],[1,13,0]],[[6,11,5],[5,18,6],[11,18,5],[6,18,11]]]
        intersects_for_cases[(0,1,0,0,1,0,1,1)] = [[[1,0,9],[9,13,1],[1,13,0],[0,13,9]],[[5,4,11],[11,4,8],[11,8,10],[11,18,5],[10,18,11],[18,10,19],[8,16,10],[10,16,19],[8,4,16],[5,16,4],[16,5,19],[19,5,18]]]
        intersects_for_cases[(0,1,0,0,1,1,0,0)] = [[[1,0,8],[1,8,7],[1,7,5],[1,13,0],[5,13,1],[13,5,17],[7,16,5],[5,16,17],[7,8,16],[0,16,8],[16,0,17],[17,0,13]]]
        intersects_for_cases[(0,1,0,0,1,1,0,1)] = [[[0,5,1],[0,8,10],[0,10,5],[5,10,6],[1,13,0],[5,13,1],[13,5,17],[10,19,6],[0,16,8],[16,0,13],[17,16,13],[8,19,10],[19,8,16],[19,16,6],[6,16,5],[17,5,16]]]
        intersects_for_cases[(0,1,0,0,1,1,1,0)] = [[[8,1,0],[8,11,1],[8,7,11],[7,6,11],[8,16,7],[6,18,11],[1,13,0],[8,17,16],[0,17,8],[13,17,0],[18,17,11],[11,17,1],[1,17,13],[7,16,17],[7,17,6],[6,17,18]]]
        intersects_for_cases[(0,1,0,0,1,1,1,1)] = [[[1,0,8],[11,1,8],[10,11,8],[8,0,13],[8,13,17],[16,8,17],[10,19,11],[18,11,19],[1,17,13],[11,17,1],[11,18,17],[10,8,16],[16,19,10],[1,13,0],[16,17,18],[18,19,16]]]
        intersects_for_cases[(0,1,0,1,0,0,0,0)] = [[[3,2,10],[3,15,2],[2,15,10],[10,15,3]],[[9,1,0],[9,13,1],[1,13,0],[0,13,9]]]
        intersects_for_cases[(0,1,0,1,0,0,0,1)] = [[[2,6,7],[2,7,3],[2,19,6],[15,19,2],[3,15,2],[6,19,7],[7,15,3],[15,7,19]],[[0,9,1],[1,13,0],[9,13,1],[0,13,9]]]
        intersects_for_cases[(0,1,0,1,0,0,1,0)] = [[[1,0,9],[1,13,0],[9,13,1],[0,13,9]],[[3,2,10],[3,15,2],[2,15,10],[10,15,3]],[[5,6,11],[11,18,5],[6,18,11],[5,18,6]]]
        intersects_for_cases[(0,1,0,1,0,0,1,1)] = [[[0,9,1],[1,13,0],[0,13,9],[9,13,1]],[[2,11,3],[3,11,5],[3,5,7],[3,15,2],[7,15,3],[15,7,19],[5,18,7],[7,18,19],[5,11,18],[2,18,11],[18,2,19],[19,2,15]]]
        intersects_for_cases[(0,1,0,1,0,1,0,0)] = [[[0,4,5],[0,5,1],[0,17,4],[13,17,0],[1,13,0],[4,17,5],[5,13,1],[13,5,17]],[[2,10,3],[3,15,2],[10,15,3],[2,15,10]]]
        intersects_for_cases[(0,1,0,1,0,1,0,1)] = [[[2,6,3],[6,7,3],[6,19,7],[3,15,2],[6,15,19],[15,6,2],[7,19,3],[3,19,15]],[[0,4,5],[0,5,1],[4,17,5],[1,13,0],[5,17,1],[13,1,17],[0,17,4],[17,0,13]]]
        intersects_for_cases[(0,1,0,1,0,1,1,0)] = [[[10,3,2],[2,15,10],[10,15,3],[3,15,2]],[[11,1,6],[6,1,0],[6,0,4],[6,18,11],[4,18,6],[18,4,17],[0,13,4],[4,13,17],[0,1,13],[11,13,1],[13,11,17],[17,11,18]]]
        intersects_for_cases[(0,1,0,1,0,1,1,1)] = [[[4,7,3],[0,4,3],[2,11,1],[7,19,15],[15,3,7],[18,17,11],[11,17,1],[1,17,13],[7,18,19],[4,18,7],[17,18,4],[3,15,2],[1,3,2],[0,3,1],[1,13,0],[4,12,0],[12,4,16],[11,19,18],[2,19,11],[15,19,2]]]
        intersects_for_cases[(0,1,0,1,1,0,0,0)] = [[[3,2,10],[3,15,2],[10,15,3],[2,15,10]],[[1,0,9],[1,13,0],[0,13,9],[9,13,1]],[[7,4,8],[8,16,7],[4,16,8],[7,16,4]]]
        intersects_for_cases[(0,1,0,1,1,0,0,1)] = [[[9,1,0],[0,13,9],[9,13,1],[1,13,0]],[[8,3,4],[4,3,2],[4,2,6],[4,16,8],[6,16,4],[16,6,19],[2,15,6],[6,15,19],[2,3,15],[8,15,3],[15,8,19],[19,8,16]]]
        intersects_for_cases[(0,1,0,1,1,0,1,0)] = [[[2,10,3],[2,15,10],[10,15,3],[3,15,2]],[[0,9,1],[9,13,1],[0,13,9],[1,13,0]],[[5,6,11],[5,18,6],[6,18,11],[11,18,5]],[[7,4,8],[7,16,4],[8,16,7],[4,16,8]]]
        intersects_for_cases[(0,1,0,1,1,0,1,1)] = [[[8,3,0],[11,1,2],[9,5,4],[1,13,0],[2,1,0],[0,3,2],[3,15,2],[18,19,5],[5,19,4],[4,19,16],[2,15,19],[2,19,11],[11,19,18],[0,13,9],[4,0,9],[8,0,4],[4,16,8],[3,19,15],[8,19,3],[16,19,8],[11,18,5],[5,1,11],[5,9,15],[9,13,1]]]
        intersects_for_cases[(0,1,0,1,1,1,0,0)] = [[[2,10,3],[3,15,2],[2,15,10],[10,15,3]],[[0,8,1],[1,8,7],[1,7,5],[1,13,0],[5,13,1],[13,5,17],[7,16,5],[5,16,17],[7,8,16],[0,16,8],[16,0,17],[17,0,13]]]
        intersects_for_cases[(0,1,0,1,1,1,0,1)] = [[[6,5,1],[2,6,1],[0,8,3],[5,17,13],[13,1,5],[16,19,8],[8,19,3],[3,19,15],[5,16,17],[6,16,5],[19,16,6],[1,13,0],[3,1,0],[2,1,3],[3,15,2],[6,14,2],[14,6,18],[8,17,16],[0,17,8],[13,17,0]]]
        intersects_for_cases[(0,1,0,1,1,1,1,0)] = [[[0,8,3],[6,10,7],[2,11,1],[10,15,3],[7,10,3],[3,8,7],[8,16,7],[18,17,11],[11,17,1],[1,17,13],[7,16,17],[7,17,6],[6,17,18],[3,15,2],[1,3,2],[0,3,1],[1,13,0],[8,17,16],[0,17,8],[13,17,0],[6,18,11],[11,10,6],[11,2,16],[2,15,10]]]
        intersects_for_cases[(0,1,0,1,1,1,1,1)] = [[[8,3,0],[1,2,11],[3,15,2],[3,2,1],[0,3,1],[1,13,0],[18,19,16],[16,17,18],[15,3,19],[8,19,3],[19,8,16],[17,13,1],[11,17,1],[17,11,18],[0,13,8],[16,8,13],[17,16,13],[2,15,19],[2,19,11],[19,18,11]]]
        intersects_for_cases[(0,1,1,0,0,0,0,0)] = [[[2,0,9],[2,9,11],[2,13,0],[14,13,2],[11,14,2],[0,13,9],[9,14,11],[14,9,13]]]
        intersects_for_cases[(0,1,1,0,0,0,0,1)] = [[[2,0,9],[2,9,11],[2,13,0],[14,13,2],[11,14,2],[0,13,9],[9,14,11],[14,9,13]],[[6,7,10],[10,19,6],[7,19,10],[6,19,7]]]
        intersects_for_cases[(0,1,1,0,0,0,1,0)] = [[[0,9,5],[0,5,6],[0,6,2],[0,13,9],[2,13,0],[13,2,14],[6,18,2],[2,18,14],[6,5,18],[9,18,5],[18,9,14],[14,9,13]]]
        intersects_for_cases[(0,1,1,0,0,0,1,1)] = [[[10,5,7],[10,2,0],[10,0,5],[5,0,9],[7,19,10],[5,19,7],[19,5,18],[0,13,9],[10,14,2],[14,10,19],[18,14,19],[2,13,0],[13,2,14],[13,14,9],[9,14,5],[18,5,14]]]
        intersects_for_cases[(0,1,1,0,0,1,0,0)] = [[[4,5,11],[4,11,2],[4,2,0],[4,17,5],[0,17,4],[17,0,13],[2,14,0],[0,14,13],[2,11,14],[5,14,11],[14,5,13],[13,5,17]]]
        intersects_for_cases[(0,1,1,0,0,1,0,1)] = [[[7,10,6],[6,19,7],[7,19,10],[10,19,6]],[[5,11,4],[4,11,2],[4,2,0],[4,17,5],[0,17,4],[17,0,13],[2,14,0],[0,14,13],[2,11,14],[5,14,11],[14,5,13],[13,5,17]]]
        intersects_for_cases[(0,1,1,0,0,1,1,0)] = [[[4,6,2],[0,4,2],[0,17,4],[17,0,13],[2,13,0],[13,2,14],[6,18,2],[14,2,18],[4,18,6],[18,4,17],[18,17,13],[18,13,14]]]
        intersects_for_cases[(0,1,1,0,0,1,1,1)] = [[[7,10,2],[4,7,2],[0,4,2],[2,10,19],[2,19,18],[14,2,18],[0,13,4],[17,4,13],[7,18,19],[4,18,7],[4,17,18],[0,2,14],[14,13,0],[7,19,10],[14,18,17],[17,13,14]]]
        intersects_for_cases[(0,1,1,0,1,0,0,0)] = [[[9,11,2],[9,2,0],[9,14,11],[13,14,9],[0,13,9],[11,14,2],[2,13,0],[13,2,14]],[[8,7,4],[4,16,8],[7,16,4],[8,16,7]]]
        intersects_for_cases[(0,1,1,0,1,0,0,1)] = [[[6,4,10],[4,8,10],[4,16,8],[10,19,6],[4,19,16],[19,4,6],[8,16,10],[10,16,19]],[[2,0,9],[2,9,11],[0,13,9],[11,14,2],[9,13,11],[14,11,13],[2,13,0],[13,2,14]]]
        intersects_for_cases[(0,1,1,0,1,0,1,0)] = [[[8,7,4],[4,16,8],[8,16,7],[7,16,4]],[[9,5,0],[0,5,6],[0,6,2],[0,13,9],[2,13,0],[13,2,14],[6,18,2],[2,18,14],[6,5,18],[9,18,5],[18,9,14],[14,9,13]]]
        intersects_for_cases[(0,1,1,0,1,0,1,1)] = [[[10,2,0],[8,10,0],[9,5,4],[2,14,13],[13,0,2],[18,19,5],[5,19,4],[4,19,16],[2,18,14],[10,18,2],[19,18,10],[0,13,9],[4,0,9],[8,0,4],[4,16,8],[10,12,8],[12,10,15],[5,14,18],[9,14,5],[13,14,9]]]
        intersects_for_cases[(0,1,1,0,1,1,0,0)] = [[[8,2,0],[8,5,2],[8,7,5],[5,11,2],[8,16,7],[11,14,2],[2,14,0],[13,0,14],[8,17,16],[0,17,8],[13,17,0],[7,17,5],[17,7,16],[11,5,14],[14,5,17],[14,17,13]]]
        intersects_for_cases[(0,1,1,0,1,1,0,1)] = [[[0,8,10],[2,0,10],[6,5,11],[8,16,19],[19,10,8],[17,13,5],[5,13,11],[11,13,14],[8,17,16],[0,17,8],[13,17,0],[10,19,6],[11,10,6],[2,10,11],[11,14,2],[0,15,2],[15,0,12],[5,16,17],[6,16,5],[19,16,6]]]
        intersects_for_cases[(0,1,1,0,1,1,1,0)] = [[[8,7,6],[0,8,6],[2,0,6],[6,7,16],[6,16,17],[18,6,17],[2,14,0],[13,0,14],[8,17,16],[0,17,8],[0,13,17],[2,6,18],[18,14,2],[8,16,7],[18,17,13],[13,14,18]]]
        intersects_for_cases[(0,1,1,0,1,1,1,1)] = [[[0,8,10],[2,0,10],[8,17,16],[0,17,8],[13,17,0],[19,18,10],[10,18,2],[2,18,14],[8,16,19],[8,19,10],[18,17,13],[13,14,18],[2,13,0],[13,2,14],[19,16,17],[17,18,19]]]
        intersects_for_cases[(0,1,1,1,0,0,0,0)] = [[[10,3,0],[10,0,9],[10,9,11],[10,15,3],[11,15,10],[15,11,14],[9,13,11],[11,13,14],[9,0,13],[3,13,0],[13,3,14],[14,3,15]]]
        intersects_for_cases[(0,1,1,1,0,0,0,1)] = [[[6,9,11],[6,3,9],[6,7,3],[3,0,9],[6,19,7],[0,13,9],[9,13,11],[14,11,13],[6,15,19],[11,15,6],[14,15,11],[7,15,3],[15,7,19],[0,3,13],[13,3,15],[13,15,14]]]
        intersects_for_cases[(0,1,1,1,0,0,1,0)] = [[[10,5,6],[10,9,5],[10,3,9],[3,0,9],[10,15,3],[0,13,9],[5,18,6],[10,14,15],[6,14,10],[18,14,6],[13,14,9],[9,14,5],[5,14,18],[3,15,14],[3,14,0],[0,14,13]]]
        intersects_for_cases[(0,1,1,1,0,0,1,1)] = [[[0,9,5],[3,0,5],[7,3,5],[5,9,13],[5,13,14],[18,5,14],[7,19,3],[15,3,19],[0,14,13],[3,14,0],[3,15,14],[7,5,18],[18,19,7],[0,13,9],[18,14,15],[15,19,18]]]
        intersects_for_cases[(0,1,1,1,0,1,0,0)] = [[[3,11,10],[3,0,4],[3,4,11],[11,4,5],[10,15,3],[11,15,10],[15,11,14],[4,17,5],[3,13,0],[13,3,15],[14,13,15],[0,17,4],[17,0,13],[17,13,5],[5,13,11],[14,11,13]]]
        intersects_for_cases[(0,1,1,1,0,1,0,1)] = [[[3,0,4],[7,3,4],[5,11,6],[0,13,17],[17,4,0],[14,15,11],[11,15,6],[6,15,19],[0,14,13],[3,14,0],[15,14,3],[4,17,5],[6,4,5],[7,4,6],[6,19,7],[3,16,7],[16,3,12],[11,13,14],[5,13,11],[17,13,5]]]
        intersects_for_cases[(0,1,1,1,0,1,1,0)] = [[[10,3,0],[6,10,0],[4,6,0],[0,3,15],[0,15,14],[13,0,14],[4,17,6],[18,6,17],[10,14,15],[6,14,10],[6,18,14],[4,0,13],[13,17,4],[10,15,3],[13,14,18],[18,17,13]]]
        intersects_for_cases[(0,1,1,1,0,1,1,1)] = [[[3,0,4],[7,3,4],[0,14,13],[3,14,0],[15,14,3],[17,18,4],[4,18,7],[7,18,19],[0,13,17],[0,17,4],[18,14,15],[15,19,18],[7,15,3],[15,7,19],[17,13,14],[14,18,17]]]
        intersects_for_cases[(0,1,1,1,1,0,0,0)] = [[[7,4,8],[8,16,7],[7,16,4],[4,16,8]],[[3,0,10],[10,0,9],[10,9,11],[10,15,3],[11,15,10],[15,11,14],[9,13,11],[11,13,14],[9,0,13],[3,13,0],[13,3,14],[14,3,15]]]
        intersects_for_cases[(0,1,1,1,1,0,0,1)] = [[[11,6,4],[9,11,4],[8,3,0],[6,19,16],[16,4,6],[15,14,3],[3,14,0],[0,14,13],[6,15,19],[11,15,6],[14,15,11],[4,16,8],[0,4,8],[9,4,0],[0,13,9],[11,17,9],[17,11,18],[3,19,15],[8,19,3],[16,19,8]]]
        intersects_for_cases[(0,1,1,1,1,0,1,0)] = [[[6,10,7],[0,8,3],[4,9,5],[8,16,7],[3,8,7],[7,10,3],[10,15,3],[13,14,9],[9,14,5],[5,14,18],[3,15,14],[3,14,0],[0,14,13],[7,16,4],[5,7,4],[6,7,5],[5,18,6],[10,14,15],[6,14,10],[18,14,6],[0,13,9],[9,8,0],[9,4,15],[4,16,8]]]
        intersects_for_cases[(0,1,1,1,1,0,1,1)] = [[[3,0,8],[4,9,5],[0,13,9],[0,9,4],[8,0,4],[4,16,8],[18,14,15],[15,19,18],[13,0,14],[3,14,0],[14,3,15],[19,16,4],[5,19,4],[19,5,18],[8,16,3],[15,3,16],[19,15,16],[9,13,14],[9,14,5],[14,18,5]]]
        intersects_for_cases[(0,1,1,1,1,1,0,0)] = [[[5,11,10],[7,5,10],[3,0,8],[11,14,15],[15,10,11],[13,17,0],[0,17,8],[8,17,16],[11,13,14],[5,13,11],[17,13,5],[10,15,3],[8,10,3],[7,10,8],[8,16,7],[5,19,7],[19,5,18],[0,14,13],[3,14,0],[15,14,3]]]
        intersects_for_cases[(0,1,1,1,1,1,0,1)] = [[[8,3,0],[11,6,5],[3,15,2],[3,14,0],[13,0,14],[6,19,16],[6,16,5],[17,5,16],[15,3,19],[8,19,3],[19,8,16],[13,14,11],[5,13,11],[5,17,13],[0,13,8],[16,8,13],[17,16,13],[15,19,6],[11,15,6],[14,15,11]]]
        intersects_for_cases[(0,1,1,1,1,1,1,0)] = [[[0,8,3],[10,7,6],[8,16,7],[8,7,10],[3,8,10],[10,15,3],[18,17,13],[13,14,18],[16,8,17],[0,17,8],[17,0,13],[14,15,10],[6,14,10],[14,6,18],[3,15,0],[13,0,15],[14,13,15],[7,16,17],[7,17,6],[17,18,6]]]
        intersects_for_cases[(0,1,1,1,1,1,1,1)] = [[[8,3,0],[16,8,0],[16,0,13],[16,13,17],[14,3,15],[3,14,0],[0,14,13],[16,19,8],[8,19,15],[8,15,3],[14,18,17],[17,13,14],[18,19,16],[16,17,18],[14,15,19],[19,18,14]]]
        intersects_for_cases[(1,0,0,0,0,0,0,0)] = [[[0,3,8],[0,12,3],[3,12,8],[8,12,0]]]
        intersects_for_cases[(1,0,0,0,0,0,0,1)] = [[[3,8,0],[3,12,8],[8,12,0],[0,12,3]],[[6,7,10],[6,19,7],[7,19,10],[10,19,6]]]
        intersects_for_cases[(1,0,0,0,0,0,1,0)] = [[[0,3,8],[0,12,3],[3,12,8],[8,12,0]],[[5,6,11],[11,18,5],[6,18,11],[5,18,6]]]
        intersects_for_cases[(1,0,0,0,0,0,1,1)] = [[[10,11,5],[10,5,7],[10,18,11],[19,18,10],[7,19,10],[11,18,5],[5,19,7],[19,5,18]],[[8,0,3],[3,12,8],[0,12,3],[8,12,0]]]
        intersects_for_cases[(1,0,0,0,0,1,0,0)] = [[[8,0,3],[8,12,0],[0,12,3],[3,12,8]],[[5,9,4],[5,17,9],[9,17,4],[4,17,5]]]
        intersects_for_cases[(1,0,0,0,0,1,0,1)] = [[[7,10,6],[7,19,10],[6,19,7],[10,19,6]],[[3,8,0],[3,12,8],[8,12,0],[0,12,3]],[[5,9,4],[4,17,5],[9,17,4],[5,17,9]]]
        intersects_for_cases[(1,0,0,0,0,1,1,0)] = [[[4,6,11],[4,11,9],[4,18,6],[17,18,4],[9,17,4],[6,18,11],[11,17,9],[17,11,18]],[[0,3,8],[8,12,0],[3,12,8],[0,12,3]]]
        intersects_for_cases[(1,0,0,0,0,1,1,1)] = [[[0,3,8],[8,12,0],[0,12,3],[3,12,8]],[[4,7,9],[9,7,10],[9,10,11],[9,17,4],[11,17,9],[17,11,18],[10,19,11],[11,19,18],[10,7,19],[4,19,7],[19,4,18],[18,4,17]]]
        intersects_for_cases[(1,0,0,0,1,0,0,0)] = [[[4,0,3],[4,3,7],[4,12,0],[16,12,4],[7,16,4],[0,12,3],[3,16,7],[16,3,12]]]
        intersects_for_cases[(1,0,0,0,1,0,0,1)] = [[[0,3,10],[0,10,6],[0,6,4],[0,12,3],[4,12,0],[12,4,16],[6,19,4],[4,19,16],[6,10,19],[3,19,10],[19,3,16],[16,3,12]]]
        intersects_for_cases[(1,0,0,0,1,0,1,0)] = [[[4,0,3],[4,3,7],[4,12,0],[16,12,4],[7,16,4],[0,12,3],[3,16,7],[16,3,12]],[[6,11,5],[5,18,6],[11,18,5],[6,18,11]]]
        intersects_for_cases[(1,0,0,0,1,0,1,1)] = [[[3,4,0],[3,10,11],[3,11,4],[4,11,5],[0,12,3],[4,12,0],[12,4,16],[11,18,5],[3,19,10],[19,3,12],[16,19,12],[10,18,11],[18,10,19],[18,19,5],[5,19,4],[16,4,19]]]
        intersects_for_cases[(1,0,0,0,1,1,0,0)] = [[[5,9,0],[5,0,3],[5,3,7],[5,17,9],[7,17,5],[17,7,16],[3,12,7],[7,12,16],[3,0,12],[9,12,0],[12,9,16],[16,9,17]]]
        intersects_for_cases[(1,0,0,0,1,1,0,1)] = [[[0,5,9],[0,6,5],[0,3,6],[3,10,6],[0,12,3],[10,19,6],[5,17,9],[0,16,12],[9,16,0],[17,16,9],[19,16,6],[6,16,5],[5,16,17],[3,12,16],[3,16,10],[10,16,19]]]
        intersects_for_cases[(1,0,0,0,1,1,1,0)] = [[[0,11,9],[0,7,11],[0,3,7],[7,6,11],[0,12,3],[6,18,11],[11,18,9],[17,9,18],[0,16,12],[9,16,0],[17,16,9],[3,16,7],[16,3,12],[6,7,18],[18,7,16],[18,16,17]]]
        intersects_for_cases[(1,0,0,0,1,1,1,1)] = [[[0,3,10],[9,0,10],[11,9,10],[10,3,12],[10,12,16],[19,10,16],[11,18,9],[17,9,18],[0,16,12],[9,16,0],[9,17,16],[11,10,19],[19,18,11],[0,12,3],[19,16,17],[17,18,19]]]
        intersects_for_cases[(1,0,0,1,0,0,0,0)] = [[[10,8,0],[10,0,2],[10,12,8],[15,12,10],[2,15,10],[8,12,0],[0,15,2],[15,0,12]]]
        intersects_for_cases[(1,0,0,1,0,0,0,1)] = [[[6,7,8],[6,8,0],[6,0,2],[6,19,7],[2,19,6],[19,2,15],[0,12,2],[2,12,15],[0,8,12],[7,12,8],[12,7,15],[15,7,19]]]
        intersects_for_cases[(1,0,0,1,0,0,1,0)] = [[[10,8,0],[10,0,2],[10,12,8],[15,12,10],[2,15,10],[8,12,0],[0,15,2],[15,0,12]],[[11,5,6],[6,18,11],[5,18,6],[11,18,5]]]
        intersects_for_cases[(1,0,0,1,0,0,1,1)] = [[[8,5,7],[8,2,5],[8,0,2],[2,11,5],[8,12,0],[11,18,5],[5,18,7],[19,7,18],[8,15,12],[7,15,8],[19,15,7],[0,15,2],[15,0,12],[11,2,18],[18,2,15],[18,15,19]]]
        intersects_for_cases[(1,0,0,1,0,1,0,0)] = [[[0,2,10],[0,10,8],[0,15,2],[12,15,0],[8,12,0],[2,15,10],[10,12,8],[12,10,15]],[[4,5,9],[9,17,4],[5,17,9],[4,17,5]]]
        intersects_for_cases[(1,0,0,1,0,1,0,1)] = [[[5,9,4],[4,17,5],[5,17,9],[9,17,4]],[[7,8,6],[6,8,0],[6,0,2],[6,19,7],[2,19,6],[19,2,15],[0,12,2],[2,12,15],[0,8,12],[7,12,8],[12,7,15],[15,7,19]]]
        intersects_for_cases[(1,0,0,1,0,1,1,0)] = [[[0,2,8],[2,10,8],[2,15,10],[8,12,0],[2,12,15],[12,2,0],[10,15,8],[8,15,12]],[[4,6,11],[4,11,9],[6,18,11],[9,17,4],[11,18,9],[17,9,18],[4,18,6],[18,4,17]]]
        intersects_for_cases[(1,0,0,1,0,1,1,1)] = [[[2,11,9],[0,2,9],[4,7,8],[11,18,17],[17,9,11],[19,15,7],[7,15,8],[8,15,12],[11,19,18],[2,19,11],[15,19,2],[9,17,4],[8,9,4],[0,9,8],[8,12,0],[2,13,0],[13,2,14],[7,18,19],[4,18,7],[17,18,4]]]
        intersects_for_cases[(1,0,0,1,1,0,0,0)] = [[[2,10,7],[2,7,4],[2,4,0],[2,15,10],[0,15,2],[15,0,12],[4,16,0],[0,16,12],[4,7,16],[10,16,7],[16,10,12],[12,10,15]]]
        intersects_for_cases[(1,0,0,1,1,0,0,1)] = [[[0,2,6],[4,0,6],[4,12,0],[12,4,16],[6,16,4],[16,6,19],[2,15,6],[19,6,15],[0,15,2],[15,0,12],[15,12,16],[15,16,19]]]
        intersects_for_cases[(1,0,0,1,1,0,1,0)] = [[[11,5,6],[6,18,11],[11,18,5],[5,18,6]],[[10,7,2],[2,7,4],[2,4,0],[2,15,10],[0,15,2],[15,0,12],[4,16,0],[0,16,12],[4,7,16],[10,16,7],[16,10,12],[12,10,15]]]
        intersects_for_cases[(1,0,0,1,1,0,1,1)] = [[[11,5,4],[2,11,4],[0,2,4],[4,5,18],[4,18,19],[16,4,19],[0,12,2],[15,2,12],[11,19,18],[2,19,11],[2,15,19],[0,4,16],[16,12,0],[11,18,5],[16,19,15],[15,12,16]]]
        intersects_for_cases[(1,0,0,1,1,1,0,0)] = [[[10,0,2],[10,7,5],[10,5,0],[0,5,9],[2,15,10],[0,15,2],[15,0,12],[5,17,9],[10,16,7],[16,10,15],[12,16,15],[7,17,5],[17,7,16],[17,16,9],[9,16,0],[12,0,16]]]
        intersects_for_cases[(1,0,0,1,1,1,0,1)] = [[[5,9,0],[6,5,0],[2,6,0],[0,9,17],[0,17,16],[12,0,16],[2,15,6],[19,6,15],[5,16,17],[6,16,5],[6,19,16],[2,0,12],[12,15,2],[5,17,9],[12,16,19],[19,15,12]]]
        intersects_for_cases[(1,0,0,1,1,1,1,0)] = [[[9,0,2],[11,9,2],[10,7,6],[0,12,15],[15,2,0],[16,17,7],[7,17,6],[6,17,18],[0,16,12],[9,16,0],[17,16,9],[2,15,10],[6,2,10],[11,2,6],[6,18,11],[9,14,11],[14,9,13],[7,12,16],[10,12,7],[15,12,10]]]
        intersects_for_cases[(1,0,0,1,1,1,1,1)] = [[[9,0,2],[11,9,2],[0,16,12],[9,16,0],[17,16,9],[15,19,2],[2,19,11],[11,19,18],[0,12,15],[0,15,2],[19,16,17],[17,18,19],[11,17,9],[17,11,18],[15,12,16],[16,19,15]]]
        intersects_for_cases[(1,0,1,0,0,0,0,0)] = [[[0,3,8],[0,12,3],[3,12,8],[8,12,0]],[[11,2,1],[11,14,2],[2,14,1],[1,14,11]]]
        intersects_for_cases[(1,0,1,0,0,0,0,1)] = [[[3,8,0],[3,12,8],[0,12,3],[8,12,0]],[[7,10,6],[7,19,10],[10,19,6],[6,19,7]],[[1,11,2],[2,14,1],[11,14,2],[1,14,11]]]
        intersects_for_cases[(1,0,1,0,0,0,1,0)] = [[[1,5,6],[1,6,2],[1,18,5],[14,18,1],[2,14,1],[5,18,6],[6,14,2],[14,6,18]],[[3,8,0],[0,12,3],[8,12,0],[3,12,8]]]
        intersects_for_cases[(1,0,1,0,0,0,1,1)] = [[[8,0,3],[3,12,8],[8,12,0],[0,12,3]],[[10,2,7],[7,2,1],[7,1,5],[7,19,10],[5,19,7],[19,5,18],[1,14,5],[5,14,18],[1,2,14],[10,14,2],[14,10,18],[18,10,19]]]
        intersects_for_cases[(1,0,1,0,0,1,0,0)] = [[[0,3,8],[0,12,3],[8,12,0],[3,12,8]],[[2,1,11],[2,14,1],[1,14,11],[11,14,2]],[[4,5,9],[9,17,4],[5,17,9],[4,17,5]]]
        intersects_for_cases[(1,0,1,0,0,1,0,1)] = [[[0,3,8],[0,12,3],[3,12,8],[8,12,0]],[[4,5,9],[5,17,9],[4,17,5],[9,17,4]],[[11,2,1],[11,14,2],[2,14,1],[1,14,11]],[[10,6,7],[10,19,6],[7,19,10],[6,19,7]]]
        intersects_for_cases[(1,0,1,0,0,1,1,0)] = [[[3,8,0],[0,12,3],[3,12,8],[8,12,0]],[[1,9,2],[2,9,4],[2,4,6],[2,14,1],[6,14,2],[14,6,18],[4,17,6],[6,17,18],[4,9,17],[1,17,9],[17,1,18],[18,1,14]]]
        intersects_for_cases[(1,0,1,0,0,1,1,1)] = [[[10,2,3],[9,0,1],[8,4,7],[0,12,3],[1,0,3],[3,2,1],[2,14,1],[17,18,4],[4,18,7],[7,18,19],[1,14,18],[1,18,9],[9,18,17],[3,12,8],[7,3,8],[10,3,7],[7,19,10],[2,18,14],[10,18,2],[19,18,10],[9,17,4],[4,0,9],[4,8,14],[8,12,0]]]
        intersects_for_cases[(1,0,1,0,1,0,0,0)] = [[[3,7,4],[3,4,0],[3,16,7],[12,16,3],[0,12,3],[7,16,4],[4,12,0],[12,4,16]],[[1,11,2],[2,14,1],[11,14,2],[1,14,11]]]
        intersects_for_cases[(1,0,1,0,1,0,0,1)] = [[[1,11,2],[2,14,1],[1,14,11],[11,14,2]],[[3,10,0],[0,10,6],[0,6,4],[0,12,3],[4,12,0],[12,4,16],[6,19,4],[4,19,16],[6,10,19],[3,19,10],[19,3,16],[16,3,12]]]
        intersects_for_cases[(1,0,1,0,1,0,1,0)] = [[[3,7,0],[7,4,0],[7,16,4],[0,12,3],[7,12,16],[12,7,3],[4,16,0],[0,16,12]],[[1,5,6],[1,6,2],[5,18,6],[2,14,1],[6,18,2],[14,2,18],[1,18,5],[18,1,14]]]
        intersects_for_cases[(1,0,1,0,1,0,1,1)] = [[[5,4,0],[1,5,0],[3,10,2],[4,16,12],[12,0,4],[19,18,10],[10,18,2],[2,18,14],[4,19,16],[5,19,4],[18,19,5],[0,12,3],[2,0,3],[1,0,2],[2,14,1],[5,13,1],[13,5,17],[10,16,19],[3,16,10],[12,16,3]]]
        intersects_for_cases[(1,0,1,0,1,1,0,0)] = [[[11,2,1],[1,14,11],[11,14,2],[2,14,1]],[[9,0,5],[5,0,3],[5,3,7],[5,17,9],[7,17,5],[17,7,16],[3,12,7],[7,12,16],[3,0,12],[9,12,0],[12,9,16],[16,9,17]]]
        intersects_for_cases[(1,0,1,0,1,1,0,1)] = [[[9,0,1],[10,2,3],[11,6,5],[2,14,1],[3,2,1],[1,0,3],[0,12,3],[19,16,6],[6,16,5],[5,16,17],[3,12,16],[3,16,10],[10,16,19],[1,14,11],[5,1,11],[9,1,5],[5,17,9],[0,16,12],[9,16,0],[17,16,9],[10,19,6],[6,2,10],[6,11,12],[11,14,2]]]
        intersects_for_cases[(1,0,1,0,1,1,1,0)] = [[[7,6,2],[3,7,2],[1,9,0],[6,18,14],[14,2,6],[17,16,9],[9,16,0],[0,16,12],[6,17,18],[7,17,6],[16,17,7],[2,14,1],[0,2,1],[3,2,0],[0,12,3],[7,15,3],[15,7,19],[9,18,17],[1,18,9],[14,18,1]]]
        intersects_for_cases[(1,0,1,0,1,1,1,1)] = [[[10,2,3],[0,1,9],[2,14,1],[2,1,0],[3,2,0],[0,12,3],[17,18,19],[19,16,17],[14,2,18],[10,18,2],[18,10,19],[16,12,0],[9,16,0],[16,9,17],[3,12,10],[19,10,12],[16,19,12],[1,14,18],[1,18,9],[18,17,9]]]
        intersects_for_cases[(1,0,1,1,0,0,0,0)] = [[[8,0,1],[8,1,11],[8,11,10],[8,12,0],[10,12,8],[12,10,15],[11,14,10],[10,14,15],[11,1,14],[0,14,1],[14,0,15],[15,0,12]]]
        intersects_for_cases[(1,0,1,1,0,0,0,1)] = [[[8,6,7],[8,11,6],[8,0,11],[0,1,11],[8,12,0],[1,14,11],[6,19,7],[8,15,12],[7,15,8],[19,15,7],[14,15,11],[11,15,6],[6,15,19],[0,12,15],[0,15,1],[1,15,14]]]
        intersects_for_cases[(1,0,1,1,0,0,1,0)] = [[[6,1,5],[6,10,8],[6,8,1],[1,8,0],[5,18,6],[1,18,5],[18,1,14],[8,12,0],[6,15,10],[15,6,18],[14,15,18],[10,12,8],[12,10,15],[12,15,0],[0,15,1],[14,1,15]]]
        intersects_for_cases[(1,0,1,1,0,0,1,1)] = [[[8,0,1],[7,8,1],[5,7,1],[1,0,12],[1,12,15],[14,1,15],[5,18,7],[19,7,18],[8,15,12],[7,15,8],[7,19,15],[5,1,14],[14,18,5],[8,12,0],[14,15,19],[19,18,14]]]
        intersects_for_cases[(1,0,1,1,0,1,0,0)] = [[[4,5,9],[9,17,4],[4,17,5],[5,17,9]],[[0,1,8],[8,1,11],[8,11,10],[8,12,0],[10,12,8],[12,10,15],[11,14,10],[10,14,15],[11,1,14],[0,14,1],[14,0,15],[15,0,12]]]
        intersects_for_cases[(1,0,1,1,0,1,0,1)] = [[[7,8,4],[1,9,0],[5,11,6],[9,17,4],[0,9,4],[4,8,0],[8,12,0],[14,15,11],[11,15,6],[6,15,19],[0,12,15],[0,15,1],[1,15,14],[4,17,5],[6,4,5],[7,4,6],[6,19,7],[8,15,12],[7,15,8],[19,15,7],[1,14,11],[11,9,1],[11,5,12],[5,17,9]]]
        intersects_for_cases[(1,0,1,1,0,1,1,0)] = [[[6,10,8],[4,6,8],[0,1,9],[10,15,12],[12,8,10],[14,18,1],[1,18,9],[9,18,17],[10,14,15],[6,14,10],[18,14,6],[8,12,0],[9,8,0],[4,8,9],[9,17,4],[6,16,4],[16,6,19],[1,15,14],[0,15,1],[12,15,0]]]
        intersects_for_cases[(1,0,1,1,0,1,1,1)] = [[[1,9,0],[8,4,7],[9,17,4],[9,4,8],[0,9,8],[8,12,0],[19,18,14],[14,15,19],[17,9,18],[1,18,9],[18,1,14],[15,12,8],[7,15,8],[15,7,19],[0,12,1],[14,1,12],[15,14,12],[4,17,18],[4,18,7],[18,19,7]]]
        intersects_for_cases[(1,0,1,1,1,0,0,0)] = [[[7,11,10],[7,0,11],[7,4,0],[0,1,11],[7,16,4],[1,14,11],[11,14,10],[15,10,14],[7,12,16],[10,12,7],[15,12,10],[4,12,0],[12,4,16],[1,0,14],[14,0,12],[14,12,15]]]
        intersects_for_cases[(1,0,1,1,1,0,0,1)] = [[[1,11,6],[0,1,6],[4,0,6],[6,11,14],[6,14,15],[19,6,15],[4,16,0],[12,0,16],[1,15,14],[0,15,1],[0,12,15],[4,6,19],[19,16,4],[1,14,11],[19,15,12],[12,16,19]]]
        intersects_for_cases[(1,0,1,1,1,0,1,0)] = [[[0,1,5],[4,0,5],[6,10,7],[1,14,18],[18,5,1],[15,12,10],[10,12,7],[7,12,16],[1,15,14],[0,15,1],[12,15,0],[5,18,6],[7,5,6],[4,5,7],[7,16,4],[0,17,4],[17,0,13],[10,14,15],[6,14,10],[18,14,6]]]
        intersects_for_cases[(1,0,1,1,1,0,1,1)] = [[[5,4,0],[1,5,0],[4,19,16],[5,19,4],[18,19,5],[12,15,0],[0,15,1],[1,15,14],[4,16,12],[4,12,0],[15,19,18],[18,14,15],[1,18,5],[18,1,14],[12,16,19],[19,15,12]]]
        intersects_for_cases[(1,0,1,1,1,1,0,0)] = [[[10,7,5],[11,10,5],[9,0,1],[7,16,17],[17,5,7],[12,15,0],[0,15,1],[1,15,14],[7,12,16],[10,12,7],[15,12,10],[5,17,9],[1,5,9],[11,5,1],[1,14,11],[10,18,11],[18,10,19],[0,16,12],[9,16,0],[17,16,9]]]
        intersects_for_cases[(1,0,1,1,1,1,0,1)] = [[[6,5,11],[1,9,0],[5,17,9],[5,9,1],[11,5,1],[1,14,11],[12,16,19],[19,15,12],[17,5,16],[6,16,5],[16,6,19],[15,14,1],[0,15,1],[15,0,12],[11,14,6],[19,6,14],[15,19,14],[9,17,16],[9,16,0],[16,12,0]]]
        intersects_for_cases[(1,0,1,1,1,1,1,0)] = [[[10,7,6],[9,0,1],[7,16,4],[7,17,6],[18,6,17],[0,12,15],[0,15,1],[14,1,15],[16,7,12],[10,12,7],[12,10,15],[18,17,9],[1,18,9],[1,14,18],[6,18,10],[15,10,18],[14,15,18],[16,12,0],[9,16,0],[17,16,9]]]
        intersects_for_cases[(1,0,1,1,1,1,1,1)] = [[[1,9,0],[14,1,0],[14,0,12],[14,12,15],[16,9,17],[9,16,0],[0,16,12],[14,18,1],[1,18,17],[1,17,9],[16,19,15],[15,12,16],[19,18,14],[14,15,19],[16,17,18],[18,19,16]]]
        intersects_for_cases[(1,1,0,0,0,0,0,0)] = [[[1,3,8],[1,8,9],[1,12,3],[13,12,1],[9,13,1],[3,12,8],[8,13,9],[13,8,12]]]
        intersects_for_cases[(1,1,0,0,0,0,0,1)] = [[[8,9,1],[8,1,3],[8,13,9],[12,13,8],[3,12,8],[9,13,1],[1,12,3],[12,1,13]],[[10,6,7],[7,19,10],[6,19,7],[10,19,6]]]
        intersects_for_cases[(1,1,0,0,0,0,1,0)] = [[[1,3,8],[1,8,9],[1,12,3],[13,12,1],[9,13,1],[3,12,8],[8,13,9],[13,8,12]],[[5,6,11],[11,18,5],[6,18,11],[5,18,6]]]
        intersects_for_cases[(1,1,0,0,0,0,1,1)] = [[[8,9,3],[9,1,3],[9,13,1],[3,12,8],[9,12,13],[12,9,8],[1,13,3],[3,13,12]],[[10,11,5],[10,5,7],[11,18,5],[7,19,10],[5,18,7],[19,7,18],[10,18,11],[18,10,19]]]
        intersects_for_cases[(1,1,0,0,0,1,0,0)] = [[[3,8,4],[3,4,5],[3,5,1],[3,12,8],[1,12,3],[12,1,13],[5,17,1],[1,17,13],[5,4,17],[8,17,4],[17,8,13],[13,8,12]]]
        intersects_for_cases[(1,1,0,0,0,1,0,1)] = [[[10,6,7],[7,19,10],[10,19,6],[6,19,7]],[[8,4,3],[3,4,5],[3,5,1],[3,12,8],[1,12,3],[12,1,13],[5,17,1],[1,17,13],[5,4,17],[8,17,4],[17,8,13],[13,8,12]]]
        intersects_for_cases[(1,1,0,0,0,1,1,0)] = [[[8,1,3],[8,4,6],[8,6,1],[1,6,11],[3,12,8],[1,12,3],[12,1,13],[6,18,11],[8,17,4],[17,8,12],[13,17,12],[4,18,6],[18,4,17],[18,17,11],[11,17,1],[13,1,17]]]
        intersects_for_cases[(1,1,0,0,0,1,1,1)] = [[[11,1,3],[10,11,3],[8,4,7],[1,13,12],[12,3,1],[17,18,4],[4,18,7],[7,18,19],[1,17,13],[11,17,1],[18,17,11],[3,12,8],[7,3,8],[10,3,7],[7,19,10],[11,15,10],[15,11,14],[4,13,17],[8,13,4],[12,13,8]]]
        intersects_for_cases[(1,1,0,0,1,0,0,0)] = [[[7,4,9],[7,9,1],[7,1,3],[7,16,4],[3,16,7],[16,3,12],[1,13,3],[3,13,12],[1,9,13],[4,13,9],[13,4,12],[12,4,16]]]
        intersects_for_cases[(1,1,0,0,1,0,0,1)] = [[[10,1,3],[10,4,1],[10,6,4],[4,9,1],[10,19,6],[9,13,1],[1,13,3],[12,3,13],[10,16,19],[3,16,10],[12,16,3],[6,16,4],[16,6,19],[9,4,13],[13,4,16],[13,16,12]]]
        intersects_for_cases[(1,1,0,0,1,0,1,0)] = [[[6,11,5],[5,18,6],[6,18,11],[11,18,5]],[[4,9,7],[7,9,1],[7,1,3],[7,16,4],[3,16,7],[16,3,12],[1,13,3],[3,13,12],[1,9,13],[4,13,9],[13,4,12],[12,4,16]]]
        intersects_for_cases[(1,1,0,0,1,0,1,1)] = [[[3,10,11],[1,3,11],[5,4,9],[10,19,18],[18,11,10],[16,12,4],[4,12,9],[9,12,13],[10,16,19],[3,16,10],[12,16,3],[11,18,5],[9,11,5],[1,11,9],[9,13,1],[3,14,1],[14,3,15],[4,19,16],[5,19,4],[18,19,5]]]
        intersects_for_cases[(1,1,0,0,1,1,0,0)] = [[[3,7,5],[1,3,5],[1,12,3],[12,1,13],[5,13,1],[13,5,17],[7,16,5],[17,5,16],[3,16,7],[16,3,12],[16,12,13],[16,13,17]]]
        intersects_for_cases[(1,1,0,0,1,1,0,1)] = [[[10,6,5],[3,10,5],[1,3,5],[5,6,19],[5,19,16],[17,5,16],[1,13,3],[12,3,13],[10,16,19],[3,16,10],[3,12,16],[1,5,17],[17,13,1],[10,19,6],[17,16,12],[12,13,17]]]
        intersects_for_cases[(1,1,0,0,1,1,1,0)] = [[[6,11,1],[7,6,1],[3,7,1],[1,11,18],[1,18,17],[13,1,17],[3,12,7],[16,7,12],[6,17,18],[7,17,6],[7,16,17],[3,1,13],[13,12,3],[6,18,11],[13,17,16],[16,12,13]]]
        intersects_for_cases[(1,1,0,0,1,1,1,1)] = [[[3,10,11],[1,3,11],[10,16,19],[3,16,10],[12,16,3],[18,17,11],[11,17,1],[1,17,13],[10,19,18],[10,18,11],[17,16,12],[12,13,17],[1,12,3],[12,1,13],[18,19,16],[16,17,18]]]
        intersects_for_cases[(1,1,0,1,0,0,0,0)] = [[[9,1,2],[9,2,10],[9,10,8],[9,13,1],[8,13,9],[13,8,12],[10,15,8],[8,15,12],[10,2,15],[1,15,2],[15,1,12],[12,1,13]]]
        intersects_for_cases[(1,1,0,1,0,0,0,1)] = [[[7,2,6],[7,8,9],[7,9,2],[2,9,1],[6,19,7],[2,19,6],[19,2,15],[9,13,1],[7,12,8],[12,7,19],[15,12,19],[8,13,9],[13,8,12],[13,12,1],[1,12,2],[15,2,12]]]
        intersects_for_cases[(1,1,0,1,0,0,1,0)] = [[[5,6,11],[11,18,5],[5,18,6],[6,18,11]],[[1,2,9],[9,2,10],[9,10,8],[9,13,1],[8,13,9],[13,8,12],[10,15,8],[8,15,12],[10,2,15],[1,15,2],[15,1,12],[12,1,13]]]
        intersects_for_cases[(1,1,0,1,0,0,1,1)] = [[[7,8,9],[5,7,9],[1,2,11],[8,12,13],[13,9,8],[15,19,2],[2,19,11],[11,19,18],[8,15,12],[7,15,8],[19,15,7],[9,13,1],[11,9,1],[5,9,11],[11,18,5],[7,17,5],[17,7,16],[2,12,15],[1,12,2],[13,12,1]]]
        intersects_for_cases[(1,1,0,1,0,1,0,0)] = [[[2,5,1],[2,8,5],[2,10,8],[8,4,5],[2,15,10],[4,17,5],[5,17,1],[13,1,17],[2,12,15],[1,12,2],[13,12,1],[10,12,8],[12,10,15],[4,8,17],[17,8,12],[17,12,13]]]
        intersects_for_cases[(1,1,0,1,0,1,0,1)] = [[[1,2,6],[5,1,6],[7,8,4],[2,15,19],[19,6,2],[12,13,8],[8,13,4],[4,13,17],[2,12,15],[1,12,2],[13,12,1],[6,19,7],[4,6,7],[5,6,4],[4,17,5],[1,18,5],[18,1,14],[8,15,12],[7,15,8],[19,15,7]]]
        intersects_for_cases[(1,1,0,1,0,1,1,0)] = [[[8,4,6],[10,8,6],[11,1,2],[4,17,18],[18,6,4],[13,12,1],[1,12,2],[2,12,15],[4,13,17],[8,13,4],[12,13,8],[6,18,11],[2,6,11],[10,6,2],[2,15,10],[8,19,10],[19,8,16],[1,17,13],[11,17,1],[18,17,11]]]
        intersects_for_cases[(1,1,0,1,0,1,1,1)] = [[[8,4,7],[11,1,2],[4,17,5],[4,18,7],[19,7,18],[1,13,12],[1,12,2],[15,2,12],[17,4,13],[8,13,4],[13,8,12],[19,18,11],[2,19,11],[2,15,19],[7,19,8],[12,8,19],[15,12,19],[17,13,1],[11,17,1],[18,17,11]]]
        intersects_for_cases[(1,1,0,1,1,0,0,0)] = [[[2,9,1],[2,4,9],[2,10,4],[10,7,4],[2,15,10],[7,16,4],[9,13,1],[2,12,15],[1,12,2],[13,12,1],[16,12,4],[4,12,9],[9,12,13],[10,15,12],[10,12,7],[7,12,16]]]
        intersects_for_cases[(1,1,0,1,1,0,0,1)] = [[[9,1,2],[4,9,2],[6,4,2],[2,1,13],[2,13,12],[15,2,12],[6,19,4],[16,4,19],[9,12,13],[4,12,9],[4,16,12],[6,2,15],[15,19,6],[9,13,1],[15,12,16],[16,19,15]]]
        intersects_for_cases[(1,1,0,1,1,0,1,0)] = [[[1,2,11],[7,6,10],[5,4,9],[6,18,11],[10,6,11],[11,2,10],[2,15,10],[16,12,4],[4,12,9],[9,12,13],[10,15,12],[10,12,7],[7,12,16],[11,18,5],[9,11,5],[1,11,9],[9,13,1],[2,12,15],[1,12,2],[13,12,1],[7,16,4],[4,6,7],[4,5,15],[5,18,6]]]
        intersects_for_cases[(1,1,0,1,1,0,1,1)] = [[[4,9,5],[11,1,2],[9,13,1],[9,1,11],[5,9,11],[11,18,5],[15,12,16],[16,19,15],[13,9,12],[4,12,9],[12,4,16],[19,18,11],[2,19,11],[19,2,15],[5,18,4],[16,4,18],[19,16,18],[1,13,12],[1,12,2],[12,15,2]]]
        intersects_for_cases[(1,1,0,1,1,1,0,0)] = [[[2,10,7],[1,2,7],[5,1,7],[7,10,15],[7,15,12],[16,7,12],[5,17,1],[13,1,17],[2,12,15],[1,12,2],[1,13,12],[5,7,16],[16,17,5],[2,15,10],[16,12,13],[13,17,16]]]
        intersects_for_cases[(1,1,0,1,1,1,0,1)] = [[[1,2,6],[5,1,6],[2,12,15],[1,12,2],[13,12,1],[19,16,6],[6,16,5],[5,16,17],[2,15,19],[2,19,6],[16,12,13],[13,17,16],[5,13,1],[13,5,17],[19,15,12],[12,16,19]]]
        intersects_for_cases[(1,1,0,1,1,1,1,0)] = [[[7,6,10],[2,11,1],[6,18,11],[6,11,2],[10,6,2],[2,15,10],[13,17,16],[16,12,13],[18,6,17],[7,17,6],[17,7,16],[12,15,2],[1,12,2],[12,1,13],[10,15,7],[16,7,15],[12,16,15],[11,18,17],[11,17,1],[17,13,1]]]
        intersects_for_cases[(1,1,0,1,1,1,1,1)] = [[[11,1,2],[18,11,2],[18,2,15],[18,15,19],[12,1,13],[1,12,2],[2,12,15],[18,17,11],[11,17,13],[11,13,1],[12,16,19],[19,15,12],[16,17,18],[18,19,16],[12,13,17],[17,16,12]]]
        intersects_for_cases[(1,1,1,0,0,0,0,0)] = [[[11,2,3],[11,3,8],[11,8,9],[11,14,2],[9,14,11],[14,9,13],[8,12,9],[9,12,13],[8,3,12],[2,12,3],[12,2,13],[13,2,14]]]
        intersects_for_cases[(1,1,1,0,0,0,0,1)] = [[[6,7,10],[10,19,6],[6,19,7],[7,19,10]],[[2,3,11],[11,3,8],[11,8,9],[11,14,2],[9,14,11],[14,9,13],[8,12,9],[9,12,13],[8,3,12],[2,12,3],[12,2,13],[13,2,14]]]
        intersects_for_cases[(1,1,1,0,0,0,1,0)] = [[[3,6,2],[3,9,6],[3,8,9],[9,5,6],[3,12,8],[5,18,6],[6,18,2],[14,2,18],[3,13,12],[2,13,3],[14,13,2],[8,13,9],[13,8,12],[5,9,18],[18,9,13],[18,13,14]]]
        intersects_for_cases[(1,1,1,0,0,0,1,1)] = [[[9,5,7],[8,9,7],[10,2,3],[5,18,19],[19,7,5],[14,13,2],[2,13,3],[3,13,12],[5,14,18],[9,14,5],[13,14,9],[7,19,10],[3,7,10],[8,7,3],[3,12,8],[9,16,8],[16,9,17],[2,18,14],[10,18,2],[19,18,10]]]
        intersects_for_cases[(1,1,1,0,0,1,0,0)] = [[[3,11,2],[3,5,11],[3,8,5],[8,4,5],[3,12,8],[4,17,5],[11,14,2],[3,13,12],[2,13,3],[14,13,2],[17,13,5],[5,13,11],[11,13,14],[8,12,13],[8,13,4],[4,13,17]]]
        intersects_for_cases[(1,1,1,0,0,1,0,1)] = [[[2,3,10],[4,7,8],[6,5,11],[7,19,10],[8,7,10],[10,3,8],[3,12,8],[17,13,5],[5,13,11],[11,13,14],[8,12,13],[8,13,4],[4,13,17],[10,19,6],[11,10,6],[2,10,11],[11,14,2],[3,13,12],[2,13,3],[14,13,2],[4,17,5],[5,7,4],[5,6,12],[6,19,7]]]
        intersects_for_cases[(1,1,1,0,0,1,1,0)] = [[[3,8,4],[2,3,4],[6,2,4],[4,8,12],[4,12,13],[17,4,13],[6,18,2],[14,2,18],[3,13,12],[2,13,3],[2,14,13],[6,4,17],[17,18,6],[3,12,8],[17,13,14],[14,18,17]]]
        intersects_for_cases[(1,1,1,0,0,1,1,1)] = [[[2,3,10],[7,8,4],[3,12,8],[3,8,7],[10,3,7],[7,19,10],[17,13,14],[14,18,17],[12,3,13],[2,13,3],[13,2,14],[18,19,7],[4,18,7],[18,4,17],[10,19,2],[14,2,19],[18,14,19],[8,12,13],[8,13,4],[13,17,4]]]
        intersects_for_cases[(1,1,1,0,1,0,0,0)] = [[[2,9,11],[2,3,7],[2,7,9],[9,7,4],[11,14,2],[9,14,11],[14,9,13],[7,16,4],[2,12,3],[12,2,14],[13,12,14],[3,16,7],[16,3,12],[16,12,4],[4,12,9],[13,9,12]]]
        intersects_for_cases[(1,1,1,0,1,0,0,1)] = [[[4,9,11],[6,4,11],[2,3,10],[9,13,14],[14,11,9],[12,16,3],[3,16,10],[10,16,19],[9,12,13],[4,12,9],[16,12,4],[11,14,2],[10,11,2],[6,11,10],[10,19,6],[4,18,6],[18,4,17],[3,13,12],[2,13,3],[14,13,2]]]
        intersects_for_cases[(1,1,1,0,1,0,1,0)] = [[[2,3,7],[6,2,7],[4,9,5],[3,12,16],[16,7,3],[13,14,9],[9,14,5],[5,14,18],[3,13,12],[2,13,3],[14,13,2],[7,16,4],[5,7,4],[6,7,5],[5,18,6],[2,19,6],[19,2,15],[9,12,13],[4,12,9],[16,12,4]]]
        intersects_for_cases[(1,1,1,0,1,0,1,1)] = [[[3,10,2],[5,4,9],[10,19,6],[10,18,2],[14,2,18],[4,16,12],[4,12,9],[13,9,12],[19,10,16],[3,16,10],[16,3,12],[14,18,5],[9,14,5],[9,13,14],[2,14,3],[12,3,14],[13,12,14],[19,16,4],[5,19,4],[18,19,5]]]
        intersects_for_cases[(1,1,1,0,1,1,0,0)] = [[[11,2,3],[5,11,3],[7,5,3],[3,2,14],[3,14,13],[12,3,13],[7,16,5],[17,5,16],[11,13,14],[5,13,11],[5,17,13],[7,3,12],[12,16,7],[11,14,2],[12,13,17],[17,16,12]]]
        intersects_for_cases[(1,1,1,0,1,1,0,1)] = [[[3,10,2],[11,6,5],[10,19,6],[10,6,11],[2,10,11],[11,14,2],[17,16,12],[12,13,17],[19,10,16],[3,16,10],[16,3,12],[13,14,11],[5,13,11],[13,5,17],[2,14,3],[12,3,14],[13,12,14],[6,19,16],[6,16,5],[16,17,5]]]
        intersects_for_cases[(1,1,1,0,1,1,1,0)] = [[[2,3,7],[6,2,7],[3,13,12],[2,13,3],[14,13,2],[16,17,7],[7,17,6],[6,17,18],[3,12,16],[3,16,7],[17,13,14],[14,18,17],[6,14,2],[14,6,18],[16,12,13],[13,17,16]]]
        intersects_for_cases[(1,1,1,0,1,1,1,1)] = [[[3,10,2],[12,3,2],[12,2,14],[12,14,13],[18,10,19],[10,18,2],[2,18,14],[12,16,3],[3,16,19],[3,19,10],[18,17,13],[13,14,18],[17,16,12],[12,13,17],[18,19,16],[16,17,18]]]
        intersects_for_cases[(1,1,1,1,0,0,0,0)] = [[[10,8,9],[11,10,9],[11,15,10],[15,11,14],[9,14,11],[14,9,13],[8,12,9],[13,9,12],[10,12,8],[12,10,15],[12,15,14],[12,14,13]]]
        intersects_for_cases[(1,1,1,1,0,0,0,1)] = [[[6,7,8],[11,6,8],[9,11,8],[8,7,19],[8,19,15],[12,8,15],[9,13,11],[14,11,13],[6,15,19],[11,15,6],[11,14,15],[9,8,12],[12,13,9],[6,19,7],[12,15,14],[14,13,12]]]
        intersects_for_cases[(1,1,1,1,0,0,1,0)] = [[[5,6,10],[9,5,10],[8,9,10],[10,6,18],[10,18,14],[15,10,14],[8,12,9],[13,9,12],[5,14,18],[9,14,5],[9,13,14],[8,10,15],[15,12,8],[5,18,6],[15,14,13],[13,12,15]]]
        intersects_for_cases[(1,1,1,1,0,0,1,1)] = [[[9,5,7],[8,9,7],[5,14,18],[9,14,5],[13,14,9],[19,15,7],[7,15,8],[8,15,12],[5,18,19],[5,19,7],[15,14,13],[13,12,15],[8,13,9],[13,8,12],[19,18,14],[14,15,19]]]
        intersects_for_cases[(1,1,1,1,0,1,0,0)] = [[[4,5,11],[8,4,11],[10,8,11],[11,5,17],[11,17,13],[14,11,13],[10,15,8],[12,8,15],[4,13,17],[8,13,4],[8,12,13],[10,11,14],[14,15,10],[4,17,5],[14,13,12],[12,15,14]]]
        intersects_for_cases[(1,1,1,1,0,1,0,1)] = [[[8,4,7],[6,5,11],[4,17,5],[4,5,6],[7,4,6],[6,19,7],[14,13,12],[12,15,14],[17,4,13],[8,13,4],[13,8,12],[15,19,6],[11,15,6],[15,11,14],[7,19,8],[12,8,19],[15,12,19],[5,17,13],[5,13,11],[13,14,11]]]
        intersects_for_cases[(1,1,1,1,0,1,1,0)] = [[[8,4,6],[10,8,6],[4,13,17],[8,13,4],[12,13,8],[18,14,6],[6,14,10],[10,14,15],[4,17,18],[4,18,6],[14,13,12],[12,15,14],[10,12,8],[12,10,15],[18,17,13],[13,14,18]]]
        intersects_for_cases[(1,1,1,1,0,1,1,1)] = [[[8,4,7],[12,8,7],[12,7,19],[12,19,15],[18,4,17],[4,18,7],[7,18,19],[12,13,8],[8,13,17],[8,17,4],[18,14,15],[15,19,18],[14,13,12],[12,15,14],[18,17,13],[13,14,18]]]
        intersects_for_cases[(1,1,1,1,1,0,0,0)] = [[[7,4,9],[10,7,9],[11,10,9],[9,4,16],[9,16,12],[13,9,12],[11,14,10],[15,10,14],[7,12,16],[10,12,7],[10,15,12],[11,9,13],[13,14,11],[7,16,4],[13,12,15],[15,14,13]]]
        intersects_for_cases[(1,1,1,1,1,0,0,1)] = [[[4,9,11],[6,4,11],[9,12,13],[4,12,9],[16,12,4],[14,15,11],[11,15,6],[6,15,19],[9,13,14],[9,14,11],[15,12,16],[16,19,15],[6,16,4],[16,6,19],[14,13,12],[12,15,14]]]
        intersects_for_cases[(1,1,1,1,1,0,1,0)] = [[[10,7,6],[5,4,9],[7,16,4],[7,4,5],[6,7,5],[5,18,6],[13,12,15],[15,14,13],[16,7,12],[10,12,7],[12,10,15],[14,18,5],[9,14,5],[14,9,13],[6,18,10],[15,10,18],[14,15,18],[4,16,12],[4,12,9],[12,13,9]]]
        intersects_for_cases[(1,1,1,1,1,0,1,1)] = [[[9,5,4],[13,9,4],[13,4,16],[13,16,12],[19,5,18],[5,19,4],[4,19,16],[13,14,9],[9,14,18],[9,18,5],[19,15,12],[12,16,19],[15,14,13],[13,12,15],[19,18,14],[14,15,19]]]
        intersects_for_cases[(1,1,1,1,1,1,0,0)] = [[[10,7,5],[11,10,5],[7,12,16],[10,12,7],[15,12,10],[17,13,5],[5,13,11],[11,13,14],[7,16,17],[7,17,5],[13,12,15],[15,14,13],[11,15,10],[15,11,14],[17,16,12],[12,13,17]]]
        intersects_for_cases[(1,1,1,1,1,1,0,1)] = [[[11,6,5],[14,11,5],[14,5,17],[14,17,13],[16,6,19],[6,16,5],[5,16,17],[14,15,11],[11,15,19],[11,19,6],[16,12,13],[13,17,16],[12,15,14],[14,13,12],[16,19,15],[15,12,16]]]
        intersects_for_cases[(1,1,1,1,1,1,1,0)] = [[[10,7,6],[15,10,6],[15,6,18],[15,18,14],[17,7,16],[7,17,6],[6,17,18],[15,12,10],[10,12,16],[10,16,7],[17,13,14],[14,18,17],[13,12,15],[15,14,13],[17,16,12],[12,13,17]]]
        intersects_for_cases[(1,1,1,1,1,1,1,1)] = ['all_triangulated']

        return intersects_for_cases

    '''
    Funcion para determinar si el punto esta dentro o sobre el cubo.
    '''
    def inCube(self,point,bound_error):
        if (point.x >= self.xmin-bound_error and point.x <= self.xmax+bound_error):
            if (point.y >= self.ymin-bound_error and point.y <= self.ymax+bound_error):
                if (point.z >= self.zmin-bound_error and point.z <= self.zmax+bound_error):
                    return True

        return False

'''
Funcion que evalua los triangulos cuyos bounding box colisionan
con el cubo, para cada coordenada.
'''
def search_collisions(min_coord,max_coord,bounding_boxes,min_b_boxes,max_b_boxes,depth):
  flag,bound = True,0
  len_bounding_boxes = len(bounding_boxes)
  #print ('lenbboxes = ',len_bounding_boxes)
  #if (min_coord >= min_b_boxes and max_coord <= max_b_boxes):
  if (min_coord >= min_b_boxes and max_coord <= max_b_boxes):
    bound = binary_search(max_coord,bounding_boxes,len_bounding_boxes,depth,1)
    bounding_boxes = bounding_boxes[:bound]
    bounding_boxes.sort(key=lambda x:x[depth*2+1])  
    bound = binary_search(min_coord,bounding_boxes,len_bounding_boxes,depth,0)
    bounding_boxes = bounding_boxes[bound:]
  elif (max_coord > min_b_boxes and min_coord < min_b_boxes):
  #elif (max_coord >= min_b_boxes and min_coord <= min_b_boxes):
    bound = binary_search(max_coord,bounding_boxes,len_bounding_boxes,depth,1)
    bounding_boxes = bounding_boxes[:bound]
  elif (min_coord < max_b_boxes and max_coord > max_b_boxes):
  #elif (min_coord <= max_b_boxes and max_coord >= max_b_boxes):
    bound = binary_search(min_coord,bounding_boxes,len_bounding_boxes,depth,0)
    bounding_boxes.sort(key=lambda x:x[depth*2+1])
    bounding_boxes = bounding_boxes[bound:]
  else:
    flag = False
  return flag,bounding_boxes

  #if (min_coord >= min_b_boxes and max_coord <= max_b_boxes):
  #  bound = binary_search(max_coord,bounding_boxes,depth,1)
  #  bounding_boxes = bounding_boxes[:bound]
  #  bounding_boxes.sort(key=lambda x:x[depth*2+1])
  #  #bounding_boxes.sort(key=lambda x:x[depth*2])  
  #  bound = binary_search(min_coord,bounding_boxes,depth,0)
  #  bounding_boxes = bounding_boxes[bound:]
  #elif (max_coord >= min_b_boxes and min_coord < min_b_boxes):
  #elif (max_coord >= min_b_boxes and min_coord < min_b_boxes and max_coord <= min_b_boxes):
  #  bound = binary_search(max_coord,bounding_boxes,depth,1)
  #  bounding_boxes = bounding_boxes[:bound]
  #elif (min_coord <= max_b_boxes and max_coord > max_b_boxes):
  #elif (min_coord <= max_b_boxes and max_coord > max_b_boxes and min_coord >= min_b_boxes):
  #  bound = binary_search(min_coord,bounding_boxes,depth,0)
  #  #bounding_boxes.sort(key=lambda x:x[depth*2+1])
  #  bounding_boxes = bounding_boxes[bound:]
  #else:
  #  flag = False
  #return flag,bounding_boxes

'''
Funcion para efectuar la busqueda binaria, cuyo objetivo es determinar la posicion de los triangulos que intersectan al cubo.
'''
'''
def binary_search(coord_cube,coord_bounding_boxes,len_bounding_boxes,depth,option):
  N = len(coord_bounding_boxes)-1
  founded_value = 0
  if N > 0:
    lo,hi = 0,N
    if (option == 0):
      while lo+1!=hi:
        mid = lo+(hi-lo)//2
        if coord_bounding_boxes[mid][depth*2+1] < coord_cube:
          lo = mid
        else:
          hi = mid

      founded_value = coord_bounding_boxes[hi][depth*2+1]
      #print ('range = ',range(0,hi))
      positions_to_evaluate = list(range(0,hi,-1))

      for i in positions_to_evaluate:
        #print ('positions_to_evaluate[',i,'] = ')
        if(coord_bounding_boxes[i][depth*2+1] < founded_value):
          return i
          break
      
    else:
      while lo+1!=hi:
        mid = lo+(hi-lo)//2
        if coord_bounding_boxes[mid][depth*2] < coord_cube:
          lo = mid
        else:
          hi = mid

      founded_value = coord_bounding_boxes[hi][depth*2]
      #print ('range = ',range(hi,len_bounding_boxes))
      positions_to_evaluate = list(range(hi,len_bounding_boxes))

      #print ('positions_to_evaluate = ',positions_to_evaluate)
      for i in positions_to_evaluate:
        #print ('positions_to_evaluate[',i,']')
        #print ('len_coord_bounding_boxes = ',len(coord_bounding_boxes))
        #print ('bb = 12',coord_bounding_boxes[12],'profundidad = ',depth*2)
        if(coord_bounding_boxes[i][depth*2] > founded_value):
          return i
          break
'''

#def binary_search(coord_cube,coord_bounding_boxes,depth,option):
def binary_search(coord_cube,coord_bounding_boxes,len_bounding_boxes,depth,option):
  # Problema esta aca.
  N = len(coord_bounding_boxes)-1
  if N > 0:
    lo,hi = 0,N
    if (option == 0):
      while lo+1!=hi:
        mid = lo+(hi-lo)//2
        if coord_bounding_boxes[mid][depth*2+1] <= coord_cube:
          lo = mid
        else:
          hi = mid

      return hi

    else:
      while lo+1!=hi:
        mid = lo+(hi-lo)//2
        if coord_bounding_boxes[mid][depth*2+0] <= coord_cube:
          lo = mid
        else:
          hi = mid

      return hi

'''
Funcion para determinar si las coordenadas pasadas como parametro estan dentro
del rango dado.
'''
def checkrange(x0,x1,min_coord,max_coord):
  if (x0 >= min_coord and x1 <= max_coord):
    return True
  else:
    return False

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
