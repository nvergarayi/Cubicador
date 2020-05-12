# -*- coding: utf-8 -*-
from geometry.controller.geometry_3d.point_3d import Point3d
from geometry.controller.geometry_2d.point_2d import Point2D
from geometry.controller.geometry_2d.segment_2d import Segment2D
import math

class Segment3d(object):

  def __init__(self, p0, p1):
    '''
    @param p0: instancia de Point3d
    @param p1: instancia de Point3d
    '''
    self.p0 = p0
    self.p1 = p1

  '''
  Funcion para determinar en que octeto del cubo se hallan los puntos
  del segmento que lo intersecta.
  '''
  def get_octets(self,center_point):
    octet1 = 0
    octet2 = 0
    if (self.p0.x >= center_point.x):
      octet1 += 1
    if (self.p0.y >= center_point.y):
      octet1 += 2
    if (self.p0.z >= center_point.z):
      octet1 += 4
    if (self.p1.x >= center_point.x):
      octet2 += 1
    if (self.p1.y >= center_point.y):
      octet2 += 2
    if (self.p1.z >= center_point.z):
      octet2 += 4
    return [octet1,octet2]

  '''
  Funcion para determinar los puntos de interseccion del segmento con el cubo.
  '''
  def get_points_intersect(self,bounds,list_segments,octet):
    seg_xy = Segment2D(Point2D(self.p0.x,self.p0.y),Point2D(self.p1.x,self.p1.y))
    seg_yz = Segment2D(Point2D(self.p0.y,self.p0.z),Point2D(self.p1.y,self.p1.z))
    seg_xz = Segment2D(Point2D(self.p0.x,self.p0.z),Point2D(self.p1.x,self.p1.z))
    new_points = []
    points_faces_cube = []
    state1,p1 = list_segments[0].solve1(seg_xy)
    state2,p2 = list_segments[1].solve2(seg_xy)
    state3,p3 = list_segments[2].solve1(seg_yz)
    state4,p4 = list_segments[3].solve2(seg_yz)
    state5,p5 = list_segments[4].solve1(seg_xz)
    state6,p6 = list_segments[5].solve2(seg_xz)
    #print ('state123 = ',state1,state2,state3)
    #print ('state456 = ',state4,state5,state6)
    if (state1 == True and state4 == True):
        p = Point3d(p1.x,p4.x,p4.y)
        #print ('pststststts',p.x,p.y,p.z)
        new_points = p.check_point3d(new_points)
        if (octet in [0,1,4,5]):
          points_faces_cube.append([p,2])
        else:
          points_faces_cube.append([p,3])
        if (p.x == bounds[0]):
          points_faces_cube.append([p,0])
        if (p.x == bounds[1]):
          points_faces_cube.append([p,1])
        if (p.y == bounds[2]):
          points_faces_cube.append([p,2])
        if (p.y == bounds[3]):
          points_faces_cube.append([p,3])
        if (p.z == bounds[4]):
          points_faces_cube.append([p,4])
        if (p.z == bounds[5]):
          points_faces_cube.append([p,5])
    if (state2 == True and state6 == True):
        p = Point3d(p2.x,p2.y,p6.y)
        #print ('pststststts',p.x,p.y,p.z)
        new_points = p.check_point3d(new_points)
        if (octet in [0,2,4,6]):
          points_faces_cube.append([p,0])
        else:
          points_faces_cube.append([p,1])
        if (p.x == bounds[0]):
          points_faces_cube.append([p,0])
        if (p.x == bounds[1]):
          points_faces_cube.append([p,1])
        if (p.y == bounds[2]):
          points_faces_cube.append([p,2])
        if (p.y == bounds[3]):
          points_faces_cube.append([p,3])
        if (p.z == bounds[4]):
          points_faces_cube.append([p,4])
        if (p.z == bounds[5]):
          points_faces_cube.append([p,5])
    if (state3 == True and state5 == True):
        p = Point3d(p5.x,p3.x,p3.y)
        #print ('pststststts',p.x,p.y,p.z)
        new_points = p.check_point3d(new_points)
        if (octet < 4):
          points_faces_cube.append([p,4])
        else:
          points_faces_cube.append([p,5])
        if (p.x == bounds[0]):
          points_faces_cube.append([p,0])
        if (p.x == bounds[1]):
          points_faces_cube.append([p,1])
        if (p.y == bounds[2]):
          points_faces_cube.append([p,2])
        if (p.y == bounds[3]):
          points_faces_cube.append([p,3])
        if (p.z == bounds[4]):
          points_faces_cube.append([p,4])
        if (p.z == bounds[5]):
          points_faces_cube.append([p,5])

    if (len(new_points) == 2):
      dist = []
      dist.append(Segment3d(self.p0,new_points[0]).checkdistance())
      dist.append(Segment3d(self.p0,new_points[1]).checkdistance())
      if (dist[0] > dist[1]):
        new_points.reverse()
    return new_points,points_faces_cube

  '''
  Metodo que calcula la distancia entre dos puntos de un segmento.
  '''
  def checkdistance(self):
    return math.sqrt(((self.p1.x-self.p0.x)**2)+((self.p1.y-self.p0.y)**2)+((self.p1.z-self.p0.z)**2))