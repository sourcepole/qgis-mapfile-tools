# -*- coding: utf-8 -*-
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
 This script initializes the plugin, making it known to QGIS.
"""

def name(): 
  return "Mapfile Tools" 
def description():
  return "Load UMN Mapserver Mapfile as Layer"
def version(): 
  return "0.9"
def qgisMinimumVersion():
  return "1.5"
def authorName():
  return "Sourcepole"
def homepage():
  return "http://github.com/sourcepole/qgis-mapfile-tools"
def classFactory(iface):
  from mapfile_tools import MapfileTools
  return MapfileTools(iface)
