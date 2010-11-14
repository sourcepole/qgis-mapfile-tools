# -*- coding: utf-8 -*-
"""
/***************************************************************************
MapfileRenderer
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

import mapscript

class MapfileRenderer():

  def __init__ (self, mapfile, messageTextEdit):
    self.mapfile = mapfile
    self.messageTextEdit = messageTextEdit
    self.styles = ""
    self.layers = ""
    self.srs = "EPSG:4326"
    self.mime_type = "image/png"
    self.messageTextEdit.append( "Opening " + self.mapfile )

  def setup(self, layers, srs = "EPSG:4326", mime_type = "image/png"):
    self.layers = layers
    self.srs = srs
    self.mime_type = mime_type

  # extent: QExtent
  # size = (width,height)
  def render(self, extent, size):
    mapObj = mapscript.mapObj(self.mapfile)

    mapObj.setConfigOption("MS_ERRORFILE", "stdout")
    mapObj.debug = 5

    mapObj.setExtent(extent.xMinimum(), extent.yMinimum(), extent.xMaximum(), extent.yMaximum())
    mapObj.setSize(int(size[0]), int(size[1]))

    mapscript.msIO_installStdoutToBuffer()

    mapImage = mapObj.draw() #= mapscript.imageObj(int(size[0]), int(size[1]), self.mime_type)
    data = mapImage.getBytes()

    out = mapscript.msIO_getStdoutBufferString()
    mapscript.msIO_resetHandlers()
    self.messageTextEdit.append( out )

    return data

  # bbox = "xmin,ymin,xmax,ymax"
  # size = (width,height)
  def renderWMS(self, bbox, size):
    mapObj = mapscript.mapObj(self.mapfile)

    req = mapscript.OWSRequest()
    req.setParameter("bbox", bbox)
    req.setParameter("width", str(size[0]))
    req.setParameter("height", str(size[1]))
    req.setParameter("srs", self.srs)
    req.setParameter("format", self.mime_type)
    req.setParameter("layers", self.layers)
    req.setParameter("request", "GetMap")

    mapObj.loadOWSParameters(req)

    mapImage = mapObj.draw()
    data = mapImage.getBytes()
    return data

  def getExtents(self):
    mapObj = mapscript.mapObj(self.mapfile)

    return (mapObj.extent.minx, mapObj.extent.miny, mapObj.extent.maxx, mapObj.extent.maxy)

  def getLayers(self):
    mapObj = mapscript.mapObj(self.mapfile)
    layers = []
    for i in range(0, mapObj.numlayers):
      layers.append(mapObj.getLayer(i).name)

    return layers

  def getProj(self):
    mapObj = mapscript.mapObj(self.mapfile)

    return mapObj.getProjection()

  def getMaxSize(self):
    mapObj = mapscript.mapObj(self.mapfile)

    return mapObj.maxsize