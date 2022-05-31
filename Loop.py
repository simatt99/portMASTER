from os import listdir
from os import walk
from Main import BigFunc
import shutil
mypath = "C:/Users/hopki/Documents/ENGR 103/FinalProject/FinalApp/Input"
output = "C:/Users/hopki/Documents/ENGR 103/FinalProject/FinalApp/Output"
Completed =  "C:/Users/hopki/Documents/ENGR 103/FinalProject/FinalApp/Completed"
Local = "C:/Users/hopki/Documents/ENGR 103/FinalProject/FinalApp"
def GetInputFiles():

    filenames = next(walk(mypath), (None, None, []))[2]  # [] if no file
    print("Found Files:")
    print(filenames)
    return filenames


Files = GetInputFiles()
for File in Files:
    Filepath =  mypath + "/" + File
    shutil.move(Filepath,Local +"/" + File )#Move file from input folder to main dir for processing
    #Completed = Completed + "/" + File
    Filename = File[0:-4]
    BigFunc(File)
    BigFuncCommandOut = Local + "/" + "OutputCommands_" + Filename + ".txt"
    CommandsOUtput = output + "/Commands/" + "OutputCommands_" + Filename + ".txt"
    OutPutActive = Local  + "/" + "OutputActive_" + Filename + ".csv"
    OutputActiveOut = output + "/" + "OutputActive_" + Filename + ".csv"
    print(Completed)
    shutil.move(Local +"/" + File,Completed)#Move the Local File to Completed
    shutil.move(BigFuncCommandOut,CommandsOUtput) # move output cmmands to output
    shutil.move(OutPutActive,OutputActiveOut)# Move outpupt Table to Output
