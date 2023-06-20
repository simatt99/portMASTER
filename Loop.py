from os import listdir
from os import walk
from os import mkdir
from Main import BigFunc
import shutil
import os
import argparse
from OpenL2MScrape import login, Quit
import time
import PySimpleGUI as sg  
import pathlib


cwd = pathlib.Path().resolve()

mypath = "/Users/matt/Desktop/CutSheetCreator/Input"
outputpath = "/Users/matt/Desktop/CutSheetCreator/Output"
Completed =  "/Users/matt/Desktop/CutSheetCreator/Completed"
Local = "/Users/matt/Desktop/CutSheetCreator"

# parser = argparse.ArgumentParser(
#     description='Take AKIPS Information and use it to generate Cutsheets')

# parser.add_argument('--username', '-u',
#                     help='Username for OpenL2M (ONID EX: Hopkinsr)', nargs=1, required=True)
# parser.add_argument('--password', '-p',
#                     help='Username for OpenL2M (ONID Password)', nargs=1, required=True)

# parser.add_argument('--mode', '-m',
#                     help='[UNFINISHED WIP] Port Organizational Mode, Options: Managed, Unmanaged, Managed attempts to organizes interfaces and Patch Panel Cables through reordering Jack numbers then paring with interface (For full rewires) [ Defaults: Unmanaged]', nargs=1, default="Unmanaged")

# args = parser.parse_args()

# print(parser.parse_args())
# Get the Username
layout = [  [sg.Text("Username:")],
            [sg.Input()],
            [sg.Text("Password:")],
            [sg.Input()],
            [sg.Button('Ok')] ]

window = sg.Window('Cutsheet Creator V1.0', layout)
event, values = window.read() 
window.close()
# print(args.username[0])
# print(args.password[0])

def GetInputFiles():

    filenames = next(walk(mypath), (None, None, []))[2]  # [] if no file
    print("Found Files:")
    print(filenames)
    return filenames

# Get all Input Files From Input Directory
Files = GetInputFiles()
# Start the Selinum Instance 
print("Logging Into OpenL2MScrape")
# Log the user into OpenL2m 
login(values[0], values[1])
for File in Files:
    print(File)
    
    if File[-4:] == ".csv":
        print(f"Starting to Process File: {File}")
        

        Filepath =  mypath + "/" + File
        shutil.move(Filepath,Local +"/" + File )#Move file from input folder to main dir for processing
        #Completed = Completed + "/" + File
        print("File Moved to Processing Directory...")

        
        Filename = File[0:-4]

        print("Running File: " + Filename)

        NewFilename = BigFunc(File) # Get the filename from the Akips File Hostname

        # Make Output Directory
        path = os.path.join(outputpath + "/", NewFilename)

        # Try to make a Directory
        try:
            os.mkdir(path)
        except FileExistsError:
            print("Output Directory already exists, continuing...")


        NewFileNameNoExt = NewFilename[0:-4]

        output = outputpath + "/" + NewFilename
        # Copy The input File into the completed output
        shutil.copy(Local + "/" + File, outputpath + "/" + NewFilename + "/INPUT_" + NewFilename + ".csv")
        # Rename the Input file to have the proper name

        os.rename(Local + "/" + File, Local + "/" + NewFilename + ".csv")

        #File was renamed so we use the new file name 
        # Move the Local File to Completed
        shutil.move(Local + "/" + NewFilename + ".csv", Completed)

        #Create a folder for each device
        print("Output Directory created")

        BigFuncCommandOut = Local + "/" + "OutputCommands_" + NewFilename + ".txt"
        CommandsOUtput = output + "/" + "OutputCommands_" + NewFilename + ".txt"
        shutil.move(BigFuncCommandOut,CommandsOUtput) # move output cmmands to output

        BigFuncCommandOut = Local + "/" + "Port_Patch_" + NewFilename + ".csv"
        CommandsOUtput = output + "/" + "Port_Patch_" + NewFilename + ".csv"
        shutil.move(BigFuncCommandOut,CommandsOUtput) # move port patch to output

        BackupCommandsLocal = Local + "/" + "Backup_" + NewFilename + ".csv"
        BackupCommandsCompleted = output + "/" + "Backup_" + NewFilename + ".csv"
        # move backup patch to output
        shutil.move(BackupCommandsLocal, BackupCommandsCompleted)


        OutPutActive = Local + "/" + "OutputActive_" + NewFilename + ".txt"
        OutPutActivecsv = Local + "/" + "OutputActive_" + NewFilename + ".csv"
        OutputActiveOut = output + "/" + "OutputActive_" + NewFilename + ".txt"
        OutputActiveOutcsv = output + "/" + "OutputActive_" + NewFilename + ".csv"
        # Move output Table to Output
        shutil.move(OutPutActive, OutputActiveOut)
        shutil.move(OutPutActivecsv,OutputActiveOutcsv)# Move output csv to Output

        OutputInactive = Local + "/" + "Deactivated_" + NewFilename + ".txt"
        OutputInactivecsv = Local + "/" + "Deactivated_" + NewFilename + ".csv"
        OutputInactiveOut = output + "/" + "Deactivated_" + NewFilename + ".txt"
        OutputInactiveOutcsv = output + "/" + "Deactivated_" + NewFilename + ".csv"
        shutil.move(OutputInactive,OutputInactiveOut)# Move output Table to Output for the inactive Sheets
        shutil.move(OutputInactivecsv,OutputInactiveOutcsv)# Move output csv to Output for the inactive sheets
        print("Output Files Moved to Output Directory...")
        print(Completed)




Quit()
