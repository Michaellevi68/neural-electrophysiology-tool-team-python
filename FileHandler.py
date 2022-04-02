import os
import MCH5Interface
import NWBInterface
import OERecordingsInterface

def GetFilePath():
    print(
        "\nThis application supports the following types:\n-\t.nwb\n-\t.h5\n-\t.OE Folder Path\n\nPlease insert a file path here:")
    inputFile = input()
    inputFile = inputFile.replace('"', '').replace("\\", "//")
    return inputFile

def FileHandler(isGui, inputFile):
    try:
        fileType = os.path.splitext(inputFile)[1].lower()
        if fileType == '.nwb':
            NWBFile=NWBInterface.HandelNWBFile(inputFile,isGui)
            NWBFile.GetData()
            return NWBFile
        elif fileType == '.h5':
            MCH5File=MCH5Interface.HandelMCH5File(inputFile,isGui)
            MCH5File.GetData()
            return MCH5File
        else:
            OEFile=OERecordingsInterface.HandelOEFile(inputFile,isGui)
            OEFile.GetData()
            return OEFile
    except Exception as e:
        print("An exception occurred. Please Try Again")
        print(e)
        return