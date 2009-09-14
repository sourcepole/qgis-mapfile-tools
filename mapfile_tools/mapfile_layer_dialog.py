"""
/***************************************************************************
MapserverLayerDialog
A QGIS plugin
add MapServer Mapfile layer
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

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui_mapfile_layer import Ui_MapfileLayer

from mapfile_renderer import MapfileRenderer

# create the dialog for zoom to point
class MapfileLayerDialog(QtGui.QDialog):
  def __init__(self): 
    QtGui.QDialog.__init__(self) 
    # Set up the user interface from Designer. 
    self.ui = Ui_MapfileLayer()
    self.ui.setupUi(self) 

    QObject.connect(self.ui.btnMapfile, SIGNAL("clicked()"), self.setMapfile)

  def setMapfile(self):
    mapfile = QFileDialog.getOpenFileName(self, "Mapfile", ".", "MapServer map files (*.map);;All files (*.*)","Filter list for selecting files from a dialog box")
    self.ui.leMapfile.setText(mapfile)
    self.updateInfo()

  def updateInfo(self):
    mapfile = self.ui.leMapfile.text()
    if mapfile != "":
      maprenderer = MapfileRenderer(str(mapfile))
      layers = maprenderer.getLayers()
      self.ui.listLayers.clear()
      for layer in layers:
        item = QtGui.QListWidgetItem(self.ui.listLayers)
        item.setText(layer)
      self.ui.listLayers.selectAll()
