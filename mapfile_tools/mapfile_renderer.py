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

  def getMapObj(self):
    mapObj = None
    try:
      mapObj = mapscript.mapObj(self.mapfile)
    except mapscript.MapServerError as err:
      self.messageTextEdit.append( str(err) )
    return mapObj

  # extent: QExtent
  # size = (width,height)
  def render(self, extent, size):
    mapObj = self.getMapObj()

    mapObj.setConfigOption("MS_ERRORFILE", "stdout")
    mapObj.debug = 5

    mapObj.setExtent(extent.xMinimum(), extent.yMinimum(), extent.xMaximum(), extent.yMaximum())
    mapObj.setSize(int(size[0]), int(size[1]))
    self.messageTextEdit.append( "Rendering " + extent.toString() )

    data = ''
    try:
      mapscript.msIO_installStdoutToBuffer()
      mapImage = mapObj.draw() #= mapscript.imageObj(int(size[0]), int(size[1]), self.mime_type)
      data = mapImage.getBytes()
      self.messageTextEdit.append( "Image size: " + str(len(data)) )

      out = mapscript.msIO_getStdoutBufferString()
      mapscript.msIO_resetHandlers()
      self.messageTextEdit.append( out )
    except mapscript.MapServerError as err:
      self.messageTextEdit.append( str(err) )

    return data

  def getExtents(self):
    mapObj = self.getMapObj()
    return (mapObj.extent.minx, mapObj.extent.miny, mapObj.extent.maxx, mapObj.extent.maxy)

  def getLayers(self):
    mapObj = self.getMapObj()
    layers = []
    for i in range(0, mapObj.numlayers):
      layers.append(mapObj.getLayer(i).name)

    return layers

  def getProj(self):
    return self.getMapObj().getProjection()

  def getMaxSize(self):
    return self.getMapObj().maxsize
