# -*- coding: utf-8 -*-
from geometry.controller.geometry_2d.point_2d import Point2D
from geometry.controller.geometry_3d.point_3d import Point3d
from geometry.controller.geometry_2d.segment_2d import Segment2D
from geometry.controller.geometry_3d.segment_3d import Segment3d
from geometry.controller.geometry_3d.cube_3d import Cube3d
from geometry.controller.geometry_3d.solid_3d import Solid3d
from geometry.controller.geometry_3d.triangle_3d import Triangle3d
from geometry.controller.geometry_3d.polygon_3d import Polygon3d
from geometry.controller.geometry_3d.face_3d import Face3d
from geometry.controller.geometry_3d.tetrahedron_3d import Tetrahedron3d
import matplotlib.pyplot as plt
import math
import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule
import numpy

class Mesh3d(object):

    def __init__(self, name='', rowid=-1):
        self.listOptions = []
        self.rowid = rowid
        self.name = name

    '''
    Funcion para crear malla de puntos.
    '''
    def CreateMesh(self,solid,cubes):
        '''
        Crear diccionario de puntos.
        '''
        points_mesh = {}
    
        '''
        Definir arreglo de indicadores. Para cada cubo se almacenara, para cada vertice, un indicador que sera de "1" si el punto se halla
        dentro del solido, y "0" si esta fuera.
        '''
        #list_options = []
    
        '''
        Calcular centroide del solido.
        '''
        centroid_solid = solid.getCentroid()
    
        for cube in cubes:
            '''
            Obtener el total de puntos del cubo.
            '''
            lpoints = cube.getPointsCube()

            '''
            Definir arreglo de opciones para los puntos del cubo en cuestion.
            '''
            options_cube = []
        
            for point in lpoints:
                pt = (round(point.x,8), round(point.y,8), round(point.z,8)) 
                if pt in points_mesh:
                    options_cube.append(points_mesh[pt])
                else:
                    if (solid.isPointInSolid(centroid_solid,point) is True):
                        points_mesh[pt] = 1
                        options_cube.append(1)
                    else:
                        points_mesh[pt] = 0
                        options_cube.append(0)

            self.listOptions.append(options_cube)

    '''
    Funcion para crear malla de puntos.
    '''
    def CreateMesh2(self,solid,centroid_solid,cubes):
        '''
        Crear diccionario de puntos.
        '''
        points_mesh = {}
        cube_evaluating = []
    
        #'''
        #Calcular centroide del solido.
        #'''
        #centroid_solid = solid.getCentroid()
    
        '''
        Definir arreglo de indicadores. Para cada cubo se almacenara, para cada vertice, un indicador que sera de "1" si el punto se halla
        dentro del solido, y "0" si esta fuera.
        '''
        for index_cube in range(0,len(cubes)):
            '''
            Obtener el total de puntos del cubo.
            '''
            lpoints_for_cube = cubes[index_cube].getPointsCube()
            lpoints = cubes[index_cube].getPointsCube()
            cube_evaluating.append(lpoints_for_cube)
            cube_evaluating[index_cube].append([0,0,0,0,0,0,0,0])
            cube_evaluating[index_cube].append([0,0,0,0,0,0,0,0])

            '''
            Definir arreglo de opciones para los puntos del cubo en cuestion.
            '''
            options_cube = []
            
            for point in lpoints:
                pt = (round(point.x,8), round(point.y,8), round(point.z,8)) 
                if pt in points_mesh:
                    points_mesh[pt].append(index_cube)
                else:
                    points_mesh[pt] = [0,index_cube]

        points_mesh_evaluated = {}
    
        for triangle in solid.triangles:
        
            tetrahedron = Tetrahedron3d(triangle.p0,triangle.p1,triangle.p2)
            points_delete = []
        
            for point in points_mesh:
                state = tetrahedron.isPointInTetrahedron(centroid_solid,Point3d(point[0],point[1],point[2]))
                if (state is True):
                    points_mesh_evaluated[point] = points_mesh[point]
                    points_mesh_evaluated[point][0] = triangle
                    points_delete.append(point)

            for point in points_delete:
                del points_mesh[point]

        #for p in points_mesh_evaluated:
        #    print ('point_mesh_evaluated = ',points_mesh_evaluated[p])
        for cube in cube_evaluating:
            for point in range(0,8):
                pt = (round(cube[point].x,8), round(cube[point].y,8), round(cube[point].z,8))
                if pt in points_mesh_evaluated:
                    cube[8][point] = 1
                    cube[9][point] = points_mesh_evaluated[pt][0]

        return cube_evaluating

    '''
    Funcion para crear malla de puntos.
    '''
    def CreateMesh3(self,solid,cubes):
        '''
        Crear diccionario de puntos.
        '''
        points_mesh = {}
        cube_evaluating = []
    
        '''
        Definir arreglo de indicadores. Para cada cubo se almacenara, para cada vertice, un indicador que sera de "1" si el punto se halla
        dentro del solido, y "0" si esta fuera.
        '''
        for index_cube in range(0,len(cubes)):
            '''
            Obtener el total de puntos del cubo.
            '''
            lpoints_for_cube = cubes[index_cube].getPointsCube()
            lpoints = cubes[index_cube].getPointsCube()
            cube_evaluating.append(lpoints_for_cube)
            cube_evaluating[index_cube].append([0,0,0,0,0,0,0,0])

            '''
            Definir arreglo de opciones para los puntos del cubo en cuestion.
            '''
            options_cube = []
            
            for point in lpoints:
                pt = (round(point.x,8), round(point.y,8), round(point.z,8)) 
                if pt in points_mesh:
                    #options_cube.append(points_mesh[pt][0])
                    points_mesh[pt].append(index_cube)
                else:
                    points_mesh[pt] = [0,index_cube]
                    #if (solid.isPointInSolid(centroid_solid,point) is True):
                    #    points_mesh[pt] = [1,index_cube]
                    #    options_cube.append(1)
                    #else:
                    #    points_mesh[pt] = [0,index_cube]
                    #    options_cube.append(0)

            #self.listOptions.append(options_cube)

        points_mesh_evaluated = {}
    
        for triangle in solid.triangles:
        
            tetrahedron = Tetrahedron3d(triangle.p0,triangle.p1,triangle.p2)
            points_delete = []
        
            for point in points_mesh:
                state = tetrahedron.isPointInTetrahedron(centroid_solid,Point3d(point[0],point[1],point[2]))
                if (state is True):
                    #pt = (round(point.x,8), round(point.y,8), round(point.z,8))
                    points_mesh_evaluated[point] = points_mesh[point]
                    points_mesh_evaluated[point][0] = 1
                    points_delete.append(point)

            for point in points_delete:
                del points_mesh[point]
                
        #print (points_mesh_evaluated,len(points_mesh_evaluated))

        for cube in cube_evaluating:
            for point in range(0,8):
                pt = (round(cube[point].x,8), round(cube[point].y,8), round(cube[point].z,8))
                if pt in points_mesh_evaluated:
                    cube[8][point] = 1

        return points_mesh_evaluated

    '''
    Funcion para crear malla de puntos.
    '''
    def CreateMesh4(self,solid,centroid_solid,cubes):
        '''
        Crear diccionario de puntos.
        '''
        points_mesh = {}
        cube_evaluating = []
        
        points = cubes[1].getPointsCube()     
        #seg = Segment3d(points[0],points[1])
        #seg = Segment3d(points[1],points[2])
        #seg = Segment3d(points[2],points[3])
        #seg = Segment3d(points[3],points[0])
        #seg = Segment3d(points[4],points[5])
        #seg = Segment3d(points[5],points[6])
        #seg = Segment3d(points[6],points[7])
        seg = Segment3d(points[7],points[4])

        print ('segment_p0.x',seg.p0.x)
        print ('segment_p0.y',seg.p0.y)
        print ('segment_p0.z',seg.p0.z)
        print ('segment_p1.x',seg.p1.x)
        print ('segment_p1.y',seg.p1.y)
        print ('segment_p1.z',seg.p1.z)
       
        tE = 0
        tL = 1

        triangle_obtained = []
        print ('solid.triangles = ',solid.triangles[0])
        print ('triangle = ',solid.triangles[0].p0.x)
        print ('triangle = ',solid.triangles[0].p0.y)
        print ('triangle = ',solid.triangles[0].p0.z)
        print ('triangle = ',solid.triangles[0].p1.x)
        print ('triangle = ',solid.triangles[0].p1.y)
        print ('triangle = ',solid.triangles[0].p1.z)
        print ('triangle = ',solid.triangles[0].p2.x)
        print ('triangle = ',solid.triangles[0].p2.y)
        print ('triangle = ',solid.triangles[0].p2.z)

        for t in solid.triangles:
            #U = p1-p0
            #V = p2-p0

            #Nx = UyVz - UzVy
            #Ny = UzVx - UxVz
            #Nz = UxVy - UyVx

            U = [t.p1.x-t.p0.x,t.p1.y-t.p0.y,t.p1.z-t.p0.z]
            V = [t.p2.x-t.p0.x,t.p2.y-t.p0.y,t.p2.z-t.p0.z]

            n_i = [U[1]*V[2] - U[2]*V[1], U[2]*V[0] - U[0]*V[2], U[0]*V[1] - U[1]*V[0]]
            N = - ((seg.p0.x-t.p0.x)*n_i[0] + (seg.p0.y-t.p0.y)*n_i[1] + (seg.p0.z-t.p0.z)*n_i[2])
            D = (seg.p1.x-seg.p0.x)*n_i[0] + (seg.p1.y-seg.p0.y)*n_i[1] + (seg.p1.z-seg.p0.z)*n_i[2]
            #t_i_n = (t.p0.x-seg.p0.x)*n_i[0] + (t.p0.y-seg.p0.y)*n_i[1] + (t.p0.z-seg.p0.z)*n_i[2]
            #t_i_d = (seg.p1.x-seg.p0.x)*n_i[0] + (seg.p1.y-seg.p0.y)*n_i[1] + (seg.p1.z-seg.p0.z)*n_i[2]
            #t_i = t_i_n/t_i_d

            if (D == 0):
                if (N < 0):
                    print ('segment out of solid')
                else:
                    print ('continue evaluating solid')                    

            else:
                t_i = N/D
                if (D < 0):
                    #print ('S is entering OMEGA')
                    tE = max(tE,t_i)
                    if (tE > tL):
                        print ('S is not entering OMEGA')
                    else:
                        print ('S is entering OMEGA')
                        triangle_obtained.append(t)
                        intersection_point = Point3d(seg.p0.x+tE*(seg.p1.x-seg.p0.x),seg.p0.y+tE*(seg.p1.y-seg.p0.y),seg.p0.z+tE*(seg.p1.z-seg.p0.z))
                        triangle_obtained.append(Triangle3d(t.p0,intersection_point,t.p1))
                        
                else:
                    #print ('S is leaving OMEGA')
                    tL = min(tL,t_i)
                    if (tL < tE):
                        print ('S is not leaving OMEGA')
                    else:
                        print ('S is leaving OMEGA')
                        triangle_obtained.append(t)
                        intersection_point = Point3d(seg.p0.x+tL*(seg.p1.x-seg.p0.x),seg.p0.y+tL*(seg.p1.y-seg.p0.y),seg.p0.z+tL*(seg.p1.z-seg.p0.z))
                        triangle_obtained.append(Triangle3d(t.p0,intersection_point,t.p1))

            print ('normal_t = ',N,D)

        #return [solid.triangles[0],Triangle3d(seg.p0.x)]
        return triangle_obtained
       