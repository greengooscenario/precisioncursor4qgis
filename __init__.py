#-----------------------------------------------------------
# PrecisionCursor - sets mouse cursor to an arrow shape for precise clicks, 
# anywhere you want it.
#
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
import PrecisionCursor.resources

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
        
        self.action.triggered.connect(self.newrun)
#        self.action.toggled.connect(self.run)
        self.action.setCheckable(True)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        QGuiApplication.instance().restoreOverrideCursor()
        self.iface.removeToolBarIcon(self.action)
        del self.action

    def newrun(self,signal):
# diagn        QMessageBox.information(None, 'PreciCursor', 'Toggled: '+str(signal))
        if signal==True :
            QGuiApplication.instance().setOverrideCursor(Qt.ArrowCursor)
# diagn            QMessageBox.information(None, 'Precision cursor plugin', 'Precision Cursor activated!')
        elif signal==False :
# diagn            QMessageBox.information(None, 'Precision cursor plugin', 'Precision Cursor deactivated!')
            QGuiApplication.instance().restoreOverrideCursor()



    def run(self):
        if self.action.checked==1 :
#            QGuiApplication.instance().setOverrideCursor(Qt.ArrowCursor)
            QMessageBox.information(None, 'Precision cursor plugin', 'Precision Cursor activated!')
        elif self.action.checked==0 :
            QMessageBox.information(None, 'Precision cursor plugin', 'Precision Cursor deactivated!')
#            QGuiApplication.instance().restoreOverrideCursor()




