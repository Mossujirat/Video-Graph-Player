# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainForm8.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(959, 834)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.MainArea = QtWidgets.QGroupBox(self.centralwidget)
        self.MainArea.setEnabled(True)
        self.MainArea.setTitle("")
        self.MainArea.setAlignment(QtCore.Qt.AlignCenter)
        self.MainArea.setCheckable(False)
        self.MainArea.setObjectName("MainArea")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.MainArea)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        self.mainarea1 = QtWidgets.QFrame(self.MainArea)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainarea1.sizePolicy().hasHeightForWidth())
        self.mainarea1.setSizePolicy(sizePolicy)
        self.mainarea1.setFrameShape(QtWidgets.QFrame.Box)
        self.mainarea1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.mainarea1.setObjectName("mainarea1")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.mainarea1)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.openButton = QtWidgets.QPushButton(self.mainarea1)
        self.openButton.setEnabled(True)
        self.openButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.openButton.setObjectName("openButton")
        self.horizontalLayout_5.addWidget(self.openButton)
        self.fileButton = QtWidgets.QPushButton(self.mainarea1)
        self.fileButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.fileButton.setObjectName("fileButton")
        self.horizontalLayout_5.addWidget(self.fileButton)
        self.slapButton = QtWidgets.QPushButton(self.mainarea1)
        self.slapButton.setEnabled(False)
        self.slapButton.setObjectName("slapButton")
        self.horizontalLayout_5.addWidget(self.slapButton)
        self.slapButton2 = QtWidgets.QPushButton(self.mainarea1)
        self.slapButton2.setEnabled(False)
        self.slapButton2.setObjectName("slapButton2")
        self.horizontalLayout_5.addWidget(self.slapButton2)
        self.startActionButton = QtWidgets.QPushButton(self.mainarea1)
        self.startActionButton.setEnabled(False)
        self.startActionButton.setObjectName("startActionButton")
        self.horizontalLayout_5.addWidget(self.startActionButton)
        self.stopActionButton = QtWidgets.QPushButton(self.mainarea1)
        self.stopActionButton.setEnabled(False)
        self.stopActionButton.setObjectName("stopActionButton")
        self.horizontalLayout_5.addWidget(self.stopActionButton)
        self.saveButton = QtWidgets.QPushButton(self.mainarea1)
        self.saveButton.setEnabled(False)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout_5.addWidget(self.saveButton)
        self.verticalLayout.addWidget(self.mainarea1)
        self.mainarea2 = QtWidgets.QFrame(self.MainArea)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainarea2.sizePolicy().hasHeightForWidth())
        self.mainarea2.setSizePolicy(sizePolicy)
        self.mainarea2.setFrameShape(QtWidgets.QFrame.Box)
        self.mainarea2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.mainarea2.setObjectName("mainarea2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.mainarea2)
        self.horizontalLayout_6.setContentsMargins(6, 6, 6, 6)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.backwardButton = QtWidgets.QPushButton(self.mainarea2)
        self.backwardButton.setEnabled(False)
        self.backwardButton.setObjectName("backwardButton")
        self.horizontalLayout_6.addWidget(self.backwardButton)
        self.startButton = QtWidgets.QPushButton(self.mainarea2)
        self.startButton.setEnabled(False)
        self.startButton.setObjectName("startButton")
        self.horizontalLayout_6.addWidget(self.startButton)
        self.pauseButton = QtWidgets.QPushButton(self.mainarea2)
        self.pauseButton.setEnabled(False)
        self.pauseButton.setObjectName("pauseButton")
        self.horizontalLayout_6.addWidget(self.pauseButton)
        self.matchingButton = QtWidgets.QPushButton(self.mainarea2)
        self.matchingButton.setEnabled(False)
        self.matchingButton.setObjectName("matchingButton")
        self.horizontalLayout_6.addWidget(self.matchingButton)
        self.forwardButton = QtWidgets.QPushButton(self.mainarea2)
        self.forwardButton.setEnabled(False)
        self.forwardButton.setObjectName("forwardButton")
        self.horizontalLayout_6.addWidget(self.forwardButton)
        self.verticalLayout.addWidget(self.mainarea2)
        self.line_2 = QtWidgets.QFrame(self.MainArea)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.mainarea3 = QtWidgets.QWidget(self.MainArea)
        self.mainarea3.setObjectName("mainarea3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.mainarea3)
        self.horizontalLayout_2.setContentsMargins(6, 6, 6, 6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.videoArea = QtWidgets.QWidget(self.mainarea3)
        self.videoArea.setObjectName("videoArea")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.videoArea)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.VideoImage = QtWidgets.QLabel(self.videoArea)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.VideoImage.sizePolicy().hasHeightForWidth())
        self.VideoImage.setSizePolicy(sizePolicy)
        self.VideoImage.setText("")
        self.VideoImage.setObjectName("VideoImage")
        self.verticalLayout_3.addWidget(self.VideoImage)
        self.line_3 = QtWidgets.QFrame(self.videoArea)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_3.addWidget(self.line_3)
        self.horizontalSlider_video = QtWidgets.QSlider(self.videoArea)
        self.horizontalSlider_video.setEnabled(False)
        self.horizontalSlider_video.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_video.setObjectName("horizontalSlider_video")
        self.verticalLayout_3.addWidget(self.horizontalSlider_video)
        self.video_menu = QtWidgets.QFrame(self.videoArea)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.video_menu.sizePolicy().hasHeightForWidth())
        self.video_menu.setSizePolicy(sizePolicy)
        self.video_menu.setObjectName("video_menu")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.video_menu)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.backwardButton_video = QtWidgets.QPushButton(self.video_menu)
        self.backwardButton_video.setEnabled(False)
        self.backwardButton_video.setObjectName("backwardButton_video")
        self.horizontalLayout_4.addWidget(self.backwardButton_video)
        self.comboBox_video = QtWidgets.QComboBox(self.video_menu)
        self.comboBox_video.setEnabled(False)
        self.comboBox_video.setObjectName("comboBox_video")
        self.comboBox_video.addItem("")
        self.comboBox_video.addItem("")
        self.comboBox_video.addItem("")
        self.horizontalLayout_4.addWidget(self.comboBox_video)
        self.forwardButton_video = QtWidgets.QPushButton(self.video_menu)
        self.forwardButton_video.setEnabled(False)
        self.forwardButton_video.setObjectName("forwardButton_video")
        self.horizontalLayout_4.addWidget(self.forwardButton_video)
        self.verticalLayout_3.addWidget(self.video_menu)
        self.horizontalLayout_2.addWidget(self.videoArea)
        self.line = QtWidgets.QFrame(self.mainarea3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setLineWidth(2)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setObjectName("line")
        self.horizontalLayout_2.addWidget(self.line)
        self.graphArea = QtWidgets.QWidget(self.mainarea3)
        self.graphArea.setObjectName("graphArea")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.graphArea)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.GraphImage = QtWidgets.QLabel(self.graphArea)
        self.GraphImage.setText("")
        self.GraphImage.setObjectName("GraphImage")
        self.verticalLayout_2.addWidget(self.GraphImage)
        self.line_4 = QtWidgets.QFrame(self.graphArea)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout_2.addWidget(self.line_4)
        self.horizontalSlider_graph = QtWidgets.QSlider(self.graphArea)
        self.horizontalSlider_graph.setEnabled(False)
        self.horizontalSlider_graph.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_graph.setObjectName("horizontalSlider_graph")
        self.verticalLayout_2.addWidget(self.horizontalSlider_graph)
        self.menu_graph = QtWidgets.QFrame(self.graphArea)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menu_graph.sizePolicy().hasHeightForWidth())
        self.menu_graph.setSizePolicy(sizePolicy)
        self.menu_graph.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.menu_graph.setLineWidth(1)
        self.menu_graph.setObjectName("menu_graph")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.menu_graph)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.backwardButton_graph = QtWidgets.QPushButton(self.menu_graph)
        self.backwardButton_graph.setEnabled(False)
        self.backwardButton_graph.setObjectName("backwardButton_graph")
        self.horizontalLayout_3.addWidget(self.backwardButton_graph)
        self.comboBox_graph = QtWidgets.QComboBox(self.menu_graph)
        self.comboBox_graph.setEnabled(False)
        self.comboBox_graph.setObjectName("comboBox_graph")
        self.comboBox_graph.addItem("")
        self.comboBox_graph.addItem("")
        self.comboBox_graph.addItem("")
        self.horizontalLayout_3.addWidget(self.comboBox_graph)
        self.comboBox_peak = QtWidgets.QComboBox(self.menu_graph)
        self.comboBox_peak.setEnabled(False)
        self.comboBox_peak.setObjectName("comboBox_peak")
        self.comboBox_peak.addItem("")
        self.comboBox_peak.addItem("")
        self.comboBox_peak.addItem("")
        self.comboBox_peak.addItem("")
        self.horizontalLayout_3.addWidget(self.comboBox_peak)
        self.comboBox_type = QtWidgets.QComboBox(self.menu_graph)
        self.comboBox_type.setEnabled(False)
        self.comboBox_type.setObjectName("comboBox_type")
        self.comboBox_type.addItem("")
        self.comboBox_type.addItem("")
        self.horizontalLayout_3.addWidget(self.comboBox_type)
        self.forwardButton_graph = QtWidgets.QPushButton(self.menu_graph)
        self.forwardButton_graph.setEnabled(False)
        self.forwardButton_graph.setObjectName("forwardButton_graph")
        self.horizontalLayout_3.addWidget(self.forwardButton_graph)
        self.verticalLayout_2.addWidget(self.menu_graph)
        self.horizontalLayout_2.addWidget(self.graphArea)
        self.verticalLayout.addWidget(self.mainarea3)
        self.horizontalLayout.addWidget(self.MainArea)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Video Graph Player - Action"))
        self.openButton.setText(_translate("MainWindow", "Open Video"))
        self.fileButton.setText(_translate("MainWindow", "Open Data File"))
        self.slapButton.setText(_translate("MainWindow", "Save Slapping 1"))
        self.slapButton2.setText(_translate("MainWindow", "Save Slapping 2"))
        self.startActionButton.setText(_translate("MainWindow", "Start Action"))
        self.stopActionButton.setText(_translate("MainWindow", "Stop Action"))
        self.saveButton.setText(_translate("MainWindow", "Save File"))
        self.backwardButton.setText(_translate("MainWindow", "Backward"))
        self.startButton.setText(_translate("MainWindow", "Start"))
        self.pauseButton.setText(_translate("MainWindow", "Pause"))
        self.matchingButton.setText(_translate("MainWindow", "Matching"))
        self.forwardButton.setText(_translate("MainWindow", "Forward"))
        self.backwardButton_video.setText(_translate("MainWindow", "Backward"))
        self.comboBox_video.setItemText(0, _translate("MainWindow", "Video Source"))
        self.comboBox_video.setItemText(1, _translate("MainWindow", "sony slow motion"))
        self.comboBox_video.setItemText(2, _translate("MainWindow", "iphone slow motion"))
        self.forwardButton_video.setText(_translate("MainWindow", "Forward"))
        self.backwardButton_graph.setText(_translate("MainWindow", "Backward"))
        self.comboBox_graph.setItemText(0, _translate("MainWindow", "20 second"))
        self.comboBox_graph.setItemText(1, _translate("MainWindow", "1 second"))
        self.comboBox_graph.setItemText(2, _translate("MainWindow", "5 second"))
        self.comboBox_peak.setItemText(0, _translate("MainWindow", "Number of Peak"))
        self.comboBox_peak.setItemText(1, _translate("MainWindow", "Peak 1"))
        self.comboBox_peak.setItemText(2, _translate("MainWindow", "Peak 2"))
        self.comboBox_peak.setItemText(3, _translate("MainWindow", "Peak 3"))
        self.comboBox_type.setItemText(0, _translate("MainWindow", "Acc"))
        self.comboBox_type.setItemText(1, _translate("MainWindow", "Gyro"))
        self.forwardButton_graph.setText(_translate("MainWindow", "Forward"))

