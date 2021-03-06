# -*- coding: utf-8 -*-
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from geometry.controller.geometry_2d.rectangle_2d import Rectangle2D
from geometry.controller.geometry_3d.triangle_3d import Triangle3d
from geometry.controller.geometry_3d.polygon_3d import Polygon3d
from geometry.controller.geometry_3d.cube_3d import Cube3d
from geometry.controller.geometry_3d.read_dxf_file import ReadDXFFile
from geometry.controller.geometry_3d.solid_3d import Solid3d
from geometry.controller.geometry_3d.curve_3d import Curve3d
from geometry.controller.geometry_3d.point_3d import Point3d
from geometry.controller.geometry_2d.point_2d import Point2D
from sys import float_info
import time
import math
# from triangle import Triangle3d

# '''
# Funcion graficadora del resultado de la triangulacion.
# '''
#def chart(polygon,color):
#   for triangle in polygon:
#     xs = []; ys = []
#     #for point in triangle:
#     #    xs.append(point.x); ys.append(point.y)
#     xs.append(triangle.p0.x)
#     xs.append(triangle.p1.x)
#     xs.append(triangle.p2.x)
#     ys.append(triangle.p0.y)
#     ys.append(triangle.p1.y)
#     ys.append(triangle.p2.y)
#     for i in range(len(xs)-1):
#       plt.plot(xs[i:i+2], ys[i:i+2], color)
#     plt.plot([xs[len(xs)-1], xs[0]], [ys[len(xs)-1], ys[0]], color)
#   #plt.show()
# 
# def chart2(curve,color):
#   xcoord = []; ycoord = [];
#   for t in curve:
#     xcoord.append(t.x)
#     ycoord.append(t.y)
#   for i in range(len(xcoord)-1):
#     plt.plot(xcoord[i:i+2], ycoord[i:i+2], color)
#   plt.plot([xcoord[len(xcoord)-1], xcoord[0]], [ycoord[len(xcoord)-1], ycoord[0]], color)
#   #plt.show()
'''
Metodo graficador.
'''
def chart(polygon):

    for subpolygon in polygon:
        xs = []; ys = []
        for point in subpolygon:
            xs.append(point.x); ys.append(point.y)
        for i in range(len(xs)-1):
            plt.plot(xs[i:i+2], ys[i:i+2], 'r')
        plt.plot([xs[len(xs)-1], xs[0]], [ys[len(xs)-1], ys[0]], 'r')
    plt.show()

