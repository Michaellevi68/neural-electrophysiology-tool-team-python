import h5py
import numpy as np
import FormatInterface

class HandelNWBFile(FormatInterface.FormatInterface):
    def __init__(self,inputFile):
        super().__init__()
        self.inputFile = inputFile
        self.listOfRecordings = []
        self.listOfProcessors = []
        self.extractedFile = []

    def GetData(self):
        try:
            self.extractedFile = h5py.File(self.inputFile,"r")
            self.listOfRecordings = self.ShowFileInnerSection(self.extractedFile['/acquisition/timeseries/'])
            for recording in self.listOfRecordings:
                self. listOfProcessors = self.ShowFileInnerSection(self.extractedFile['/acquisition/timeseries/'+recording+'/continuous/'])
                for processor in self.listOfProcessors:
                    startTimestamps = np.array(self.extractedFile['/acquisition/timeseries/' + recording + '/continuous/' + processor + '/timestamps'][0])
                    secondTimestamps = np.array(self.extractedFile['/acquisition/timeseries/' + recording + '/continuous/' + processor + '/timestamps'][1])
                    self.timeStepMS=  (secondTimestamps-startTimestamps)*1e3
                    self.durationMS=(self.extractedFile['/acquisition/timeseries/' + recording + '/continuous/' + processor + '/timestamps']).shape[0]*self.timeStepMS
                    self.GetRelevantTimestamps()
                    self.nChannels = self.extractedFile['/acquisition/timeseries/'+recording+'/continuous/'+processor+'/data'].shape[1]
                    self.GetRelevantChannels()
                    if ((self.startTimeIndex != None) and (self.endTimeIndex != None) and ( self.startChannel != None) and (self.endChannel != None) and ( self.timestamps[0] != None)):
                        self.metaData = np.array((self.extractedFile['/acquisition/timeseries/'+recording+'/continuous/'+processor+'/data'][self.startTimeIndex:self.endTimeIndex,self.startChannel - 1:self.endChannel]))
                        self.PlotData()
                        #self.allData.append(currentData)
                    else:
                        print("Error Loading Data, Please Try Again")
        except Exception as e:
            print("An exception occurred. Please Try Again")
            print(e)
            return