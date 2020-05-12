# -*- coding: utf-8 -*-
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from material_design.common.color import Color
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.figure import Figure
from PyQt4.QtGui import QSizePolicy
from matplotlib import font_manager

class SetOfPoint3dScatter3d(FigureCanvasQTAgg):
    
    def __init__(self, values):
        figure = Figure()
        FigureCanvasQTAgg.__init__(self, figure)
        prop = font_manager.FontProperties(fname='resources/fonts/FUTURA_LT_LIGHT.TTF')
        
        sizePolicy = QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(True)
        self.setSizePolicy(sizePolicy)
        
        self.subplot = Axes3D(figure)
        self.figure = figure
        
        xs, ys, zs = zip(*values)
        self.subplot.scatter(xs, ys, zs)

        self.xlabel = self.subplot.set_xlabel('COORDENADA X')
        self.ylabel = self.subplot.set_ylabel('COORDENADA Y')
        self.zlabel = self.subplot.set_zlabel('COORDENADA Z')
        
        for label in [self.xlabel, self.ylabel, self.zlabel]:
            label.set_color(Color.matplotlib('DARK_DARK_GRAY'))
            label.set_fontproperties(prop)
            label.set_fontsize(12)
        
        for axis in [self.subplot.w_xaxis, self.subplot.w_yaxis, self.subplot.w_zaxis]:
            axis.set_pane_color(Color.matplotlib('SOFT_SOFT_GRAY'))
            for tick in axis.get_major_ticks():
                tick.label1.set_color(Color.matplotlib('DARK_DARK_GRAY'))
                tick.label1.set_fontproperties(prop)
                tick.label1.set_fontsize(9)