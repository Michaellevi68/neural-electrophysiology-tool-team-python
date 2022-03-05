import h5py
import numpy as np
import FormatInterface

class HandelMCH5File:
    def __init__(self,inputFile):
       self.inputFile=inputFile
       self.listOfRecordings=[]
       self.listOfStreams=[]
       self.allData = []

    def GetData(self):
        try:
            tickPosition = 9
            extractedFile = h5py.File(self.inputFile,"r")
            self.listOfRecordings= FormatInterface.ShowFileInnerSection(extractedFile['/Data/'])
            for recording in self.listOfRecordings:
                self.listOfStreams= FormatInterface.ShowFileInnerSection(extractedFile['/Data/'+recording+'/AnalogStream/'])
                for stream in self.listOfStreams:
                    currentData= FormatInterface.FormatInterface()
                    currentData.timeStepMS= (extractedFile['/Data/' + recording + '/AnalogStream/' + stream + '/InfoChannel'][0])[tickPosition]*1e-3
                    currentData.durationMS = (extractedFile['/Data/' + recording + '/AnalogStream/' + stream + '/ChannelDataTimeStamps'][0,2])* currentData.timeStepMS
                    currentData.GetRelevantTimestamps()
                    currentData. nChannels = len(np.array((extractedFile['/Data/' + recording + '/AnalogStream/' + stream + '/ChannelData'])[:, 0]))
                    currentData.GetRelevantChannels()
                    if (( currentData.startTimeIndex!=None) and ( currentData.endTimeIndex!=None) and ( currentData.startChannel!=None) and ( currentData.endChannel!=None) and ( currentData.timestamps[0]!=None)):
                        currentData.metaData = np.array(
                            (extractedFile['/Data/' + recording + '/AnalogStream/' + stream + '/ChannelData'])[ currentData.startChannel-1: currentData.endChannel,  currentData.startTimeIndex: currentData.endTimeIndex])
                        currentData.metaData=currentData.metaData.transpose()
                        currentData.PlotData()
                        self.allData.append(currentData)
                    else:
                        print("Error Loading Data, Please Try Again")
        except Exception as e:
            print("An exception occurred. Please Try Again")
            print(e)
            return
