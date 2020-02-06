import os, sys
from configobj import ConfigObj
from time import sleep
import cv2
from threading import Timer,Thread,Event
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication,QMainWindow,QFileDialog,QVBoxLayout,QMessageBox
from PyQt5 import QtGui, QtCore ,QtWidgets

from MainForm4 import Ui_MainWindow
import numpy as np
import pandas as pd
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import datetime
from scipy.signal import find_peaks
import math


############## Graph Updating ##############
class workerThread(QThread):
    #updatedLine = QtCore.pyqtSignal(int)
    def __init__(self,mw):
        self.mw = mw
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):        
        while self.mw.isRunGraph:  
            if self.mw.isthreadActiveGraph and self.mw.isUpdateGraph:
                # Update frame of graph and Xlim
                self.mw.setGraphX()
                self.mw.ax1.lines.remove(self.mw.ax1.lines[4])
                if self.mw.ui.comboBox_type.currentIndex() == 0:
                    self.mw.ax1.plot([self.mw.data[self.mw.frameGraphUpdate,10],self.mw.data[self.mw.frameGraphUpdate,-1]],[-10,10],'Gray',linewidth=2.0) 
                elif self.mw.ui.comboBox_type.currentIndex() == 1:
                    self.mw.ax1.plot([self.mw.data[self.mw.frameGraphUpdate,10],self.mw.data[self.mw.frameGraphUpdate,-1]],[-100,100],'Gray',linewidth=2.0) 
                self.mw.ui.GraphImage.canvas.draw()
                # reset parameter
                self.mw.isUpdateGraph = False
                self.mw.ui.backwardButton_graph.setEnabled(True)
                self.mw.ui.forwardButton_graph.setEnabled(True)
                # calculate time
                self.mw.calculationTime()
                QApplication.processEvents()

