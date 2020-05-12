# -*- coding: utf-8 -*-
class Curve3d(object):
    
    def __init__(self, points, name='', rowid=-1):
        '''
        @param points: lista de puntos Point3d.
        '''
        self.points = points
        self.rowid = rowid
        self.name = name
        
    def __str__(self, ):
        return str([(p.x, p.y, p.z) for p in self.points])

