# Cut Sheet Creator


### Introduction
**What is cut Sheet Creator?**
Cut Sheet Creator is a powerful script that is designed to take AKIPS reports
from existing network infrastructure hardware (Network Switches),and output the
commands that would be required to configure new switches based off the HPE
platform. In this process there is also an integrated system that removes all
unused ports and converts the Text Based Vlans from the AKIPS report into
numerical code based off a master Vlan List.

**How it works**
Cut Sheet Creator is designed to be efficient and deployable as a cron job.
With that in mind all the user is required to do is drop the AKIPS report(s) they
want to process into the Input Folder, and run `python loop.py` from the main
directory, and within minutes will be presented with Not only a terminal output
of the updated ports and Vlans, but also get a text file with the table for each switch,
and also a separate text file in the commands folder of output that contains the
commands that you can cut and paste onto a HPE switch during configuration.


### Usage:
1. **Download From GitHub** - Using `git Clone https://github.com/Hopalonger/CutSheetCreator.git`
2. **Install Dependencies** - This tool requires a few Dependencies to operate
these can be installed by running these commands `pip install tabulate`
3. **Importing Reports** - This system is designed to Use specific AKIPS reports,
the report that we are going to use is going to to be gotten from using the
unused interfaces menu and selecting a device, then selecting download as a csv.
Once this file has been downloaded I recommend renaming it as the device name
 just to keep track of it. Then move the file into the Input folder of the Program
4. ** Running the Program** - to run the program it is very straight forward,
all it takes is running `python loop.py` and it will find all of the files and
process them into the reports
5.** Understanding output** - Understanding the output of the program can be a
bit much, it was designed to be as simple as possible, but still can be alot
The termal and main ouput file will display a table that looks like this:
`+--------------+--------------+------------+--------+-------+------------------+-------------+-------------------+---------+----------+
|    Device    | Interface ID |   Speed    | Status | State |   Last Change    |    Desc     |     Vlan Name     | Vlan ID | New Port |
+--------------+--------------+------------+--------+-------+------------------+-------------+-------------------+---------+----------+
| Aus-310-vfsw |    Gi2/25    | 100000000  |  used  |  up   | 2020-11-23 12:26 |    D.31     |   Voice-Over-IP   |   503   |  1/0/25  |
| Aus-310-vfsw |    Gi2/26    | 100000000  |  used  |  up   | 2020-11-23 12:27 |    D.27     |   Voice-Over-IP   |   503   |  1/0/26  |
| Aus-310-vfsw |    Gi2/27    | 1000000000 |  free  | down  | 2022-01-04 15:01 |    D.77     |                   |    1    |  1/0/27  |
| Aus-310-vfsw |    Gi2/28    | 100000000  |  used  |  up   | 2021-09-20 15:36 |    D.297    |   Voice-Over-IP   |   503   |  1/0/28  |
| Aus-310-vfsw |    Gi2/29    | 100000000  |  used  |  up   | 2020-11-23 12:29 |    D.289    |   Voice-Over-IP   |   503   |  1/0/29  |
| Aus-310-vfsw |    Gi2/30    | 100000000  |  used  |  up   | 2020-11-23 12:30 |    D.295    |   Voice-Over-IP   |   503   |  1/0/30  |
| Aus-310-vfsw |    Gi2/31    | 100000000  |  used  |  up   | 2020-11-23 12:33 |    D.187    |   Voice-Over-IP   |   503   |  1/0/31  |
| Aus-310-vfsw |    Gi2/32    | 100000000  |  used  |  up   | 2020-11-24 12:16 |    D.193    |   Voice-Over-IP   |   503   |  1/0/32  |
| Aus-310-vfsw |    Gi2/33    | 100000000  |  used  |  up   | 2020-11-23 13:21 |    D.287    |   Voice-Over-IP   |   503   |  1/0/33  |
| Aus-310-vfsw |    Gi2/34    | 100000000  |  used  |  up   | 2020-11-23 13:13 |    D.195    |   Voice-Over-IP   |   503   |  1/0/34  |
`
This table is well name and formatted but shows the install report information
and also the new information after processing. This will mostly be used when patching over ports,
and only shows the ports that need to be patched over. The commands folder
Contains the HPE commands, which can be just copied and pasted, no need for Explanation
as HPE is another section of hardware.
