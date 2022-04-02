import os
import sys
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT, FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QDialog,QPushButton, QVBoxLayout, QFileDialog, QMessageBox,QApplication,QHBoxLayout ,QWidget
from PyQt5 import QtCore
from easygui import multenterbox,choicebox,multchoicebox
import FileHandler , FormatInterface

class Window(QDialog):
    def __init__(self):
        super(Window, self).__init__()
        # setting title
        self.setWindowTitle("Neural Electrophysiology Data Analyzer")
        #Set Window maximized
        self.showMaximized()
        #A figure instance to plot on
        self.figure= Figure()
        #Set Current file elements
        self.nchannels=0
        self.duration =0
        self.currentFile=FormatInterface.FormatInterface()
        #Window buttons- Minimize,close, change size
        self.win= self.setWindowFlags(QtCore.Qt.Window|QtCore.Qt.WindowMinMaxButtonsHint
                                      |QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint |
                                      QtCore.Qt.WindowCloseButtonHint |QtCore.Qt.WindowStaysOnTopHint)

        #This is the Canvas Widget that displays the `figure`
        #It takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvasQTAgg(self.figure)

        #This is the Navigation widget
        #It takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar2QT(self.canvas,self)

        #Buttons:
        self.plotButton = QPushButton('Plot',self)
        self.plotButton.clicked.connect(self.ploti)
        self.fileExplorerButton = QPushButton('File Explorer', self)
        self.fileExplorerButton.clicked.connect(self.openFileNameDialog)
        self.timeWindowButton = QPushButton('Time Selection', self)
        self.timeWindowButton.clicked.connect(self.SelectTime)
        self.ChannelSelectionButton= QPushButton('Channel Selection', self)
        self.ChannelSelectionButton.clicked.connect(self.chosenChannels)
        self.forwardTimeButton = QPushButton('+ Time Window', self)
        self.forwardTimeButton.clicked.connect(self.forwardTime)
        self.backwardTimeButton = QPushButton('- Time Window', self)
        self.backwardTimeButton.clicked.connect(self.backwardTime)

        #Set the toolbar layout
        self.buttonsWidget = QWidget()
        self.buttonsWidgetLayout = QHBoxLayout(self.buttonsWidget)
        self.buttons = [self.fileExplorerButton,self.ChannelSelectionButton,self.timeWindowButton,self.plotButton,self.backwardTimeButton,self.forwardTimeButton]
        for button in self.buttons:
            self.buttonsWidgetLayout.addWidget(button)
        self.buttonsWidgetLayout.setMenuBar(self.toolbar)
        self.buttonsWidgetLayout.setAlignment(QtCore.Qt.AlignLeft)

        #Set the overall layout
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint)
        self.layout = QVBoxLayout()
        self.layout.setMenuBar(self.buttonsWidget)
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

    def forwardTime(self):
        try:
            self.currentFile.startTime=self.currentFile.startTime+self.currentFile.windowTime
            if (self.currentFile.startTime + self.currentFile.windowTime) > self.currentFile.durationMS:
                self.currentFile.startTime=  self.currentFile.durationMS -self.currentFile.windowTime
            self.currentFile.GetTimeIndex()
            self.ploti()
        except Exception as e:
            QMessageBox.critical(self, "An exception occurred", f"Forward Time Error.\nError: {str(e)}")
            print("An exception occurred. Please Try Again")
            print(e)
            return

    def backwardTime(self):
        try:
            self.currentFile.startTime = self.currentFile.startTime - self.currentFile.windowTime
            if (self.currentFile.startTime - self.currentFile.windowTime) < 0:
                self.currentFile.startTime=0
            self.currentFile.GetTimeIndex()
            self.ploti()
        except Exception as e:
            QMessageBox.critical(self, "An exception occurred", f"Cannot get any earlier timestamp.\nError: {str(e)}")
            print("An exception occurred. Please Try Again")
            print(e)
            return

    def openFileNameDialog(self):
        try:
            msg = "Please Choose File Type"
            title = "Neural Electrophysiology Data Analyzer"
            fileTypes = ["MCH5","NWB", "OE"]
            self.selectedFileType = choicebox(msg, title, fileTypes)
            options = QFileDialog.Options()
            self.nchannels=[]
            if "OE"==self.selectedFileType:#Chooses a folder for OE
                home = os.getenv("HOME")
                self.fileName=QFileDialog.getExistingDirectory(self,"Please Choose OE Node Folder",home,QFileDialog.ShowDirsOnly)
                # Gets the file data->Duration and number of channels
                self.currentFile = FileHandler.FileHandler(True, self.fileName)
            if ("MCH5"==self.selectedFileType or "NWB"==self.selectedFileType):#Chooses a file for "MCH5" or "NWB"
                self.fileName, _ = QFileDialog.getOpenFileName(self, "Please Choose File", "",
                                                    "All Files (*);;Python Files (*.py)", options=options)
                #Gets the file data->Duration and number of channels
                self.currentFile=FileHandler.FileHandler(True,self.fileName)
        except Exception as e:
            QMessageBox.critical(self, "An exception occurred", str(e))
            print("An exception occurred. Please Try Again")
            print(e)
            return


    def SelectTime(self):
        try:
            windowTime = (f"Window Time\n out of { int(self.currentFile.durationMS)} in ms:")
            msg = "Please Fill in The Following Time Parameters"
            title = "Neural Electrophysiology Data Analyzer"
            fieldNames = [ "Start Time",windowTime]
            fieldValues = []  # we start with blanks for the values
            fieldValues = multenterbox(msg, title, fieldNames)
            if len(fieldValues)>1:
                self.currentFile.startTime = int(fieldValues[0])
                self.currentFile.windowTime = int(fieldValues[1])
                if (self.currentFile.startTime + self.currentFile.windowTime) > self.currentFile.durationMS:
                    self.currentFile.startTime=  self.currentFile.durationMS -self.currentFile.windowTime
            self.currentFile.GetTimeIndex()
        except Exception as e:
            QMessageBox.critical(self, "An exception occurred", f"File not loaded or invalid input.\nError: {str(e)}")
            print("An exception occurred. Please Try Again")
            print(e)
            return

    def chosenChannels (self):
        try:
            msg = "Choose Channels To Display"
            title = "Neural Electrophysiology Data Analyzer"
            channels = []
            for i in range(self.currentFile.nChannels):
                channels.append((int(i+1)))
            self.currentFile.listOfChannels = multchoicebox(msg, title, channels)
        except Exception as e:
            QMessageBox.critical(self, "An exception occurred", f"File not loaded.\nError: {str(e)}")
            print("An exception occurred. Please Try Again")
            print(e)
            return

    def ploti(self):
        try:
            if 0<len(self.currentFile.listOfChannels) and 0!=self.currentFile.windowTime:
                plt.close('all')
                self.canvas.figure = self.currentFile.GetAndPlotMetaData()
                self.canvas.figure.set_size_inches([self.canvas.width() / 100.0, self.canvas.height() / 100.0])
                self.canvas.draw()
                self.toolbar.__init__(self.canvas, self)
            else:
                raise
        except Exception as e:
            QMessageBox.critical(self, "An exception occurred",f"Parameters to plot are not found.\nError: {str(e)}")
            print("An exception occurred. Please Try Again")
            print(e)
            return

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())