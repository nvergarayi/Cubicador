# -*- coding: utf-8 -*-
from geometry.controller.geometry_3d.set_of_point_3d import SetOfPoint3d
from data_base.model.table_facade import TableFacade, addConnection
from geometry.controller.geometry_3d.point_3d import Point3d

class SetOfPoint3dFacade(TableFacade):
    
    def __init__(self):
        TableFacade.__init__(self, 'SET_OF_POINT_3D')
        if self.exist() is False:
            columns = [('NAME', TableFacade.COLUMN_TEXT)]
            self.create(columns)
            
    def factory(self, row):
        name, rowid = row
        points = _SetOfPoint3dPoint3dFacade().findBySetOfPoint3dId(rowid)
        return SetOfPoint3d(points, name, rowid)
    
    def save(self, setOfPoint3d):
        columns = ['NAME']
        values = [setOfPoint3d.name]
        setOfPoint3d.rowid = TableFacade.save(self, columns, values)
        _SetOfPoint3dPoint3dFacade().save(setOfPoint3d)
        
    @addConnection
    def delete(self, conn, setOfPoint3d):
        rowid = setOfPoint3d.rowid
        query = 'DELETE FROM %s' % self.table
        query += ' WHERE rowid=%s' % rowid
        conn.execute(query)
        conn.commit()
        return _SetOfPoint3dPoint3dFacade().deleteBySetOfPoint3dId(rowid)
    
    def findAll(self):
        columns = ['NAME']
        result = self.findByColumnsWithRowid(columns)
        return [self.factory(row) for row in result]
    
    def findByRowid(self, rowid):
        columns = ['NAME']
        where = 'rowid=%s' % rowid
        result = self.findByColumnsWithRowid(columns, where)
        result = [self.factory(row) for row in result]
        if len(result) > 0: return result[0]
        
    def findByName(self, name):
        columns = ['NAME']
        where = 'NAME=\'%s\'' % name
        result = self.findByColumnsWithRowid(columns, where)
        result = [self.factory(row) for row in result]
        if len(result) > 0: return result[0]
        
    def findAllWithoutPoints(self):
        columns = ['NAME']
        result = self.findByColumnsWithRowid(columns)
        return [SetOfPoint3d([], name, rowid) for name, rowid in result]
        
class _SetOfPoint3dPoint3dFacade(TableFacade):
    
    def __init__(self):
        TableFacade.__init__(self, 'SET_OF_POINT_3D_POINT_3D')
        if self.exist() is False:
            columns = [('X', TableFacade.COLUMN_REAL),\
                       ('Y', TableFacade.COLUMN_REAL),\
                       ('Z', TableFacade.COLUMN_REAL),\
                       ('NEXT', TableFacade.COLUMN_INTEGER),\
                       ('SET_OF_POINT_3D', TableFacade.COLUMN_INTEGER)]
            self.create(columns)
            
    def save(self, setOfPoint3d):
        points = setOfPoint3d.points
        points.reverse()
        
        maxid = self.maxRowid()
        columns = ['X', 'Y', 'Z', 'NEXT', 'SET_OF_POINT_3D']
        ids = [-1] + [maxid+i+1 for i in range(len(setOfPoint3d.points)-1)]
        values = [(setOfPoint3d.points[i].x, setOfPoint3d.points[i].y, setOfPoint3d.points[i].z,\
                   ids[i], setOfPoint3d.rowid) for i in range(len(setOfPoint3d.points))]
        self.saveMany(columns, values)
        
    @addConnection
    def deleteBySetOfPoint3dId(self, conn, setOfPoint3dId):
        query = 'DELETE FROM %s' % self.table
        query += ' WHERE SET_OF_POINT_3D=%s' % setOfPoint3dId
        conn.execute(query)
        conn.commit()
        return True
    
    def findBySetOfPoint3dId(self, setOfPoint3dId):
        columns = ['X', 'Y', 'Z', 'NEXT']
        where = 'SET_OF_POINT_3D=%s' % setOfPoint3dId
        points = self.findByColumnsWithRowid(columns, where)
        points = sorted(points, reverse=True, key=lambda (x, y, z, nextid, rowid):nextid)
        return [Point3d(x, y, z, rowid) for x, y, z, nextid, rowid in points]        