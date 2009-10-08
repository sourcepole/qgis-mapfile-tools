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

from mapfile_renderer import MapfileRenderer

class MapfileLayer(QObject):
  def __init__(self):
    QObject.__init__(self)
    self.mapfile = ""
    self.layers = ""
    self.maprenderer = None

  def create(self, mapfile, layers):
    self.mapfile = mapfile
    self.layers = layers

    # add new layer
    self.layer = QgsPluginLayer("MapfileLayer", "Mapfile (%s)" % self.mapfile, self.mapfile)
    if self.layer.isValid():
      QgsMapLayerRegistry.instance().addMapLayer(self.layer)

    return self.setup()

  def createFromLayer(self, maplayer):
    self.mapfile = maplayer.source()
    self.layers = ""

    # get layers
    properties = maplayer.pluginProperties()
    layersNode = properties.namedItem("layers")
    if not layersNode.isNull():
      self.layers = str(layersNode.toElement().text())

    # use existing layer
    self.layer = maplayer

    return self.setup()

  def setup(self):
    if self.mapfile == "":
      return False

    # open mapfile
    self.maprenderer = MapfileRenderer(str(self.mapfile))

    # get projection as EPSG
    self.crs = QgsCoordinateReferenceSystem()
    self.crs.createFromProj4(self.maprenderer.getProj())
    if not self.crs.isValid():
      self.crs.validate()

    srs = "EPSG:%d" % self.crs.epsg()

    # always use default format for now
    self.maprenderer.setup(self.layers, srs)

    if self.layer.isValid():
      # set projection
      self.layer.setCrs(self.crs)

      # set extents
      extents = self.maprenderer.getExtents()
      self.layer.setExtent(QgsRectangle(extents[0], extents[1], extents[2], extents[3]))

      self.pixmap = QPixmap()

      # layer remove
      QObject.connect(self.layer, SIGNAL("layerDeleted()"), self.layerDeleted)
      # layer draw
      QObject.connect(self.layer, SIGNAL("drawLayer(QgsRenderContext&)"), self.drawLayer)
      # layer save
      QObject.connect(self.layer, SIGNAL("writePluginProperties(QDomNode&, QDomDocument&)"), self.writePluginProperties)

      return True

    return False

  def layerDeleted(self):
    self.layer = None
    self.emit(SIGNAL("layerDeleted()"))

  def drawLayer(self, rendererContext):
    extents = rendererContext.extent()
    bbox = "%f,%f,%f,%f" % (extents.xMinimum(), extents.yMinimum(), extents.xMaximum(), extents.yMaximum())
    viewport = rendererContext.painter().viewport()

    img = self.maprenderer.render(bbox, (viewport.width(), viewport.height()))
    self.pixmap.loadFromData(img)

    painter = rendererContext.painter()
    painter.drawPixmap(0, 0, self.pixmap)

  def writePluginProperties(self, node, doc):
    layers = doc.createElement("layers")
    layersText = doc.createTextNode(self.layers)
    layers.appendChild(layersText)
    node.appendChild(layers);
