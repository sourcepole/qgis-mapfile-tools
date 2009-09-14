"""
/***************************************************************************
MapfileTools
A QGIS plugin
MapServer Mapfile Tools
                             -------------------
begin                : 2009-09-09
copyright            : (C) 2009 by Sourcepole
email                : info at sourcepole dot ch
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import resources

from mapfile_layer import MapfileLayer

class MapfileTools:

  def __init__(self, iface):
    # Save reference to the QGIS interface
    self.iface = iface
    self.mapfileLayer = None

  def initGui(self):
    # Create action that will start plugin configuration
    self.actionLayer = QAction(QIcon(":/plugins/mapfile_tools/icon.png"), "Mapfile Layer", self.iface.mainWindow())
    # connect the action to the run method
    QObject.connect(self.actionLayer, SIGNAL("triggered()"), self.runLayer)

    # Add toolbar button and menu item
    self.iface.addToolBarIcon(self.actionLayer)
    self.iface.addPluginToMenu("Mapfile Tools", self.actionLayer)

  def unload(self):
    if self.mapfileLayer != None:
      self.mapfileLayer.cleanup()

    # Remove the plugin menu item and icon
    self.iface.removePluginMenu("Mapfile Tools",self.actionLayer)
    self.iface.removeToolBarIcon(self.actionLayer)

  def runLayer(self):
    if self.mapfileLayer == None:
      self.mapfileLayer = MapfileLayer(self.iface)
    self.mapfileLayer.run()
    return
