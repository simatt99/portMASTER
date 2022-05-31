import csv
from tabulate import tabulate
from datetime import datetime
import sys


CutoffDate = datetime.strptime("2019-06-17", "%Y-%m-%d")

def ReadSheet(File):
    with open(File, newline='') as f:
        reader = csv.reader(f)
        return list(reader)

def GetActiveInterfaces(ImportSheet):
    ActiveInts = []

    for Interface in ImportSheet:
        if Interface[5] == "":
            Interface[5] = "2019-06-16 12:00" #if there is no time, assume it is older than Cutoff

        try:
        #    print(Interface[5])
            TimeValue = datetime.strptime(Interface[5],"%Y-%m-%d %H:%M")
        except ValueError:
            TimeValue = datetime.strptime(Interface[5],"%m/%d/%Y %H:%M" )

        if Interface[0] != "":
            #print(Interface)
            if Interface[4] =='up': # If Port is currently up Append it to list
                ActiveInts.append(Interface)
            elif Interface[4] == 'down' and TimeValue >= CutoffDate:
                ActiveInts.append(Interface)
    return ActiveInts


def UpdateVlans(Interfaces,Vlans):
    for Interface in Interfaces:
        VlanNum = GetVlan(Interface[7],Vlans)
    #    print(VlanNum)
        Interface.append(VlanNum)

    return Interfaces

def GetVlan(Text,Vlans):
    for Vlan in Vlans:
        #print(Text)
        #print(Vlan[0])
        if Text.replace("-","_") == Vlan[0].replace("-","_"):
            #print("Vlans are Equal")
            return Vlan[1]



def ImportVlans():
    Vlans = ReadSheet("Vlans.csv")
    print(tabulate(Vlans, headers=["Vlan Name","Vlan Number" ], tablefmt="pretty"))
    return Vlans

def ExportFile(Sides,Filename):
    name = "OutputActive_" + Filename + ".txt"
    with open(name,'w') as f:
        f.write(tabulate(Sides[0], headers=["Device","Interface ID","Speed","Status","State","Last Change","Desc","Vlan Name","Vlan ID","New Port" ], tablefmt="pretty"))
        f.write(tabulate(Sides[1], headers=["Device","Interface ID","Speed","Status","State","Last Change","Desc","Vlan Name","Vlan ID","New Port" ], tablefmt="pretty"))

def Organize(Interfaces):
    RightInterfaces = []
    LeftInterfaces = []
    for Interface in Interfaces:

        if Interface[1][0:2] == "Gi":
        #    print(int(Interface[1][4:]))
            if int(Interface[1][4:]) > 24:
            #    print("Interface is on the right")
            #    print(Interface)
                RightInterfaces.append(Interface)
            else:
                LeftInterfaces.append(Interface)
#    print("Right Side Interfaces")
#    print(tabulate(RightInterfaces, headers=["Device","Interface ID","Speed","Status","State","Last Change","Desc","Vlan Name","Vlan ID" ], tablefmt="pretty"))
#    print("Left  Side Interfaces")
#    print(tabulate(LeftInterfaces, headers=["Device","Interface ID","Speed","Status","State","Last Change","Desc","Vlan Name","Vlan ID" ], tablefmt="pretty"))

    Sides = [RightInterfaces, LeftInterfaces]
    return Sides
def GetNewPort(Sides):
    RightInterfaces = Sides[0]
    LeftInterfaces = Sides[1]
    i = 24
    d = 1
    for Interface in RightInterfaces:
        i += 1
        Interface.append(str(d) +"/0/" + str(i))
        if i == 48:
            i = 24
            d += 1
    i = 0
    d = 1
    for Interface in LeftInterfaces:
        i += 1
        Interface.append(str(d) +"/0/" + str(i))
        if i == 24:
            i = 0
            d += 1


    return [RightInterfaces,LeftInterfaces]



def OutputCommands(Sides,Filename):
    RightInterfaces = Sides[0]
    LeftInterfaces = Sides[1]
    name = "OutputCommands_" + Filename + ".txt"
    out = open(name,'w')
    i = 24
    d = 1
    for Interface in RightInterfaces:
        i += 1
        if Interface[8] == None:
            Interface[8] = "1"
        out.write( "int gi "+ str(d) +"/0/" + str(i) + "\n")
        out.write( "port trunk permit vlan " + Interface[8]+ "\n")
        out.write( "port trunk pvid vlan " + Interface[8]+ "\n")
        out.write( "desc " + Interface[6]+ "\n")
        if i == 48:
            i = 24
            d += 1
    devices = d
    i = 0
    d = 1
    for Interface in LeftInterfaces:
        i += 1
        if Interface[8] == None:
            Interface[8] = "1"
        out.write( "int gi "+ str(d) +"/0/" + str(i) + "\n")
        out.write( "port trunk permit vlan " + Interface[8]+ "\n")
        out.write( "port trunk pvid vlan " + Interface[8]+ "\n")
        out.write( "desc " + Interface[6]+ "\n")
        if i == 24:
            i = 0
            d += 1

    if d > devices:
        return d
    return devices

# Main Section Here
def BigFunc(File):

    Filename = File[0:-4]

    print(Filename)
    #File = "Aus-310-vfsw_Source.csv"
    ImportSheet = ReadSheet(File)
    #print(ImportSheet)
    header =  ImportSheet[0]
    del ImportSheet[0] # Remove the header of the sheet

    ActiveInts = GetActiveInterfaces(ImportSheet)
    Vlans = ImportVlans()
    Interfaces = UpdateVlans(ActiveInts,Vlans)
    #print(tabulate(Interfaces, headers=["Device","Interface ID","Speed","Status","State","Last Change","Desc","Vlan Name","Vlan ID" ], tablefmt="pretty"))

    Sides = Organize(Interfaces)
    Sides = GetNewPort(Sides)
    print("Right Side Interfaces")
    ExportFile(Sides,Filename)
    print(tabulate(Sides[0], headers=["Device","Interface ID","Speed","Status","State","Last Change","Desc","Vlan Name","Vlan ID","New Port" ], tablefmt="pretty"))
    print("Left Side Interfaces")
    print(tabulate(Sides[1], headers=["Device","Interface ID","Speed","Status","State","Last Change","Desc","Vlan Name","Vlan ID", "New Port" ], tablefmt="pretty"))
    Devices = OutputCommands(Sides,Filename)

    print("Num of HPE Switches Needed: " + str(Devices))
