# -*- coding: utf-8 -*-
from geometry.model.set_of_point_3d_facade import SetOfPoint3dFacade
from material_design.components.file_dialog import FileDialog
from material_design.nav.nav_tab_widget import NavTabWidget
from material_design.nav.item_widget import ItemWidget
from material_design.nav.nav_content import NavContent

class GeometryTab(NavTabWidget):
    
    def __init__(self, main, **kwargs):
        NavTabWidget.__init__(self, main, **kwargs)
        
        importCSVItem = ItemWidget('Importar desde CSV', icon='geometry_add_gray.png',\
                                   iconHover='geometry_add_blue.png', **kwargs)
        importCSVItem.released = self.importCSV
        self.addWidget(importCSVItem)
        
        self.addSeparator()
        self.geometryContent = NavContent(**kwargs)
        self.addWidget(self.geometryContent)
        
        for setOfPoint3d in SetOfPoint3dFacade().findAllWithoutPoints():
            self.addSetOfPoint3d(setOfPoint3d)
        
    def addSetOfPoint3d(self, setOfPoint3d):
        item = _SetOfPoint3dItem(setOfPoint3d, self, **self.kwargs)
        self.geometryContent.addItem(item)
        
    def importCSV(self):
        path = FileDialog.getOpenFileName(self.main, 'CSV', filter=('Csv (*.csv)'))
        if path is not None and len(path) > 0:
            from geometry.view.set_of_point_3d.import_from_csv.import_from_csv_content_button import ImportFromCSVContentButton
            ImportFromCSVContentButton(path, self)
            self.main.navWidget.hide()
            
class _SetOfPoint3dItem(ItemWidget):
    
    def __init__(self, setOfPoint3d, geometryTab, **kwargs):
        ItemWidget.__init__(self, setOfPoint3d.name, remove=True, **kwargs)
        self.setOfPoint3d = setOfPoint3d
        self.geometryTab = geometryTab
        self.main = geometryTab.main
        
    def remove(self):
        ItemWidget.remove(self)
        self.geometryTab.layout().removeWidget(self)
        SetOfPoint3dFacade().delete(self.setOfPoint3d)