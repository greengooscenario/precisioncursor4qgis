"""PrecisionCursor plugin for QGIS - sets mouse cursor to an arrow shape for precise clicks, 
anywhere you want it."""
#----------------------------------------------------------
# Copyright (C) 2021 Matthias Jacobs
# based upon "Minimal Plugin" by Martin Dobias
#-----------------------------------------------------------
# Licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#---------------------------------------------------------------------

from PyQt5.QtWidgets import QAction, QMessageBox
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from . import resources

def classFactory(iface):
    return PrecisionCursorPlugin(iface)


class PrecisionCursorPlugin:
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        self.action = QAction('P!', self.iface.mainWindow())
        myicon = QIcon(":/icons/PrecisionCursorIcon-png") # watch out: this is not a filename, but a logical path and nickname defined in resources.qrc (which is then compiled to resources.py, which we imported above)
        self.action.setIcon(myicon)        
        self.action.setToolTip("Switches the mouse cursor to a precision arrow")
        
        self.action.triggered.connect(self.run)
        self.action.setCheckable(True)
        self.iface.addToolBarIcon(self.action)


    def unload(self):
        QGuiApplication.instance().restoreOverrideCursor()
        self.iface.removeToolBarIcon(self.action)
        del self.action


    def run(self,signal):
        if signal==True :
            QGuiApplication.instance().setOverrideCursor(Qt.ArrowCursor)
        elif signal==False :
            QGuiApplication.instance().restoreOverrideCursor()



