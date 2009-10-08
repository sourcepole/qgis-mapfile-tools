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
import string

from mapfile_layer_dialog import MapfileLayerDialog
from mapfile_layer import MapfileLayer

class MapfileTools:

  def __init__(self, iface):
    # Save reference to the QGIS interface
    self.iface = iface
    self.mapfileLayers = []
    self.mapfile = ""

  def initGui(self):
    # Create action that will start plugin configuration
    self.actionLayer = QAction(QIcon(":/plugins/mapfile_tools/icon.png"), "Mapfile Layer", self.iface.mainWindow())
    # connect the action to the run method
    QObject.connect(self.actionLayer, SIGNAL("triggered()"), self.addLayer)

    # Add toolbar button and menu item
    self.iface.addToolBarIcon(self.actionLayer)
    self.iface.addPluginToMenu("Mapfile Tools", self.actionLayer)

    # Mapfile layers
    QObject.connect(QgsProject.instance(), SIGNAL("readProject(QDomDocument)"), self.readProject)

  def unload(self):
    # Remove the plugin menu item and icon
    self.iface.removePluginMenu("Mapfile Tools",self.actionLayer)
    self.iface.removeToolBarIcon(self.actionLayer)

  def readProject(self, doc):
    # restore mapfile layers after loading a project
    mapLayers = QgsMapLayerRegistry.instance().mapLayers()
    for name, maplayer in mapLayers.iteritems():
      if maplayer.type() == QgsMapLayer.PluginLayer and maplayer.pluginId() == "MapfileLayer":
        mapfileLayer = MapfileLayer()
        if mapfileLayer.createFromLayer(maplayer):
          self.mapfileLayers.append(mapfileLayer)
          QObject.connect(mapfileLayer, SIGNAL("layerDeleted()"), self.removeLayer)

  def addLayer(self):
    # create and show the dialog
    dlg = MapfileLayerDialog()

    # show the dialog
    dlg.ui.leMapfile.setText(self.mapfile)
    dlg.updateInfo()
    dlg.show()

    # See if OK was pressed
    if dlg.exec_() == 1:
      self.mapfile = dlg.ui.leMapfile.text()

      # selected layers
      items = dlg.ui.listLayers.selectedItems()
      layerlist = []
      for item in items:
        layerlist.append(str(item.text()))
      layers = string.join(layerlist, ",")

      # add new mapfile layer
      mapfileLayer = MapfileLayer()
      if mapfileLayer.create(self.mapfile, layers):
        self.mapfileLayers.append(mapfileLayer)
        QObject.connect(mapfileLayer, SIGNAL("layerDeleted()"), self.removeLayer)

        # use mapfile extents for initial view if this is the only layer
        if self.iface.mapCanvas().layerCount() == 1:
          extents = mapfileLayer.maprenderer.getExtents()
          self.iface.mapCanvas().setExtent(QgsRectangle(extents[0], extents[1], extents[2], extents[3]))

        self.iface.mapCanvas().refresh()

  def removeLayer(self):
    layerToRemove = None
    for mapfileLayer in self.mapfileLayers:
      if mapfileLayer.layer == None:
        layerToRemove = mapfileLayer
        break

    if layerToRemove != None:
      self.mapfileLayers.remove(layerToRemove)
