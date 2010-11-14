# -*- coding: utf-8 -*-

import os
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui_message_window import Ui_DockWidget

class MessageWindow(QDockWidget, Ui_DockWidget):
    def __init__(self, parent=None):
        QDockWidget.__init__(self, parent.iface.mainWindow())
        # Set up the user interface from Designer. 
        self.parent = parent
        self.setupUi(self)
    
    def closeEvent(self, event):
        self.parent.dock_window = None