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
import math

from mapfile_renderer import MapfileRenderer
from mapfile_layer_dialog import MapfileLayerDialog

class MapfileLayer(QgsPluginLayer):

  LAYER_TYPE="mapfile"

  def __init__(self, messageTextEdit):
    QgsPluginLayer.__init__(self, MapfileLayer.LAYER_TYPE, "Mapfile Tools plugin layer")
    self.setValid(True)

    self.messageTextEdit = messageTextEdit
    self.mapfile = ""
    self.layers = ""
    self.maprenderer = None
    self.pixmap = None

  def setupPaintArea(self, rendererContext):
    rasterScaleFactor = rendererContext.rasterScaleFactor()
    invRasterScaleFactor = 1.0/rasterScaleFactor

    # setup painter
    painter = rendererContext.painter()
    painter.scale(invRasterScaleFactor, invRasterScaleFactor)

    # get dimensions of painter area (so it is also correctly scaled in print composer)
    extent = rendererContext.extent()
    mapToPixel = rendererContext.mapToPixel()
    topleft = mapToPixel.transform(extent.xMinimum(), extent.yMaximum())
    bottomright = mapToPixel.transform(extent.xMaximum(), extent.yMinimum())

    topleft.multiply(rasterScaleFactor)
    bottomright.multiply(rasterScaleFactor)

    return QgsRectangle(topleft, bottomright)

  def drawUntiled(self, painter, extent, viewport):
    img = self.maprenderer.render(extent, (viewport.width(), viewport.height()))
    #bbox = "%f,%f,%f,%f" % (extent.xMinimum(), extent.yMinimum(), extent.xMaximum(), extent.yMaximum())
    #img = self.maprenderer.renderWMS(bbox, (viewport.width(), viewport.height()))
    self.pixmap.loadFromData(img)
    painter.drawPixmap(viewport.xMinimum(), viewport.yMinimum(), self.pixmap)

  def drawTiled(self, painter, extent, viewport, maxWidth, maxHeight):
    # dimensions
    mapMinX = extent.xMinimum()
    mapMaxX = extent.xMaximum()
    mapMinY = extent.yMinimum()
    mapMaxY = extent.yMaximum()
    viewportWidth = viewport.width()
    viewportHeight = viewport.height()
    pixelToMapUnitsX = (mapMaxX - mapMinX) / viewportWidth
    pixelToMapUnitsY = (mapMaxY - mapMinY) / viewportHeight

    # draw tiles
    nx = int( math.ceil(viewportWidth / maxWidth) )
    ny = int( math.ceil(viewportHeight / maxHeight) )
    for i in range(0,nx):
      for j in range(0,ny):
        # tile size
        left = i * maxWidth
        right = min((i+1) * maxWidth, viewportWidth)
        top = j * maxHeight
        bottom = min((j+1) * maxHeight, viewportHeight)
        width = right - left
        height = bottom - top

        # tile extents
        mapBottomLeft = QgsPoint(mapMinX + left * pixelToMapUnitsX, mapMaxY - bottom * pixelToMapUnitsY)
        mapTopRight = QgsPoint(mapMinX + right * pixelToMapUnitsX, mapMaxY - top * pixelToMapUnitsY)
        bbox = "%f,%f,%f,%f" % (mapBottomLeft.x(), mapBottomLeft.y(), mapTopRight.x(), mapTopRight.y())

        # render and compose image
        img = self.maprenderer.render(bbox, (width, height))
        self.pixmap.loadFromData(img)
        painter.drawPixmap(viewport.xMinimum() + left, viewport.yMinimum() + top, self.pixmap)

  def draw(self, rendererContext):
    if self.maprenderer == None:
      return True

    painter = rendererContext.painter()
    painter.save()

    maxSize = self.maprenderer.getMaxSize()
    extent = rendererContext.extent()
    viewport = self.setupPaintArea(rendererContext)

    maxWidth = min(viewport.width(), maxSize)
    maxHeight = min(viewport.height(), maxSize)
    if maxWidth < viewport.width() or maxHeight < viewport.height():
      # compose image from tiles with maxSize
      self.drawTiled(painter, extent, viewport, maxWidth, maxHeight)
    else:
      self.drawUntiled(painter, extent, viewport)

    painter.restore()

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
    self.messageTextEdit.append( "Loading " + mapfile )

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

  def openMapfile(self):
    mapfile = QFileDialog.getOpenFileName(None, "Mapfile", ".", "MapServer map files (*.map);;All files (*.*)","Filter list for selecting files from a dialog box")
    if mapfile != "":
      self.loadMapfile(str(mapfile), ())
      return True
    return False

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