def main():
  
  polygon = Polygon3d([Point3d(x, y, z) for x, y, z in [(82369.828, 72182.659, 2543.001), (82372.394, 72178.129, 2542.758), (82377.71, 72169.938, 2542.415), (82381.014, 72163.561, 2542.425), (82383.613, 72159.13, 2542.314), (82386.395, 72154.729, 2542.105), (82388.84, 72150.153, 2542.13), (82393.078, 72140.715, 2541.759), (82394.764, 72135.952, 2541.478), (82396.178, 72130.901, 2541.117), (82397.238, 72125.88, 2540.579), (82396.412, 72121.84, 2540.473), (82393.572, 72117.671, 2540.043), (82390.316, 72113.789, 2539.779), (82386.786, 72109.922, 2539.73), (82382.201, 72107.695, 2539.91), (82377.656, 72104.957, 2539.593), (82373.125, 72102.197, 2539.514), (82369.272, 72098.901, 2539.373), (82364.919, 72095.949, 2539.313), (82360.274, 72093.544, 2539.256), (82355.67, 72090.941, 2539.09), (82351.024, 72088.91, 2539.052), (82346.553, 72086.26, 2538.897), (82340.765, 72081.55, 2538.492), (82336.421, 72078.906, 2538.275), (82332.389, 72075.677, 2538.08), (82328.749, 72071.917, 2537.946), (82325.232, 72067.99, 2537.863), (82321.724, 72064.288, 2537.865), (82318.032, 72060.64, 2537.995), (82314.75, 72056.624, 2538.017), (82310.962, 72053.089, 2537.922), (82307.38, 72049.586, 2537.804), (82303.823, 72045.841, 2537.735), (82300.126, 72041.951, 2537.747), (82296.32, 72038.292, 2537.723), (82292.355, 72034.778, 2537.566), (82288.594, 72031.263, 2537.352), (82284.654, 72027.722, 2537.029), (82281.074, 72024.148, 2536.822), (82277.508, 72020.384, 2536.627), (82273.735, 72016.843, 2536.457), (82269.93, 72013.2, 2536.385), (82266.065, 72009.778, 2536.227), (82262.37, 72006.324, 2536.185), (82258.884, 72002.69, 2536.148), (82255.453, 71998.997, 2536.099), (82251.876, 71995.41, 2535.969), (82248.024, 71991.789, 2535.847), (82244.074, 71988.548, 2535.651), (82240.137, 71985.019, 2535.465), (82236.765, 71981.315, 2535.263), (82236.335, 71980.402, 2535.275), (82234.357, 71979.281, 2535.125), (82230.418, 71975.802, 2534.927), (82227.031, 71971.862, 2534.841), (82223.439, 71968.257, 2534.823), (82219.499, 71964.906, 2534.659), (82215.936, 71961.306, 2534.475), (82212.413, 71957.5, 2534.274), (82208.833, 71953.711, 2534.234), (82205.363, 71950.077, 2534.043), (82201.612, 71946.528, 2533.885), (82197.352, 71943.452, 2533.742), (82192.79, 71940.75, 2533.574), (82189.011, 71937.374, 2533.426), (82185.075, 71933.809, 2533.357), (82181.333, 71930.441, 2533.241), (82177.676, 71926.617, 2533.18), (82174.124, 71922.848, 2533.026), (82170.492, 71919.195, 2532.803), (82166.973, 71915.632, 2532.674), (82163.657, 71911.859, 2532.499), (82160.215, 71908.068, 2532.296), (82156.525, 71904.293, 2532.099), (82152.663, 71901.065, 2532.049), (82148.795, 71897.547, 2532.011), (82145.085, 71893.926, 2531.817), (82141.571, 71890.289, 2531.74), (82138.226, 71886.362, 2531.62), (82134.64, 71882.58, 2531.433), (82130.95, 71878.869, 2531.401), (82127.11, 71875.365, 2531.312), (82123.844, 71871.409, 2531.3), (82120.335, 71867.672, 2531.21), (82116.797, 71864.1, 2531.059), (82113.125, 71860.705, 2530.866), (82109.467, 71857.295, 2530.64), (82105.652, 71853.936, 2530.401), (82101.636, 71850.499, 2530.271), (82097.961, 71846.75, 2530.148), (82094.565, 71842.904, 2529.938), (82091.122, 71839.215, 2529.794), (82087.025, 71835.936, 2529.671), (82082.911, 71832.916, 2529.595), (82079.009, 71829.706, 2529.554), (82075.205, 71826.423, 2529.308), (82072.017, 71822.489, 2528.915), (82068.843, 71818.269, 2528.727), (82065.404, 71814.373, 2528.693), (82062.137, 71807.216, 2529.544), (82059.046, 71803.125, 2528.435), (82056.724, 71798.606, 2528.604), (82055.39, 71793.711, 2528.411), (82052.458, 71789.376, 2528.275), (82049.912, 71784.877, 2527.995), (82046.315, 71782.778, 2528.062), (82043.679, 71787.036, 2528.12), (82041.465, 71791.685, 2528.189), (82039.339, 71796.55, 2528.374), (82037.178, 71801.243, 2528.63), (82035.386, 71805.992, 2528.85), (82033.205, 71810.572, 2528.905), (82030.552, 71815.172, 2528.842), (82029.088, 71817.474, 2528.914), (82027.326, 71820.863, 2529.009), (82024.764, 71825.185, 2529.161), (82022.508, 71829.965, 2529.268), (82019.987, 71834.504, 2529.344), (82017.926, 71839.16, 2529.625), (82015.264, 71843.456, 2529.666), (82013.051, 71847.986, 2529.894), (82010.367, 71852.53, 2530.145), (82007.997, 71857.104, 2530.749), (82007.857, 71862.179, 2531.416), (82011.547, 71865.559, 2532.317), (82016.381, 71867.204, 2530.533), (82020.954, 71869.406, 2530.005), (82024.554, 71872.888, 2530.271), (82028.313, 71876.533, 2530.357), (82031.942, 71880.174, 2530.483), (82034.937, 71884.316, 2530.521), (82038.175, 71888.407, 2530.616), (82041.439, 71892.513, 2530.814), (82044.708, 71896.332, 2530.865), (82047.987, 71900.339, 2530.984), (82051.051, 71904.322, 2531.082), (82054.452, 71908.248, 2531.247), (82058.01, 71912.027, 2531.44), (82061.753, 71915.643, 2531.579), (82065.435, 71919.149, 2531.786), (82069.29, 71922.813, 2532.002), (82072.604, 71926.697, 2532.211), (82076.147, 71930.318, 2532.316), (82079.715, 71933.891, 2532.391), (82083.675, 71937.071, 2532.603), (82087.691, 71940.146, 2532.792), (82091.754, 71943.615, 2532.896), (82095.738, 71946.935, 2533.097), (82099.564, 71950.395, 2533.223), (82103.675, 71953.476, 2533.309), (82107.673, 71956.838, 2533.389), (82111.221, 71960.595, 2533.576), (82114.852, 71964.167, 2533.824), (82119.066, 71967.379, 2533.907), (82122.879, 71970.782, 2534.154), (82126.464, 71974.574, 2534.36), (82130.17, 71978.053, 2534.449), (82133.801, 71981.511, 2534.423), (82137.261, 71985.478, 2534.288), (82140.724, 71989.099, 2534.28), (82144.481, 71992.44, 2534.371), (82148.223, 71995.87, 2534.564), (82152.173, 71999.402, 2534.689), (82155.887, 72003.23, 2534.901), (82159.599, 72006.773, 2535.036), (82163.261, 72010.358, 2535.191), (82166.875, 72014.097, 2535.307), (82170.592, 72017.768, 2535.358), (82174.405, 72021.328, 2535.511), (82178.331, 72024.631, 2535.77), (82182.378, 72027.743, 2535.929), (82186.495, 72030.95, 2536.091), (82190.523, 72034.082, 2536.416), (82194.542, 72037.129, 2536.637), (82198.427, 72040.321, 2536.782), (82202.606, 72043.482, 2536.784), (82206.456, 72046.887, 2537.011), (82210.715, 72049.871, 2537.062), (82214.595, 72053.161, 2537.2), (82218.348, 72056.569, 2537.324), (82221.829, 72059.528, 2537.357), (82221.91, 72059.541, 2537.363), (82225.889, 72062.811, 2537.561), (82229.69, 72066.265, 2537.596), (82232.92, 72070.169, 2537.718), (82236.148, 72074.034, 2537.836), (82239.923, 72077.457, 2537.95), (82243.638, 72081.161, 2538.06), (82247.411, 72084.887, 2538.212), (82251.438, 72088.357, 2538.371), (82255.584, 72091.547, 2538.551), (82259.459, 72095.081, 2538.731), (82263.217, 72098.845, 2538.923), (82266.798, 72102.5, 2539.065), (82270.475, 72106.0, 2539.229), (82274.165, 72109.499, 2539.311), (82277.882, 72112.951, 2539.411), (82281.465, 72116.681, 2539.469), (82284.749, 72120.499, 2539.536), (82287.954, 72124.405, 2539.677), (82291.744, 72127.806, 2539.899), (82295.753, 72131.145, 2540.021), (82299.376, 72134.669, 2540.016), (82305.692, 72141.673, 2540.717), (82309.467, 72144.98, 2540.995), (82313.32, 72148.536, 2541.071), (82316.38, 72152.524, 2540.944), (82320.642, 72155.454, 2541.016), (82324.569, 72158.789, 2541.067), (82328.502, 72162.236, 2541.373), (82332.72, 72164.992, 2541.52), (82337.296, 72167.244, 2541.611), (82341.459, 72170.258, 2541.807), (82345.834, 72173.021, 2542.01), (82350.134, 72175.757, 2542.174), (82354.611, 72178.522, 2542.338), (82358.778, 72181.405, 2542.468), (82363.033, 72184.075, 2542.634)]])
  advanceBottom = Curve3d([Point3d(x, y, z) for x, y, z in [(82041.198, 71877.897, 2530.732), (82042.544, 71873.069, 2530.565), (82043.888, 71868.055, 2530.45), (82046.268, 71863.635, 2530.39), (82048.76, 71859.247, 2530.339), (82051.924, 71855.153, 2530.253), (82055.489, 71851.327, 2530.292), (82059.436, 71848.056, 2530.155), (82063.586, 71845.105, 2529.952), (82068.117, 71842.832, 2529.949), (82072.69, 71840.604, 2529.902), (82077.572, 71839.088, 2529.923), (82082.54, 71840.274, 2529.971)]])
  advanceTop = Curve3d([Point3d(x, y, z) for x, y, z in [(82074.096, 71830.142, 2535.588), (82074.63, 71832.07, 2535.588), (82069.141, 71831.559, 2535.702), (82069.786, 71833.454, 2535.702), (82064.402, 71833.439, 2535.705), (82065.162, 71835.29, 2535.705), (82059.645, 71835.459, 2535.64), (82060.594, 71837.229, 2535.64), (82055.23, 71838.369, 2535.629), (82056.364, 71840.017, 2535.629), (82051.127, 71841.317, 2535.618), (82052.413, 71842.856, 2535.618), (82047.417, 71844.905, 2535.8), (82048.904, 71846.249, 2535.8), (82044.215, 71848.97, 2535.841), (82045.777, 71850.22, 2535.841), (82041.01, 71852.918, 2535.91), (82042.649, 71854.072, 2535.91), (82038.399, 71857.229, 2535.933), (82040.153, 71858.195, 2535.933), (82036.148, 71861.747, 2536.066), (82037.946, 71862.624, 2536.066), (82033.921, 71866.418, 2536.173), (82035.8, 71867.125, 2536.173)]])
  headBottom = Curve3d([Point3d(x, y, z) for x, y, z in [(82017.222, 71859.594, 2529.976), (82018.919, 71854.719, 2529.917), (82021.159, 71850.186, 2529.721), (82023.539, 71845.549, 2529.647), (82026.3, 71841.342, 2529.736), (82029.341, 71837.069, 2529.539), (82032.389, 71832.957, 2529.357), (82035.815, 71829.249, 2529.197), (82038.71, 71825.037, 2529.172), (82041.766, 71820.909, 2529.243), (82045.926, 71817.936, 2529.091), (82049.073, 71813.767, 2528.658), (82052.587, 71810.142, 2528.306)]])
  headTop = Curve3d([Point3d(x, y, z) for x, y, z in [(82027.093, 71863.713, 2536.132), (82025.195, 71863.081, 2536.132), (82028.829, 71858.898, 2536.154), (82027.029, 71857.992, 2536.154), (82031.696, 71854.586, 2536.092), (82029.973, 71853.565, 2536.092), (82034.074, 71850.049, 2536.033), (82032.384, 71848.965, 2536.033), (82037.134, 71846.087, 2536.023), (82035.494, 71844.939, 2536.023), (82039.9, 71841.705, 2535.814), (82038.315, 71840.47, 2535.814), (82043.361, 71838.07, 2535.831), (82041.975, 71836.625, 2535.831), (82047.172, 71834.727, 2535.739), (82045.927, 71833.159, 2535.739), (82051.313, 71831.756, 2535.774), (82050.137, 71830.138, 2535.774), (82055.514, 71828.659, 2535.746), (82054.489, 71826.93, 2535.746), (82060.237, 71826.469, 2535.624), (82059.471, 71824.62, 2535.624), (82065.077, 71824.695, 2535.722), (82064.417, 71822.807, 2535.722)]])

  left_curve = headBottom
  right_curve = advanceBottom
  left_crown = headTop
  right_crown = advanceTop

