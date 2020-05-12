# -*- coding: utf-8 -*-
from import_from_csv_content_widget import ImportFromCSVContentWidget

class ImportFromCSVContentButton():
    
    def __init__(self, path, geometryTabWidget):
        widget = ImportFromCSVContentWidget(path, geometryTabWidget)
        geometryTabWidget.main.addTab('Importar desde CSV', widget)