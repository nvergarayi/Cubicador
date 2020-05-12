# -*- coding: utf-8 -*-
from geometry.controller.common.common import checkIntervalClosed, checkIntervalSemiopen, checkIntervalSemiopen2, checkIntervalOpen, gaussianElimination
from geometry.controller.geometry_2d.point_2d import Point2D
from geometry.controller.geometry_3d.triangle_3d import Triangle3d
from geometry.controller.geometry_3d.tetrahedron_3d import Tetrahedron3d
from geometry.controller.geometry_3d.point_3d import Point3d
from geometry.controller.geometry_3d.curve_3d import Curve3d
from geometry.controller.geometry_2d.segment_2d import Segment2D
from geometry.controller.geometry_3d.segment_3d import Segment3d
from geometry.controller.geometry_3d.polygon_3d import Polygon3d
import matplotlib.pyplot as plt
import math
import time

class Solid3d(object):
    
    def __init__(self, triangles, rowid=-1):
        self.triangles = triangles
        self.rowid = rowid
    
    @property
    def volume(self):
        '''
        Funcion que calcula el volumen de un solido convexo.
        '''  
        
        '''
        Obtener el centroide del solido.
        '''
        #print ('obtain_solid_volume = ',self.triangles)
        centroid = self.getCentroid()
        volume = 0
        '''
        Calcular los volumenes de los tetraedros formados por el centro del
        solido y cada triangulo de este. Luego sumarlos.
        '''
        for triangle in self.triangles:
            p0 = Point3d(triangle.p0.x-centroid.x, triangle.p0.y-centroid.y, triangle.p0.z-centroid.z)
            p1 = Point3d(triangle.p1.x-centroid.x, triangle.p1.y-centroid.y, triangle.p1.z-centroid.z)
            p2 = Point3d(triangle.p2.x-centroid.x, triangle.p2.y-centroid.y, triangle.p2.z-centroid.z)
            volume += Tetrahedron3d(p0, p1, p2).tetrahedronVolume
        return volume

    '''
    Funcion que verifica si un punto se encuentra dentro de un solido, descomponiendolo en
    tetrahedros y evaluando dicho punto en cada uno de ellos.
    '''
    def isPointInSolid(self,centroid_father_solid,point):
        '''
        Obtener el centroide del solido.
        '''
        #centroid = self.getCentroid()      

        state = False

        '''
        Evaluar si el punto se halla en cada uno de los tetraedros formados por el centro
        del solido y cada triangulo de este.
        '''
        for triangle in self.triangles:
            #point_modified1 = Point3d(point.x-2,point.y-2,point.z-2)
            #point_modified2 = Point3d(point.x+2,point.y+2,point.z-2)
            #chart7([point_modified1,point,point_modified2],[triangle])
            #chart7([],[triangle])
            tetrahedron = Tetrahedron3d(triangle.p0,triangle.p1,triangle.p2)
            state = tetrahedron.isPointInTetrahedron(centroid_father_solid,point)
            if (state == True): break

        return state

    '''
    Funcion para detectar la interseccion de un segmento respecto a un solido.
    '''
    def cutSegment(self,segment,cube,centroid_solid):

        min_num = 0.01
        for t in self.triangles:
            '''
            Calculo de vectores para obtener la normal al triangulo en evaluacion.
            '''       
            U = [t.p1.x-t.p0.x,t.p1.y-t.p0.y,t.p1.z-t.p0.z]
            V = [t.p2.x-t.p0.x,t.p2.y-t.p0.y,t.p2.z-t.p0.z]

            '''
            Calculo del vector normal al triangulo.
            '''            
            n_i = [U[1]*V[2] - U[2]*V[1], U[2]*V[0] - U[0]*V[2], U[0]*V[1] - U[1]*V[0]]

            N = - ((segment.p0.x-t.p0.x)*n_i[0] + (segment.p0.y-t.p0.y)*n_i[1] + (segment.p0.z-t.p0.z)*n_i[2])
            D = (segment.p1.x-segment.p0.x)*n_i[0] + (segment.p1.y-segment.p0.y)*n_i[1] + (segment.p1.z-segment.p0.z)*n_i[2]

            if (abs(D) >= 0.001):
                '''
                Caso en que el segmento intersecta el plano del triangulo. Se calcula el punto de interseccion.
                '''
                t_i = N/D
                P_t = Point3d(segment.p0.x+t_i*(segment.p1.x-segment.p0.x),segment.p0.y+t_i*(segment.p1.y-segment.p0.y),segment.p0.z+t_i*(segment.p1.z-segment.p0.z))

                '''
                Evaluar el punto obtenido, para conocer si efectivamente es la interseccion del bloque con el solido.
                '''
                if cube.inCube(P_t,min_num) is True:
                    tetrahedron = Tetrahedron3d(t.p0,t.p1,t.p2)
                    state = tetrahedron.isPointInTetrahedron(centroid_solid,P_t)
                    if (state is True):
                        return P_t

    '''
    Funcion para detectar la interseccion de un conjunto de segmentos respecto a un solido.
    '''
    def cutSegment2(self,cubes,centroid_solid,list_for_triangles,list_intersection_triangles):

        list_intersection_solids = []

        min_num = 0.01

        '''
        Evaluar para cada triangulo del solido a intersectar, los puntos de interseccion a partir del total de bloques.
        '''
        for t_ind in range(len(self.triangles)):
            '''
            Calculo de vectores para obtener la normal al triangulo en evaluacion.
            '''       
            U = [self.triangles[t_ind].p1.x-self.triangles[t_ind].p0.x,self.triangles[t_ind].p1.y-self.triangles[t_ind].p0.y,self.triangles[t_ind].p1.z-self.triangles[t_ind].p0.z]
            V = [self.triangles[t_ind].p2.x-self.triangles[t_ind].p0.x,self.triangles[t_ind].p2.y-self.triangles[t_ind].p0.y,self.triangles[t_ind].p2.z-self.triangles[t_ind].p0.z]

            '''
            Calculo del vector normal al triangulo.
            '''            
            n_i = [U[1]*V[2] - U[2]*V[1], U[2]*V[0] - U[0]*V[2], U[0]*V[1] - U[1]*V[0]]

            '''
            Generar el tetrahedro relacionado al triangulo.
            '''
            tetrahedron = Tetrahedron3d(self.triangles[t_ind].p0,self.triangles[t_ind].p1,self.triangles[t_ind].p2)

            '''
            Lista para quitar del diccionario los conjuntos de lados y vertices de los triangulos ya formados para los solidos
            de interseccion, con el fin de que no sean evaluados en los proximos triangulos del solido a intersectar.
            '''
            triangles_delete = []

            '''
            Recorrer cada uno de los conjuntos de lados y vertices, con los cuales hay que construir los triangulos para los
            solidos de interseccion.
            '''
            for t_eval in list_for_triangles.keys():

                count = 0
                '''
                Evaluar cada uno de los puntos del triangulo de interseccion.
                '''
                for pts_index in range(3):
                    if (len(list_for_triangles[t_eval][pts_index]) == 2):
                        '''
                        Caso en que se tiene un lado procedente de un bloque y se debe buscar la interseccion
                        con un triangulo del solido a intersectar.
                        '''
                        count += 1
                        segment = Segment3d(list_for_triangles[t_eval][pts_index][0],list_for_triangles[t_eval][pts_index][1])            
                        
                        N = - ((segment.p0.x-self.triangles[t_ind].p0.x)*n_i[0] + (segment.p0.y-self.triangles[t_ind].p0.y)*n_i[1] + (segment.p0.z-self.triangles[t_ind].p0.z)*n_i[2])
                        D = (segment.p1.x-segment.p0.x)*n_i[0] + (segment.p1.y-segment.p0.y)*n_i[1] + (segment.p1.z-segment.p0.z)*n_i[2]

                        if (abs(D) >= 0.001):
                            '''
                            Caso en que el segmento intersecta el plano del triangulo. Se calcula el punto de interseccion.
                            '''
                            t_i = N/D
                            P_t = Point3d(segment.p0.x+t_i*(segment.p1.x-segment.p0.x),segment.p0.y+t_i*(segment.p1.y-segment.p0.y),segment.p0.z+t_i*(segment.p1.z-segment.p0.z))

                            '''
                            Evaluar el punto obtenido, para conocer si efectivamente es la interseccion de un bloque con el solido a intersectar.
                            '''
                            if cubes[t_eval[0]].inCube(P_t,min_num) is True:
                                        state = tetrahedron.isPointInTetrahedron(centroid_solid,P_t)
                                        if (state is True):
                                            list_for_triangles[t_eval][pts_index] = [P_t]
                                            count -= 1
                '''
                En caso de que ya esten todos los puntos del triangulo de interseccion calculados, se añade a los que ya han sido construidos
                y se saca de la evaluacion de los proximos triangulos del solido a intersectar. 
                '''    
                if count == 0:
                    list_intersection_triangles[t_eval[0]][t_eval[1]].append(Triangle3d(list_for_triangles[t_eval][0][0],list_for_triangles[t_eval][1][0],list_for_triangles[t_eval][2][0]))
                    triangles_delete.append(t_eval) 

            '''
            Eliminacion de los lados y vertices de los triangulos ya construidos para que no se evalue
            su interseccion con los siguientes triangulos del solido a intersectar.
            '''
            for t_for_delete in triangles_delete:
                del list_for_triangles[t_for_delete]            

        return list_intersection_triangles                                             

    '''
    Funcion que calcula las intersecciones de un conjunto de bloques con respecto a un solido o conjunto
    de solidos, empleando el algoritmo Marching Cubes.
    '''
    def cubicatorMarchingCubes(self,cubes):
        from geometry.controller.geometry_3d.cube_3d import Cube3d
        from geometry.controller.geometry_3d.polygon_3d import Polygon3d
        from geometry.controller.geometry_3d.mesh_3d import Mesh3d 
        init = time.time()
        '''
        Dividir los solidos en caso de haber mas de uno.
        '''
        solids = self.divideSolids()
        volume = []

        '''
        Abrir el archivo para entregar el porcentaje de minado para cada bloque.
        '''
        mining_solid = open('mining_solid.txt','w')
        mining_solid.write('Volumen del solido intersectado    Volumen del bloque    Minado\n')
        mining_solid.write('---------------------------------------------------------------\n')

        '''
        Crear dicionario con el identificador de los vertices para cada uno de los lados del bloque.
        '''
        edges_pointer = {}
        edges_pointer[0] = [0,1]
        edges_pointer[1] = [1,2]
        edges_pointer[2] = [2,3]
        edges_pointer[3] = [3,0]
        edges_pointer[4] = [4,5]
        edges_pointer[5] = [5,6]
        edges_pointer[6] = [6,7]
        edges_pointer[7] = [7,4]
        edges_pointer[8] = [0,4]
        edges_pointer[9] = [1,5]
        edges_pointer[10] = [3,7]
        edges_pointer[11] = [2,6]
        edges_pointer[12] = [0,0]
        edges_pointer[13] = [1,1]
        edges_pointer[14] = [2,2]
        edges_pointer[15] = [3,3]
        edges_pointer[16] = [4,4]
        edges_pointer[17] = [5,5]
        edges_pointer[18] = [6,6]
        edges_pointer[19] = [7,7]

        '''
        Repetir el proceso para cada solido.
        '''
        for solid in solids:                
            '''
            Orientar los triangulos del solido.
            '''
            solid = solid.orientTriangles()

            '''
            Calcular el volumen del solido.
            '''
            volume.append(solid.volume)
            print ('volume',volume[0])

            '''
            Calcular centroide del solido.
            '''
            centroid_solid = solid.getCentroid()

            '''
            Crear malla.
            '''
            mesh = Mesh3d()

            list_cubes = mesh.CreateMesh2(solid,centroid_solid,cubes)
            '''
            Obtener el detalle de las intersecciones, para cada una de las 256 combinaciones posibles tomando
            en cuenta los estados de los vertices del bloque. Etiqueta "1" en caso de que el vertice este dentro
            del solido, y "0" si esta afuera.
            '''
            cubes_cases = Cube3d.generateMarchingCubesIntersections()

            '''
            Crear un diccionario que almacene el detalle de las intersecciones para cada triangulo de interseccion
            que se debe construir, y una lista que almacene los triangulos que esten listos.
            '''
            total_cubes_cases = {}
            total_intersection_solids = []

            '''
            Determinar para el total de bloques el detalle de las intersecciones.
            '''
            for n_cub in range(len(list_cubes)):
                
                total_intersection_solids.append([])
                l_v = list_cubes[n_cub][8]
                cand = []

                if (tuple(l_v) == (1,1,1,1,1,1,1,1)):
                    '''
                    En el caso de que todos los vertices del bloque esten dentro del solido,
                    triangularlo completamente asignando dos triangulos por cara.
                    '''
                    intersection_solid = cubes[n_cub].get_triangulated_cube()
                    total_intersection_solids[n_cub].append([intersection_solid])
                else:
                    '''
                    En el caso de que solo algunos de los vertices esten dentro del bloque, determinar
                    sus intersecciones segun el detalle precalculado.
                    '''
                    intersection_solid = Solid3d([])
                    cube_case = cubes_cases[tuple(l_v)]

                    for l_triangles in range(len(cube_case)):
                        total_intersection_solids[n_cub].append([])

                        for n_triangle in range(len(cube_case[l_triangles])):
                            '''
                            Generar para cada triangulo un registro en el diccionario sobre el detalle de sus intersecciones.
                            '''
                            total_cubes_cases[(n_cub,l_triangles,n_triangle)] = []

                            for p in cube_case[l_triangles][n_triangle]:

                                if p < 12:
                                    '''
                                    Caso en que el punto a hallar esta en un lado, y por tanto, se deben
                                    calcular sus coordenadas cortando dicho lado.
                                    '''
                                    p0 = list_cubes[n_cub][edges_pointer[p][0]]
                                    p1 = list_cubes[n_cub][edges_pointer[p][1]]
                                    total_cubes_cases[(n_cub,l_triangles,n_triangle)].append([p0,p1])
                                   
                                else:
                                    '''
                                    Caso en que el punto a hallar corresponde a una esquina del bloque.
                                    '''
                                    total_cubes_cases[(n_cub,l_triangles,n_triangle)].append([list_cubes[n_cub][edges_pointer[p][0]]])

            total_intersection_solids = solid.cutSegment2(cubes,centroid_solid,total_cubes_cases,total_intersection_solids)

            '''
            Construir cada uno de los triangulos tomando en cuenta los puntos de interseccion ya obtenidos.
            '''
            for n_cub in range(len(total_intersection_solids)):
                volume_intersection_solid = 0
                if (len(total_intersection_solids[n_cub][0]) != 1):
                    '''
                    Caso en que el bloque corta el solido a intersectar.
                    '''
                    for list_triangle in total_intersection_solids[n_cub]:
                        intersection_solid = Solid3d(list_triangle)

                    volume_intersection_solid += intersection_solid.volume
                    #chart2(cubes[n_cub],[],[],intersection_solid.triangles,solid.triangles,[])
                else:
                    '''
                    Caso en que el bloque esta dentro del solido a intersectar.
                    '''
                    volume_intersection_solid = total_intersection_solids[n_cub][0][0].volume
                    #chart2(cubes[n_cub],[],[],total_intersection_solids[n_cub][0][0].triangles,solid.triangles,[])

                #chart2(cubes[n_cub],[],[],intersection_solid.triangles,solid.triangles,[])
                volume_cube = cubes[n_cub].calculateVolumeCube()
                
                '''
                Calcular el porcentaje de minado y agregarlo al archivo de salida.
                '''
                mining_percentage = volume_intersection_solid/volume_cube
                mining_solid.write(str(volume_intersection_solid))
                mining_solid.write('   ')
                mining_solid.write(str(volume_cube))
                mining_solid.write('   ')
                mining_solid.write(str(mining_percentage))            
                mining_solid.write('\n')             
                #chart2(cube,prov,candidates_triangles,intersect_triangles,solid.triangles,[])                                        

            #chart2(cube,prov,candidates_triangles,intersect_triangles,solid.triangles,[])
            mining_solid.write('---------------------------------------------------------------\n')
            
        mining_solid.close()
        print (str('time_cubicator ='),time.time()-init)    

    '''
    Funcion que calcula las intersecciones de un conjunto de bloques con respecto a un solido o conjunto
    de solidos, empleando el algoritmo Marching Cubes.
    '''
    def cubicatorMarchingCubes2(self,cubes):
        from geometry.controller.geometry_3d.cube_3d import Cube3d
        from geometry.controller.geometry_3d.polygon_3d import Polygon3d
        from geometry.controller.geometry_3d.mesh_3d import Mesh3d 
        init = time.time()
        '''
        Dividir los solidos en caso de haber mas de uno.
        '''
        solids = self.divideSolids()
        volume = []

        '''
        Abrir el archivo para entregar el porcentaje de minado para cada bloque.
        '''
        mining_solid = open('mining_solid.txt','w')
        mining_solid.write('Volumen del solido intersectado    Volumen del bloque    Minado\n')
        mining_solid.write('---------------------------------------------------------------\n')

        '''
        Repetir el proceso para cada solido.
        '''
        for solid in solids:                
            '''
            Orientar los triangulos del solido.
            '''
            solid = solid.orientTriangles()

            '''
            Calcular el volumen del solido.
            '''
            volume.append(solid.volume)
            print ('volume',volume[0])

            '''
            Calcular centroide del solido.
            '''
            centroid_solid = solid.getCentroid()

            '''
            Crear malla.
            '''
            mesh = Mesh3d()

            list_cubes = mesh.CreateMesh2(solid,centroid_solid,cubes)
            '''
            Obtener el detalle de las intersecciones, para cada una de las 256 combinaciones posibles tomando
            en cuenta los estados de los vertices del bloque. Etiqueta "1" en caso de que el vertice este dentro
            del solido, y "0" si esta afuera.
            '''
            cubes_cases = Cube3d.generateMarchingCubesIntersections()

            '''
            Crear dicionario con el identificador de los vertices para cada uno de los lados del bloque.
            '''
            edges_pointer = {}
            edges_pointer[0] = [0,1]
            edges_pointer[1] = [1,2]
            edges_pointer[2] = [2,3]
            edges_pointer[3] = [3,0]
            edges_pointer[4] = [4,5]
            edges_pointer[5] = [5,6]
            edges_pointer[6] = [6,7]
            edges_pointer[7] = [7,4]
            edges_pointer[8] = [0,4]
            edges_pointer[9] = [1,5]
            edges_pointer[10] = [3,7]
            edges_pointer[11] = [2,6]
            edges_pointer[12] = [0,0]
            edges_pointer[13] = [1,1]
            edges_pointer[14] = [2,2]
            edges_pointer[15] = [3,3]
            edges_pointer[16] = [4,4]
            edges_pointer[17] = [5,5]
            edges_pointer[18] = [6,6]
            edges_pointer[19] = [7,7]

            '''
            Recorrer para el total de bloques.
            '''
            for n_cub in range(len(list_cubes)):

                l_v = list_cubes[n_cub][8]
                cand = []

                if (tuple(l_v) == (1,1,1,1,1,1,1,1)):
                    '''
                    En el caso de que todos los vertices del bloque esten dentro del solido,
                    triangularlo completamente asignando dos triangulos por cara.
                    '''
                    intersection_solid = cubes[n_cub].get_triangulated_cube()
                    volume_intersection_solid = cubes[n_cub].calculateVolumeCube()
                else:
                    '''
                    En el caso de que solo algunos de los vertices esten dentro del bloque, generar las intersecciones
                    segun el detalle precalculado.
                    '''
                    intersection_solid = Solid3d([])
                    cube_case = cubes_cases[tuple(l_v)]
                    volume_intersection_solid = 0

                    for list_triangles in cube_case:

                        for triangle in list_triangles:
                            new_p = []
                            '''
                            Generar cada triangulo para el solido de interseccion.
                            '''
                            for p in triangle:
                                if p < 12:
                                    '''
                                    Caso en que el punto a hallar esta en un lado, y por tanto, se deben
                                    calcular sus coordenadas cortando dicho lado.
                                    '''
                                    p0 = list_cubes[n_cub][edges_pointer[p][0]]
                                    p1 = list_cubes[n_cub][edges_pointer[p][1]]

                                    seg = Segment3d(p0,p1)
                                    '''
                                    Obtener el punto de interseccion del lado del bloque con el solido.                                    
                                    '''
                                    intersection_point = solid.cutSegment(seg,cubes[n_cub],centroid_solid)

                                    if (intersection_point is None):
                                        new_p.append(Point3d((p1.x+p0.x)/2,(p1.y+p0.y)/2,(p1.z+p0.z)/2))
                                    else:
                                        new_p.append(intersection_point)                                    
                                else:
                                    '''
                                    Caso en que el punto a hallar corresponde a una esquina del bloque.
                                    '''
                                    new_p.append(list_cubes[n_cub][edges_pointer[p][0]])
                            
                                #chart2(cubes[n_cub],[Triangle3d(seg.p0,seg.p1,seg.p0)],[],intersection_solid.triangles,solid.triangles,[])

                            '''
                            Agrupar todos los triangulos de interseccion en un solido de interseccion.
                            '''
                            triangle_for_solid = Triangle3d(new_p[0],new_p[1],new_p[2])
                            intersection_solid.triangles.append(triangle_for_solid)
                            #chart2(cubes[n_cub],[Triangle3d(seg.p0,seg.p1,seg.p0)],[],intersection_solid.triangles,solid.triangles,[])

                        '''
                        Sumar los volumenes del solido de interseccion en el caso de que este dividido.
                        '''
                        #chart2(cubes[n_cub],[],[],intersection_solid.triangles,solid.triangles,[])
                        volume_intersection_solid += intersection_solid.volume
                        #print ('volume_intersection_solid = ',volume_intersection_solid)

                '''
                Calcular el volumen del bloque.
                '''
                volume_cube = cubes[n_cub].calculateVolumeCube()

                '''
                Calcular el porcentaje de minado tomando en cuenta el solido de interseccion.
                '''
                mining_percentage = volume_intersection_solid/volume_cube
                mining_solid.write(str(volume_intersection_solid))
                mining_solid.write('   ')
                mining_solid.write(str(volume_cube))
                mining_solid.write('   ')
                mining_solid.write(str(mining_percentage))            
                mining_solid.write('\n')             
                #chart2(cube,prov,candidates_triangles,intersect_triangles,solid.triangles,[])

            #chart2(cube,prov,candidates_triangles,intersect_triangles,solid.triangles,[])
            mining_solid.write('---------------------------------------------------------------\n')
            
        mining_solid.close()
        print (str('time_cubicator ='),time.time()-init)

    '''
    Funcion que calcula las intersecciones de un conjunto de bloques con respecto a un solido o conjunto
    de solidos, de acuerdo a procedimientos geometricos.
    '''
    def cubicatorGeometricVersion(self,cubes):
        from geometry.controller.geometry_3d.cube_3d import Cube3d
        from geometry.controller.geometry_3d.polygon_3d import Polygon3d
        from geometry.controller.geometry_3d.mesh_3d import Mesh3d
        init = time.time()
        solids = self.divideSolids()
        volume = []
        new_surfaces = []

        '''
        Abrir el archivo para entregar el porcentaje de minado para cada bloque.
        '''
        mining_solid = open('mining_solid.txt','w')
        mining_solid.write('Volumen del solido intersectado    Volumen del bloque    Minado\n')
        mining_solid.write('---------------------------------------------------------------\n')

        '''
        Repetir el proceso para cada solido.
        '''
        for solid in solids:            
            '''
            Orientar los triangulos del solido.
            '''
            solid = solid.orientTriangles()

            '''
            Calcular el volumen del solido.
            '''
            volume.append(solid.volume)
            print ('volume',volume[0])
            
            centroid = solid.getCentroid()
            '''
            Obtener los paralelepipedos circunscritos a los triangulos del solido, 
            para asi determinar cuales colisionan con el bloque.
            '''
            max_b_boxes,general_bounding_boxes = solid.obtain_bounding_boxes()
            '''
            Ordenar los bounding boxes de acuerdo a las coordenadas x, y y z, respectivamente.  
            '''
            general_bounding_boxes.sort()

            '''
            Repetir para cada bloque.
            '''
            for cube in cubes:
                '''
                Calcular el volumen del bloque.
                '''
                volume_cube = cube.calculateVolumeCube()

                '''
                Generar una copia de los bounding boxes ordenados.
                '''
                bounding_boxes = general_bounding_boxes               
                '''
                Obtener los triangulos cuyos bounding box colisionan con el bloque.
                '''
                collision_candidates,candidates_polygon = cube.obtain_collision_candidates(bounding_boxes,max_b_boxes)
                candidates_triangles = []
                
                if (len(candidates_polygon) > 0):
                    new_pols1 = solid.obtainPolygons('xy',cube.xmin)
                    new_pols2 = solid.obtainPolygons('xy',cube.xmax)
                    if (new_pols1 is not None):
                        flag = new_pols1[0].checkPointInPolygon(Point2D(cube.ymin,cube.zmin),'yz')

                    prov = []

                    for col in candidates_polygon:
                        index = cube.inner_triangle(col)
                        if (index != -1):
                            triangles.append(solid.triangles[index])
                        else:
                            prov.append(solid.triangles[col[6]])

                elif(len(candidates_polygon) > 0):
                    new_pols = solid.obtainPolygons('xy',cube.xmin)
                    if (new_pols[0].checkPointInPolygon(Point2D(cube.ymin,cube.zmin),'yz') == True):
                        new_surfaces.append(cube.get_triangulated_cube())
                    '''
                    Triangulacion caras internas.                    
                    '''
                if(len(candidates_polygon) > 0):
                    for candidate in candidates_polygon:
                        candidates_triangles.append(solid.triangles[candidate[6]])

                edges = cube.get_edges()
                cp = cube.center_point()
                intersect_triangles = []
                intersections_cube = [[],[],[],[],[],[]]
                bounds = [cube.xmin,cube.xmax,cube.ymin,cube.ymax,cube.zmin,cube.zmax]

                for t in prov:
                    intersect_polygon = Polygon3d([])
                    segments = t.get_segments()
                    
                    for s in segments:
                        octets = s.get_octets(cp)
                        
                        for octet in octets:
                            pts,points_faces_cube = s.get_points_intersect(bounds,edges[octet],octet)
                            
                            for p in pts:
                                intersect_polygon.points = p.check_point3d(intersect_polygon.points)
                                
                            for p in points_faces_cube:
                                intersections_cube = p[0].points_faces_cube(intersections_cube,p[1])
                            
                    if (len(intersect_polygon.points) >= 3):
                        triangles_for_check = intersect_polygon.get_intersection_triangles()
                        intersect_triangles.extend(cube.checkTriangles(triangles_for_check))
                
                '''
                Anadir caras internas del bloque.
                '''
                triangulated_faces = cube.addInternalFaces(solid,centroid,intersections_cube,candidates_polygon)
                intersect_triangles.extend(triangulated_faces.triangles)
                intersection_solid = Solid3d([])
                intersection_solid.triangles = intersect_triangles

                '''
                Obtener el volumen del solido de interseccion y calcular el porcentaje de minado.
                '''
                volume_intersection_solid = intersection_solid.volume
                mining_percentage = volume_intersection_solid/volume_cube
                mining_solid.write(str(volume_intersection_solid))
                mining_solid.write('   ')
                mining_solid.write(str(volume_cube))
                mining_solid.write('   ')
                mining_solid.write(str(mining_percentage))            
                mining_solid.write('\n')             
                #chart2(cube,prov,candidates_triangles,intersect_triangles,solid.triangles,[])

            mining_solid.write('---------------------------------------------------------------\n')
            
        mining_solid.close()
        print (str('time_cubicator ='),time.time()-init)

    def divideSolids(self):
        '''
        Funcion que separa los solidos a partir de un conjunto de triangulos.
        '''        

        '''
        Obtener los puntos medios de cada segmento de los triangulos
        del solido. Filtrar los repetidos. Tambien determinar cual o
        cuales son los triangulos vecinos al punto medio.
        '''
        pm_d = {}; tm_d = {}
        for t in self.triangles:
            pm_s = []
            for p0, p1 in [(t.p0, t.p1), (t.p1, t.p2), (t.p2, t.p0)]:
                pm = (round((p0.x+p1.x)/2,8), round((p0.y+p1.y)/2,8), round((p0.z+p1.z)/2,8))
                if pm not in pm_d:
                    pm_d[pm] = [t]
                else:
                    pm_d[pm].append(t)
                pm_s.append(pm)
            tm_d[t] = pm_s

        '''
        Encontrar para cada triangulo, los triangulos vecinos. 
        '''
        aux_d = {}
        for t in tm_d:
            list_triangles = []
            for pm in tm_d[t]:
                prov = [tm for tm in pm_d[pm] if tm != t]
                if (len(prov) > 0):
                    list_triangles.append(prov[0])
            aux_d[t] = list_triangles

        '''
        Separar los solidos.
        '''
        groupTriangle_s = []
        while len(aux_d) > 0:
            key = list(aux_d.keys())[0]

            solid = Solid3d([])
            search_s = [key]
            while len(search_s) > 0:
                newSearch_s = []
                for search in search_s:
                    if search in aux_d:
                        solid.triangles.append(search)
                        newSearch_s += aux_d.pop(search)
                        
                search_s = newSearch_s
            groupTriangle_s.append(solid)
        return groupTriangle_s

    def orientTriangles(self):
        '''
        Funcion que separa los solidos a partir de un conjunto de triangulos.
        '''
        
        '''
        Obtener los puntos medios de cada segmento de los triangulos
        del solido. Filtrar los repetidos. Tambien determinar cual o
        cuales son los triangulos vecinos al punto medio.
        '''
        pm_d = {}; tm_d = {}; segments = {}; espejo = {}

        key = self.triangles[0]
        v1 = (key.p1.x-key.p0.x, key.p1.y-key.p0.y, key.p1.z-key.p0.z)
        v2 = (key.p2.x-key.p1.x, key.p2.y-key.p1.y, key.p2.z-key.p1.z)
        centroid = Point3d((key.p0.x+key.p1.x+key.p2.x)/3,(key.p0.y+key.p1.y+key.p2.y)/3,(key.p0.z+key.p1.z+key.p2.z)/3)
        mod1 = math.sqrt((v1[0]**2)+(v1[1]**2)+(v1[2]**2))
        mod2 = math.sqrt((v2[0]**2)+(v2[1]**2)+(v2[2]**2))
        v1 = (v1[0]/mod1, v1[1]/mod1, v1[2]/mod1)
        v2 = (v2[0]/mod2, v2[1]/mod2, v2[2]/mod2)
        normal = (v1[1]*v2[2]-v1[2]*v2[1], v1[2]*v2[0]-v1[0]*v2[2], v1[0]*v2[1]-v1[1]*v2[0])
        mod_normal = math.sqrt((normal[0]**2)+(normal[1]**2)+(normal[2]**2))
        normal = (normal[0]/mod_normal, normal[1]/mod_normal, normal[2]/mod_normal)
        centroid2 = Point3d(centroid.x+normal[0],centroid.y+normal[1],centroid.z+normal[2])
        if (self.checkPointInSolid(centroid2) == False):
            self.triangles[0] = Triangle3d(key.p2,key.p1,key.p0)
        key = self.triangles[0]

        for t in self.triangles:

            espejo[t] = t
            pm_s = []
            for p0, p1 in [(t.p0, t.p1), (t.p1, t.p2), (t.p2, t.p0)]:
                pm = (round((p0.x+p1.x)/2,8), round((p0.y+p1.y)/2,8), round((p0.z+p1.z)/2,8))
                if pm not in pm_d:
                    pm_d[pm] = [t]
                    segments[pm] = [[Segment3d(p0,p1),t]]
                else:
                    pm_d[pm].append(t)
                    segments[pm].append([Segment3d(p0,p1),t])
                pm_s.append(pm)
            tm_d[t] = pm_s

        '''
        Encontrar para cada triangulo, los triangulos vecinos. 
        '''
        while len(tm_d) > 0:
            search_s = [key]
            solid = Solid3d([])
            while len(search_s) > 0:
                 newSearch_s = []
                 for search in search_s:
                     if search in tm_d:
                         for pm in tm_d[search]:
                             prov = [tm for tm in pm_d[pm] if tm != search]
                             if (len(prov) > 0):
                                 if prov[0] in tm_d:
                                     [s0, t0], [s1, t1] = segments[pm]
                                     if (round(s0.p0.x,8) == round(s1.p0.x,8) and round(s0.p0.y,8) == round(s1.p0.y,8) and \
                                      round(s0.p0.z,8) == round(s1.p0.z,8)):
                                         t_prov = espejo[prov[0]]
                                         pm_s = tm_d[prov[0]]
                                         for p in pm_s:
                                             [s0_old, ta], [s1_old, tb] = segments[p]
                                             if (prov[0] == ta):
                                                 segments[p] = [[Segment3d(s0_old.p1,s0_old.p0), ta], [s1_old, tb]]
                                             if (prov[0] == tb):
                                                 segments[p] = [[s0_old, ta], [Segment3d(s1_old.p1,s1_old.p0), tb]]
                                         espejo[prov[0]] = Triangle3d(t_prov.p2,t_prov.p1,t_prov.p0)
                                     newSearch_s.append(prov[0])
                         solid.triangles.append(espejo.pop(search))
                         del tm_d[search]
                 search_s = newSearch_s

        for t in solid.triangles:
            '''
            v1 = (t.p1.x-t.p0.x, t.p1.y-t.p0.y, t.p1.z-t.p0.z)
            v2 = (t.p2.x-t.p1.x, t.p2.y-t.p1.y, t.p2.z-t.p1.z)
            centroid = Point3d((t.p0.x+t.p1.x+t.p2.x)/3,(t.p0.y+t.p1.y+t.p2.y)/3,(t.p0.z+t.p1.z+t.p2.z)/3)
            mod1 = math.sqrt((v1[0]**2)+(v1[1]**2)+(v1[2]**2))
            mod2 = math.sqrt((v2[0]**2)+(v2[1]**2)+(v2[2]**2))
            v1 = (v1[0]/mod1, v1[1]/mod1, v1[2]/mod1)
            v2 = (v2[0]/mod2, v2[1]/mod2, v2[2]/mod2)
            normal = (v1[1]*v2[2]-v1[2]*v2[1], v1[2]*v2[0]-v1[0]*v2[2], v1[0]*v2[1]-v1[1]*v2[0])
            mod_normal = math.sqrt((normal[0]**2)+(normal[1]**2)+(normal[2]**2))
            normal = (normal[0]/mod_normal, normal[1]/mod_normal, normal[2]/mod_normal)
            centroid2 = Point3d(centroid.x+10*normal[0],centroid.y+10*normal[1],centroid.z+10*normal[2])
            chart5([[centroid,centroid2]],[t],solid.triangles)
            '''
        return solid

    def subSolids(self,curve,plane):
        '''
        Funcion para obtener subsolidos a partir de una curva de corte.
        @param curve: instancia de Curve3d. Corresponde a la curva de corte.
        @param plane: indica el plano cuyas coordenadas se emplearan en la division del solido.
        '''
        from geometry.controller.geometry_3d.polygon_3d import Polygon3d
        subsolids = []
        sub_solid1 = Solid3d([])
        sub_solid2 = Solid3d([])
        middle = Solid3d([])

        '''
        Transformar la curva divisoria en una recta, segun el plano de referencia. Extraer triangulos a la izquierda
        y a la derecha del rectangulo circunscrito a la curva.
        '''
        if (plane == 'xy'):
            triangulate_option = 2
            consts_curve1 = Polygon3d([curve.points[0],curve.points[len(curve.points)-1]]).obtainConsts(0)
            #min_abs,max_abs,abs_range = self.getRangeXForCandidates(curve)
            #sub_solid1,sub_solid2,middle = self.getPreSubSolids(min_abs,max_abs,abs_range)
        elif (plane == 'yz'):
            triangulate_option = 3
            consts_curve1 = Polygon3d([Point2D(curve.points[0].y,curve.points[0].z), \
             Point2D(curve.points[len(curve.points)-1].y,curve.points[len(curve.points)-1].z)]).obtainConsts(0)
            #min_abs,max_abs,abs_range = self.getRangeYForCandidates(curve)
            #sub_solid1,sub_solid2,middle = self.getPreSubSolids(min_abs,max_abs,abs_range)
        elif (plane == 'zx'):
            triangulate_option = 1
            consts_curve1 = Polygon3d([Point2D(curve.points[0].z,curve.points[0].x), \
             Point2D(curve.points[len(curve.points)-1].z,curve.points[len(curve.points)-1].x)]).obtainConsts(0)
            #min_abs,max_abs,abs_range = self.getRangeZForCandidates(curve)
            #sub_solid1,sub_solid2,middle = self.getPreSubSolids(min_abs,max_abs,abs_range)

        '''
        Determinar a que subsolido corresponde cada triangulo del solido, o si es uno que haya
        que cortar.
        '''
        for t in self.triangles:

            reduced_coords = t.getReducedCoordinates(plane)
            cases = [0,0,0]

            '''
            Determinar en que posicion con respecto a la recta se encuentran los puntos de cada
            triangulo del solido. Si esta a la izquierda de la recta, sera un caso "1". Si esta
            a la derecha, sera un caso "2". Si esta justo en la recta, un caso "0".
            '''
            for i in range(3):
                if (consts_curve1[0] is None):
                    if (round(reduced_coords[0][i],8) < round(consts_curve1[1].x,8)):
                        cases[i] = 1
                    elif (round(reduced_coords[0][i],8) > round(consts_curve1[1].x,8)):
                        cases[i] = 2
                else:
                    if (round(reduced_coords[1][i],8) > round(consts_curve1[0]*reduced_coords[0][i]+consts_curve1[1],8)):
                        cases[i] = 1
                    elif (round(reduced_coords[1][i],8) < round(consts_curve1[0]*reduced_coords[0][i]+consts_curve1[1],8)):
                        cases[i] = 2

            cases.sort()

            '''
            En base a la posicion de cada punto con respecto a la recta, determinar la posicion
            del triangulo y agregarlo en el subsolido que corresponda.
            '''
            if (cases == [1,1,1] or cases == [0,1,1] or cases == [0,0,1]):
                sub_solid1.triangles.append(t)
            elif (cases == [2,2,2] or cases == [0,2,2] or cases == [0,0,2]):
                sub_solid2.triangles.append(t)
            elif (cases == [0,0,0]):
                middle.triangles.append(t)
            elif (cases == [1,2,2] or cases == [1,1,2] or cases == [0,1,2]):
                '''
                Caso en que el triangulo debe ser cortado.
                '''

                intersect_points = t.getTriangleIntersections(consts_curve1,reduced_coords,plane)
                intersect_points.sort()

                '''
                Generar los nuevos triangulos de acuerdo a los puntos de interseccion obtenidos.
                '''
                if (consts_curve1[0] is None):
                    if (intersect_points[0][0] == 0):
                        if (intersect_points[0][1] == 1):
                            if (intersect_points[1][1] == 1):
                                if (intersect_points[1][0] == 1): 
                                    if (reduced_coords[0][0] < consts_curve1[1].x):
                                        sub_solid1.triangles.append(Triangle3d(t.p0,intersect_points[1][2],intersect_points[0][2]))
                                        sub_solid2.triangles.append(Triangle3d(intersect_points[0][2],intersect_points[1][2],t.p1))
                                        sub_solid2.triangles.append(Triangle3d(intersect_points[0][2],t.p1,t.p2))
                                    else:
                                        sub_solid2.triangles.append(Triangle3d(t.p0,intersect_points[1][2],intersect_points[0][2]))
                                        sub_solid1.triangles.append(Triangle3d(intersect_points[0][2],intersect_points[1][2],t.p1))
                                        sub_solid1.triangles.append(Triangle3d(intersect_points[0][2],t.p1,t.p2))
                                elif(intersect_points[1][0] == 2):
                                    if (reduced_coords[0][2] > consts_curve1[1].x):
                                        sub_solid1.triangles.append(Triangle3d(t.p0,t.p1,intersect_points[0][2]))
                                        sub_solid1.triangles.append(Triangle3d(intersect_points[0][2],t.p1,intersect_points[1][2]))
                                        sub_solid2.triangles.append(Triangle3d(intersect_points[0][2],intersect_points[1][2],t.p2))
                                    else:
                                        sub_solid2.triangles.append(Triangle3d(t.p0,t.p1,intersect_points[0][2]))
                                        sub_solid2.triangles.append(Triangle3d(intersect_points[0][2],t.p1,intersect_points[1][2]))
                                        sub_solid1.triangles.append(Triangle3d(intersect_points[0][2],intersect_points[1][2],t.p2))
                            elif (intersect_points[1][0] == 1 and intersect_points[1][1] == 0):
                                if (reduced_coords[0][0] < consts_curve1[1].x):
                                    sub_solid1.triangles.append(Triangle3d(t.p0,t.p1,intersect_points[0][2]))
                                    sub_solid2.triangles.append(Triangle3d(intersect_points[0][2],t.p1,t.p2))
                                else:
                                    sub_solid2.triangles.append(Triangle3d(t.p0,t.p1,intersect_points[0][2]))
                                    sub_solid1.triangles.append(Triangle3d(intersect_points[0][2],t.p1,t.p2))
                        elif (intersect_points[0][1] == 0 and intersect_points[1][1] == 1):
                            if (reduced_coords[0][2] > consts_curve1[1].x):
                                sub_solid1.triangles.append(Triangle3d(t.p0,t.p1,intersect_points[1][2]))
                                sub_solid2.triangles.append(Triangle3d(intersect_points[1][2],t.p2,t.p0))
                            else:
                                sub_solid2.triangles.append(Triangle3d(t.p0,t.p1,intersect_points[1][2]))
                                sub_solid1.triangles.append(Triangle3d(intersect_points[1][2],t.p2,t.p0))
                    elif (intersect_points[0][0] == 1):
                        if (intersect_points[1][0] == 2):
                            if (intersect_points[1][1] == 1):
                                if (reduced_coords[0][1] < consts_curve1[1].x):
                                    sub_solid1.triangles.append(Triangle3d(intersect_points[0][2],t.p1,intersect_points[1][2]))
                                    sub_solid2.triangles.append(Triangle3d(t.p0,intersect_points[0][2],t.p2))
                                    sub_solid2.triangles.append(Triangle3d(t.p2,intersect_points[0][2],intersect_points[1][2]))
                                else:
                                    sub_solid2.triangles.append(Triangle3d(intersect_points[0][2],t.p1,intersect_points[1][2]))
                                    sub_solid1.triangles.append(Triangle3d(t.p0,intersect_points[0][2],t.p2))
                                    sub_solid1.triangles.append(Triangle3d(t.p2,intersect_points[0][2],intersect_points[1][2]))
                            elif (intersect_points[1][1] == 0):
                                if (reduced_coords[0][1] < consts_curve1[1].x):
                                    sub_solid1.triangles.append(Triangle3d(t.p1,t.p2,intersect_points[0][2]))
                                    sub_solid2.triangles.append(Triangle3d(intersect_points[0][2],t.p2,t.p0))
                                else:
                                    sub_solid2.triangles.append(Triangle3d(t.p1,t.p2,intersect_points[0][2]))
                                    sub_solid1.triangles.append(Triangle3d(intersect_points[0][2],t.p2,t.p0))
                else:
                    if (intersect_points[0][0] == 0):
                        if (intersect_points[0][1] == 1):
                            if (intersect_points[1][1] == 1):
                                if (intersect_points[1][0] == 1): 
                                    if (reduced_coords[1][0] > consts_curve1[0]*reduced_coords[0][0]+consts_curve1[1]):
                                        sub_solid1.triangles.append(Triangle3d(t.p0,intersect_points[1][2],intersect_points[0][2]))
                                        sub_solid2.triangles.append(Triangle3d(intersect_points[0][2],intersect_points[1][2],t.p1))
                                        sub_solid2.triangles.append(Triangle3d(intersect_points[0][2],t.p1,t.p2))
                                    else:
                                        sub_solid2.triangles.append(Triangle3d(t.p0,intersect_points[1][2],intersect_points[0][2]))
                                        sub_solid1.triangles.append(Triangle3d(intersect_points[0][2],intersect_points[1][2],t.p1))
                                        sub_solid1.triangles.append(Triangle3d(intersect_points[0][2],t.p1,t.p2))
                                elif(intersect_points[1][0] == 2):
                                    if (reduced_coords[1][2] < consts_curve1[0]*reduced_coords[0][2]+consts_curve1[1]):
                                        sub_solid1.triangles.append(Triangle3d(t.p0,t.p1,intersect_points[0][2]))
                                        sub_solid1.triangles.append(Triangle3d(intersect_points[0][2],t.p1,intersect_points[1][2]))
                                        sub_solid2.triangles.append(Triangle3d(intersect_points[0][2],intersect_points[1][2],t.p2))
                                    else:
                                        sub_solid2.triangles.append(Triangle3d(t.p0,t.p1,intersect_points[0][2]))
                                        sub_solid2.triangles.append(Triangle3d(intersect_points[0][2],t.p1,intersect_points[1][2]))
                                        sub_solid1.triangles.append(Triangle3d(intersect_points[0][2],intersect_points[1][2],t.p2))
                            elif (intersect_points[1][0] == 1 and intersect_points[1][1] == 0):
                                if (reduced_coords[1][0] > consts_curve1[0]*reduced_coords[0][0]+consts_curve1[1]):
                                    sub_solid1.triangles.append(Triangle3d(t.p0,t.p1,intersect_points[0][2]))
                                    sub_solid2.triangles.append(Triangle3d(intersect_points[0][2],t.p1,t.p2))
                                else:
                                    sub_solid2.triangles.append(Triangle3d(t.p0,t.p1,intersect_points[0][2]))
                                    sub_solid1.triangles.append(Triangle3d(intersect_points[0][2],t.p1,t.p2))
                        elif (intersect_points[0][1] == 0 and intersect_points[1][1] == 1):
                            if (reduced_coords[1][2] < consts_curve1[0]*reduced_coords[0][2]+consts_curve1[1]):
                                sub_solid1.triangles.append(Triangle3d(t.p0,t.p1,intersect_points[1][2]))
                                sub_solid2.triangles.append(Triangle3d(intersect_points[1][2],t.p2,t.p0))
                            else:
                                sub_solid2.triangles.append(Triangle3d(t.p0,t.p1,intersect_points[1][2]))
                                sub_solid1.triangles.append(Triangle3d(intersect_points[1][2],t.p2,t.p0))
                    elif (intersect_points[0][0] == 1):
                        if (intersect_points[1][0] == 2):
                            if (intersect_points[1][1] == 1):
                                if (reduced_coords[1][1] > consts_curve1[0]*reduced_coords[0][1]+consts_curve1[1]):
                                    sub_solid1.triangles.append(Triangle3d(intersect_points[0][2],t.p1,intersect_points[1][2]))
                                    sub_solid2.triangles.append(Triangle3d(t.p0,intersect_points[0][2],t.p2))
                                    sub_solid2.triangles.append(Triangle3d(t.p2,intersect_points[0][2],intersect_points[1][2]))
                                else:
                                    sub_solid2.triangles.append(Triangle3d(intersect_points[0][2],t.p1,intersect_points[1][2]))
                                    sub_solid1.triangles.append(Triangle3d(t.p0,intersect_points[0][2],t.p2))
                                    sub_solid1.triangles.append(Triangle3d(t.p2,intersect_points[0][2],intersect_points[1][2]))
                            elif (intersect_points[1][1] == 0):
                                if (reduced_coords[1][1] > consts_curve1[0]*reduced_coords[0][1]+consts_curve1[1]):
                                    sub_solid1.triangles.append(Triangle3d(t.p1,t.p2,intersect_points[0][2]))
                                    sub_solid2.triangles.append(Triangle3d(intersect_points[0][2],t.p2,t.p0))
                                else:
                                    sub_solid2.triangles.append(Triangle3d(t.p1,t.p2,intersect_points[0][2]))
                                    sub_solid1.triangles.append(Triangle3d(intersect_points[0][2],t.p2,t.p0))

        '''
        Determinar cuantos subsolidos existen tanto a la izquierda como a la derecha de la curva.
        '''
        subsolids1 = sub_solid1.divideSolids()
        subsolids2 = sub_solid2.divideSolids()

        if (len(subsolids1) == 0):
             '''
             Caso en que solo se genera un subsolido a la derecha.
             '''
             sub_solid2.triangles = self.triangles
        elif (len(subsolids2) == 0):
             '''
             Caso en que solo se genera un subsolido a la izquierda.
             '''
             sub_solid1.triangles = self.triangles
        else:
            '''
            Casos en que se generan uno o mas solidos tanto a la derecha como a la izquierda de la
            curva.
            '''
            if (len(subsolids1) > len(subsolids2)):
                '''
                Si hay mas subsolidos a la izquierda de la curva, se deja alli el subsolido inferior
                y el resto se agrupa a la derecha en un solo subsolido derecho.
                '''
                sub_solid1 = subsolids1[0]
                for i in range(1,len(subsolids1)):
                    sub_solid2.triangles.extend(subsolids1[i].triangles)
                sub_solid2.triangles.extend(middle.triangles)
            
                '''
                Obtener los puntos de interseccion entre los dos subsolidos para construir el poligono
                de interseccion.
                '''
                points_polygon = sub_solid1.getPointsPolygonFromSubSolid(consts_curve1,plane)

            else:
                '''
                Si hay mas subsolidos a la derecha de la curva, o el numero de subsolidos es el mismo tanto
                tanto a la izquierda como a la derecha de ella, se deja a la derecha el subsolido inferior del
                lado derecho. El resto se agrupa a la izquierda en un solo subsolido izquierdo.
                '''
                sub_solid2 = subsolids2[0]
                for i in range(1,len(subsolids2)):
                    sub_solid1.triangles.extend(subsolids2[i].triangles)
                sub_solid1.triangles.extend(middle.triangles)

                '''
                Obtener los puntos de interseccion entre los dos subsolidos para construir el poligono
                de interseccion.
                '''
                points_polygon = sub_solid2.getPointsPolygonFromSubSolid(consts_curve1,plane)

            '''
            Construir el poligono de interseccion.
            '''
            cut_pol = points_polygon.getDivisionPolygon(plane)

            '''
            Triangular los costados de cada subsolido y agregarlos.
            '''
            if (sub_solid2.triangles != []):
                sub_solid2.triangles.extend(cut_pol.triangulate(range(len(cut_pol.points)),triangulate_option))
            cut_pol.points.reverse()
            if (sub_solid1.triangles != []):
                sub_solid1.triangles.extend(cut_pol.triangulate(range(len(cut_pol.points)),triangulate_option))

        '''
        Dividir y triangular recursivamente los subsolidos resultantes.
        '''
        if (sub_solid1.triangles != []):
            if (sub_solid2.triangles != []):
                #chart3(sub_solid1.triangles)
                #chart3(sub_solid2.triangles)
                subsolids.extend(sub_solid1.subSolids(curve,plane))
                subsolids.extend(sub_solid2.subSolids(curve,plane))
                return subsolids
            else:
                return [sub_solid1]
        else:
            return [sub_solid2]

    def obtainPolygons(self,plane,value):
        '''
        Funcion para obtener uno o mas poligonos de corte del solido,
        entregando un valor para una de las coordenadas en tres dimensiones.
        @param coord: indica a que coordenada 3D corresponde el valor de corte del solido.
        @param value: constante que señala donde se debe cortar el solido para obtener el poligono.
        '''
        from geometry.controller.geometry_3d.polygon_3d import Polygon3d
        middle_triangles = Solid3d([])
        polygons = []

        '''
        Determinar cual es el rango de la abscisa para cada triangulo, segun el plano
        de referencia.
        '''
        if (plane == 'xy'):
            min_abs = [min(t.p0.x,t.p1.x,t.p2.x) for t in self.triangles]
            max_abs = [max(t.p0.x,t.p1.x,t.p2.x) for t in self.triangles]
        if (plane == 'yz'):
            min_abs = [min(t.p0.y,t.p1.y,t.p2.y) for t in self.triangles]
            max_abs = [max(t.p0.y,t.p1.y,t.p2.y) for t in self.triangles]
        if (plane == 'zx'):
            min_abs = [min(t.p0.z,t.p1.z,t.p2.z) for t in self.triangles]
            max_abs = [max(t.p0.z,t.p1.z,t.p2.z) for t in self.triangles]

        '''
        Almacenar los triangulos que estan dentro del valor de corte.
        '''
        for i in range(len(self.triangles)):
            if (checkIntervalClosed(min_abs[i],max_abs[i],value) == True):
                middle_triangles.triangles.append(self.triangles[i])
        
        '''
        En el caso de que el valor de corte este fuera del rango del solido, devolver None.
        '''
        if (len(middle_triangles.triangles) == 0):    
            return None

        '''
        Verificar si para ese valor de corte se obtienen una o mas envolturas a partir del solido.
        Con ella o ellas se construiran el o los poligonos de corte.
        '''
        wrappings = middle_triangles.divideSolids()
        value /= 1000
        
        '''
        Para cada envoltura obtener el poligono de corte.
        '''
        for wrapping in wrappings:
            points_polygon = Polygon3d([])
            '''
            Recorrer cada triangulo de la envoltura.
            '''
            for t in wrapping.triangles:
                reduced_coords = t.getReducedCoordinates(plane)
                cases = [0,0,0]
                pts = [t.p0,t.p1,t.p2]

                '''
                Determinar en que posicion con respecto al valor de division se encuentran los puntos
                de cada triangulo de la envoltura. Si esta a la izquierda, sera un caso "1". Si esta
                a la derecha, sera un caso "2". Si esta justo sobre el, un caso "0" y se agrega como
                punto de interseccion.
                '''
                for i in range(3):
                    if (round(reduced_coords[0][i],8) < round(value,8)):
                        cases[i] = 1
                    elif (round(reduced_coords[0][i],8) > round(value,8)):
                        cases[i] = 2
                    else:
                        points_polygon.points.append(pts[i])

                cases.sort()
                '''
                Si el triangulo tiene los puntos con caso distinto de "0", debe ser cortado para obtener
                los puntos de interseccion.
                '''
                if (cases == [1,2,2] or cases == [1,1,2] or cases == [0,1,2]):
                    points_polygon.points.extend([p[2] for p in t.getTriangleIntersections([None,Point2D(value,0),\
                     Point2D(0,0)],reduced_coords,plane)])

            '''
            Finalmente se construye el poligono de corte, a partir de los puntos de interseccion, para cada envoltura.
            '''
            polygons.append(points_polygon.getDivisionPolygon(plane))
           
        return polygons

    def getPreSubSolids(self,min_abs,max_abs,abs_range):
        '''
        Funcion para extraer los triangulos para el subsolido de la izquierda y el subsolido de la derecha,
        que esten fuera del rango del bounding box circunscrito a la curva de corte.
        @param min_abs  : Lista de los bordes inferiores de cada triangulo para el eje de las abscisas.
        @param max_abs  : Lista de los bordes superiores de cada triangulo para el eje de las abscisas.
        @param abs_range: Rango para el eje de las abscisas de la curva de corte. 

        '''
        sub_solid1 = Solid3d([])
        sub_solid2 = Solid3d([])
        middle = Solid3d([])

        '''
        Recorrer cada triangulo del solido y determinar si hay que agregarlo a uno de los dos subsolidos,
        o bien queda dentro del bounding box de la curva y hay que que seguir procesandolo.
        '''
        for i in range(len(self.triangles)):
            if (max_abs[i] < abs_range[0]):
                sub_solid1.triangles.append(self.triangles[i])
            elif (min_abs[i] > abs_range[1]):
                sub_solid2.triangles.append(self.triangles[i])
            else:
                middle.triangles.append(self.triangles[i])

        return sub_solid1,sub_solid2,middle

    def getPointsPolygonFromSubSolid(self,consts_curve1,plane):
        '''
        Funcion que extrae puntos para el poligono de interseccion a partir de la evaluacion de los bordes
        de un subsolido con respecto a la curva de corte.
        @param consts_curve1: Lista con las constantes de la recta correspondiente a la curva de corte.
        @param plane        : Plano de referencia que fija la abscisa y la ordenada para efectuar la
                              extraccion de puntos.
        '''
        from geometry.controller.geometry_3d.polygon_3d import Polygon3d

        points_polygon = Polygon3d([])

        '''
        Recorrer cada triangulo del subsolido.
        '''
        for t in self.triangles:
            '''
            Obtener las coordenadas de cada punto del triangulo divididas por 1000.
            '''
            pts = [t.p0,t.p1,t.p2]
            reduced_coords = t.getReducedCoordinates(plane)

            '''
            Evaluar si el punto en cuestion del triangulo esta sobre la curva. De ser
            asi, se trata de un punto del poligono de division y se agrega a "points_polygon".
            '''
            for i in range(3):
                if (consts_curve1[0] is None):
                    if (round(reduced_coords[0][i],8) == round(consts_curve1[1].x,8)):
                        points_polygon.points.append(pts[i])
                else:
                    if (round(reduced_coords[1][i],8) == round(consts_curve1[0]*reduced_coords[0][i]+consts_curve1[1],8)):
                        points_polygon.points.append(pts[i])

        return points_polygon

    def checkPointInSolid(self,point):
        '''
        Funcion para verificar si un punto esta dentro de un solido o no. Devuelve "True" en caso
        afirmativo y "False" en caso negativo.
        @param point: Objeto de tipo Point3d que corresponde al punto que se debe evaluar.
        '''

        '''
        Tomar el valor del punto en el eje z y generar el o los poligonos de interseccion con respecto
        al solido para dicho eje.
        '''
        polygons = self.obtainPolygons('zx',point.z)

        '''
        Evaluar en el poligono o los poligonos resultantes si el punto esta dentro o no. Si es asi, significa
        que el punto esta dentro del solido. Sino, que esta fuera de el.
        '''
        if polygons is not None:
            for polygon in polygons:

                if (polygon is not None):
                    in_polygon = polygon.checkPointInPolygon(point,'xy')
                    if(in_polygon == True):
                        return True
        return False

    def getRangeXForCandidates(self,curve):
        '''
        Funcion para obtener cual es el rango de la curva de corte para la abscisa, ademas de los valores
        minimos y maximos de los triangulos del solido pasado como parametro, para dicha coordenada.
        Esto para saber cuales son los triangulos candidatos para intersectar la curva.
        Se toma como referencia el plano "xy".
        @param curve: instancia de Curve3d. Corresponde a la curva de corte.
        '''

        '''
        Obtener los valores minimos y maximos de cada triangulo precandidato
        para el eje "x". Ademas obtener el rango de la curva para dicho eje.
        '''
        min_abs = [min(t.p0.x,t.p1.x,t.p2.x) for t in self.triangles]
        max_abs = [max(t.p0.x,t.p1.x,t.p2.x) for t in self.triangles]
        abs_range = [min(curve.points[0].x,curve.points[len(curve.points)-1].x),\
         max(curve.points[0].x,curve.points[len(curve.points)-1].x)]

        return min_abs,max_abs,abs_range

    def getRangeYForCandidates(self,curve):
        '''
        Funcion para obtener cual es el rango de la curva de corte para la abscisa, ademas de los valores
        minimos y maximos de los triangulos del solido pasado como parametro, para dicha coordenada.
        Esto para saber cuales son los triangulos candidatos para intersectar la curva.
        Se toma como referencia el plano "yz".
        @param curve: instancia de Curve3d. Corresponde a la curva de corte.
        '''

        '''
        Obtener los valores minimos y maximos de cada triangulo precandidato
        para el eje "y". Ademas obtener el rango de la curva para dicho eje.
        '''
        min_abs = [min(t.p0.y,t.p1.y,t.p2.y) for t in self.triangles]
        max_abs = [max(t.p0.y,t.p1.y,t.p2.y) for t in self.triangles]
        abs_range = [min(curve.points[0].y,curve.points[len(curve.points)-1].y),\
         max(curve.points[0].y,curve.points[len(curve.points)-1].y)]

        return min_abs,max_abs,abs_range

    def getRangeZForCandidates(self,curve):
        '''
        Funcion para obtener cual es el rango de la curva de corte para la abscisa, ademas de los valores
        minimos y maximos de los triangulos del solido pasado como parametro, para dicha coordenada.
        Esto para saber cuales son los triangulos candidatos para intersectar la curva.
        Se toma como referencia el plano "zx".
        @param curve: instancia de Curve3d. Corresponde a la curva de corte.
        '''

        '''
        Obtener los valores minimos y maximos de cada triangulo precandidato
        para el eje "z". Ademas obtener el rango de la curva para dicho eje.
        '''
        min_abs = [min(t.p0.z,t.p1.z,t.p2.z) for t in self.triangles]
        max_abs = [max(t.p0.z,t.p1.z,t.p2.z) for t in self.triangles]
        abs_range = [min(curve.points[0].z,curve.points[len(curve.points)-1].z),\
         max(curve.points[0].z,curve.points[len(curve.points)-1].z)]

        return min_abs,max_abs,abs_range

    def getCentroid(self):
        '''
        Funcion que obtiene el centroide de un solido.
        '''

        '''
        Sumar los valores de las coordenadas de todos los puntos 3D, eliminando repeticiones.
        '''
        ps = {}
        for t in self.triangles:
            for p in [t.p0,t.p1,t.p2]:
                #print ('t0_t1_t2 = ',t.p0,t.p1,t.p2,p)
                p_evaluate = (round(p.x,8), round(p.y,8), round(p.z,8))
                if p_evaluate not in ps:
                    ps[p_evaluate] = (0,0,0)

        points = ps.keys()
        xs = [point[0] for point in points]
        ys = [point[1] for point in points]
        zs = [point[2] for point in points]

        '''
        Calcular el centroide del solido.
        '''
        cx = sum(xs)/len(xs)
        cy = sum(ys)/len(ys)
        cz = sum(zs)/len(zs)
        
        return Point3d(cx,cy,cz)

    def getPositionSolid(self,curve,plane):
        '''
        Funcion para determinar si un solido se halla a la izquierda, a la derecha o sobre una
        curva de corte, de acuerdo al plano de referencia pasado como parametro. Devuelve "1"
        si esta a la izquierda, "2" si esta a la derecha y "0" si esta sobre la curva.
        
        @param curve: instancia de Curve3d que coresponde a la curva de corte.
        @param plane: indica el plano cuyas coordenadas se emplearan para determinar la 
                      posicion del solido.
        '''
        from geometry.controller.geometry_3d.polygon_3d import Polygon3d

        '''
        Obtener el centroide del solido.
        '''
        cx,cy,cz = self.getCentroid()

        '''
        Determinar la abscisa y la ordenada para el centroide del solido. Dividir los valores
        por 1000.
        '''
        if (plane == 'xy'):
            reduced_centroid = Point2D(cx/1000,cy/1000)
            consts_curve1 = Polygon3d([curve.points[0],curve.points[len(curve.points)-1]]).obtainConsts(0)
        if (plane == 'yz'):
            reduced_centroid = Point2D(cy/1000,cz/1000)
            consts_curve1 = Polygon3d([Point2D(curve.points[0].y,curve.points[0].z), \
             Point2D(curve.points[len(curve.points)-1].y,curve.points[len(curve.points)-1].z)]).obtainConsts(0)
        if (plane == 'zx'):
            reduced_centroid = Point2D(cz/1000,cx/1000)
            consts_curve1 = Polygon3d([Point2D(curve.points[0].z,curve.points[0].x), \
             Point2D(curve.points[len(curve.points)-1].z,curve.points[len(curve.points)-1].x)]).obtainConsts(0)

        '''
        Determinar en que posicion con respecto a la recta se encuentra el centroide del
        solido.
        '''
        if (consts_curve1[0] is None):
            '''
            Caso en que la curva es vertical. 
            '''
            if (round(reduced_centroid.x,8) < round(consts_curve1[1].x,8)):
                return 1
            elif (round(reduced_centroid.x,8) > round(consts_curve1[1].x,8)):
                return 2
            else:
                return 0
        elif (consts_curve1[0] > 0):
            '''
            Caso en que la pendente de la curva es mayor que 0. 
            '''
            if (round(reduced_centroid.y,8) > round(consts_curve1[0]*reduced_centroid.x+consts_curve1[1],8)):
                return 1
            elif (round(reduced_centroid.y,8) < round(consts_curve1[0]*reduced_centroid.x+consts_curve1[1],8)):
                return 2
            else:
                return 0
        else:
            '''
            Caso en que la pendente de la curva es menor o igual que 0. 
            '''
            if (round(reduced_centroid.y,8) < round(consts_curve1[0]*reduced_centroid.x+consts_curve1[1],8)):
                return 1
            elif (round(reduced_centroid.y,8) > round(consts_curve1[0]*reduced_centroid.x+consts_curve1[1],8)):
                return 2
            else:
                return 0

    def obtainHeightsSolid(self):
        '''
        Funcion para obtener las alturas de un solido a partir de su version triangulada.
        '''
        from geometry.controller.geometry_3d.polygon_3d import Polygon3d

        polygon_inf = Polygon3d([])
        polygon_sup = Polygon3d([])
        polygon_inf_red = Polygon3d([])
        polygon_sup_red = Polygon3d([])
        triangles_candidates = Solid3d([])
        ordered_triangles = []

        '''
        Obtener el valor medio en la coordenada "z", con el fin de saber cuales son los
        triangulos del cuerpo del solido (exceptuando los de la cara inferior y de la 
        cara superior.)
        '''
        min_z = min([min(t.p0.z,t.p1.z,t.p2.z) for t in self.triangles])
        max_z = max([max(t.p0.z,t.p1.z,t.p2.z) for t in self.triangles])
        value = (min_z+max_z)/2

        '''
        Separar los triangulos que pertenecen al cuerpo del solido (los que traspasan el eje
        creado por el valor medio en la coordenada "z").
        '''
        for t in self.triangles:
            pts = [t.p0,t.p1,t.p2]
            cases = [0,0,0]
            for i in range(3):
                if (pts[i].z >= value):
                    cases[i] = 1
                else:
                    cases[i] = 0
            cases.sort()
            if (cases != [0,0,0] and cases != [1,1,1]):
                triangles_candidates.triangles.append(t)
        #chart3(triangles_candidates.triangles)

        '''
        Obtener los puntos de los triangulos del cuerpo del solido. Verificar que no se repitan.
        Verificar si estan debajo o encima del eje creado por el valor medio en la coordenada "z".
        Agregarlos al poligono superior o inferior.
        '''
        ps = {}
        for t in triangles_candidates.triangles:
            for p in [t.p0,t.p1,t.p2]:
                p_evaluate = (round(p.x,8), round(p.y,8), round(p.z,8))
                if p_evaluate not in ps:
                    ps[p_evaluate] = (0,0,0)
                    if (p.z >= value):
                        polygon_sup.points.append(p)
                        polygon_sup_red.points.append(Point2D(p.x,p.y))
                    else:
                        polygon_inf.points.append(p)
                        polygon_inf_red.points.append(Point2D(p.x,p.y))

        '''
        Generar los poligonos ordenados empleando coordenadas polares.
        '''
        pol_coord = polygon_sup_red.transformCoord(range(len(polygon_sup_red.points)))
        pol_coord.points.sort()
        p_sup = Polygon3d([])
        for pol in pol_coord.points:
            p_sup.points.append(polygon_sup.points[pol[1]])

        pol_coord = polygon_inf_red.transformCoord(range(len(polygon_inf_red.points)))
        pol_coord.points.sort()
        p_inf = Polygon3d([])
        for pol in pol_coord.points:
            p_inf.points.append(polygon_inf.points[pol[1]])

        #chart([p_inf.points,p_sup.points],['g','r'])

        '''
        Orientar el poligono inferior en contra de las manecillas del reloj.
        '''
        p_inf.checkOrientation([])
        
        '''
        Calcular las alturas empleando los poligonos inferior y superior obtenidos a partir del solido.
        '''
        return p_inf.obtainHeights(p_sup)

    def obtainHeightsSolid2(self):
        '''
        Funcion para obtener las alturas de un solido a partir de su version triangulada.
        '''
        from geometry.controller.geometry_3d.polygon_3d import Polygon3d

        polygon_inf = Polygon3d([])
        polygon_sup = Polygon3d([])
        triangles_candidates = Solid3d([])
        ordered_triangles = []

        '''
        Obtener el valor medio en la coordenada "z", con el fin de saber cuales son los
        triangulos del cuerpo del solido (exceptuando los de la cara inferior y de la 
        cara superior.)
        '''
        min_z = min([min(t.p0.z,t.p1.z,t.p2.z) for t in self.triangles])
        max_z = max([max(t.p0.z,t.p1.z,t.p2.z) for t in self.triangles])
        value = (min_z+max_z)/2

        '''
        Separar los triangulos que pertenecen al cuerpo del solido (los que traspasan el eje
        creado por el valor medio en la coordenada "z").
        '''
        for t in self.triangles:
            pts = [t.p0,t.p1,t.p2]
            cases = [0,0,0]
            for i in range(3):
                if (pts[i].z >= value):
                    cases[i] = 1
                else:
                    cases[i] = 0
            cases.sort()
            if (cases != [0,0,0] and cases != [1,1,1]):
                triangles_candidates.triangles.append(t)
        chart3(triangles_candidates.triangles)

        '''
        Obtener los puntos medios de cada segmento de los triangulos
        del cuerpo del solido. Filtrar los repetidos. Tambien determinar cual o
        cuales son los triangulos vecinos al punto medio.
        '''
        pm_d = {}; tm_d = {}
        for t in triangles_candidates.triangles:
            pm_s = []
            for p0, p1 in [(t.p0, t.p1), (t.p1, t.p2), (t.p2, t.p0)]:
                pm = (round((p0.x+p1.x)/2,8), round((p0.y+p1.y)/2,8), round((p0.z+p1.z)/2,8))
                if pm_d.has_key(pm) is False:
                    pm_d[pm] = [t]
                else:
                    pm_d[pm].append(t)
                pm_s.append(pm)
            tm_d[t] = pm_s

        '''
        Ordenar los triangulos del cuerpo uno tras otro, en una direccion (a favor o en contra de
        las manecillas del reloj).
        '''
        init_triangle = tm_d.keys()[0]
        ordered_triangles.append(init_triangle)
        found = True
        while (len(tm_d) > 1) and (found is True):
            t = ordered_triangles[len(ordered_triangles)-1]
            pm_s = tm_d[t]
            found = False
            for p in pm_s:
                candidates = pm_d[p]
                for cand in candidates:
                    if ((tm_d.has_key(cand) is True) and (cand != t) and (tm_d.has_key(t) is True)):
                        ordered_triangles.append(cand)
                        found = True
                        del tm_d[t]
                        break
        
        '''
        Ordenar los triangulos del cuerpo uno tras otro en contra de las manecillas del reloj.
        '''
        prov = Polygon3d([])
        for t in ordered_triangles:
            prov.points.append(Point3d((t.p0.x+t.p1.x+t.p2.x)/3,(t.p0.y+t.p1.y+t.p2.y)/3,\
             (t.p0.z+t.p1.z+t.p2.z)/3))

        #chart([prov.points],['g'])
        prov.checkOrientation([])
        #chart([prov.points],['r'])
        
        '''
        Determinar que puntos estan arriba o debajo del eje creado por el valor medio en la coordenada "z".
        Generar los poligonos inferior y superior orientados en contra de las manecillas del reloj.
        '''
        psolid = {}
        for t in ordered_triangles:
            segments = []
            segments.append(Segment3d(t.p0,t.p1))
            segments.append(Segment3d(t.p1,t.p2))
            segments.append(Segment3d(t.p2,t.p0))
            points_left = []; points_right = [] 
            for s in segments:
                if (s.p0.z > value and s.p1.z < value):
                    points_right.append(s.p1)
                    points_right.append(s.p0)
                elif (s.p0.z < value and s.p1.z > value):
                    points_left.append(s.p0)
                    points_left.append(s.p1) 

            if (psolid.has_key((round(points_left[0].x,8),round(points_left[0].y,8),round(points_left[0].z,8))) == False):
                psolid[(round(points_left[0].x,8),round(points_left[0].y,8),round(points_left[0].z,8))] = (0,0,0)
                polygon_inf.points.append(points_left[0])

            if (psolid.has_key((round(points_right[0].x,8),round(points_right[0].y,8),round(points_right[0].z,8))) == False):
                psolid[(round(points_right[0].x,8),round(points_right[0].y,8),round(points_right[0].z,8))] = (0,0,0)
                polygon_inf.points.append(points_right[0])

            if (psolid.has_key((round(points_left[1].x,8),round(points_left[1].y,8),round(points_left[1].z,8))) == False):
                psolid[(round(points_left[1].x,8),round(points_left[1].y,8),round(points_left[1].z,8))] = (0,0,0)
                polygon_sup.points.append(points_left[1])

            if (psolid.has_key((round(points_right[1].x,8),round(points_right[1].y,8),round(points_right[1].z,8))) == False):
                psolid[(round(points_right[1].x,8),round(points_right[1].y,8),round(points_right[1].z,8))] = (0,0,0)
                polygon_sup.points.append(points_right[1])

        #chart([polygon_inf.points,polygon_sup.points],['g','r'])

        '''
        Orientar el poligono superior a favor de las manecillas del reloj.
        '''
        polygon_sup.points.reverse()
        
        '''
        Calcular las alturas empleando los poligonos inferior y superior obtenidos a partir del solido.
        '''
        return polygon_inf.obtainHeights(polygon_sup)

    '''
    Funcion que orienta los triangulos de un solido.
    '''
    def orient_triangles(self):
        for i in range(len(self.triangles)):

	        p0 = Point3d(self.triangles[i].p0.x,self.triangles[i].p0.y,self.triangles[i].p0.z)
	        p1 = Point3d(self.triangles[i].p1.x,self.triangles[i].p1.y,self.triangles[i].p1.z)
	        p2 = Point3d(self.triangles[i].p2.x,self.triangles[i].p2.y,self.triangles[i].p2.z)

	        pm0 = Point3d((p1.x+p0.x)/2,(p1.y+p0.y)/2,(p1.z+p0.z)/2)
	        pm1 = Point3d((p2.x+p1.x)/2,(p2.y+p1.y)/2,(p2.z+p1.z)/2)

	        if (p0.z == p1.z) or (p1.z == p2.z):
		        m1 = -1.0/((p1.y-p0.y)/(p1.x-p0.x))
		        m2 = -1.0/((p2.y-p1.y)/(p2.x-p1.x))
	        else:
		        m1 = -1.0/((p1.z-p0.z)/(p1.x-p0.x))
		        m2 = -1.0/((p2.z-p1.z)/(p2.x-p1.x))

	        if (p0.z == p1.z) or (p1.z == p2.z):
		        pcc = solve(array([[m1,-1.0],[m2,-1.0]]),array([[m1*pm0.x-pm0.y],[m2*pm1.x-pm1.y]]))
		        dist = math.sqrt(math.pow(p0.y-pcc[1][0],2)+math.pow(p0.x-pcc[0][0],2))
	        else: 
		        pcc = solve(array([[m1,-1.0],[m2,-1.0]]),array([[m1*pm0.x-pm0.z],[m2*pm1.x-pm1.z]]))
		        dist = math.sqrt(math.pow(p0.z-pcc[1][0],2)+math.pow(p0.x-pcc[0][0],2))

	        p0.x = unit_coords(p0.x,pcc[0][0],dist)
	        p1.x = unit_coords(p1.x,pcc[0][0],dist)
	        p2.x = unit_coords(p2.x,pcc[0][0],dist)

	        if (p0.z == p1.z) or (p1.z == p2.z):
		        p0.y = unit_coords(p0.y,pcc[1][0],dist)
		        p1.y = unit_coords(p1.y,pcc[1][0],dist)
		        p2.y = unit_coords(p2.y,pcc[1][0],dist)
	        else:
		        p0.z = unit_coords(p0.z,pcc[1][0],dist)
		        p1.z = unit_coords(p1.z,pcc[1][0],dist)
		        p2.z = unit_coords(p2.z,pcc[1][0],dist)

	        ang0 = 0.0
	        ang1 = 0.0
	        ang2 = 0.0

	        if (p0.z == p1.z) or (p1.z == p2.z):
		        ang0 = Point2D(p0.x,p0.y).transform_angle()	
		        ang1 = Point2D(p1.x,p1.y).transform_angle()
		        ang2 = Point2D(p2.x,p2.y).transform_angle()		
	        else:
		        ang0 = Point2D(p0.x,p0.z).transform_angle()
		        ang1 = Point2D(p1.x,p1.z).transform_angle()		
		        ang2 = Point2D(p2.x,p2.z).transform_angle()

	        min_angle = min(ang0,ang1,ang2)
	        angles_to_order = [ang0,ang1,ang2]

	        position = angles_to_order.index(min_angle)
	        angles_to_order.extend(angles_to_order[0:position])
	        angles_to_order[0:position] = []

	        if angles_to_order[2] < angles_to_order[1]:
		        self.triangles[i] = Triangle3d(self.triangles[i].p0,self.triangles[i].p2,self.triangles[i].p1)

        return self

    '''
    Funcion para obtener los paralelepipedos circunscritos a los triangulos del
    solido, para asi determinar cuales colisionan con el cubo.
    '''
    def obtain_bounding_boxes(self):
        bounding_boxes = []
        max_b_boxes = []
        for i in range(len(self.triangles)):
            xmin = min(self.triangles[i].p0.x,self.triangles[i].p1.x,self.triangles[i].p2.x)
            xmax = max(self.triangles[i].p0.x,self.triangles[i].p1.x,self.triangles[i].p2.x)
            ymin = min(self.triangles[i].p0.y,self.triangles[i].p1.y,self.triangles[i].p2.y)
            ymax = max(self.triangles[i].p0.y,self.triangles[i].p1.y,self.triangles[i].p2.y)
            zmin = min(self.triangles[i].p0.z,self.triangles[i].p1.z,self.triangles[i].p2.z)
            zmax = max(self.triangles[i].p0.z,self.triangles[i].p1.z,self.triangles[i].p2.z)
            max_b_boxes.append(xmax)
            bounding_boxes.append([xmin,xmax,ymin,ymax,zmin,zmax,i])
        return max(max_b_boxes),bounding_boxes

