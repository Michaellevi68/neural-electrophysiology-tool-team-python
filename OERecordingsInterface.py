
import pyopenephys
import numpy as np
import CommonFunctions as CF

def HandelOEFile(inputFile):
    extractedFile = pyopenephys.File(inputFile)
    experiments=extractedFile.experiments
    for experiment in experiments:
        recordings =experiment.recordings
        for recording in recordings:
            #metaData = np.array((recording.analog_signals[0]).signal)
            #timestamps = np.array((recording.analog_signals[0]).times)
           # userPreferences = CF.GetUserPreferences(timestamps, len(metaData))
            userPreferences = {}
            durationMS = float((recording).duration)*1e3 # Scan all files and gets the total duration, therefore, needs to come first
            samplingRate=float(recording.sample_rate)
            timeStepMS = float(1/samplingRate)*1e3
            userPreferences = CF.GetRelevantTimestamps(durationMS, timeStepMS, userPreferences)
            nChannels =int (recording.nchan)
            userPreferences = CF.GetRelevantChannels(nChannels, userPreferences)
            if ((userPreferences['startTimeIndex'] != None) and (userPreferences['endTimeIndex'] != None) and (userPreferences['startChannel'] != None) and (userPreferences['endChannel'] != None) and (userPreferences['timestamps'][0] != None)):
                metaData = np.array(((recording.analog_signals[0]).signal)[userPreferences['startChannel'] - 1:userPreferences['endChannel'], userPreferences['startTimeIndex']:userPreferences['endTimeIndex']])
                CF.PlotData(metaData.transpose(), userPreferences)
            else:
                print("Error Loading Data, Please Try Again")



