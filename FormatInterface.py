import numpy as np
import matplotlib.pyplot as plt

class FileFormat:
    def __init__(self):
       self.inputFile =""
       self.durationMS=0
       self.timeStepMS=0
       self.windowTime=0
       self.startTime=0
       self.endTime=0
       self.startTimeIndex=0
       self.endTimeIndex=0
       self.relativeStartChannelIndex=0
       self.relativeEndChannelIndex=0
       self.timestamps=[]
       self.nChannels=0
       self.startChannel=0
       self.endChannel=0
       self.relativeStartChannelIndex=0
       self.relativeEndChannelIndex=0
       self.metaData=[]


    def GetFilePath (self):
        print("\nThis application supports the following types:\n-\t.nwb\n-\t.h5\n-\t.OE Folder Path\n\nPlease insert a file path here:")
        inputFile = input()
        inputFile= inputFile.replace('"','').replace("\\","//")
        return inputFile


    def PlotData(metaData,userPreferences):
        nSelectedChannels= userPreferences['endChannel']-userPreferences['startChannel']+1
        colors = plt.rcParams["axes.prop_cycle"]()
        fig, graph = plt.subplots(nSelectedChannels,1, sharex=True)
        graphIndex = 0
        if nSelectedChannels>1:
            for channel in range(userPreferences['relativeStartChannelIndex'],userPreferences['relativeEndChannelIndex']+1):
                selectedData=metaData[(userPreferences['relativeStartTimeIndex']):(userPreferences['relativeEndTimeIndex']), channel]
                color = next(colors)["color"]
                graph[graphIndex].plot( userPreferences['timestamps'][userPreferences['relativeStartTimeIndex']:userPreferences['relativeEndTimeIndex']],selectedData,color=color)
                graph[graphIndex].set_ylabel(('CH %s'% (userPreferences['startChannel']+channel)),fontsize=8.0,rotation= 90)# Y label
                graph[graphIndex].tick_params(axis='y', which='major', labelsize=6.0)
                minY=int(min(selectedData))
                maxY=int(max(selectedData))
                graph[graphIndex].set_yticks((minY,maxY, ((minY+maxY)/2)))
                graphIndex=graphIndex+1
        else:
            selectedData = metaData[(userPreferences['relativeStartTimeIndex']):(userPreferences['relativeEndTimeIndex']), userPreferences['relativeStartChannelIndex']]
            graph.plot( userPreferences['timestamps'][userPreferences['relativeStartTimeIndex']:userPreferences['relativeEndTimeIndex']],selectedData)
            graph.set_ylabel(('CH %s' % (userPreferences['startChannel'] )), fontsize=6.0, rotation=90)  # Y label
        plt.subplots_adjust(wspace=0, hspace=0)
        fig.supylabel("V[uV]")
        fig.supxlabel("T[ms]")
        fig.align_ylabels()
        plt.show()



    def GetUserPreferences(timestamps,numOfChannels):
        userPref={}
        if len (timestamps)>1:
            timeStep= timestamps[1]-timestamps[0]
            print(timeStep)
        else:
            timeStep=0
        normalizedTimestampsMs = (timestamps - timestamps[0]) * 1e3
        userPref['normalizedTimestampsMs'] =normalizedTimestampsMs
        userPref['timeStep'] =timeStep
        print("Please Choose Window Time in Milliseconds:")
        userPref['windowTime'] = float(input())
        print("Please Choose Start Time in Milliseconds 0 out of",(normalizedTimestampsMs[len(normalizedTimestampsMs)-1]),':')
        userPref['startTime']= float(input())
        print("Channel Range Selection:")
        print("Please Choose Start Channel Index to Display out of ",numOfChannels,':')
        startChannel= int(input())
        print("Please Choose End Channel Index (greater thank start channel) to Display out of ", numOfChannels,':')
        endChannel = int(input())
        while (startChannel > endChannel)|(startChannel < 0)|(endChannel > numOfChannels):
            print("Invalid Choice, You Can Do Better!")
            print("Please Choose Start Channel Index to Display out of ", numOfChannels,':')
            startChannel = int(input())
            print("Please Choose End Channel Index (greater than start channel) to Display out of ", numOfChannels,':')
            endChannel = int(input())
        userPref['startChannel'] = startChannel-1 # zero base
        userPref['endChannel'] = endChannel-1 # zero base
        userPref['startTimeIndex'] = int(np.where(normalizedTimestampsMs==min(normalizedTimestampsMs, key=lambda x: abs(x - userPref['startTime'])))[0])
        if (userPref['startTime'] + userPref['windowTime']) > normalizedTimestampsMs[len(normalizedTimestampsMs) - 1]:
            userPref['endTime'] = normalizedTimestampsMs[len(normalizedTimestampsMs)-1]
        else:
            userPref['endTime'] = (userPref['startTime'] + userPref['windowTime'])
        userPref['endTimeIndex'] = int(np.where(normalizedTimestampsMs == min(normalizedTimestampsMs, key=lambda x: abs(x - userPref['endTime'])))[0])+1
        return userPref

    def GetRelevantChannels (numOfChannels, userPref):
        print("Channel Range Selection:\nPlease Choose Start Channel Index to Display out of ",numOfChannels,':')
        startChannel= int(input())
        print("Please Choose End Channel Index (greater thank start channel) to Display out of ", numOfChannels,':')
        endChannel = int(input())
        while (startChannel > endChannel)|(startChannel < 1)|(endChannel > numOfChannels):
            print("Invalid Choice, You Can Do Better!")
            print("Please Choose Start Channel Index to Display out of ", numOfChannels,':')
            startChannel = int(input())
            print("Please Choose End Channel Index (greater than start channel) to Display out of ", numOfChannels,':')
            endChannel = int(input())
        userPref['startChannel'] = startChannel
        userPref['endChannel'] = endChannel
        userPref['relativeEndChannelIndex'] = userPref['endChannel'] - userPref['startChannel']
        userPref['relativeStartChannelIndex'] = 0
        return userPref

    def GetRelevantTimestamps (duration, timeStep, userPref):
        print("Please Choose Start Time in Milliseconds 0 out of",duration, ':')
        userPref['startTime'] = float(input())
        print("Please Choose Time Window in Milliseconds:")
        userPref['windowTime'] = float(input())
        if (userPref['startTime'] + userPref['windowTime']) > duration:
            userPref['windowTime'] = duration-userPref['startTime']
        userPref['startTimeIndex']= round((userPref['startTime'])/timeStep)
        userPref['endTimeIndex'] = round((userPref['startTime']+userPref['windowTime'])/timeStep)
        userPref['timestamps'] = np.linspace(userPref['startTimeIndex']*timeStep,userPref['endTimeIndex']*timeStep, userPref['endTimeIndex']-userPref['startTimeIndex'])
        userPref['relativeEndTimeIndex']=  userPref['endTimeIndex']- userPref['startTimeIndex']-1
        userPref['relativeStartTimeIndex']=0
        return userPref

