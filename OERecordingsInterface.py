import pyopenephys
import numpy as np
import FormatInterface

class HandelOEFile(FormatInterface.FormatInterface):
    def __init__(self,inputFile):
        super().__init__()
        self.inputFile = inputFile
        self.experiments = []
        self.recordings = []
        self.extractedFile = []

    def GetData(self):
        try:
            self.extractedFile = pyopenephys.File(self.inputFile)
            self.experiments=self.extractedFile.experiments
            for experiment in  self.experiments:
                self.recordings =experiment.recordings
                for recording in  self.recordings:
                    self.durationMS = float((recording).duration)*1e3 # Scan all files and gets the total duration, therefore, needs to come first
                    samplingRate=float(recording.sample_rate)
                    self.timeStepMS = float(1/samplingRate)*1e3
                    self.GetRelevantTimestamps()
                    self.nChannels =int (recording.nchan)
                    self.GetRelevantChannels()
                    if ((self.startTimeIndex != None) and (self.endTimeIndex != None) and ( self.startChannel != None) and (self.endChannel != None) and ( self.timestamps[0] != None)):
                        self.metaData = np.array(((recording.analog_signals[0]).signal)[ self.startChannel-1: self.endChannel,  self.startTimeIndex: self.endTimeIndex])
                        self.metaData = self.metaData.transpose()
                        self.PlotData()
                    else:
                        print("Error Loading Data, Please Try Again")
        except Exception as e:
            print("An exception occurred. Please Try Again")
            print(e)
            return