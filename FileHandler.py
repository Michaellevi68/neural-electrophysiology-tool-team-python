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

def FileHandler():
    try:
        inputFile= GetFilePath()
        fileType = os.path.splitext(inputFile)[1].lower()
        if fileType == '.nwb':
            NWBFile= NWBInterface.HandelNWBFile(inputFile)
            NWBFile.GetData()
            return
        elif fileType == '.h5':
            MCH5File= MCH5Interface.HandelMCH5File(inputFile)
            MCH5File.GetData()
            return
        else:
            OEFile=OERecordingsInterface.HandelOEFile(inputFile)
            OEFile.GetData()
            return
    except Exception as e:
        print("An exception occurred. Please Try Again")
        print(e)
        return