from os import listdir
from os import walk
from os import mkdir
from Main import BigFunc
import shutil
import os
from OpenL2MScrape import login, Quit
mypath = "C:/Users/ripte/Documents/CutSheetCreator/Input"
outputpath = "C:/Users/ripte/Documents/CutSheetCreator/Output"
Completed =  "C:/Users/ripte/Documents/CutSheetCreator/Completed"
Local = "C:/Users/ripte/Documents/CutSheetCreator"
def GetInputFiles():

    filenames = next(walk(mypath), (None, None, []))[2]  # [] if no file
    print("Found Files:")
    print(filenames)
    return filenames


Files = GetInputFiles()
print("Logging Into OpenL2MScrape")
login()
for File in Files:
    Filepath =  mypath + "/" + File
    shutil.move(Filepath,Local +"/" + File )#Move file from input folder to main dir for processing
    #Completed = Completed + "/" + File
    Filename = File[0:-4]
    BigFunc(File)
    shutil.move(Local +"/" + File,Completed)#Move the Local File to Completed
    # Create a folder for each device
    path = os.path.join(outputpath + "/", Filename)
    os.mkdir(path)


    output = outputpath + "/" + Filename

    BigFuncCommandOut = Local + "/" + "OutputCommands_" + Filename + ".txt"
    CommandsOUtput = output + "/" + "OutputCommands_" + Filename + ".txt"
    shutil.move(BigFuncCommandOut,CommandsOUtput) # move output cmmands to output


    OutPutActive = Local  + "/" + "OutputActive_" + Filename + ".txt"
    OutPutActivecsv = Local  + "/" + "OutputActive_" + Filename + ".csv"
    OutputActiveOut = output + "/" + "OutputActive_" + Filename + ".txt"
    OutputActiveOutcsv = output + "/" + "OutputActive_" + Filename + ".csv"
    shutil.move(OutPutActive,OutputActiveOut)# Move output Table to Output
    shutil.move(OutPutActivecsv,OutputActiveOutcsv)# Move output csv to Output

    OutputInactive = Local  + "/" + "Deactivated_" + Filename + ".txt"
    OutputInactivecsv = Local  + "/" + "Deactivated_" + Filename + ".csv"
    OutputInactiveOut = output + "/" + "Deactivated_" + Filename + ".txt"
    OutputInactiveOutcsv = output + "/" + "Deactivated_" + Filename + ".csv"
    shutil.move(OutputInactive,OutputInactiveOut)# Move output Table to Output for the inactive Sheets
    shutil.move(OutputInactivecsv,OutputInactiveOutcsv)# Move output csv to Output for the inactive sheets
    print(Completed)



Quit()