'''
Funcion que transforma las coordenadas rectangulares en unitarias.
'''
def unit_coords(original_coord,circumcenter_coord,radius):
  return (original_coord - circumcenter_coord)/radius

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

def chart2(cube,triangles,candidates_triangles,intersect_triangles,triangles_solid,vertexes):
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
  
  xs = []; ys = []; zs = []
  xs.append(cube.xmin); ys.append(cube.ymin); zs.append(cube.zmin)
  xs.append(cube.xmax); ys.append(cube.ymin); zs.append(cube.zmin)
  xs.append(cube.xmax); ys.append(cube.ymax); zs.append(cube.zmin)
  xs.append(cube.xmin); ys.append(cube.ymax); zs.append(cube.zmin)
  for i in range(len(xs)-1):
    plt.plot(xs[i:i+2], ys[i:i+2], zs[i:i+2], 'b')
  plt.plot([xs[len(xs)-1], xs[0]], [ys[len(xs)-1], ys[0]],  [zs[len(xs)-1], zs[0]], 'b')
  xs = []; ys = []; zs = []
  xs.append(cube.xmin); ys.append(cube.ymin); zs.append(cube.zmax)
  xs.append(cube.xmax); ys.append(cube.ymin); zs.append(cube.zmax)
  xs.append(cube.xmax); ys.append(cube.ymax); zs.append(cube.zmax)
  xs.append(cube.xmin); ys.append(cube.ymax); zs.append(cube.zmax)
  for i in range(len(xs)-1):
    plt.plot(xs[i:i+2], ys[i:i+2], zs[i:i+2], 'b')
  plt.plot([xs[len(xs)-1], xs[0]], [ys[len(xs)-1], ys[0]],  [zs[len(xs)-1], zs[0]], 'b')
  plt.plot([cube.xmin,cube.xmin], [cube.ymin,cube.ymin],  [cube.zmin,cube.zmax], 'b')
  plt.plot([cube.xmax,cube.xmax], [cube.ymin,cube.ymin],  [cube.zmin,cube.zmax], 'b')
  plt.plot([cube.xmin,cube.xmin], [cube.ymax,cube.ymax],  [cube.zmin,cube.zmax], 'b')
  plt.plot([cube.xmax,cube.xmax], [cube.ymax,cube.ymax],  [cube.zmin,cube.zmax], 'b')
  
  for candidate in candidates_triangles:
    xs = []; ys = []; zs = []
    xs.append(candidate.p0.x)
    xs.append(candidate.p1.x)
    xs.append(candidate.p2.x)
    ys.append(candidate.p0.y)
    ys.append(candidate.p1.y)
    ys.append(candidate.p2.y)
    zs.append(candidate.p0.z)
    zs.append(candidate.p1.z)
    zs.append(candidate.p2.z)
    for i in range(len(xs)-1):
      plt.plot(xs[i:i+2], ys[i:i+2], zs[i:i+2], 'r')
    plt.plot([xs[len(xs)-1], xs[0]], [ys[len(xs)-1], ys[0]],  [zs[len(xs)-1], zs[0]], 'r')
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
      plt.plot(xs[i:i+2], ys[i:i+2], zs[i:i+2], 'k')
    plt.plot([xs[len(xs)-1], xs[0]], [ys[len(xs)-1], ys[0]],  [zs[len(xs)-1], zs[0]], 'k')
  for triangle in intersect_triangles:
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
      plt.plot(xs[i:i+2], ys[i:i+2], zs[i:i+2], 'g')
    plt.plot([xs[len(xs)-1], xs[0]], [ys[len(xs)-1], ys[0]],  [zs[len(xs)-1], zs[0]], 'g')
    for i in range(len(vertexes)):
        ax.scatter(vertexes[i].x, vertexes[i].y, vertexes[i].z, color="r", s=100)
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

