import h5py
import numpy as np
import CommonFunctions as CF




def HandelNWBFile(inputFile):
    extractedFile = h5py.File(inputFile,"r")
    listOfRecordings = CF.ShowFileInnerSection(extractedFile['/acquisition/timeseries/'])
    for recording in listOfRecordings:
        listOfProcessors = CF.ShowFileInnerSection(extractedFile['/acquisition/timeseries/'+recording+'/continuous/'])
        for processor in listOfProcessors:
            startTimestamps = np.array(extractedFile['/acquisition/timeseries/' + recording + '/continuous/' + processor + '/timestamps'][0])
            secondTimestamps = np.array(extractedFile['/acquisition/timeseries/' + recording + '/continuous/' + processor + '/timestamps'][1])
            timeStepMS=  (secondTimestamps-startTimestamps)*1e3
            durationMS=(extractedFile['/acquisition/timeseries/' + recording + '/continuous/' + processor + '/timestamps']).shape[0]*timeStepMS
            userPreferences = {}
            userPreferences = CF.GetRelevantTimestamps(durationMS, timeStepMS, userPreferences)
            nChannels = extractedFile['/acquisition/timeseries/'+recording+'/continuous/'+processor+'/data'].shape[1]
            userPreferences = CF.GetRelevantChannels(nChannels, userPreferences)
            if ((userPreferences['startTimeIndex'] != None) and (userPreferences['endTimeIndex'] != None) and ( userPreferences['startChannel'] != None) and (userPreferences['endChannel'] != None) and ( userPreferences['timestamps'][0] != None)):
                metaData = np.array((extractedFile['/acquisition/timeseries/'+recording+'/continuous/'+processor+'/data'][userPreferences['startTimeIndex']:userPreferences['endTimeIndex'],userPreferences['startChannel'] - 1:userPreferences['endChannel']]))
                CF.PlotData(metaData, userPreferences)
                return
            else:
                print("Error Loading Data, Please Try Again")

