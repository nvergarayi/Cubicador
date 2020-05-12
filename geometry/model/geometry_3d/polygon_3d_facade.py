# -*- coding: utf-8 -*-
from data_base.model.table_facade import TableFacade, addConnection
from geometry.controller.geometry_3d.polygon_3d import Polygon3d
from geometry.controller.geometry_3d.point_3d import Point3d

class Polygon3dFacade(TableFacade):
    
    def __init__(self):
        TableFacade.__init__(self, 'POLYGON_3D')
        if self.exist() is False:
            columns = [('NAME', TableFacade.COLUMN_TEXT)]
            self.create(columns)
            
    def factory(self, row):
        name, rowid = row
        points = _Polygon3dPoint3dFacade().findByPolygon3dId(rowid)
        return Polygon3d(points, name, rowid)
            
    def save(self, polygon3d):
        columns = ['NAME']
        values = [polygon3d.name]
        polygon3d.rowid = TableFacade.save(self, columns, values)
        _Polygon3dPoint3dFacade().save(polygon3d)
        return polygon3d.rowid
        
    @addConnection
    def delete(self, conn, polygon3d):
        query = 'DELETE FROM %s' % self.table
        query += ' WHERE rowid=%s' % polygon3d.rowid
        conn.execute(query)
        conn.commit()
        return _Polygon3dPoint3dFacade().deleteByPolygon3d(polygon3d)
    
    def findByRowid(self, rowid):
        columns = ['NAME']
        where = 'rowid=%s' % rowid
        result = self.findByColumnsWithRowid(columns, where)
        for row in result:
            return self.factory(row)
            
class _Polygon3dPoint3dFacade(TableFacade):
    
    def __init__(self):
        TableFacade.__init__(self, 'POLYGON_3D_POINT_3D')
        if self.exist() is False:
            columns = [('X', TableFacade.COLUMN_REAL),\
                       ('Y', TableFacade.COLUMN_REAL),\
                       ('Z', TableFacade.COLUMN_REAL),\
                       ('NEXT', TableFacade.COLUMN_INTEGER),\
                       ('POLYGON_3D', TableFacade.COLUMN_INTEGER)]
            self.create(columns)
            
    def save(self, polygon3d):
        points = polygon3d.points
        points.reverse()
        
        maxid = self.maxRowid()
        columns = ['X', 'Y', 'Z', 'NEXT', 'POLYGON_3D']
        ids = [-1] + [maxid+i+1 for i in range(len(polygon3d.points)-1)]
        values = [(polygon3d.points[i].x, polygon3d.points[i].y, polygon3d.points[i].z,\
                   ids[i], polygon3d.rowid) for i in range(len(polygon3d.points))]
        self.saveMany(columns, values)
        
    @addConnection
    def deleteByPolygon3d(self, conn, polygon3d):
        query = 'DELETE FROM %s' % self.table
        query += ' WHERE POLYGON_3D=%s' % polygon3d.rowid
        conn.execute(query)
        conn.commit()
        return True
    
    def findByPolygon3dId(self, polygon3dId):
        columns = ['X', 'Y', 'Z', 'NEXT']
        where = 'POLYGON_3D=%s' % polygon3dId
        points = self.findByColumnsWithRowid(columns, where)
        points = dict([(next, Point3d(x, y, z, rowid)) for x, y, z, next, rowid in points])
        
        next = -1
        result = []
        while next in points:
            point = points[next]
            result.append(point)
            next = point.rowid
        return result