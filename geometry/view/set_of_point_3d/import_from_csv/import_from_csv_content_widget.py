# -*- coding: utf-8 -*-
from geometry.controller.geometry_3d.set_of_point_3d import SetOfPoint3d
from material_design.components.slider_vertical import SliderVertical
from material_design.components.layout.hbox_layout import HBoxLayout
from geometry.model.set_of_point_3d_facade import SetOfPoint3dFacade
from material_design.tab_content_widget import TabContentWidget
from geometry.controller.geometry_3d.point_3d import Point3d
from material_design.flat_button import FlatButton
from material_design.components.label import Label
from material_design.text_field import TextField
from coordinate_button import CoordinateButton
from material_design.common.font import Font
from material_design.table import Table
from os.path import splitext, basename
from PyQt4.QtCore import Qt

class ImportFromCSVContentWidget(TabContentWidget):
    
    def __init__(self, path, geometryTabWidget):
        TabContentWidget.__init__(self, geometryTabWidget.main)
        self.geometryTabWidget = geometryTabWidget
        self.path = path
        
        infile = open(path, 'r')
        values = [line.replace('\n', '').split(',') for line in infile]
        headers = [] if len(values) < 1 else ['Columna %s' % (i+1) for i in range(len(values[0]))] 
        
        self.nameText = TextField(splitext(basename(path))[0])
        self.nameText.setMaximumWidth(400)
        
        nameLayout = HBoxLayout(margins=(0,0,0,0))
        nameLayout.addWidget(Label('Nombre:', color='GRAY',  font=Font.FUTURA_LT_LIGHT, font_size=12))
        nameLayout.addWidget(self.nameText)
        nameLayout.addStretch(0)
        self.addLayout(nameLayout)
        self.addSpacing(40)
        
        buttonsLayout = HBoxLayout(margins=(0,0,0,0), alignment=Qt.AlignCenter)
        buttonsLayout.addWidget(CoordinateButton('COORDENADA X', 'RED_500'))
        buttonsLayout.addWidget(CoordinateButton('COORDENADA Y', 'GREEN_500'))
        buttonsLayout.addWidget(CoordinateButton('COORDENADA Z', 'BLUE_500'))
        self.addLayout(buttonsLayout)
        self.addSpacing(20)
        
        self.tableWidget = Table(headers, values)
        tableLayout = HBoxLayout(margins=(0,0,0,0), alignment=Qt.AlignCenter)
        tableLayout.addWidget(self.tableWidget)
        self.addLayout(tableLayout)
        
        self.tableWidget._headerWidget.setAcceptDrops(True)
        self.tableWidget._headerWidget.dragEnterEvent = self._dragEnterEvent
        self.tableWidget._headerWidget.dragMoveEvent = self._dragMoveEvent
        self.tableWidget._headerWidget.dropEvent = self._dropEvent
        
        importButton = FlatButton('I M P O R T A R', reverse=True)
        importButton.released = self.importFromCSV
        importLayout = HBoxLayout(margins=(0,0,0,0), spacing=0)
        importLayout.setAlignment(Qt.AlignRight)
        importLayout.addWidget(importButton)
        self.addLayout(importLayout)
        
    def importFromCSV(self):
        coordx = None; coordy = None; coordz = None
        for i in range(self.tableWidget._headerWidget.columnCount()):
            background = self.tableWidget._headerWidget.item(0, i)._background
            if background == 'RED_500': coordx = i
            elif background == 'GREEN_500': coordy = i
            elif background == 'BLUE_500': coordz = i
        
        if coordx is not None and coordy is not None and coordz is not None:
            infile = open(self.path, 'r')
            values = [line.replace('\n', '').split(',') for line in infile]
            points = [Point3d(value[coordx], value[coordy], value[coordz]) for value in values]
            setOfPoint3d = SetOfPoint3d(points, splitext(basename(self.path))[0])
            SetOfPoint3dFacade().save(setOfPoint3d)
            self.geometryTabWidget.addSetOfPoint3d(setOfPoint3d)
            self.close()
            
    def resizeEvent(self, event):
        TabContentWidget.resizeEvent(self, event)
        width = self.tableWidget.COLUMN_WIDTH*self.tableWidget.columnCount()
        width += SliderVertical.WIDTH + 4
        width = self.content.width()-40 if self.content.width()-40 < width else width
        self.tableWidget.setWidth(width)
        
    def _dragMoveEvent(self, event):
        event.acceptProposedAction()
        
    def _dragEnterEvent(self, event):
        event.acceptProposedAction()
        
    def _dropEvent(self, event):
        column = self.tableWidget._headerWidget.columnAt(event.pos().x())
        event.setDropAction(Qt.MoveAction)
        event.acceptProposedAction()
        
        if str(event.mimeData().data(CoordinateButton.MIME_TYPE)) == 'COORDENADA X':
            background = 'RED_500'
        elif str(event.mimeData().data(CoordinateButton.MIME_TYPE)) == 'COORDENADA Y':
            background = 'GREEN_500'
        elif str(event.mimeData().data(CoordinateButton.MIME_TYPE)) == 'COORDENADA Z':
            background = 'BLUE_500'
            
        item = self.tableWidget._headerWidget.item(0, column)
        item.setBackgroundColor(background)
        item.setColor('WHITE')
        
        for c in range(self.tableWidget._headerWidget.columnCount()):
            if self.tableWidget._headerWidget.item(0, c)._background == background\
               and self.tableWidget._headerWidget.item(0, c) != item:
                self.tableWidget._headerWidget.item(0, c).setBackgroundColor(Table.HEADER_BACKGROUND)
                self.tableWidget._headerWidget.item(0, c).setColor(Table.HEADER_COLOR)