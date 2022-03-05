import numpy as np
import matplotlib.pyplot as plt

class FormatInterface:
    def __init__(self):
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

    def PlotData(self):
        try:
            nSelectedChannels= self.endChannel-self.startChannel+1
            colors = plt.rcParams["axes.prop_cycle"]()
            fig, graph = plt.subplots(nSelectedChannels,1, sharex=True)
            graphIndex = 0
            if nSelectedChannels>1:
                for channel in range(self.relativeStartChannelIndex,self.relativeEndChannelIndex+1):
                    selectedData=self.metaData[(self.relativeStartTimeIndex):(self.relativeEndTimeIndex), channel]
                    color = next(colors)["color"]
                    graph[graphIndex].plot( self.timestamps[self.relativeStartTimeIndex:self.relativeEndTimeIndex],selectedData,color=color)
                    graph[graphIndex].set_ylabel(('CH %s'% (self.startChannel+channel)),fontsize=8.0,rotation= 90)# Y label
                    graph[graphIndex].tick_params(axis='y', which='major', labelsize=6.0)
                    minY=int(min(selectedData))
                    maxY=int(max(selectedData))
                    graph[graphIndex].set_yticks((minY,maxY, ((minY+maxY)/2)))
                    graphIndex=graphIndex+1
            else:
                selectedData = self.metaData[(self.relativeStartTimeIndex):(self.relativeEndTimeIndex), self.relativeStartChannelIndex]
                graph.plot( self.timestamps[self.relativeStartTimeIndex:self.relativeEndTimeIndex],selectedData)
                graph.set_ylabel(('CH %s' % (self.startChannel )), fontsize=6.0, rotation=90)  # Y label
            plt.subplots_adjust(wspace=0, hspace=0)
            fig.supylabel("V[uV]")
            fig.supxlabel("T[ms]")
            fig.align_ylabels()
            plt.show()
        except Exception as e:
            print("An exception occurred. Please Try Again")
            print(e)
            return

    def GetRelevantChannels (self):
        print("Channel Range Selection:\nPlease Choose Start Channel Index to Display out of ",self.nChannels,':')
        startChannel= int(input())
        print("Please Choose End Channel Index (greater thank start channel) to Display out of ", self.nChannels,':')
        endChannel = int(input())
        while (startChannel > endChannel)|(startChannel < 1)|(endChannel > self.nChannels):
            print("Invalid Choice, You Can Do Better!")
            print("Please Choose Start Channel Index to Display out of ", self.nChannels,':')
            startChannel = int(input())
            print("Please Choose End Channel Index (greater than start channel) to Display out of ", self.nChannels,':')
            endChannel = int(input())
        self.startChannel = startChannel
        self.endChannel = endChannel
        self.relativeEndChannelIndex =self.endChannel -self.startChannel
        self.relativeStartChannelIndex = 0


    def GetRelevantTimestamps (self):
        print("Please Choose Start Time in Milliseconds 0 out of",self.durationMS, ':')
        self.startTime = float(input())
        print("Please Choose Time Window in Milliseconds:")
        self.windowTime= float(input())
        if (self.startTime + self.windowTime) > self.durationMS:
            self.windowTime =  self.durationMS-self.startTime
        self.startTimeIndex= round((self.startTime/self.timeStepMS))
        self.endTimeIndex = round((self.startTime+self.windowTime)/self.timeStepMS)
        self.timestamps = np.linspace(self.startTimeIndex*self.timeStepMS,self.endTimeIndex*self.timeStepMS, self.endTimeIndex-self.startTimeIndex)
        self.relativeEndTimeIndex=  self.endTimeIndex- self.startTimeIndex-1
        self.relativeStartTimeIndex=0

    def ShowFileInnerSection(self,fileSec):
        try:
            innerSectionList = []
            for i in fileSec:
                innerSectionList.append(i)
            return innerSectionList
        except Exception as e:
            print("An exception occurred. Please Try Again")
            print(e)
            return