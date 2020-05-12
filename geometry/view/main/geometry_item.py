# -*- coding: utf-8 -*-
from material_design.nav.nav_tab_item import NavTabItem
from geometry_tab import GeometryTab

class GeometryItem(NavTabItem):
    
    def __init__(self, navWidget, **kwargs):
        kwargs['icon'] = 'geometry_white.png'
        kwargs['activeIcon'] = 'geometry_gray.png'
        tab = GeometryTab(navWidget.main, color='GRAY_600')
        NavTabItem.__init__(self, 'Geometrias', navWidget, tab, **kwargs)

# from material_design.nav.title_widget import TitleWidget
# from geometry_tab_widget import GeometryTabWidget
# 
# class GeometryTitleWidget(TitleWidget):
#     
#     def __init__(self, navWidget):
#         TitleWidget.__init__(self, 'Geometrias', color='NAV_COLOR')
#         self.geometryTabWidget = GeometryTabWidget(navWidget)
# #         navWidget.addTab(self.geometryTabWidget)
#         
#     def released(self):
#         self.geometryTabWidget.show()