# -*- coding: utf-8 -*-
from material_design.components.layout.hbox_layout import HBoxLayout
from material_design.tab_content_widget import TabContentWidget
from set_of_point_3d_scatter_3d import SetOfPoint3dScatter3d
from material_design.components.widget import Widget
from material_design.table import Table
from PyQt4.QtGui import QSizePolicy

class SetOfPoint3dContentWidget(TabContentWidget):
    
    def __init__(self, setOfPoint3d, main):
        TabContentWidget.__init__(self, main)
        self.setOfPoint3d = setOfPoint3d
        
        headers = ['COORDENADA X', 'COORDENADA Y', 'COORDENADA Z']
        values = [(point.x, point.y, point.z) for point in self.setOfPoint3d.points]
        self.table = Table(headers, values, columnWidth=140)
        self.table.setWidth(140*3+4+16)
        
        self.scatterArea = _SetOfPoint3dScatter3dArea(values)
        
        horizontalLayout = HBoxLayout(margins=(0,0,0,0), spacing=0)
        horizontalLayout.addWidget(self.table)
        horizontalLayout.addWidget(self.scatterArea)
        self.addLayout(horizontalLayout)
        
class _SetOfPoint3dScatter3dArea(Widget):
    
    def __init__(self, values):
        Widget.__init__(self)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setLayout(HBoxLayout(margins=(2,2,2,2)))
        self.scatter =  SetOfPoint3dScatter3d(values)
        self.layout().addWidget(self.scatter)
        
    def resizeEvent(self, event):
        Widget.resizeEvent(self, event)
        vmin = (self.width() if self.width() < self.height() else self.height())-4
        self.scatter.setMinimumSize(vmin, vmin)
        self.scatter.setMaximumSize(vmin, vmin)