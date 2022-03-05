import h5py
import numpy as np
import FormatInterface

class HandelNWBFile:
    def __init__(self,inputFile):
       self.inputFile=inputFile
       self.listOfRecordings=[]
       self.listOfProcessors=[]
       self.allData = []

    def GetData(self):
        try:
            extractedFile = h5py.File(self.inputFile,"r")
            self.listOfRecordings = FormatInterface.ShowFileInnerSection(extractedFile['/acquisition/timeseries/'])
            for recording in self.listOfRecordings:
                self. listOfProcessors = FormatInterface.ShowFileInnerSection(extractedFile['/acquisition/timeseries/'+recording+'/continuous/'])
                for processor in self.listOfProcessors:
                    currentData = FormatInterface.FormatInterface()
                    startTimestamps = np.array(extractedFile['/acquisition/timeseries/' + recording + '/continuous/' + processor + '/timestamps'][0])
                    secondTimestamps = np.array(extractedFile['/acquisition/timeseries/' + recording + '/continuous/' + processor + '/timestamps'][1])
                    currentData.timeStepMS=  (secondTimestamps-startTimestamps)*1e3
                    currentData.durationMS=(extractedFile['/acquisition/timeseries/' + recording + '/continuous/' + processor + '/timestamps']).shape[0]*currentData.timeStepMS
                    currentData.GetRelevantTimestamps()
                    currentData.nChannels = extractedFile['/acquisition/timeseries/'+recording+'/continuous/'+processor+'/data'].shape[1]
                    currentData.GetRelevantChannels()
                    if ((currentData.startTimeIndex != None) and (currentData.endTimeIndex != None) and ( currentData.startChannel != None) and (currentData.endChannel != None) and ( currentData.timestamps[0] != None)):
                        currentData.metaData = np.array((extractedFile['/acquisition/timeseries/'+recording+'/continuous/'+processor+'/data'][currentData.startTimeIndex:currentData.endTimeIndex,currentData.startChannel - 1:currentData.endChannel]))
                        currentData.PlotData()
                        self.allData.append(currentData)
                    else:
                        print("Error Loading Data, Please Try Again")
        except Exception as e:
            print("An exception occurred. Please Try Again")
            print(e)
            return