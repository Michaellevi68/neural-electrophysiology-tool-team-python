import h5py
import numpy as np
import CommonFunctions as CF


def HandelMCH5File(inputFile):
    tickPosition = 9
    extractedFile = h5py.File(inputFile,"r")
    listOfRecordings= CF.ShowFileInnerSection(extractedFile['/Data/'])
    for recording in listOfRecordings:
        listOfStreams= CF.ShowFileInnerSection(extractedFile['/Data/'+recording+'/AnalogStream/'])
        for stream in listOfStreams:
           #metaData = np.array((extractedFile['/Data/'+recording+'/AnalogStream/'+stream+'/ChannelData'])[0:252,0:100000])
           # metaData = np.array((extractedFile['/Data/' + recording + '/AnalogStream/' + stream + '/ChannelData']))
           #timestamps = np.array(np.linspace(0, len(metaData[0]) * timeStep, len(metaData[0])))
           # timeStep = (extractedFile['/Data/' + recording + '/AnalogStream/' + stream + '/InfoChannel'][0])[  tickPosition] * 1e-6
            userPreferences={}
            timeStepMS= (extractedFile['/Data/' + recording + '/AnalogStream/' + stream + '/InfoChannel'][0])[tickPosition]*1e-3
            durationMS = (extractedFile['/Data/' + recording + '/AnalogStream/' + stream + '/ChannelDataTimeStamps'][0,2])*timeStepMS
            userPreferences=CF.GetRelevantTimestamps(durationMS,timeStepMS,userPreferences)
            nChannels = len(np.array((extractedFile['/Data/' + recording + '/AnalogStream/' + stream + '/ChannelData'])[:, 0]))
            userPreferences=CF.GetRelevantChannels(nChannels,userPreferences)
            if ((userPreferences['startTimeIndex']!=None) and (userPreferences['endTimeIndex']!=None) and (userPreferences['startChannel']!=None) and (userPreferences['endChannel']!=None) and (userPreferences['timestamps'][0]!=None)):
                metaData = np.array(
                    (extractedFile['/Data/' + recording + '/AnalogStream/' + stream + '/ChannelData'])[userPreferences['startChannel']-1:userPreferences['endChannel'], userPreferences['startTimeIndex']:userPreferences['endTimeIndex']])
                CF.PlotData(metaData.transpose(), userPreferences)
            else: print("Error Loading Data, Please Try Again")