# Main application (Function)
class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # set full screen
        self.showMaximized()

        # set icon
        self.setWindowIcon(QtGui.QIcon('asset/Logo4.ico')) 
        self.ui.startActionButton.setIcon(QtGui.QIcon('asset/fallButton.png'))
        self.ui.stopActionButton.setIcon(QtGui.QIcon('asset/fallButton.png'))
        self.ui.saveButton.setIcon(QtGui.QIcon('asset/saveButton.png'))
        self.ui.forwardButton_graph.setIcon(QtGui.QIcon('asset/forwardButton.png'))
        self.ui.backwardButton_graph.setIcon(QtGui.QIcon('asset/backwardButton.png'))
        self.ui.fileButton.setIcon(QtGui.QIcon('asset/fileButton.png'))
        self.ui.personalButton.setIcon(QtGui.QIcon('asset/personalButton.png'))

        # set save config file (slap button and fall button)
        self.ui.startActionButton.clicked.connect(self.startActionButtonPressed)
        self.ui.stopActionButton.clicked.connect(self.stopActionButtonPressed)
        self.ui.saveButton.clicked.connect(self.saveButtonPressed)
        
        # For open personal data file
        self.ui.personalButton.clicked.connect(self.personalButtonPressed)
        self.ui.statusbar.showMessage("Select personal data file before opening graph")

        # set graph button (Connection)
        self.ui.fileButton.clicked.connect(self.fileButtonPressed)      
        self.ui.horizontalSlider_graph.sliderPressed.connect(self.horizontalSliderGraphPressed)
        self.ui.horizontalSlider_graph.sliderReleased.connect(self.horizontalSliderGraphReleased)
        self.ui.backwardButton_graph.clicked.connect(self.backwardButtonGraphPressed)
        self.ui.forwardButton_graph.clicked.connect(self.forwardButtonGraphPressed)
        self.ui.comboBox_graph.currentIndexChanged.connect(self.selectGraphChange)
        self.ui.comboBox_type.currentIndexChanged.connect(self.selectTypeChange)
        self.ui.comboBox_peak.currentIndexChanged.connect(self.selectPeakChange)

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
        self.wthread = workerThread(self)           
        self.wthread.start() 
        self.frameGraphUpdate = 0
        self.maxGraphX = 40000
        self.timeGraph = 0
        self.graphUpdate = 40
    
    ######################### Open personal data #######################
    def personalButtonPressed(self):
        self.directory = "D:/"
        fileName = QFileDialog.getOpenFileName(None,caption="Select Personal Data File in Excel", directory=self.directory)
        self.directory = os.path.dirname(fileName[0])
        if len(fileName[0])>0: 
            try:
                xls = pd.ExcelFile(fileName[0])
                self.dfPersonal = pd.read_excel(xls)
                self.ui.fileButton.setEnabled(True)
                self.ui.personalButton.setEnabled(False)
                self.ui.statusbar.showMessage("Open Personal Data successfully") 
                self.successMessage("Open Personal Data successfully")
            except Exception as e:
                self.ui.statusbar.showMessage("Error::Please try again") 
                self.errorMessage(e) 
    
    ######################### Calculate time ########################
    def calculationTime(self):
        self.timeGraph = round((self.frameGraphUpdate*0.0005),2)
        self.ui.statusbar.showMessage("Number of Signal :: " + str(self.frameGraphUpdate+1) +
            "/"+ str(self.maxGraphX) + " (Time =" + str(self.timeGraph) + " second)")
    
    ######################### Message Box ##############################
    def errorMessage(self,message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(str(message))
        msg.setWindowTitle("Error")
        msg.exec_()      
    
    def successMessage(self,message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Success")
        msg.setInformativeText(str(message))
        msg.setWindowTitle("Success")
        msg.exec_()  

    ######################### Save config ##############################
    def startActionButtonPressed(self):
        # set name for saving file
        wordG = self.fileGraph.split('/')
        NewwordG = wordG[len(wordG)-1].split('.')
        fileNameG = NewwordG[0]
        # set directory
        directory = ""
        for i in range(len(wordG)-1):
            directory = directory + wordG[i] + "/"
        directory = directory + "/Database"
        if not os.path.exists(directory):
            os.makedirs(directory)
        # set file name
        filename = directory+"/"+str(fileNameG)+"(time).config"
        # Save 
        config = ConfigObj(filename, encoding='utf8')
        config.filename = filename
        self.startActionTime = self.timeStamp[self.frameGraphUpdate]
        config["StartAction-Graph"] = str(self.startActionTime)
        config.write()
        self.ui.statusbar.showMessage("Save successfully - StartAction-Graph = " +str(self.timeGraph)+ " second") 
        self.successMessage("Save successfully - StartAction-Graph = " +str(self.timeGraph)+ " second")

    def stopActionButtonPressed(self):
        # set name for saving file
        wordG = self.fileGraph.split('/')
        NewwordG = wordG[len(wordG)-1].split('.')
        fileNameG = NewwordG[0]
        # set directory
        directory = ""
        for i in range(len(wordG)-1):
            directory = directory + wordG[i] + "/"
        directory = directory + "/Database"
        if not os.path.exists(directory):
            os.makedirs(directory)
        # set file name
        filename = directory+"/"+str(fileNameG)+"(time).config"
        # Save 
        config = ConfigObj(filename, encoding='utf8')
        config.filename = filename
        self.stopActionTime = self.timeStamp[self.frameGraphUpdate]
        config["StopAction-Graph"] = str(self.stopActionTime)
        config.write()
        self.ui.statusbar.showMessage("Save successfully - StopAction-Graph = " +str(self.timeGraph)+ " second") 
        self.successMessage("Save successfully - StopAction-Graph = " +str(self.timeGraph)+ " second")
        self.ui.saveButton.setEnabled(True)
    
    def saveButtonPressed(self):
        positionStart = int(self.df[self.df['TimeStamp']==self.startActionTime]['TimestampCounter'].values)
        positionStop = int(self.df[self.df['TimeStamp']==self.stopActionTime]['TimestampCounter'].values)
        pos1 = positionStart
        pos2 = positionStop
        #define Label 
        self.df['Label'] = 0
        # cut data
        try: 
            self.df.drop(columns=['Real_Time'], inplace=True)
            self.df.drop(self.df.index[positionStop:self.maxGraphX], inplace=True)
            self.df.drop(self.df.index[0:positionStart], inplace=True)
            # set name for saving file
            wordG = self.fileGraph.split('/')
            NewwordG = wordG[len(wordG)-1].split('.')
            fileNameG = NewwordG[0]
            # set personal parameter
            try: 
                splitFileNameG = fileNameG.split('_')
                participant_ID = splitFileNameG[1]
                for i in range(len(self.dfPersonal.Participant_ID)):
                    if self.dfPersonal.Participant_ID[i].find(participant_ID)>-1:
                        participant_BMI = self.dfPersonal.BMI[i]
                        self.df['BMI'] = participant_BMI
                        participant_SexM = self.dfPersonal.Sex_M[i]
                        self.df['SEXM'] = participant_SexM
                        participant_SexF = self.dfPersonal.Sex_F[i]
                        self.df['SEXF'] = participant_SexF
                        participant_Active = self.dfPersonal.Active[i]
                        self.df['Active'] = participant_Active
            except: pass
            # set directory
            directory = ""
            for i in range(len(wordG)-1):
                directory = directory + wordG[i] + "/"
            directory = directory + "/Database"
            if not os.path.exists(directory):
                os.makedirs(directory)
            # set file name
            filename = directory+"/"+str(fileNameG)+"(Cropped).csv"
            self.df.to_csv(filename) 
            self.successMessage("Save CSV file successfully")
            self.ui.saveButton.setEnabled(False)
        except Exception as e:
            #self.errorMessage("Please click save start and stop action button before click this button") 
            self.errorMessage(e) 

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
        if self.ui.comboBox_type.currentIndex() == 0:
            self.ax1.plot([self.data[self.frameGraphUpdate,10],self.data[self.frameGraphUpdate,10]],[-10,10],'Gray',linewidth=2.0) 
        elif self.ui.comboBox_type.currentIndex() == 1:
            self.ax1.plot([self.data[self.frameGraphUpdate,10],self.data[self.frameGraphUpdate,10]],[-100,100],'Gray',linewidth=2.0) 
        self.ui.GraphImage.canvas.draw()
    
    def selectTypeChange(self):
        self.draw()
    
    def selectPeakChange(self):
        if self.ui.comboBox_peak.currentIndex() == 0: pass
        else: 
            pos = self.listPeak[self.ui.comboBox_peak.currentIndex()-1]
            self.ui.horizontalSlider_graph.setValue(pos)
            self.frameGraphUpdate = self.ui.horizontalSlider_graph.value()
            self.sliderbusyGraph = False
            self.isUpdateGraph = True
    
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
        fileName = QFileDialog.getOpenFileName(None,caption="Select Data File in Excel",directory=self.directory)
        self.directory = os.path.dirname(fileName[0])
        if len(fileName[0])>0:
            try:
                try:
                    self.data = pd.read_csv(fileName[0], converters={"TimestampCounter": lambda x: int(x, 16),
                                                                    "TimeStamp": lambda x: int(x, 16)/1000000,           # convert column Timestamp to 
                                                                    "Ax": lambda x: self.twos_comp(int(x, 16), 16)*(1/2048),  # convert data with two complement  * +-16G scale 
                                                                    "Ay": lambda x: self.twos_comp(int(x, 16), 16)*(1/2048),  # convert data with two complement  * +-16G scale 
                                                                    "Az": lambda x: self.twos_comp(int(x, 16), 16)*(1/2048),  # convert data with two complement  * +-16G scale 
                                                                    "Gx": lambda x: self.twos_comp(int(x, 16), 16)/131,       # convert data with two complement  * +-2000 scale 
                                                                    "Gy": lambda x: self.twos_comp(int(x, 16), 16)/131,       # convert data with two complement  * +-2000 scale 
                                                                    "Gz": lambda x: self.twos_comp(int(x, 16), 16)/131})      # convert data with two complement  * +-2000 scale 
                    self.df = self.data.copy()
                    self.df['rss_A'] =  np.sqrt((self.df.Ax*self.df.Ax)+(self.df.Ay*self.df.Ay)+(self.df.Az*self.df.Az)) # add rss acc signals to dataframe  
                    self.df['rss_G'] =  np.sqrt((self.df.Gx*self.df.Gx)+(self.df.Gy*self.df.Gy)+(self.df.Gz*self.df.Gz)) # add rss gyro signals to dataframe
                    self.df['Real_Time'] = (self.df.TimestampCounter*0.0005)
                    self.df['Deg_saggital'] = np.arctan(self.df['Az']/self.df['Ay'])*(180/math.pi)
                    self.df['Deg_Frontal'] = np.arctan(self.df['Ax']/self.df['Ay'])*(180/math.pi)
                    self.timeStamp = self.df["TimeStamp"]
                    self.df = self.df.round({'Ax': 3,'Ay': 3,'Az': 3,'Gx': 3,'Gy': 3,'Gz': 3,'rss_A': 3,'rss_G': 3}) # roundup data     
                    self.frameGraphUpdate = 0
                    self.draw()  
                except Exception as e: 
                    self.data = pd.read_csv(fileName[0])
                    self.df = self.data.copy()
                    self.df['Real_Time'] = (self.df.TimestampCounter*0.0005)
                    self.df['Deg_saggital'] = np.arctan(self.df['Az']/self.df['Ay'])*(180/math.pi)
                    self.df['Deg_Frontal'] = np.arctan(self.df['Ax']/self.df['Ay'])*(180/math.pi)
                    self.timeStamp = self.df["TimeStamp"]
                    self.df = self.df.round({'Ax': 3,'Ay': 3,'Az': 3,'Gx': 3,'Gy': 3,'Gz': 3,'rss_A': 3,'rss_G': 3}) # roundup data     
                    self.frameGraphUpdate = 0
                    self.draw()  
                # Setting parameters
                self.slaptime1 = None
                self.slaptime2 = None
                self.falltime = None
                # setting button and status bar
                self.findPeak()
                self.fileGraph = fileName[0]
                self.ui.statusbar.showMessage("File Graph:: " + self.fileGraph)  
                self.ui.comboBox_graph.setCurrentIndex(0)
                self.ui.comboBox_peak.setCurrentIndex(0)
                self.ui.horizontalSlider_graph.setValue(self.frameGraphUpdate)
                self.ui.forwardButton_graph.setEnabled(True)
                self.ui.backwardButton_graph.setEnabled(True)
                self.ui.horizontalSlider_graph.setEnabled(True)
                self.ui.comboBox_graph.setEnabled(True)
                self.ui.comboBox_type.setEnabled(True)
                self.ui.comboBox_peak.setEnabled(True)
                self.isthreadActiveGraph = True
                if self.isthreadActiveGraph:
                    self.ui.startActionButton.setEnabled(True)
                    self.ui.stopActionButton.setEnabled(True)
            except Exception as e:  
                self.ui.statusbar.showMessage("Error::Please try again") 
                self.errorMessage(e)     

    def draw(self):  
        self.ax1.clear() 
        self.data = self.df.values[:,0:11]
        if self.ui.comboBox_type.currentIndex() == 0:
            self.ax1.plot(self.data[:,10],self.data[:,2],'y') # Ax
            self.ax1.plot(self.data[:,10],self.data[:,3],'r') # Ay
            self.ax1.plot(self.data[:,10],self.data[:,4],'g') # Az
            self.ax1.plot(self.data[:,10],self.data[:,8],'b') # rss_A
            self.ax1.set_ylim(-10, 10)
            self.setGraphX()
            self.ui.horizontalSlider_graph.setMaximum(self.maxGraphX-1)
            self.ax1.plot([self.data[self.frameGraphUpdate,10],self.data[self.frameGraphUpdate,-1]],[-10,10],'Gray',linewidth=2.0)
        elif self.ui.comboBox_type.currentIndex() == 1:
            self.ax1.plot(self.data[:,10],self.data[:,5],'y') # Gx
            self.ax1.plot(self.data[:,10],self.data[:,6],'r') # Gy
            self.ax1.plot(self.data[:,10],self.data[:,7],'g') # Gz
            self.ax1.plot(self.data[:,10],self.data[:,9],'b') # rss_G
            self.ax1.set_ylim(-100, 100)
            self.setGraphX()
            self.ui.horizontalSlider_graph.setMaximum(self.maxGraphX-1)
            self.ax1.plot([self.data[self.frameGraphUpdate,10],self.data[self.frameGraphUpdate,-1]],[-100,100],'Gray',linewidth=2.0)    
        self.ui.GraphImage.canvas.draw()

    def findPeak(self):
        final_list = [] 
        N = 5
        A = np.array((self.data[:,8]))
        peaks, _ = find_peaks(A,distance=200)    
        list1 = peaks.tolist()
        for i in range(0, N):  
            max1 = 0
            for j in range(len(list1)):      
                if A[list1[j]] > max1: 
                    max1 = A[list1[j]]
                    position = list1[j]
            list1.remove(position) 
            final_list.append(position) 
        self.listPeak = final_list
    
    def twos_comp(self, val, bits):                                                      
        """compute the 2's complement of int value val"""                          
        if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
            val = val - (1 << bits)        # compute negative value                
        return val                         # return positive value as is  


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    sys.exit(app.exec_())