# -*- coding: utf-8 -*-
from data_base.model.table_facade import TableFacade, addConnection
from geometry.controller.geometry_3d.curve_3d import Curve3d
from geometry.controller.geometry_3d.point_3d import Point3d

class Curve3dFacade(TableFacade):
    
    def __init__(self):
        TableFacade.__init__(self, 'CURVE_3D')
        if self.exist() is False:
            columns = [('NAME', TableFacade.COLUMN_TEXT)]
            self.create(columns)
            
    def factory(self, row):
        name, rowid = row
        points = _Curve3dPoint3dFacade().findByCurve3dId(rowid)
        return Curve3d(points, name, rowid)
    
    def save(self, curve3d):
        columns = ['NAME']
        values = [curve3d.name]
        curve3d.rowid = TableFacade.save(self, columns, values)
        _Curve3dPoint3dFacade().save(curve3d)
        
    @addConnection
    def delete(self, conn, curve3d):
        query = 'DELETE FROM %s' % self.table
        query += ' WHERE rowid=%s' % curve3d.rowid
        conn.execute(query)
        conn.commit()
        return _Curve3dPoint3dFacade().deleteByCurve3d(curve3d)
    
    def findByRowid(self, rowid):
        columns = ['NAME']
        where = 'rowid=%s' % rowid
        result = self.findByColumnsWithRowid(columns, where)
        for row in result:
            return self.factory(row)
        
class _Curve3dPoint3dFacade(TableFacade):
    
    def __init__(self):
        TableFacade.__init__(self, 'CURVE_3D_POINT_3D')
        if self.exist() is False:
            columns = [('X', TableFacade.COLUMN_REAL),\
                       ('Y', TableFacade.COLUMN_REAL),\
                       ('Z', TableFacade.COLUMN_REAL),\
                       ('NEXT', TableFacade.COLUMN_INTEGER),\
                       ('CURVE_3D', TableFacade.COLUMN_INTEGER)]
            self.create(columns)
            
    def save(self, curve3d):
        points = curve3d.points
        points.reverse()
        
        maxid = self.maxRowid()
        columns = ['X', 'Y', 'Z', 'NEXT', 'CURVE_3D']
        ids = [-1] + [maxid+i+1 for i in range(len(curve3d.points)-1)]
        values = [(curve3d.points[i].x, curve3d.points[i].y, curve3d.points[i].z,\
                   ids[i], curve3d.rowid) for i in range(len(curve3d.points))]
        self.saveMany(columns, values)
        
    @addConnection
    def deleteByCurve3d(self, conn, curve3d):
        query = 'DELETE FROM %s' % self.table
        query += ' WHERE CURVE_3D=%s' % curve3d.rowid
        conn.execute(query)
        conn.commit()
        return True
    
    def findByCurve3dId(self, curve3dId):
        columns = ['X', 'Y', 'Z', 'NEXT']
        where = 'CURVE_3D=%s' % curve3dId
        points = self.findByColumnsWithRowid(columns, where)
        points = dict([(next, Point3d(x, y, z, rowid)) for x, y, z, next, rowid in points])
        
        next = -1
        result = []
        while next in points:
            point = points[next]
            result.append(point)
            next = point.rowid
        return result