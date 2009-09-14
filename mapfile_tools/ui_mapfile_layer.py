# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_mapfile_layer.ui'
#
# Created: Fri Sep 11 15:41:02 2009
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MapfileLayer(object):
    def setupUi(self, MapfileLayer):
        MapfileLayer.setObjectName("MapfileLayer")
        MapfileLayer.resize(QtCore.QSize(QtCore.QRect(0,0,360,283).size()).expandedTo(MapfileLayer.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(MapfileLayer)
        self.vboxlayout.setObjectName("vboxlayout")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        self.label = QtGui.QLabel(MapfileLayer)
        self.label.setObjectName("label")
        self.hboxlayout.addWidget(self.label)

        self.leMapfile = QtGui.QLineEdit(MapfileLayer)
        self.leMapfile.setReadOnly(True)
        self.leMapfile.setObjectName("leMapfile")
        self.hboxlayout.addWidget(self.leMapfile)

        self.btnMapfile = QtGui.QPushButton(MapfileLayer)
        self.btnMapfile.setObjectName("btnMapfile")
        self.hboxlayout.addWidget(self.btnMapfile)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.label_2 = QtGui.QLabel(MapfileLayer)
        self.label_2.setObjectName("label_2")
        self.vboxlayout.addWidget(self.label_2)

        self.listLayers = QtGui.QListWidget(MapfileLayer)
        self.listLayers.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.listLayers.setObjectName("listLayers")
        self.vboxlayout.addWidget(self.listLayers)

        self.buttonBox = QtGui.QDialogButtonBox(MapfileLayer)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(MapfileLayer)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),MapfileLayer.accept)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),MapfileLayer.reject)
        QtCore.QMetaObject.connectSlotsByName(MapfileLayer)

    def retranslateUi(self, MapfileLayer):
        MapfileLayer.setWindowTitle(QtGui.QApplication.translate("MapfileLayer", "Add Mapfile Layer", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MapfileLayer", "Map file", None, QtGui.QApplication.UnicodeUTF8))
        self.btnMapfile.setText(QtGui.QApplication.translate("MapfileLayer", "Browse...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MapfileLayer", "Layers", None, QtGui.QApplication.UnicodeUTF8))