def chart4(cube,polygons):
  fig = plt.figure(figsize=(8,6))
  ax = fig.add_subplot(1, 1, 1, projection='3d')
  for i in range(len(polygons)):
    xs = []; ys = []; zs = []
    for point in polygons[i]:
      xs.append(point.x); ys.append(point.y); zs.append(point.z)
    for j in range(len(xs)-1):
      plt.plot(xs[j:j+2], ys[j:j+2], zs[j:j+2], 'r')
    #plt.plot([xs[len(xs)-1], xs[0]], [ys[len(xs)-1], ys[0]], [zs[len(xs)-1], zs[0]], 'r')

  xs = []; ys = []; zs = []
  xs.append(cube.xmin); ys.append(cube.ymin); zs.append(cube.zmin)
  xs.append(cube.xmax); ys.append(cube.ymin); zs.append(cube.zmin)
  xs.append(cube.xmax); ys.append(cube.ymax); zs.append(cube.zmin)
  xs.append(cube.xmin); ys.append(cube.ymax); zs.append(cube.zmin)
  for i in range(len(xs)-1):
    plt.plot(xs[i:i+2], ys[i:i+2], zs[i:i+2], 'b')
  plt.plot([xs[len(xs)-1], xs[0]], [ys[len(xs)-1], ys[0]],  [zs[len(xs)-1], zs[0]], 'b')
  xs = []; ys = []; zs = []
  xs.append(cube.xmin); ys.append(cube.ymin); zs.append(cube.zmax)
  xs.append(cube.xmax); ys.append(cube.ymin); zs.append(cube.zmax)
  xs.append(cube.xmax); ys.append(cube.ymax); zs.append(cube.zmax)
  xs.append(cube.xmin); ys.append(cube.ymax); zs.append(cube.zmax)
  for i in range(len(xs)-1):
    plt.plot(xs[i:i+2], ys[i:i+2], zs[i:i+2], 'b')
  plt.plot([xs[len(xs)-1], xs[0]], [ys[len(xs)-1], ys[0]],  [zs[len(xs)-1], zs[0]], 'b')
  plt.plot([cube.xmin,cube.xmin], [cube.ymin,cube.ymin],  [cube.zmin,cube.zmax], 'b')
  plt.plot([cube.xmax,cube.xmax], [cube.ymin,cube.ymin],  [cube.zmin,cube.zmax], 'b')
  plt.plot([cube.xmin,cube.xmin], [cube.ymax,cube.ymax],  [cube.zmin,cube.zmax], 'b')
  plt.plot([cube.xmax,cube.xmax], [cube.ymax,cube.ymax],  [cube.zmin,cube.zmax], 'b')
  plt.show()