#   for p in polygon0:
#     polygon.points.append(Point3d(p[0],p[1],p[2]))
#   for p in curve0:
#     right_curve.points.append(Point3d(p[0],p[1],p[2]))
# 
#   '''
#   Generar la segunda curva que intersecta la cancha.
#   '''
#   for p in right_curve.points:
#     left_curve.points.append(Point3d(p.x,p.y+30,p.z+1))
# 
#   '''
#   Generar las coronas.
#   '''
#   for p in left_curve.points:
#     left_crown.points.append(Point3d(p.x,p.y,p.z+50))
#   for p in right_curve.points:
#     right_crown.points.append(Point3d(p.x,p.y,p.z+50))

  '''
  Intersectar un poligono con varios rectangulos para obtener los rectangulos de interseccion.
  '''
  polygon_rect = Polygon3d.getPolygons3DFromDXF('poligono.dxf')
  rectangles = Rectangle2D.getRectangles2DFromCSV('modelo.csv', 'xcentre', 'ycentre', 'zcentre', 'xlength', 'ylength', 'zlength', 'poly')
  polygons = polygon_rect.getIntersectionRectangles(rectangles)
  #chart(polygons)

  '''
  Intersectar un solido con varios cubos para obtener los cubos de interseccion.
  '''
  #solid = ReadDXFFile.getTriangle_s("FY12_lito_BRXH.dxf")
  solid = ReadDXFFile.getTriangle_s("solido.dxf")
  cubes = Cube3d.getCubes3DFromCSV('modelo.csv', 'xcentre', 'ycentre', 'zcentre', 'xlength', 'ylength', 'zlength', 'poly')
  #init = time.time()
  #solid.cubicatorGeometricVersion(cubes)
  solid.cubicatorMarchingCubes(cubes)
  #solid.cubicatorMarchingCubes2(cubes)
  #print (str('time ='),time.time()-init)
  
  '''
  Generar el solido de interseccion y calcular su volumen.
  '''
  intersection_solid, volume_solid , sub_solids, heights= \
   polygon.getIntersectionSolid(left_curve,right_curve,left_crown,right_crown)

