import pyopenephys
import numpy as np
import FormatInterface

class HandelOEFile(FormatInterface.FormatInterface):
    def __init__(self,inputFile,isGui):
        super().__init__()
        self.isGui=isGui
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
                    self.nChannels =int (recording.nchan)
                    if (self.isGui == False):
                        self.GetRelevantTimestamps()
                        self.GetRelevantChannels()
                        if ((self.startTimeIndex != None) and (self.endTimeIndex != None) and ( self.startChannel != None) and (self.endChannel != None) and ( self.timestamps[0] != None)):
                            self.metaData = np.array(((recording.analog_signals[0]).signal)[ self.startChannel-1: self.endChannel,  self.startTimeIndex: self.endTimeIndex])
                            self.metaData = self.metaData.transpose()
                            self.PlotData(self.isGui)
                        else:
                            print("Error Loading Data, Please Try Again")
        except Exception as e:
            print("An exception occurred. Please Try Again")
            print(e)
            return

    def GetAndPlotMetaData(self):
        self.metaData = np.array(((self.recordings[0].analog_signals[0]).signal)[0: self.nChannels,
                                 self.startTimeIndex: self.endTimeIndex])
        self.metaData = self.metaData.transpose()
        return self.PlotData(self.isGui)