def chart5(polygons,triangles,triangles_solid):
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
  for triangle in triangles:
    #print ('tttttttttt = ',triangle)
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
      plt.plot(xs[i:i+2], ys[i:i+2], zs[i:i+2], 'k')
    plt.plot([xs[len(xs)-1], xs[0]], [ys[len(xs)-1], ys[0]],  [zs[len(xs)-1], zs[0]], 'k')
  for i in range(len(polygons)):
    xs = []; ys = []; zs = []
    for point in polygons[i]:
      xs.append(point.x); ys.append(point.y); zs.append(point.z)
    for j in range(len(xs)-1):
      plt.plot(xs[j:j+2], ys[j:j+2], zs[j:j+2], 'b')
    #plt.plot([xs[len(xs)-1], xs[0]], [ys[len(xs)-1], ys[0]], [zs[len(xs)-1], zs[0]], 'b')
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

def chart7(polygons,triangles_solid):
  #fig = plt.figure(figsize=(8,6))
  #ax = fig.add_subplot(1, 1, 1, projection='3d')
  colours = ['r','k','b','c','m','g','r','k','b','c','m','g','r','k','b','c','m','g']
  triangles_solid2 = []
  triangles_solid2 = triangles_solid2 + triangles_solid
  for triangle_observated in triangles_solid:
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    for triangle in triangles_solid2:
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
      for j in range(len(xs)-1):
        plt.plot(xs[j:j+2], ys[j:j+2], zs[j:j+2], 'y')
      plt.plot([xs[len(xs)-1], xs[0]], [ys[len(xs)-1], ys[0]],  [zs[len(xs)-1], zs[0]], 'y')
    xs_obs= []; ys_obs = []; zs_obs = []
    xs_obs.append(triangle_observated.p0.x)
    xs_obs.append(triangle_observated.p1.x)
    xs_obs.append(triangle_observated.p2.x)
    ys_obs.append(triangle_observated.p0.y)
    ys_obs.append(triangle_observated.p1.y)
    ys_obs.append(triangle_observated.p2.y)
    zs_obs.append(triangle_observated.p0.z)
    zs_obs.append(triangle_observated.p1.z)
    zs_obs.append(triangle_observated.p2.z)   
    for i in range(len(xs_obs)-1):
      plt.plot(xs_obs[i:i+2], ys_obs[i:i+2], zs_obs[i:i+2], colours[i])
    plt.plot([xs_obs[len(xs_obs)-1], xs_obs[0]], [ys_obs[len(xs_obs)-1], ys_obs[0]],  [zs_obs[len(xs_obs)-1], zs_obs[0]], colours[2])
  xc = []; yc = []; zc = []
  #for point in polygons.points:
  for point in polygons:
    xc.append(point.x); yc.append(point.y); zc.append(point.z)
  plt.plot([xc[0], xc[1]], [yc[0], yc[1]], [zc[0], zc[1]], 'c')
  plt.plot([xc[1], xc[2]], [yc[1], yc[2]], [zc[1], zc[2]], 'c')
    #colours = ['r','k','b','c','m','g','r','k','b','c','m','g','r','k','b','c','m','g']
    #for j in range(len(xs)-1):
      #plt.plot(xs[j:j+2], ys[j:j+2], zs[j:j+2], colours[j])
      #plt.plot(xs[j:j+2], ys[j:j+2], zs[j:j+2], 'r')
      #if (xs != []):
        #plt.plot([xs[len(xs)-1], xs[0]], [ys[len(xs)-1], ys[0]], [zs[len(xs)-1], zs[0]], 'g')
        #plt.plot([xs[len(xs)-1], xs[0]], [ys[len(xs)-1], ys[0]], [zs[len(xs)-1], zs[0]], 'r')
  plt.show()
