# -*- coding: utf-8 -*-
from geometry.controller.common.common import checkIntervalSemiopen, checkIntervalSemiopen2, checkIntervalClosed, checkIntervalOpen

class SetOfPoint3d(object):
     
    def __init__(self, points, name='', rowid=-1):
        self.points = points
        self.rowid = rowid
        self.name = name
        
    def processPolygon(self):
        '''
        Funcion recursiva para obtener los subpoligonos monotonos dentro de cada poligono.
        '''
        newpolygons = []
        '''
        Recorrer el poligono.
        '''
        while (len(self.points) >= 3):
            '''
            Operar en el caso de que no sea un triangulo.
            '''
            if (len(self.points) > 3):
                i = 1
                while(i < len(self.points)-1):
                    flag = False
                    '''
                    Obtener el subpoligono monotono si el vertice evaluado es de combinacion.
                    '''
                    if(self.points[i][2] == 5):
                        '''
                        Evaluar si el vertice inmediatamente a la derecha es uno de division.
                        '''
                        if(self.points[i+1][2] == 4):
                            self.points[i][2] = 3
                            self.points[i+1][2] = 3
                            self,newpolygon = self.extractPolygon(i+1,i)
                            newpolygons.extend(newpolygon.processPolygon())
                            flag = True
                            i = 1
                        '''
                        Evaluar si el vertice inmediatamente a la derecha es otro de combinacion o uno regular.
                        '''
                        if(self.points[i+1][2] in [3,5]):
                            self.points[i][2] = 3
                            self,newpolygon = self.extractPolygon(i+1,i)
                            newpolygons.extend(newpolygon.processPolygon())
                            flag = True
                            i = 1
                        elif (i < len(self.points)-2):
                            '''
                            Evaluar si el vertice inmediatamente a la derecha es uno inicial y el siguiente
                            a ese es otro de combinacion o uno regular.
                            '''
                            if(self.points[i+2][2] in [3,5]):
                                self.points[i][2] = 3
                                self,newpolygon = self.extractPolygon(i+2,i)
                                newpolygons.extend(newpolygon.processPolygon())
                                flag = True
                                i = 1
                                '''
                                Evaluar si el vertice inmediatamente a la derecha es uno inicial y el siguiente
                                a ese es uno de division.
                                '''
                            elif(self.points[i+2][2] == 4):
                                self.points[i][2] = 3
                                self.points[i+1][2] = 3
                                self,newpolygon = self.extractPolygon(i+2,i)
                                newpolygons.extend(newpolygon.processPolygon())
                                flag = True
                                i = 1
                        '''
                        Obtener el subpoligono monotono si el vertice evaluado es de division.
                        '''
                    elif(self.points[i][2] == 4):
                        '''
                        Evaluar si el vertice inmediatamente a la izquierda es uno regular.
                        '''
                        if(self.points[i-1][2] == 3):
                            self.points[i][2] = 3
                            self,newpolygon = self.extractPolygon(i-1,i)
                            newpolygons.extend(newpolygon.processPolygon())
                            flag = True
                            i = 1
                            '''
                            Evaluar si el vertice inmediatamente a la izquierda es uno final y el
                            anterior a ese es uno regular.
                            '''
                        elif(self.points[i-2][2] == 3):
                            self.points[i][2] = 3
                            self,newpolygon = self.extractPolygon(i-2,i)
                            newpolygons.extend(newpolygon.processPolygon())
                            flag = True
                            i = 1
                    else:
                        i += 1
                if (flag == False):
                    if (newpolygons == []):
                        '''
                        Devolver orientado correctamente como subpoligono monotono si el poligono es monotono.
                        '''
                        newpolygons = self.orderPolygon()
                        return [newpolygons]
                    else:
                        '''
                        Devolver el resultado de la funcion recursiva.
                        '''
                        newpolygons.extend([self.orderPolygon()])
                        return newpolygons
                else:
                    return newpolygons
            else:
                '''
                Devolver el triangulo orientado correctamente si el subpoligono monotono es un triangulo.
                '''
                newpolygons = self.orderPolygon()
                return [newpolygons]

    def extractPolygon(self,i,j):
        '''
        Funcion para separar el subpoligono monotono del resto del poligono.
        @param i,j: Indices de los puntos de corte del subpoligono.
        '''

        '''
        Ordenar los puntos del poligono de acuerdo a los indices.
        '''
        newpolygon = SetOfPoint3d([])
        i1 = self.points[i][3]
        i2 = self.points[j][3]
        self.points.sort(key=lambda x:x[3])
        index = 0
        state = False
    
        '''
        Recorrer el poligono, hasta encontrar los puntos de corte y separar el subpoligono.
        '''
        while True:
            if (state == True):
                newpolygon.points.append(self.points[index])
                if (self.points[index][3] == i2):
                    break
                else:
                    del self.points[index]
            else:
                if (self.points[index][3] == i1):
                    state = True
                    newpolygon.points.append(self.points[index])
                index += 1
            if (index == len(self.points)):
                index = 0

        self.points.sort()
        newpolygon.points.sort()
        return self,newpolygon

    def orderPolygon(self):
        '''
        Funcion para orientar correctamente tanto triangulos como subpoligonos
        monotonos, empleando los indices originales.
        '''
        self.points.sort(key=lambda x:x[3])
        newpolygons = []
        for p in self.points:
            newpolygons.append(p[3])
        return newpolygons

    def obtainSegments(self,newcoord2,limit_corners,option):
        '''
        Funcion para obtener los segmentos que unen los puntos entre los dos poligonos del cuerpo.
        @param newcoord2     : Objeto ListPoints3d que contiene las coordenadas polares y los indices del poligono superior.
        @param limit_corners : Lista de subintervalos en los cuales se debe restringir la busqueda. Si es "None", dichos
                               subintervalos no estan construidos y se debe buscar en todo el poligono opuesto.
        @param option        : Indica el tipo de vertice que se debe buscar en el poligono opuesto. Si es "0",
                               se debe encontrar un vertice de tipo similar que este mas cerca. Si es "1", se busca el
                               vertice regular mas cercano o de cualquier tipo. 
        '''

        newsegments = []
        '''
        Recorrer el poligono con mas puntos, para obtener un segmento para cada uno.
        '''
        for i in range(len(self.points)):
            candidates = SetOfPoint3d([])
            '''
            Obtener los puntos del poligono con menos puntos, que estan mas cercanos al punto
            evaluado del poligono con mas puntos.
            '''
            '''
            Caso en que no hay subintervalos de busqueda definidos (sin prebusqueda).
            '''
            if (limit_corners is None):
                for j in range(len(newcoord2.points)):
                    value1 = self.points[i][0]
                    value2 = newcoord2.points[j][0]
                    if (checkIntervalClosed(0,90,value1) == True and checkIntervalOpen(270,360,value2) == True):
                        value2 -= 360
                    if (checkIntervalClosed(0,90,value2) == True and checkIntervalOpen(270,360,value1) == True):
                        value2 += 360
                    if(abs(value1-value2) <= 90):
                        candidates.points.append([abs(value1-value2),newcoord2.points[j][1],j])
                '''
                Caso en que hubo prebusqueda (hay subintervalos iniciales de busqueda definidos). Se deben
                obtener nuevos subintervalos de busqueda mas acotados (definitivos). 
                '''
            else:
                for j in range(len(newcoord2.points)):
                    flag = False
                    for k in range(len(limit_corners)-1):
                        if ((checkIntervalSemiopen(limit_corners[k][0],limit_corners[k+1][0],i) == True) and \
                         (checkIntervalClosed(limit_corners[k+1][1],limit_corners[k][1],j) == True)):
                            flag = True
                    if ((i >= limit_corners[len(limit_corners)-1][0] or i < limit_corners[0][0]) and \
                     (j <= limit_corners[len(limit_corners)-1][1] or j >= limit_corners[0][1])):
                        flag = True
                    if (flag == True):
                        value1 = self.points[i][0]
                        value2 = newcoord2.points[j][0]
                        if (checkIntervalClosed(0,90,value1) == True and checkIntervalOpen(270,360,value2) == True):
                            value2 -= 360
                        if (checkIntervalClosed(0,90,value2) == True and checkIntervalOpen(270,360,value1) == True):
                            value2 += 360
                        if(abs(value1-value2) <= 90):
                            candidates.points.append([abs(value1-value2),newcoord2.points[j][1],j])

            candidates.points.sort()

            '''
            Reglas para buscar el vertice de tipo similar mas cercano, en caso de que se requiera 
            formar subintervalos iniciales o definitivos de busqueda.
            '''
            if (limit_corners is None or option == 0):
                '''
                Si el vertice evaluado es uno inicial, encontrar uno del mismo tipo en el poligono con menos puntos. Luego,
                intentar encontrar un vertice regular. Sino, el vertice mas cercano.
                '''
                if (self.points[i][1] == 1):
                    newsegments.append(candidates.checkCases([1],[3]))
                    '''
                    Si el vertice evaluado es uno final, encontrar uno del mismo tipo en el poligono con menos puntos. Luego,
                    intentar encontrar un vertice regular. Sino, el vertice mas cercano.
                    '''
                elif (self.points[i][1] == 2):
                    newsegments.append(candidates.checkCases([2],[3]))
                    '''
                    Si el vertice evaluado es uno de division, encontrar uno del mismo tipo en el poligono con menos puntos.
                    Luego, intentar encontrar un vertice regular. Sino, el vertice mas cercano.
                    '''
                elif (self.points[i][1] == 4):
                    newsegments.append(candidates.checkCases([4],[3]))
                    '''
                    Si el vertice evaluado es uno de combinacion, encontrar uno del mismo tipo en el poligono con menos puntos.
                    Luego, intentar encontrar un vertice regular. Sino, el vertice mas cercano.
                    '''
                elif (self.points[i][1] == 5):
                    newsegments.append(candidates.checkCases([5],[3]))
                    '''
                    Si el vertice evaluado es una esquina del poligono, encontrar a esquina mas cercana del poligono opuesto.
                    '''
                elif (self.points[i][1] == 7):
                    newsegments.append(candidates.checkCandidates([7])[1])
                    '''
                    Si el vertice evaluado es uno regular, mayor o igual a 90 grados, encontrar uno del mismo tipo en el
                    poligono con menos puntos. Sino, el vertice mas cercano.
                    '''
                elif (self.points[i][1] == 3):
                    newsegments.append(candidates.checkCases([3],[0]))
                    '''
                    Si el vertice evaluado es uno regular, menor a 90 grados, encontrar uno del mismo tipo en el
                    poligono con menos puntos. Luego, intentar con uno inicial, final, de division o combinacion, segun el caso.
                    Posteriormente, probar con uno regular igual o mayor a 90 grados.
                    Sino, el vertice mas cercano.
                    '''
                else:
                    newsegments.append(candidates.checkCases([self.points[i][1],1+self.points[i][1]-6,2+self.points[i][1]-6],[3]))
                '''
                Encontrar el vertice regular mas cercano o cualquiera, en caso de que los subintervalos definitivos 
                de busqueda esten creados.
                '''
            else:
                newsegments.append(candidates.checkCases([3],[0]))

        newsegments.sort()
        newsegments.reverse()
        return newsegments

    def checkCases(self,typevertex,typevertex2):
        '''
        Funcion para obtener un vertice del poligono con menos puntos, del tipo indicado y mas cercano. 
        En caso de no encontrarlo, hallarlo empleando la segunda lista de tipos. Si aun no se tiene exito devolver
        el vertice mas cercano sin importar el tipo.
        @param typevertex : Lista de tipos de vertices de los cuales se debe obtener el mas cercano.
                            Si el valor es 0, se obtiene el primero, sin importar el tipo.
        @param typevertex2: Lista de tipos de vertices de los cuales se debe obtener el mas cercano, en
                            caso de que falle la lista "typevertex".
        '''
        flag,result = self.checkCandidates(typevertex)
        if (flag == True):
            return result
        else:
            flag,result = self.checkCandidates(typevertex2)
            if (flag == True):
                return result
            else:
                flag,result = self.checkCandidates([0])
                return result

    def checkCandidates(self,typevertex):
        '''
        Funcion para obtener dentro de una lista de vertices candidatos, el mas cercano del tipo
        indicado.
        @param typevertex: Lista de tipos de vertices de los cuales se debe obtener el mas cercano.
                           Si el valor es 0, se obtiene el primero, sin importar el tipo.
        '''
        find = False
        for cand in self.points:
            if (cand[1] in typevertex or typevertex[0] == 0):
                find = True
                return True,cand[2]
        if (find == False):
            return find,0
