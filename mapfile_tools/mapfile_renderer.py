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

  def __init__ (self, mapfile = None):
    self.mapfile = mapfile
    self.styles = ""
    self.layers = ""
    self.srs = "EPSG:4326"
    self.mime_type = "image/png"

  def setup(self, layers, srs = None, mime_type = "image/png"):
    self.layers = layers
    self.srs = srs
    self.mime_type = mime_type

  # bbox = "xmin,ymin,xmax,ymax"
  # size = (width,height)
  def render(self, bbox, size):
    wms = mapscript.mapObj(self.mapfile)

    req = mapscript.OWSRequest()
    req.setParameter("bbox", bbox)
    req.setParameter("width", str(size[0]))
    req.setParameter("height", str(size[1]))
    if self.srs != None:
      req.setParameter("srs", self.srs)
    req.setParameter("format", self.mime_type)
    req.setParameter("layers", self.layers)
    req.setParameter("request", "GetMap")

    wms.loadOWSParameters(req)
    mapImage = wms.draw()
    data = mapImage.getBytes()
    return data

  def getExtents(self):
    wms = mapscript.mapObj(self.mapfile)

    return (wms.extent.minx, wms.extent.miny, wms.extent.maxx, wms.extent.maxy)

  def getLayers(self):
    wms = mapscript.mapObj(self.mapfile)
    layers = []
    for i in range(0, wms.numlayers):
      layers.append(wms.getLayer(i).name)

    return layers
