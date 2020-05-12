# -*- coding: utf-8 -*-
from geometry.controller.geometry_3d.point_3d import Point3d
from geometry.controller.geometry_3d.triangle_3d import Triangle3d
from geometry.controller.geometry_3d.solid_3d import Solid3d

class ReadDXFFile(object):

    @staticmethod
    def  getTriangle_s(path):
        result = []

        file = open(path)
        lines = file.readlines()

        index = 0

        while index < len(lines):

            if str(lines[index]).startswith("3DFACE"):

                while str(lines[index]).startswith(" 10") is False : index += 1
                x0 = float(lines[index+1])
                while str(lines[index]).startswith(" 20") is False : index += 1
                y0 = float(lines[index+1])
                while str(lines[index]).startswith(" 30") is False : index += 1
                z0 = float(lines[index+1])
                while str(lines[index]).startswith(" 11") is False : index += 1
                x1 = float(lines[index+1])
                while str(lines[index]).startswith(" 21") is False : index += 1
                y1 = float(lines[index+1])
                while str(lines[index]).startswith(" 31") is False : index += 1
                z1 = float(lines[index+1])
                while str(lines[index]).startswith(" 12") is False : index += 1
                x2 = float(lines[index+1])
                while str(lines[index]).startswith(" 22") is False : index += 1
                y2 = float(lines[index+1])
                while str(lines[index]).startswith(" 32") is False : index += 1
                z2 = float(lines[index+1])

                p0 = Point3d(x0, y0, z0)
                p1 = Point3d(x1, y1, z1)
                p2 = Point3d(x2, y2, z2)
                
                result.append(Triangle3d(p0, p1, p2))
            
            index += 1
                
        return Solid3d(result)

