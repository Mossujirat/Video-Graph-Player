import os, sys
from configobj import ConfigObj
from time import sleep
import cv2
from threading import Timer,Thread,Event
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication,QMainWindow,QFileDialog,QVBoxLayout
from PyQt5 import QtGui, QtCore ,QtWidgets

from MainForm import Ui_MainWindow
import numpy as np
import pandas as pd
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import datetime

############## Video Updating ##############
class workerThread(QThread):
        
    def __init__(self,mw):
        self.mw=mw
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        while self.mw.isRunVideo:          
            if self.mw.isthreadActiveVideo and self.mw.isUpdateVideo and not self.mw.autoData:
                self.mw.cap.set(cv2.CAP_PROP_POS_FRAMES,self.mw.frameVideo)           
                ret, frame = self.mw.cap.read()
                self.mw.limg = frame            
                self.mw.on_zoomfit_clicked()
                nchannel = frame.shape[2]
                limg2 = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)                  
                timg=cv2.resize(limg2,(int(self.mw.scaleFactor*limg2.shape[1]),int(self.mw.scaleFactor*limg2.shape[0]))) 
                limage = QtGui.QImage(timg.data, timg.shape[1], timg.shape[0], nchannel*timg.shape[1], QtGui.QImage.Format_RGB888)  
                self.mw.ui.VideoImage.setPixmap(QtGui.QPixmap(limage))
                # calculate time
                self.mw.calculationTime()
                # reset parameter
                self.mw.isUpdateVideo = False 
                self.mw.ui.backwardButton_video.setEnabled(True)
                self.mw.ui.forwardButton_video.setEnabled(True)
                QApplication.processEvents()

############## Graph Updating ##############
class workerThread2(QThread):
    #updatedLine = QtCore.pyqtSignal(int)
    def __init__(self,mw):
        self.mw = mw
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):        
        while self.mw.isRunGraph:  
            if self.mw.isthreadActiveGraph and self.mw.isUpdateGraph and not self.mw.autoData:
                # Update frame of graph and Xlim
                self.mw.setGraphX()
                self.mw.ax1.lines.remove(self.mw.ax1.lines[4])
                self.mw.ax1.plot([self.mw.data[self.mw.frameGraphUpdate-1,5],self.mw.data[self.mw.frameGraphUpdate-1,5]],[-10,10],'Gray',linewidth=2.0) 
                self.mw.ui.GraphImage.canvas.draw()
                # reset parameter
                self.mw.isUpdateGraph = False
                self.mw.ui.backwardButton_graph.setEnabled(True)
                self.mw.ui.forwardButton_graph.setEnabled(True)
                # calculate time
                self.mw.calculationTime()
                QApplication.processEvents()

############## Auto graph and video ##############
class workerThread3(QThread):
    def __init__(self,mw):
        self.mw = mw
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):  
        while self.mw.isRunGraph and self.mw.isRunVideo:
            if self.mw.isthreadActiveGraph and self.mw.isthreadActiveVideo and self.mw.autoData:
                if self.mw.frameVideo < self.mw.endframe - self.mw.videoUpdate and self.mw.frameGraphUpdate < self.mw.maxGraphX - self.mw.graphUpdate:
                    # Video
                    self.mw.frameVideo+=self.mw.videoUpdate
                    self.mw.cap.set(cv2.CAP_PROP_POS_FRAMES,self.mw.frameVideo)           
                    ret, frame = self.mw.cap.read()
                    self.mw.limg = frame            
                    self.mw.on_zoomfit_clicked()
                    nchannel = frame.shape[2]
                    limg2 = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)                  
                    timg=cv2.resize(limg2,(int(self.mw.scaleFactor*limg2.shape[1]),int(self.mw.scaleFactor*limg2.shape[0]))) 
                    limage = QtGui.QImage(timg.data, timg.shape[1], timg.shape[0], nchannel*timg.shape[1], QtGui.QImage.Format_RGB888)  
                    self.mw.ui.VideoImage.setPixmap(QtGui.QPixmap(limage))
                    self.mw.ui.horizontalSlider_video.setValue(self.mw.frameVideo)
                    # Graph and Update Xlim
                    self.mw.frameGraphUpdate+=self.mw.graphUpdate
                    self.mw.setGraphX()
                    self.mw.ax1.lines.remove(self.mw.ax1.lines[4])
                    self.mw.ax1.plot([self.mw.data[self.mw.frameGraphUpdate,5],self.mw.data[self.mw.frameGraphUpdate,-1]],[-10,10],'Gray',linewidth=2.0) 
                    self.mw.ui.horizontalSlider_graph.setValue(self.mw.frameGraphUpdate)
                    self.mw.ui.GraphImage.canvas.draw() 
                    # Calculation
                    self.mw.calculationTime()
                    QApplication.processEvents()  
                else:
                    if self.mw.matching == 0:
                        # Video
                        self.mw.ui.forwardButton_video.setEnabled(True)
                        self.mw.ui.backwardButton_video.setEnabled(True)
                        self.mw.ui.horizontalSlider_video.setEnabled(True)
                        # Graph
                        self.mw.ui.forwardButton_graph.setEnabled(True)
                        self.mw.ui.backwardButton_graph.setEnabled(True)
                        self.mw.ui.horizontalSlider_graph.setEnabled(True) 
                        # Upper menu
                        self.mw.ui.fileButton.setEnabled(True)
                        self.mw.ui.openButton.setEnabled(True)
                        self.mw.ui.startButton.setEnabled(True)
                        self.mw.ui.pauseButton.setEnabled(True)
                        self.mw.ui.forwardButton.setEnabled(True)
                        self.mw.ui.backwardButton.setEnabled(True)
                        self.mw.ui.fallButton.setEnabled(True)
                        self.mw.ui.slapButton.setEnabled(True)
                        self.mw.ui.autoButton.setEnabled(True)
                        self.mw.ui.matchingButton.setEnabled(True)
                        self.mw.autoData = False
                    elif self.mw.matching == 1:
                        # Video
                        self.mw.ui.forwardButton_video.setEnabled(False)
                        self.mw.ui.backwardButton_video.setEnabled(False)
                        self.mw.ui.horizontalSlider_video.setEnabled(True)
                        # Graph
                        self.mw.ui.forwardButton_graph.setEnabled(False)
                        self.mw.ui.backwardButton_graph.setEnabled(False)
                        self.mw.ui.horizontalSlider_graph.setEnabled(False) 
                        # Upper menu
                        self.mw.ui.fileButton.setEnabled(False)
                        self.mw.ui.openButton.setEnabled(False)
                        self.mw.ui.startButton.setEnabled(True)
                        self.mw.ui.pauseButton.setEnabled(True)
                        self.mw.ui.forwardButton.setEnabled(True)
                        self.mw.ui.backwardButton.setEnabled(True)
                        self.mw.ui.fallButton.setEnabled(True)
                        self.mw.ui.slapButton.setEnabled(True)
                        self.mw.ui.autoButton.setEnabled(True)
                        self.mw.ui.matchingButton.setEnabled(True)
                        self.mw.autoData = False
                    QApplication.processEvents()

