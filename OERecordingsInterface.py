import pyopenephys
import numpy as np
import FormatInterface

class HandelOEFile:
    def __init__(self,inputFile):
       self.inputFile=inputFile
       self.experiments=[]
       self.recordings=[]
       self.allData = []

    def GetData(self):
        try:
            extractedFile = pyopenephys.File(self.inputFile)
            self.experiments=extractedFile.experiments
            for experiment in  self.experiments:
                self.recordings =experiment.recordings
                for recording in  self.recordings:
                    currentData = FormatInterface.FormatInterface()
                    currentData.durationMS = float((recording).duration)*1e3 # Scan all files and gets the total duration, therefore, needs to come first
                    samplingRate=float(recording.sample_rate)
                    currentData.timeStepMS = float(1/samplingRate)*1e3
                    currentData.GetRelevantTimestamps()
                    currentData.nChannels =int (recording.nchan)
                    currentData.GetRelevantChannels()
                    if ((currentData.startTimeIndex != None) and (currentData.endTimeIndex != None) and ( currentData.startChannel != None) and (currentData.endChannel != None) and ( currentData.timestamps[0] != None)):
                        currentData.metaData = np.array(((recording.analog_signals[0]).signal)[ currentData.startChannel-1: currentData.endChannel,  currentData.startTimeIndex: currentData.endTimeIndex])
                        currentData.metaData = currentData.metaData.transpose()
                        currentData.PlotData()
                        self.allData.append(currentData)
                    else:
                        print("Error Loading Data, Please Try Again")
        except Exception as e:
            print("An exception occurred. Please Try Again")
            print(e)
            return