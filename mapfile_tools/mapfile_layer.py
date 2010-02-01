# -*- coding: utf-8 -*-
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

import string

from mapfile_renderer import MapfileRenderer
from mapfile_layer_dialog import MapfileLayerDialog

class MapfileLayer(QgsPluginLayer):

  LAYER_TYPE="mapfile"

  def __init__(self):
    QgsPluginLayer.__init__(self, MapfileLayer.LAYER_TYPE, "Mapfile Tools plugin layer")
    self.setValid(True)

    self.mapfile = ""
    self.layers = ""
    self.maprenderer = None
    self.pixmap = None

  def draw(self, rendererContext):
    if self.maprenderer == None:
      return True

    extents = rendererContext.extent()
    bbox = "%f,%f,%f,%f" % (extents.xMinimum(), extents.yMinimum(), extents.xMaximum(), extents.yMaximum())
    viewport = rendererContext.painter().viewport()

    img = self.maprenderer.render(bbox, (viewport.width(), viewport.height()))
    self.pixmap.loadFromData(img)

    painter = rendererContext.painter()
    painter.drawPixmap(0, 0, self.pixmap)

    return True

  def readXml(self, node):
    # custom properties
    mapfile = node.toElement().attribute("mapfile", "")
    layers = str(node.toElement().attribute("layers", ""))
    self.loadMapfile(mapfile, layers)
    return True

  def writeXml(self, node, doc):
    element = node.toElement();
    # write plugin layer type to project (essential to be read from project)
    element.setAttribute("type", "plugin")
    element.setAttribute("name", MapfileLayer.LAYER_TYPE);
    # custom properties
    element.setAttribute("mapfile", str(self.mapfile))
    element.setAttribute("layers", str(self.layers))
    return True

  def loadMapfile(self, mapfile, layers):
    self.mapfile = mapfile
    self.layers = layers
    if self.mapfile == "":
      return

    # open mapfile
    self.maprenderer = MapfileRenderer(str(self.mapfile))

    # get projection as EPSG
    crs = QgsCoordinateReferenceSystem()
    crs.createFromProj4(self.maprenderer.getProj())
    if not crs.isValid():
      crs.validate()

    srs = "EPSG:%d" % crs.epsg()

    # always use default format for now
    self.maprenderer.setup(self.layers, srs)

    # set projection
    self.setCrs(crs)

    # TODO: set extents
#    extents = self.maprenderer.getExtents()
#    self.setExtent(QgsRectangle(extents[0], extents[1], extents[2], extents[3]))

    if self.pixmap == None:
      self.pixmap = QPixmap()

    # trigger repaint
    self.setCacheImage(None)
    self.emit(SIGNAL("repaintRequested()"))

  def showProperties(self):
    # create and show the dialog
    dlg = MapfileLayerDialog()

    # show the dialog
    dlg.ui.leMapfile.setText(self.mapfile)
    dlg.updateInfo()
    dlg.show()

    # See if OK was pressed
    if dlg.exec_() == 1:
      mapfile = dlg.ui.leMapfile.text()

      # selected layers
      items = dlg.ui.listLayers.selectedItems()
      layerlist = []
      for item in items:
        layerlist.append(str(item.text()))
      layers = string.join(layerlist, ",")

      self.loadMapfile(mapfile, layers)
      return True

    return False
