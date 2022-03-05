import h5py
import numpy as np
import FormatInterface

class HandelMCH5File(FormatInterface.FormatInterface):
    def __init__(self,inputFile):
        super().__init__()
        self.inputFile = inputFile
        self.listOfRecordings = []
        self.listOfStreams = []
        self.extractedFile = []
    def GetData(self):
        try:
            tickPosition = 9
            self.extractedFile = h5py.File(self.inputFile,"r")
            self.listOfRecordings= self.ShowFileInnerSection(self.extractedFile['/Data/'])
            for recording in self.listOfRecordings:
                self.listOfStreams= self.ShowFileInnerSection(self.extractedFile['/Data/'+recording+'/AnalogStream/'])
                for stream in self.listOfStreams:
                    self.timeStepMS= (self.extractedFile['/Data/' + recording + '/AnalogStream/' + stream + '/InfoChannel'][0])[tickPosition]*1e-3
                    self.durationMS = (self.extractedFile['/Data/' + recording + '/AnalogStream/' + stream + '/ChannelDataTimeStamps'][0,2])* self.timeStepMS
                    self.GetRelevantTimestamps()
                    self. nChannels = len(np.array((self.extractedFile['/Data/' + recording + '/AnalogStream/' + stream + '/ChannelData'])[:, 0]))
                    self.GetRelevantChannels()
                    if (( self.startTimeIndex!=None) and ( self.endTimeIndex!=None) and ( self.startChannel!=None) and ( self.endChannel!=None) and ( self.timestamps[0]!=None)):
                        self.metaData = np.array(
                            (self.extractedFile['/Data/' + recording + '/AnalogStream/' + stream + '/ChannelData'])[ self.startChannel-1: self.endChannel,  self.startTimeIndex: self.endTimeIndex])
                        self.metaData=self.metaData.transpose()
                        self.PlotData()
                    else:
                        print("Error Loading Data, Please Try Again")
        except Exception as e:
            print("An exception occurred. Please Try Again")
            print(e)
            return
