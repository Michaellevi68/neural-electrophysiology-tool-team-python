import MCH5Interface
import NWBInterface
import OERecordingsInterface


def FileHandler(fileType, inputFile):
    if fileType == '.nwb':
        NWBInterface.HandelNWBFile(inputFile)
        return
    elif fileType == '.h5':
        MCH5Interface.HandelMCH5File(inputFile)
        return
    else:
        OERecordingsInterface.HandelOEFile(inputFile)
        return

