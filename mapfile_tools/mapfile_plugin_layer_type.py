# -*- coding: utf-8 -*-
"""
/***************************************************************************
MapfileTools
A QGIS plugin
MapServer Mapfile Tools
                             -------------------
begin                : 2010-02-01
copyright            : (C) 2010 by Sourcepole
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

from mapfile_layer import MapfileLayer

class MapfilePluginLayerType(QgsPluginLayerType):

  def __init__(self):
    QgsPluginLayerType.__init__(self, MapfileLayer.LAYER_TYPE)

  def createLayer(self):
    return MapfileLayer()

  def showLayerProperties(self, layer):
    layer.showProperties()

    # indicate that we have shown the properties dialog
    return True
