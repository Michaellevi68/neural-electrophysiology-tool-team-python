# This application was developed by Michael Levi and Eyal Brand
#


import os
import CommonFunctions as CF
import FileHandler


userSelection=1
while (userSelection!=0):
    inputFile= CF.GetFilePath()
    fileType = os.path.splitext(inputFile)[1].lower()
    FileHandler.FileHandler(fileType,inputFile)
    print("\n\nTo Exit Please Press 0 or Press 1 To Continue")
    userSelection=int(input())