#   print intersection_solid.triangles
#   
  print ('volume_solid =',volume_solid)

  '''
  Graficar los dos subpoligonos.
  '''
  #chart(left_polygon,'b')
  #chart(right_polygon,'r')
  #plt.show()
  #chart(intersection_solid.triangles,'g')
  #plt.show()
  
  
  fig = plt.figure()
  ax = Axes3D(fig)
  
  xmin = float_info.max; xmax = float_info.min
  ymin = float_info.max; ymax = float_info.min
  zmin = float_info.max; zmax = float_info.min
  
  
  verts = []
  for t in intersection_solid.triangles:
#     verts.append()
    ax.add_collection3d(Poly3DCollection([[t.p0.values, t.p1.values, t.p2.values]]))
    for p in [t.p0, t.p1, t.p2]:
        xmin = xmin if xmin < p.x else p.x
        xmax = xmax if xmax > p.x else p.x
        
        ymin = ymin if ymin < p.y else p.y
        ymax = ymax if ymax > p.y else p.y
        
        zmin = zmin if zmin < p.z else p.z
        zmax = zmax if zmax > p.z else p.z
        
  print (xmin, xmax)
  print (ymin, ymax)
  print (zmin, zmax)
#       print , t.p1, t.p2
  ax.set_xlim(xmin, xmax)
  ax.set_ylim(ymin, ymax)
  ax.set_zlim(zmin, zmax)
#   x = [0,1,1]
#   y = [0,0,1]
#   z = [0,1,0]
#   verts = [zip(x, y,z)]
  
  plt.show()

if __name__ == "__main__":
    main()
