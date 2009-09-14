"""
/***************************************************************************
MapfileLayer
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
from qgis.core import *

from mapfile_layer_dialog import MapfileLayerDialog

import string
import tempfile
import os.path
from mapfile_renderer import MapfileRenderer

class MapfileLayer:

  def __init__(self, iface):
    self.iface = iface
    self.layer = None
    self.mapfile = ""

  def run(self):
    # create and show the dialog 
    dlg = MapfileLayerDialog()

    # show the dialog
    dlg.ui.leMapfile.setText(self.mapfile)
    dlg.updateInfo()
    dlg.show()
    result = dlg.exec_()

    # See if OK was pressed
    if result == 1:
      # remove old layer
      if self.layer != None:
        if QMessageBox.question(dlg, \
          QtGui.QApplication.translate("MapserverImport", "Load Mapfile", None, QtGui.QApplication.UnicodeUTF8), \
          QtGui.QApplication.translate("MapserverImport", "The existing Mapfile layer will be replaced.\nDo you want to continue?", None, QtGui.QApplication.UnicodeUTF8), \
          QMessageBox.Ok | QMessageBox.Cancel) != QMessageBox.Ok:
            return

        QgsMapLayerRegistry.instance().removeMapLayer(self.layer.getLayerID())

      # open mapfile
      self.mapfile = dlg.ui.leMapfile.text()
      self.maprenderer = MapfileRenderer(str(self.mapfile))

      # selected layers
      items = dlg.ui.listLayers.selectedItems()
      layerlist = []
      for item in items:
        layerlist.append(str(item.text()))
      layers = string.join(layerlist, ",")

      # always use default SRS and format for now
      self.maprenderer.setup(layers)

      # setup temporary image file
      tmpfilename = tempfile.NamedTemporaryFile(prefix="qgis-").name
      self.imgPath = tmpfilename + ".png"
      self.worldfilePath = tmpfilename + ".pgw"
      self.pixmap = QPixmap()
      self.renderMapfile()

      # add new layer
      self.layer = QgsRasterLayer(self.imgPath, "Mapfile (%s)" % self.mapfile)
      if self.layer.isValid():
        QgsMapLayerRegistry.instance().addMapLayer(self.layer)

        # handle view change
        QObject.connect(self.iface.mapCanvas(), SIGNAL("extentsChanged()"), self.updateRender)
        # handle layer visibility
        QObject.connect(self.iface.mapCanvas(), SIGNAL("layersChanged()"), self.updateRender)
        # handle layer remove
        QObject.connect(QgsMapLayerRegistry.instance(), SIGNAL("layerWillBeRemoved(QString)"), self.cleanupOnRemove)

        # use mapfile extents for initial view if this is the only layer
        if self.iface.mapCanvas().layerCount() == 1:
          extents = self.maprenderer.getExtents()
          self.iface.mapCanvas().setExtent(QgsRectangle(extents[0], extents[1], extents[2], extents[3]))
          self.iface.mapCanvas().refresh()

  def updateRender(self):
    if self.layerIsVisible():
      self.renderMapfile()

  def renderMapfile(self):
    extents = self.iface.mapCanvas().extent()
    bbox = "%f,%f,%f,%f" % (extents.xMinimum(), extents.yMinimum(), extents.xMaximum(), extents.yMaximum())
    renderer = self.iface.mapCanvas().mapRenderer()

    img = self.maprenderer.render(bbox, (renderer.width(), renderer.height()))
    self.pixmap.loadFromData(img)

    # save as georeferenced temp image
    self.pixmap.save(self.imgPath)

    pixelsize = self.iface.mapCanvas().mapUnitsPerPixel()
    worldfile = open(self.worldfilePath, "w")
    worldfile.write("%s\n0.0\n0.0\n%s\n" % (pixelsize, -pixelsize))
    worldfile.write("%s\n%s\n" % (extents.xMinimum() + pixelsize/2, extents.yMaximum() - pixelsize/2))
    worldfile.close()

  def cleanupOnRemove(self, layerId):
    if layerId == self.layer.getLayerID():
      self.cleanup()

  def cleanup(self):
    if self.layer != None:
      QObject.disconnect(self.iface.mapCanvas(), SIGNAL("extentsChanged()"), self.renderMapfile)
      QObject.disconnect(self.iface.mapCanvas(), SIGNAL("layersChanged()"), self.updateRender)
      QObject.disconnect(QgsMapLayerRegistry.instance(), SIGNAL("layerWillBeRemoved(QString)"), self.cleanupOnRemove)
      # remove temp files
      os.remove(self.imgPath)
      os.remove(self.worldfilePath)
      self.layer = None

  def layerIsVisible(self):
    for i in range(0, self.iface.mapCanvas().layerCount()):
      layer = self.iface.mapCanvas().layer(i)
      if layer == self.layer:
        return True

    return False