############## Graph and Video Updating ##############
class workerThread4(QThread):
    def __init__(self,mw):
        self.mw = mw
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):        
        while self.mw.isRunGraph and self.mw.isRunVideo:  
            if self.mw.isthreadActiveGraph and self.mw.isthreadActiveVideo and self.mw.isUpdateGV and not self.mw.autoData:
                # Update frame of graph and Xlim
                self.mw.setGraphX()
                self.mw.ax1.lines.remove(self.mw.ax1.lines[4])
                self.mw.ax1.plot([self.mw.data[self.mw.frameGraphUpdate-1,5],self.mw.data[self.mw.frameGraphUpdate-1,5]],[-10,10],'Gray',linewidth=2.0) 
                self.mw.ui.GraphImage.canvas.draw()
                # Update frame of video
                self.mw.cap.set(cv2.CAP_PROP_POS_FRAMES,self.mw.frameVideo)           
                ret, frame = self.mw.cap.read()
                self.mw.limg = frame            
                self.mw.on_zoomfit_clicked()
                nchannel = frame.shape[2]
                limg2 = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)                  
                timg=cv2.resize(limg2,(int(self.mw.scaleFactor*limg2.shape[1]),int(self.mw.scaleFactor*limg2.shape[0]))) 
                limage = QtGui.QImage(timg.data, timg.shape[1], timg.shape[0], nchannel*timg.shape[1], QtGui.QImage.Format_RGB888)  
                self.mw.ui.VideoImage.setPixmap(QtGui.QPixmap(limage))
                # Calculate time
                self.mw.calculationTime()
                # reset parameter
                self.mw.isUpdateGV = False
                self.mw.ui.backwardButton.setEnabled(True)
                self.mw.ui.forwardButton.setEnabled(True)
                QApplication.processEvents()

