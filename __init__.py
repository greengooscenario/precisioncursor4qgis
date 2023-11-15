"""PrecisionCursor plugin for QGIS -
sets mouse cursor to a crosshair or arrow shape
for precise clicks, anytime you want it."""
# ----------------------------------------------------------
# Copyright (C) 2021-2023 Matthias Jacobs
# based upon "Minimal Plugin" by Martin Dobias
# -----------------------------------------------------------
# Licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# ---------------------------------------------------------------------

import os

from PyQt5.QtWidgets import QAction, QActionGroup, QToolButton, QMenu
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *

from qgis.core import (Qgis, QgsSettings)


def classFactory(iface):
	return PrecisionCursorPlugin(iface)


class PrecisionCursorPlugin:
	def __init__(self, iface):
		self.parentInterface = iface
		#self.parentInterface.messageBar().pushMessage('Note', 'Initiating PrecisionCursor Plugin...') # <- diagnostic
	
	
	def initGui(self):
		# Load settings
		self.s = QgsSettings()
		# Scan for pointer image files
		self.scanFiles()
		self.choice = int(self.s.value("PreciCursorPlugin/pointerChoice", 0))
		# ^ Note well: Changing this QgsSetting in the middle of the code
		# produces hard-to-track errors! Better use a normal variable, and only
		# save the setting in the unload procedure.
		
		# Generate main button
		self.switchOn = QAction('Mouse cursor shape override', self.parentInterface.mainWindow())
		iconPath = os.path.join(os.path.dirname(__file__), 'graphics','PrecisionCursorIcon07.png')
		#iconPath = (self.s.value("PreciCursorPlugin/pointerFileName" + self.s.value( "PreciCursorPlugin/pointerChoice", 0).__str__())) # <- this variant changes the main button icon based on cursor choice
		myIcon = QIcon(iconPath)
		self.switchOn.setIcon(myIcon)
		self.switchOn.setToolTip('Switches the mouse cursor to a configurable pointer')
		#self.switchOn.setStatusTip('Mouse cursor override active!')
		self.switchOn.setCheckable(True)
		#self.switchOn.triggered.connect(self.run)
		self.switchOn.toggled.connect(self.run) # "hovered" and "changed" may also be worth a try?
		# Have the Cursor palette initiated based on the settings
		palette = self.initSelectionMenu()
		self.switchOn.setMenu(palette)
		
		# generate a button, bind the main QAction to it and install to toolbar
		switchOnButton = QToolButton()
		switchOnButton.setPopupMode(QToolButton.MenuButtonPopup)
		switchOnButton.setDefaultAction(self.switchOn)
		self.ourToolBar = self.parentInterface.pluginToolBar()
		self.buttonHandle = self.ourToolBar.addWidget(switchOnButton)
	
	
	def scanFiles(self):
		"""
		scans for .png-files the "pointers" dir and saves them as settings
		:return: a string with the first pointer filename and the number of pointer files found, or "Fail!".
		"""
		self.s = QgsSettings()
		i = 0
		for path, directories, files in os.walk(os.path.join(os.path.dirname(__file__), "pointers")):
			for file in files:
				if file.upper().endswith('PNG'):
					self.s.setValue("PreciCursorPlugin/pointerFileName" + str(i), os.path.join(path, file))
					self.s.setValue("PreciCursorPlugin/hotspotX" + str(i), int(15))
					self.s.setValue("PreciCursorPlugin/hotspotY" + str(i), int(15))
					i += 1
		self.s.remove("PreciCursorPlugin/pointerFileName" + str(i))
		self.s.remove("PreciCursorPlugin/hotspotX" + str(i))
		self.s.remove("PreciCursorPlugin/hotspotY" + str(i))
		return self.s.value("PreciCursorPlugin/pointerFileName0", "FAIL!").__str__() + ' -' + str(i) + (
			' File entries')
	
	
	def initSelectionMenu(self):
		selectionMenu = QMenu()
		selectionMenu.setTearOffEnabled(True)
		selectionGroup = QActionGroup(selectionMenu)
		
		# Generate an entry for the system standard ArrowCursor:
		sysStdArrow = QAction('Standard Arrow', self.parentInterface.mainWindow())
		
		arrowIconPath = os.path.join(os.path.dirname(__file__), 'graphics', 'SysStdArrowIcon03.png')
		arrowIcon = QIcon(arrowIconPath)
		sysStdArrow.setIcon(arrowIcon)
		
		sysStdArrow.setToolTip('System Standard Arrow Cursor') # <- does not seem to work?!
		sysStdArrow.setCheckable(True)
		sysStdArrow.triggered.connect(lambda chk: self.processCursorChoice(chk, -1))
		selectionGroup.addAction(sysStdArrow)
		selectionMenu.addAction(sysStdArrow)
		
		# Generate an entry for the system standard CrossCursor:
		sysStdCross = QAction('Standard Cross', self.parentInterface.mainWindow())
		
		crossIconPath = os.path.join(os.path.dirname(__file__), 'graphics', 'SysStdCrossIcon03.png')
		crossIcon = QIcon(crossIconPath)
		sysStdCross.setIcon(crossIcon)
		
		sysStdCross.setToolTip('System Standard Crosshair Cursor')
		sysStdCross.setCheckable(True)
		sysStdCross.triggered.connect(lambda chk: self.processCursorChoice(chk, -2))
		selectionGroup.addAction(sysStdCross)
		selectionMenu.addAction(sysStdCross)
		
		i = 0
		actionList = []
		# we walk through the stored settings pointerFileName0, pointerFileName1, ...:
		while self.s.value("PreciCursorPlugin/pointerFileName" + str(i), None) != None:
			actionList.append(QAction("Pointer " + str(i), self.parentInterface.mainWindow()))
			actionList[i].setToolTip(f'Pointer {i}: ' + self.s.value("PreciCursorPlugin/pointerFileName" + str(i), 'X'))
			actionList[i].setCheckable(True)
			iconPath = (self.s.value("PreciCursorPlugin/pointerFileName" + str(i)))
			myIcon = QIcon(iconPath)
			actionList[i].setIcon(myIcon)
			
			actionList[i].triggered.connect(lambda chk, choice=i: self.processCursorChoice(chk, choice))
			
			selectionGroup.addAction(actionList[i])
			selectionMenu.addAction(actionList[i])

			i += 1
		#i = 1000 # <- diagnostic: should never become relevant,
		# but sometimes does => helps to detect python's quaint handling of i
		
		# make the previously chosen cursor option checked:
		if self.choice == -1:
			sysStdArrow.setChecked(True)
		elif self.choice == -2:
			sysStdCross.setChecked(True)
		else:
			actionList[int(self.choice)].setChecked(True)
		return selectionMenu
	
	
	def processCursorChoice(self, chk, choice):
		if chk == True:
			self.choice = int(choice)
			self.switchOn.setChecked(False)
			self.switchOn.setChecked(True)
			#self.run(True) # if you go without the "setChecked(False)" above,
			# you need to run self.run to get the cursor switched when the button is already activated
	
	
	def run(self, signal):
		if signal == True:
			if self.choice == -1:
				myMouseCursor = Qt.ArrowCursor
			elif self.choice == -2:
				myMouseCursor = Qt.CrossCursor
			else:
				myCursorPixMap = QPixmap(self.s.value("PreciCursorPlugin/pointerFileName" + self.choice.__str__()))
				xKey = "PreciCursorPlugin/hotspotX" + self.choice.__str__()
				yKey = "PreciCursorPlugin/hotspotY" + self.choice.__str__()
				myMouseCursor = QCursor(myCursorPixMap, int(self.s.value(xKey, 0)), int(self.s.value(yKey, 0)))
			# now we do what we've come for:
			QGuiApplication.instance().restoreOverrideCursor()
			QGuiApplication.instance().setOverrideCursor(myMouseCursor)
		elif signal == False:
			QGuiApplication.instance().restoreOverrideCursor()
	
	
	def unload(self):
		QGuiApplication.instance().restoreOverrideCursor()
		# save our choice of pointer:
		self.s.setValue("PreciCursorPlugin/pointerChoice", self.choice)

		self.ourToolBar.removeAction(self.buttonHandle)
		del self.switchOn