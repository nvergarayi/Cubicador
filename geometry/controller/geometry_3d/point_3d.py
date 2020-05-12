# -*- coding: utf-8 -*-
class Point3d(object):

    def __init__(self, x, y, z, rowid=-1):
        '''
        @param x: instancia de float
        @param y: instancia de float
        @param z: instancia de float
        '''
        self.x = float(x) 
        self.y = float(y)
        self.z = float(z)
        self.rowid = rowid
        
    @property
    def values(self):
        return (self.x, self.y, self.z)

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

    def check_point3d(self,list_points):
        '''
        Funcion para determinar si un punto existe en la lista dada como
        parametro o no. En caso positivo agregarlo.
        '''
        state = False
        for pt in list_points:
            if ((pt.x == self.x) and (pt.y == self.y) and (pt.z == self.z)):
                state = True
        #print ('state_point = ',state)
        if (state == False):
            list_points.append(self)

        return list_points

    def points_faces_cube(self,intersections_cube,face):
        '''
        Funcion para determinar si un punto existe en la lista de caras
        del cubo como parametro o no. En caso negativo agregarlo.
        '''
        state = False
        #print ('intersections_cube[face]',intersections_cube[face])
        for pt in intersections_cube[face]:
            if ((pt.x == self.x) and (pt.y == self.y) and (pt.z == self.z)):
                state = True
        if (state == False):
            intersections_cube[face].append(self)

        return intersections_cube