# Main application (Function)
class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # set icon
        self.setWindowIcon(QtGui.QIcon('asset/Logo.ico')) 
        self.ui.slapButton.setIcon(QtGui.QIcon('asset/slapButton.png'))
        self.ui.fallButton.setIcon(QtGui.QIcon('asset/fallButton.png'))
        self.ui.pauseButton.setIcon(QtGui.QIcon('asset/pauseButton.png'))
        self.ui.startButton.setIcon(QtGui.QIcon('asset/startButton.png'))
        self.ui.forwardButton.setIcon(QtGui.QIcon('asset/forwardButton.png'))
        self.ui.backwardButton.setIcon(QtGui.QIcon('asset/backwardButton.png'))
        self.ui.forwardButton_graph.setIcon(QtGui.QIcon('asset/forwardButton.png'))
        self.ui.backwardButton_graph.setIcon(QtGui.QIcon('asset/backwardButton.png'))
        self.ui.forwardButton_video.setIcon(QtGui.QIcon('asset/forwardButton.png'))
        self.ui.backwardButton_video.setIcon(QtGui.QIcon('asset/backwardButton.png'))
        self.ui.matchingButton.setIcon(QtGui.QIcon('asset/matchingButton.png'))
        self.ui.autoButton.setIcon(QtGui.QIcon('asset/autoButton.png'))
        self.ui.fileButton.setIcon(QtGui.QIcon('asset/fileButton.png'))
        self.ui.openButton.setIcon(QtGui.QIcon('asset/openButton.png'))

        # set save config file (slap button and fall button)
        self.ui.slapButton.clicked.connect(self.slapButtonPressed)
        self.ui.fallButton.clicked.connect(self.fallButtonPressed)

        # set graph and video button (Connection)
        self.ui.pauseButton.clicked.connect(self.pauseButtonPressed)
        self.ui.startButton.clicked.connect(self.startButtonPressed)
        self.ui.autoButton.clicked.connect(self.autoButtonPressed)
        self.ui.forwardButton.clicked.connect(self.forwardButtonPressed)
        self.ui.backwardButton.clicked.connect(self.backwardButtonPressed)
        self.ui.matchingButton.clicked.connect(self.matchingButtonPressed)
        self.ui.statusbar.showMessage("Select File Video and Data")

        # set graph button (Connection)
        self.ui.fileButton.clicked.connect(self.fileButtonPressed)      
        self.ui.horizontalSlider_graph.sliderPressed.connect(self.horizontalSliderGraphPressed)
        self.ui.horizontalSlider_graph.sliderReleased.connect(self.horizontalSliderGraphReleased)
        self.ui.backwardButton_graph.clicked.connect(self.backwardButtonGraphPressed)
        self.ui.forwardButton_graph.clicked.connect(self.forwardButtonGraphPressed)
        self.ui.comboBox_graph.currentIndexChanged.connect(self.selectGraphChange)

        # set graph
        layout = QVBoxLayout()
        self.figure = Figure()
        self.ui.GraphImage.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.ui.GraphImage.canvas)
        self.ui.GraphImage.setLayout(layout)
        self.ax1 = self.figure.add_subplot(1,1,1)
        self.ax1.get_yaxis().set_visible(False)
        self.ax1.get_xaxis().set_visible(True)
        self.figure.subplots_adjust(left=0.001, right=0.999, top=1.0, bottom=0.1)

        # parameter graph and pointing graph
        self.isRunGraph = True # for loop
        self.isthreadActiveGraph = False # for active graph
        self.isUpdateGraph = False # for updating graph
        self.wthread2 = workerThread2(self)           
        self.wthread2.start() 
        self.frameGraphUpdate = 0
        self.maxGraphX = 40000
        self.timeGraph = 0
        self.graphUpdate = 40

        # set video
        self.ui.openButton.clicked.connect(self.openButtonPressed)
        self.ui.forwardButton_video.clicked.connect(self.forwardButtonVideoPressed)
        self.ui.backwardButton_video.clicked.connect(self.backwardButtonVideoPressed)
        self.ui.horizontalSlider_video.sliderPressed.connect(self.horizontalSliderVideoPressed)
        self.ui.horizontalSlider_video.sliderReleased.connect(self.horizontalSliderVideoReleased)
        self.ui.comboBox_video.currentIndexChanged.connect(self.selectVideoChange)

        # parameter video and pointing video
        self.isRunVideo = True # for loop
        self.resizegoing = False 
        self.isthreadActiveVideo = False # for active video
        self.isUpdateVideo = False # for updating graph
        self.wthread = workerThread(self)           
        self.wthread.start() 
        self.frameVideo = 0
        self.timeVideo = 0
        self.endframe = 1
        self.videoUpdate = 20

        # Graph and Video Connection
        self.isUpdateGV = False
        self.wthread4 = workerThread4(self)           
        self.wthread4.start() 
        self.autoData = False
        self.wthread3 = workerThread3(self)           
        self.wthread3.start() 
        self.matching = 0
    
    ######################### Calculate time ########################
    def calculationTime(self):
        self.timeGraph = round((self.frameGraphUpdate*0.0005),2)
        try: self.timeVideo = round((self.frameVideo/self.fps),2)
        except: self.timeVideo = 0
        self.ui.statusbar.showMessage("Frame of Video ::" + str(self.frameVideo) + "/" + str(self.endframe-1) +
            " (Time = " + str(datetime.timedelta(seconds=self.timeVideo)) + " second) Number of Signal :: " + str(self.frameGraphUpdate) +
            "/"+ str(self.maxGraphX) + " (Time =" + str(datetime.timedelta(seconds=self.timeGraph)) + " second)")
        
    ######################### Auto run ##############################
    def pauseButtonPressed(self):
        self.autoData = False   
        # Main menu and slider
        self.ui.horizontalSlider_video.setEnabled(True) 
        self.ui.horizontalSlider_graph.setEnabled(True) 
        self.ui.startButton.setEnabled(True)
        self.ui.slapButton.setEnabled(True)
        self.ui.fallButton.setEnabled(True)
        self.ui.forwardButton.setEnabled(True)
        self.ui.backwardButton.setEnabled(True)
        self.ui.matchingButton.setEnabled(True)
        # if matching button was clicked
        if self.matching == 1:
            self.ui.autoButton.setEnabled(False)
            # For video     
            self.ui.forwardButton_video.setEnabled(False)
            self.ui.backwardButton_video.setEnabled(False)
            self.ui.openButton.setEnabled(False)
            self.ui.comboBox_video.setEnabled(False)
            # For graph
            self.ui.forwardButton_graph.setEnabled(False)
            self.ui.backwardButton_graph.setEnabled(False)
            self.ui.fileButton.setEnabled(False)
            self.ui.comboBox_graph.setEnabled(False)
        else: # if matching button was not clicked
            self.ui.autoButton.setEnabled(True)
            # For video     
            self.ui.forwardButton_video.setEnabled(True)
            self.ui.backwardButton_video.setEnabled(True)
            self.ui.openButton.setEnabled(True)
            self.ui.comboBox_video.setEnabled(True)
            # For graph
            self.ui.forwardButton_graph.setEnabled(True)
            self.ui.backwardButton_graph.setEnabled(True)
            self.ui.fileButton.setEnabled(True)
            self.ui.comboBox_graph.setEnabled(True)

    def startButtonPressed(self):
        if self.isthreadActiveVideo and self.isthreadActiveGraph:
            self.autoData = True
            # For video 
            self.ui.forwardButton_video.setEnabled(False)
            self.ui.backwardButton_video.setEnabled(False)
            self.ui.fileButton.setEnabled(False)
            self.ui.openButton.setEnabled(False)
            self.ui.horizontalSlider_video.setEnabled(False)
            self.ui.comboBox_video.setEnabled(False)
            # For graph
            self.ui.forwardButton_graph.setEnabled(False)
            self.ui.backwardButton_graph.setEnabled(False)
            self.ui.fileButton.setEnabled(False)
            self.ui.openButton.setEnabled(False)
            self.ui.horizontalSlider_graph.setEnabled(False)
            self.ui.comboBox_graph.setEnabled(False)
            # For main menu
            self.ui.autoButton.setEnabled(False)
            self.ui.fallButton.setEnabled(False)
            self.ui.slapButton.setEnabled(False)
            self.ui.startButton.setEnabled(False)
            self.ui.forwardButton.setEnabled(False)
            self.ui.backwardButton.setEnabled(False)
            self.ui.matchingButton.setEnabled(False)

    def autoButtonPressed(self):
        a = np.array((self.data[:,4]))
        if self.matching == 0:
            self.ui.horizontalSlider_graph.setValue(a.argmax())
            self.frameGraphUpdate = self.ui.horizontalSlider_graph.value()
            self.sliderbusyGraph = False
            self.isUpdateGraph = True
        elif self.matching == 1:
            a = np.array((self.data[:,4]))
            current = a - self.matchGraph
            self.frameGraphUpdate = round(self.matchGraph + (current*(self.graphUpdate/self.videoUpdate)))
            self.ui.horizontalSlider_graph.setValue(self.frameGraphUpdate)
            self.frameVideo = round(self.matchVideo + (current*(self.videoUpdate/self.graphUpdate)))
            self.isUpdateGV = True
            self.sliderbusyVideo = False

    def backwardButtonPressed(self):
        if self.frameGraphUpdate-(self.graphUpdate*3) >= 0 and self.frameVideo-(self.videoUpdate*3) > 0:
            self.frameGraphUpdate -= self.graphUpdate*3
            self.ui.horizontalSlider_graph.setValue(self.frameGraphUpdate)
            self.frameVideo -= self.videoUpdate*3
            self.ui.horizontalSlider_video.setValue(self.frameVideo)
            self.isUpdateGV = True
            self.ui.backwardButton.setEnabled(False)
            self.ui.forwardButton.setEnabled(False)
        elif self.frameGraphUpdate-(self.graphUpdate*3) >= 0 and self.frameVideo-(self.videoUpdate*3) <= 0:
            self.frameGraphUpdate -= self.graphUpdate*3
            self.ui.horizontalSlider_graph.setValue(self.frameGraphUpdate)
            self.frameVideo = self.stframe
            self.ui.horizontalSlider_video.setValue(self.frameVideo)
            self.ui.horizontalSlider_graph.setValue(self.frameGraphUpdate)
            self.isUpdateGV = True
            self.ui.backwardButton.setEnabled(False)
            self.ui.forwardButton.setEnabled(False)
        elif self.frameGraphUpdate-(self.graphUpdate*3) < 0 and self.frameVideo-(self.videoUpdate*3) > 0:
            self.frameGraphUpdate = 0
            self.ui.horizontalSlider_graph.setValue(self.frameGraphUpdate)
            self.frameVideo -= self.videoUpdate*3
            self.ui.horizontalSlider_video.setValue(self.frameVideo)
            self.isUpdateGV = True
            self.ui.backwardButton.setEnabled(False)
            self.ui.forwardButton.setEnabled(False)

    def forwardButtonPressed(self):
        if self.frameGraphUpdate+(self.graphUpdate*3) < self.maxGraphX and self.frameVideo+(self.videoUpdate*3) < self.endframe:
            self.frameGraphUpdate += self.graphUpdate*3
            self.ui.horizontalSlider_graph.setValue(self.frameGraphUpdate)
            self.frameVideo += self.videoUpdate*3
            self.ui.horizontalSlider_video.setValue(self.frameVideo)
            self.isUpdateGV = True
            self.ui.backwardButton.setEnabled(False)
            self.ui.forwardButton.setEnabled(False)
        elif self.frameGraphUpdate+(self.graphUpdate*3) < self.maxGraphX and self.frameVideo+(self.videoUpdate*3) >= self.endframe:
            self.frameGraphUpdate += self.graphUpdate*3
            self.ui.horizontalSlider_graph.setValue(self.frameGraphUpdate)
            self.frameVideo = self.stframe
            self.ui.horizontalSlider_video.setValue(self.frameVideo)
            self.ui.horizontalSlider_graph.setValue(self.frameGraphUpdate)
            self.isUpdateGV = True
            self.ui.backwardButton.setEnabled(False)
            self.ui.forwardButton.setEnabled(False)
        elif self.frameGraphUpdate+(self.graphUpdate*3) >= self.maxGraphX and self.frameVideo+(self.videoUpdate*3) < self.endframe:
            self.frameGraphUpdate = 0
            self.ui.horizontalSlider_graph.setValue(self.frameGraphUpdate)
            self.frameVideo += self.videoUpdate*3
            self.ui.horizontalSlider_video.setValue(self.frameVideo)
            self.isUpdateGV = True
            self.ui.backwardButton.setEnabled(False)
            self.ui.forwardButton.setEnabled(False)

    def matchingButtonPressed(self):
        if self.matching == 0:
            self.matching = 1
            self.ui.matchingButton.setStyleSheet("background-color: #7EA6BF")
            self.ui.horizontalSlider_graph.setEnabled(False)
            self.ui.forwardButton_graph.setEnabled(False)
            self.ui.backwardButton_graph.setEnabled(False)
            self.ui.forwardButton_video.setEnabled(False)
            self.ui.backwardButton_video.setEnabled(False)
            self.ui.openButton.setEnabled(False)
            self.ui.fileButton.setEnabled(False)
            self.ui.autoButton.setEnabled(False)
            self.ui.comboBox_graph.setEnabled(False)
            self.ui.comboBox_video.setEnabled(False)
            self.matchVideo = self.ui.horizontalSlider_video.value()
            self.matchGraph = self.ui.horizontalSlider_graph.value()
        elif self.matching == 1:
            self.matching = 0
            self.ui.matchingButton.setStyleSheet("background-color: light gray")
            self.ui.horizontalSlider_graph.setEnabled(True)
            self.ui.forwardButton_graph.setEnabled(True)
            self.ui.backwardButton_graph.setEnabled(True)
            self.ui.forwardButton_video.setEnabled(True)
            self.ui.backwardButton_video.setEnabled(True)
            self.ui.openButton.setEnabled(True)
            self.ui.fileButton.setEnabled(True)
            self.ui.autoButton.setEnabled(True)
            self.ui.forwardButton.setEnabled(True)
            self.ui.backwardButton.setEnabled(True)
            self.ui.comboBox_graph.setEnabled(True)
            self.ui.comboBox_video.setEnabled(True)

    ######################### Save config ##############################
    def fallButtonPressed(self):
        # set name for saving file
        wordV = self.fileVideo.split('/')
        NewwordV = wordV[len(wordV)-1].split('.')
        fileNameV = NewwordV[0]
        wordG = self.fileGraph.split('/')
        NewwordG = wordG[len(wordG)-1].split('.')
        fileNameG = NewwordG[0]
        # set directory
        directory = "Database"
        if not os.path.exists(directory):
            os.makedirs(directory)
        # set file name
        filename = directory+"/"+str(fileNameV)+"("+str(fileNameG)+")"+".config"
        # Save 
        config = ConfigObj(filename, encoding='utf8')
        config.filename = filename
        config["Fall-Graph"] = str(datetime.timedelta(seconds=self.timeGraph))
        config["Fall-Video"] = str(datetime.timedelta(seconds=self.timeVideo))
        config.write()
        self.ui.statusbar.showMessage("Save successfully - Fall-Graph = " +str(datetime.timedelta(seconds=self.timeGraph))+ 
            " second, Fall-Video = " +str(datetime.timedelta(seconds=self.timeVideo))+ " second") 

    def slapButtonPressed(self):
        # set name for saving file
        wordV = self.fileVideo.split('/')
        NewwordV = wordV[len(wordV)-1].split('.')
        fileNameV = NewwordV[0]
        wordG = self.fileGraph.split('/')
        NewwordG = wordG[len(wordG)-1].split('.')
        fileNameG = NewwordG[0]
        # set directory
        directory = "Database"
        if not os.path.exists(directory):
            os.makedirs(directory)
        # set file name
        filename = directory+"/"+str(fileNameV)+"("+str(fileNameG)+")"+".config"
        # Save 
        config = ConfigObj(filename, encoding='utf8')
        config.filename = filename
        config["Slap-Graph"] = round((self.frameGraphUpdate)*0.0005,3)
        config["Slap-Video"] = round((self.frameVideo)/self.fps,3)
        config.write()
        self.ui.statusbar.showMessage("Save successfully - Slap-Graph = " +str(round((self.frameGraphUpdate)*0.0005,3))+ " second, Slap-Video = " +str(round((self.frameVideo)/self.fps,3))+ " second") 

    ######################### Graph ##############################
    def backwardButtonGraphPressed(self):
        if self.frameGraphUpdate-self.graphUpdate >= 0:
            self.frameGraphUpdate -= self.graphUpdate
            self.ui.horizontalSlider_graph.setValue(self.frameGraphUpdate)
            self.isUpdateGraph = True
            self.ui.backwardButton_graph.setEnabled(False)
            self.ui.forwardButton_graph.setEnabled(False)
        else:
            self.frameGraphUpdate = 0
            self.ui.horizontalSlider_graph.setValue(self.frameGraphUpdate)
            self.isUpdateGraph = True
            self.ui.backwardButton_graph.setEnabled(False)
            self.ui.forwardButton_graph.setEnabled(False)

    def forwardButtonGraphPressed(self):
        if self.frameGraphUpdate+self.graphUpdate < self.maxGraphX:
            self.frameGraphUpdate += self.graphUpdate
            self.ui.horizontalSlider_graph.setValue(self.frameGraphUpdate)
            self.isUpdateGraph = True
            self.ui.backwardButton_graph.setEnabled(False)
            self.ui.forwardButton_graph.setEnabled(False)
        else:
            self.frameGraphUpdate = self.maxGraphX - 1
            self.ui.horizontalSlider_graph.setValue(self.frameGraphUpdate)
            self.isUpdateGraph = True
            self.ui.backwardButton_graph.setEnabled(False)
            self.ui.forwardButton_graph.setEnabled(False)
    
    def selectGraphChange(self):
        self.setGraphX()
        self.ax1.lines.remove(self.ax1.lines[4])
        self.ax1.plot([self.data[self.frameGraphUpdate-1,5],self.data[self.frameGraphUpdate-1,5]],[-10,10],'Gray',linewidth=2.0) 
        self.ui.GraphImage.canvas.draw()
    
    def setGraphX(self):
        if self.ui.comboBox_graph.currentIndex() == 1:
            if self.frameGraphUpdate >= 0 and self.frameGraphUpdate < 2000: self.ax1.set_xlim(0,1)
            elif self.frameGraphUpdate >= 2000 and self.frameGraphUpdate < 4000: self.ax1.set_xlim(1,2)
            elif self.frameGraphUpdate >= 4000 and self.frameGraphUpdate < 6000: self.ax1.set_xlim(2,3)
            elif self.frameGraphUpdate >= 6000 and self.frameGraphUpdate < 8000: self.ax1.set_xlim(3,4)
            elif self.frameGraphUpdate >= 8000 and self.frameGraphUpdate < 10000: self.ax1.set_xlim(4,5)
            elif self.frameGraphUpdate >= 10000 and self.frameGraphUpdate < 12000: self.ax1.set_xlim(5,6)
            elif self.frameGraphUpdate >= 12000 and self.frameGraphUpdate < 14000: self.ax1.set_xlim(6,7)
            elif self.frameGraphUpdate >= 14000 and self.frameGraphUpdate < 16000: self.ax1.set_xlim(7,8)
            elif self.frameGraphUpdate >= 16000 and self.frameGraphUpdate < 18000: self.ax1.set_xlim(8,9)
            elif self.frameGraphUpdate >= 18000 and self.frameGraphUpdate < 20000: self.ax1.set_xlim(9,10)
            elif self.frameGraphUpdate >= 20000 and self.frameGraphUpdate < 22000: self.ax1.set_xlim(10,11)
            elif self.frameGraphUpdate >= 22000 and self.frameGraphUpdate < 24000: self.ax1.set_xlim(11,12)
            elif self.frameGraphUpdate >= 24000 and self.frameGraphUpdate < 26000: self.ax1.set_xlim(12,13)
            elif self.frameGraphUpdate >= 26000 and self.frameGraphUpdate < 28000: self.ax1.set_xlim(13,14)
            elif self.frameGraphUpdate >= 28000 and self.frameGraphUpdate < 30000: self.ax1.set_xlim(14,15)
            elif self.frameGraphUpdate >= 30000 and self.frameGraphUpdate < 32000: self.ax1.set_xlim(15,16)
            elif self.frameGraphUpdate >= 32000 and self.frameGraphUpdate < 34000: self.ax1.set_xlim(16,17)
            elif self.frameGraphUpdate >= 34000 and self.frameGraphUpdate < 36000: self.ax1.set_xlim(17,18)
            elif self.frameGraphUpdate >= 36000 and self.frameGraphUpdate < 38000: self.ax1.set_xlim(18,19)
            elif self.frameGraphUpdate >= 38000 and self.frameGraphUpdate < 40000: self.ax1.set_xlim(19,20)
        elif self.ui.comboBox_graph.currentIndex() == 2:
            if self.frameGraphUpdate >= 0 and self.frameGraphUpdate < 10000: self.ax1.set_xlim(0,5)
            elif self.frameGraphUpdate >= 10000 and self.frameGraphUpdate < 20000: self.ax1.set_xlim(5,10)
            elif self.frameGraphUpdate >= 20000 and self.frameGraphUpdate < 30000: self.ax1.set_xlim(10,15)
            elif self.frameGraphUpdate >= 30000 and self.frameGraphUpdate < 40000: self.ax1.set_xlim(15,20)
        else:
            self.ax1.set_xlim(0,20)

    def horizontalSliderGraphPressed(self):
        self.sliderbusyGraph = True
    
    def horizontalSliderGraphReleased(self):
        self.frameGraphUpdate = self.ui.horizontalSlider_graph.value()
        self.ui.backwardButton_graph.setEnabled(False)
        self.ui.forwardButton_graph.setEnabled(False)
        self.sliderbusyGraph = False
        self.isUpdateGraph = True
    
    def fileButtonPressed(self):
        self.frameGraphUpdate = 0
        self.ui.horizontalSlider_graph.setValue(self.frameGraphUpdate)
        fileName = QFileDialog.getOpenFileName(None,caption="Select Data File in Excel",directory=QtCore.QDir.currentPath())
        if len(fileName[0])>0:
            try:
                try:
                    self.df = pd.read_csv(fileName[0], converters={"TimestampCounter": lambda x: int(x, 16),
                                                                    "TimeStamp": lambda x: int(x, 16)/1000000,           # convert column Timestamp to 
                                                                    "Ax": lambda x: self.twos_comp(int(x, 16), 16)*(1/2048),  # convert data with two complement  * +-16G scale 
                                                                    "Ay": lambda x: self.twos_comp(int(x, 16), 16)*(1/2048),  # convert data with two complement  * +-16G scale 
                                                                    "Az": lambda x: self.twos_comp(int(x, 16), 16)*(1/2048)})  # convert data with two complement  * +-16G scale  
                    self.df['rms_A'] =  np.sqrt((self.df.Ax*self.df.Ax)+(self.df.Ay*self.df.Ay)+(self.df.Az*self.df.Az)) # add rms acc signals to dataframe  
                    self.df['Real_Time'] = (self.df.TimestampCounter*0.0005)
                    self.df = self.df.round({'Ax': 3,'Ay': 3,'Az': 3,'rms_A': 3}) # roundup data     
                    self.draw()  
                except:
                    self.df = pd.read_csv(fileName[0])
                    self.df['Real_Time'] = (self.df.TimestampCounter*0.0005)
                    self.df = self.df.round({'Ax': 3,'Ay': 3,'Az': 3,'rms_A': 3}) # roundup data     
                    self.draw()  
                # setting button and status bar
                self.fileGraph = fileName[0]
                self.ui.statusbar.showMessage("File Graph:: " + self.fileGraph)  
                self.ui.comboBox_graph.setCurrentIndex(0)
                self.ui.forwardButton_graph.setEnabled(True)
                self.ui.backwardButton_graph.setEnabled(True)
                self.ui.autoButton.setEnabled(True)
                self.ui.horizontalSlider_graph.setEnabled(True)
                self.ui.comboBox_graph.setEnabled(True)
                self.isthreadActiveGraph = True
                if self.isthreadActiveVideo and self.isthreadActiveGraph:
                    self.ui.startButton.setEnabled(True)
                    self.ui.pauseButton.setEnabled(True)
                    self.ui.fallButton.setEnabled(True)
                    self.ui.slapButton.setEnabled(True)
                    self.ui.forwardButton.setEnabled(True)
                    self.ui.backwardButton.setEnabled(True)
                    self.ui.matchingButton.setEnabled(True)
            except: self.ui.statusbar.showMessage("Error::Please try again") 

    def draw(self):  
        self.ax1.clear() 
        try: self.df.drop(columns=['TimeStamp','Gx','Gy','Gz','rms_G'], inplace=True) #  remove roll /s, pitch/s, yaw/s and timestamp  
        except: self.df.drop(columns=['TimeStamp','Gx','Gy','Gz'], inplace=True)
        self.data = self.df.values[0:self.maxGraphX,0:6]
        self.ax1.plot(self.data[:,5],self.data[:,1],'y')
        self.ax1.plot(self.data[:,5],self.data[:,2],'r')
        self.ax1.plot(self.data[:,5],self.data[:,3],'g')
        self.ax1.plot(self.data[:,5],self.data[:,4],'b')
        self.ax1.set_ylim(-10, 10)
        self.ax1.set_xlim(0,20)
        self.ui.horizontalSlider_graph.setMaximum(self.maxGraphX)
        self.ax1.plot([self.data[0,5],self.data[0,-1]],[-10,10],'Gray',linewidth=2.0)    
        self.ui.GraphImage.canvas.draw()
    
    def twos_comp(self, val, bits):                                                      
        """compute the 2's complement of int value val"""                          
        if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
            val = val - (1 << bits)        # compute negative value                
        return val                         # return positive value as is  

    ######################### Video ##############################
    def openButtonPressed(self):
        self.frameVideo = 0
        self.ui.horizontalSlider_video.setValue(self.frameVideo)
        try:
            fileName = QFileDialog.getOpenFileName(None,caption="Select Video File",directory=QtCore.QDir.currentPath())
            if len(fileName[0])>0:
                self.cap = cv2.VideoCapture(fileName[0])
                self.isthreadActiveVideo = True
            else:
                self.isthreadActiveVideo = False
                return
            self.length = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.fps = self.cap.get(cv2.CAP_PROP_FPS)
            # set fps specific for updating video
            if round(self.fps) == 50: self.ui.comboBox_video.setCurrentIndex(1)
            elif round(self.fps) == 30: self.ui.comboBox_video.setCurrentIndex(2)
            else: self.ui.comboBox_video.setCurrentIndex(0)
            self.setVideo() 
            self.ui.horizontalSlider_video.setMaximum(self.endframe-self.stframe)
            self.cap.set(1,self.stframe)
            ret, frame = self.cap.read()
            self.frameVideo = self.stframe
            self.limg = frame
            self.frameHeight = frame.shape[0]
            self.frameWidth = frame.shape[1] 
            self.on_zoomfit_clicked()
            nchannel = frame.shape[2]
            limg2 = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  
            timg = cv2.resize(limg2,(int(self.scaleFactor*limg2.shape[1]),int(self.scaleFactor*limg2.shape[0]))) 
            limage = QtGui.QImage(timg.data, timg.shape[1], timg.shape[0], nchannel*timg.shape[1], QtGui.QImage.Format_RGB888)  
            self.ui.VideoImage.setPixmap(QtGui.QPixmap(limage))
            self.ui.forwardButton_video.setEnabled(True)
            self.ui.backwardButton_video.setEnabled(True)
            self.ui.horizontalSlider_video.setEnabled(True)
            self.ui.comboBox_video.setEnabled(True)
            self.ui.statusbar.showMessage("File Video:: " + str(fileName[0])) 
            self.fileVideo = fileName[0]
            if self.isthreadActiveGraph and self.isthreadActiveVideo:
                self.ui.startButton.setEnabled(True)
                self.ui.pauseButton.setEnabled(True)
                self.ui.fallButton.setEnabled(True)
                self.ui.slapButton.setEnabled(True)
                self.ui.forwardButton.setEnabled(True)
                self.ui.backwardButton.setEnabled(True)
                self.ui.matchingButton.setEnabled(True)
        except: self.ui.statusbar.showMessage("Error::Please try again")
    
    def on_zoomfit_clicked(self): # for fitting frame of window   
        self.resizegoing = True
        a = self.ui.VideoImage.size()
        if a.width()/self.frameWidth < a.height()/self.frameHeight:
            self.scaleFactor = a.width()/self.frameWidth
            self.startx = 0
            self.starty = (a.height() - self.scaleFactor * self.frameHeight)/2
        else:
            self.scaleFactor=1.0*a.height()/self.frameHeight
            self.starty = 0
            self.startx = (a.width() - self.scaleFactor * self.frameWidth)/2.0
        sleep(0.2)
        self.resizegoing = False
    
    def setVideo(self):
        if self.ui.comboBox_video.currentIndex() == 1:
            self.graphUpdate = 40
            self.videoUpdate = 20
            self.stframe = int(0)    
            self.endframe = int(self.length) 
        elif self.ui.comboBox_video.currentIndex() == 2:
            self.graphUpdate = 32
            self.videoUpdate = 4
            self.stframe = int(0)    
            self.endframe = int(self.length-8) 
        else:
            self.graphUpdate = 40
            self.videoUpdate = 20
            self.stframe = int(0)    
            self.endframe = int(self.length) 

    def forwardButtonVideoPressed(self):
        if self.frameVideo+self.videoUpdate < self.endframe:
            self.frameVideo+=self.videoUpdate
            self.ui.horizontalSlider_video.setValue(self.frameVideo)
            self.isUpdateVideo = True
            self.ui.backwardButton_video.setEnabled(False)
            self.ui.forwardButton_video.setEnabled(False)
        else:
            self.frameVideo = self.endframe - 1
            self.ui.horizontalSlider_video.setValue(self.frameVideo+1)
            self.isUpdateVideo = True
            self.ui.backwardButton_video.setEnabled(False)
            self.ui.forwardButton_video.setEnabled(False)

    def backwardButtonVideoPressed(self):
        if self.frameVideo-self.videoUpdate > 0:
            self.frameVideo -= self.videoUpdate
            self.ui.horizontalSlider_video.setValue(self.frameVideo)
            self.isUpdateVideo = True
            self.ui.backwardButton_video.setEnabled(False)
            self.ui.forwardButton_video.setEnabled(False)
        else:
            self.frameVideo = self.stframe
            self.ui.horizontalSlider_video.setValue(self.frameVideo)
            self.isUpdateVideo = True
            self.ui.backwardButton_video.setEnabled(False)
            self.ui.forwardButton_video.setEnabled(False)

    def selectVideoChange(self):
        self.setVideo()

    def horizontalSliderVideoPressed(self):
        self.sliderbusyVideo = True

    def horizontalSliderVideoReleased(self):
        self.frameVideo = self.stframe + self.ui.horizontalSlider_video.value() - 1
        if self.matching == 0:
            self.ui.backwardButton_video.setEnabled(False)
            self.ui.forwardButton_video.setEnabled(False)
            self.isUpdateVideo = True
            self.sliderbusyVideo = False
        elif self.matching == 1:
            current = self.frameVideo - self.matchVideo
            self.frameGraphUpdate = round(self.matchGraph + (current*(self.graphUpdate/self.videoUpdate)))
            if self.frameGraphUpdate < 0: self.frameGraphUpdate = 0
            elif self.frameGraphUpdate > self.maxGraphX: self.frameGraphUpdate = self.maxGraphX - 1
            self.ui.horizontalSlider_graph.setValue(self.frameGraphUpdate)
            self.isUpdateGV = True
            self.sliderbusyVideo = False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    sys.exit(app.exec_())