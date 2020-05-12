# -*- coding: utf-8 -*-
from material_design.flat_button import FlatButton
from PyQt4.QtCore import QMimeData, QByteArray, Qt
from PyQt4.QtGui import QDrag

class CoordinateButton(FlatButton):
    
    MIME_TYPE = 'COORDINATE_BUTTON'
    
    def __init__(self, text, background):
        FlatButton.__init__(self, text, background=background, colorHover='WHITE',
                            backgroundHover=background)
    
    def mousePressEvent(self, event):
        self._selected = True
        
    def mouseReleaseEvent(self, event):
        del(self._selected)
        
    def mouseMoveEvent(self, event):
        if '_selected' in self.__dict__:
            mimeData = QMimeData()
            byteArray = QByteArray(self._label.text())
            mimeData.setData(CoordinateButton.MIME_TYPE, byteArray)
            
            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.start(Qt.CopyAction)
            
    def dragEnterEvent(self, event):
        event.accept()