# Takes all the modified files that got pulled off the container and checks them against the MITM log file
# to see what was actually created by the attacker
# This will likely still need manual review because I dont think scripts that make files will be caught
import os
from datetime import datetime

# I'm going to assume all the files pulled off are in a subdirectory named "modfiles"
# Files that are deemed relevant are going to be put in a subdir called "sorted"
# These files are then put into another subdir called "{datetime}_{attacker#}_sorted" 
# Then that dir is going to have a subdir called useful and junk
#   we are storing junk so that if get a script that references a file in junk we can find it and pull it up
# 
# Example file structure:
#   |   
#   |   fileSieve.py
#   |___modfiles
#   |   
#   |___sorted
#       |___2022-10-8-1630_1_sorted
#       |    |___useful
#       |   |   |   files that were deemed modded by attacker go here
#       |   |
#       |   |___junk
#       |       |   files that were deemed junk go here
#       |
#       |___2022-10-20-0845_2_sorted
#       |    |___useful
#       |   |   |   files that were deeded modded by attacker go here
#       |   |
#       |   |___junk
#       |       |   files that were deemed junk go here
#
#   Dates are in the format of Year-Month-Day-24hrTime


# Note that modlist isn't currently being used but probably will get implemented
# at some point to increase program efficiency
#MOD_LIST = ["rm",
#            "cp",
#            "mv",
#            "mkdir",
#            "nano",
#            "vim",
#            "vi",
#            "touch",
#           "wget",
#            "curl",
#            "apt",
#            "apt-get"
#            ]

UNSORT = "modfiles/"
SORTED = "sorted/"
LOGPATH = "path/to/mitm/log"


def sort(time):
    """Sorts the files in modfiles\n
    Going to try to do it by just looking through the logs for any metnion of the file but can very easily
    changed to use MOD_LIST to check for modification commands"""
    # Lets make dirs first
    try:
        os.mkdir(SORTED) # will throw exception if it exists already
    except:
        pass
    # need to get the current attacker number
    # could hold it in a file but thats a little clunky
    dirs = os.listdir(SORTED) # returns a list for sorted dirs
    num = 1
    for dir in dirs:
        # get the attacker number
        splits = dir.split("_")
        no = splits[1]
        if no > num:
            num = no
    num = num+1 # need to bump it up to advance
    os.makedirs(f"{SORTED}{time}_{num}_sorted/useful")
    os.makedirs(f"{SORTED}{time}_{num}_sorted/junk")

    # now lets get a list of the files to sort
    toSort = os.listdir(UNSORT)
    useful = []
    # checking for file operations using modlist is more efficient but this works for now
    with open(LOGPATH, "r") as logs:
        for line in logs:
            for file in toSort:
                if file in line:
                    useful.append(file)
    junk = set(toSort) - set(useful) # returns the elements in toSort that are not in useful (our junk)   

    # now we need to move all the files from modfiles to sorted
    for file in toSort:
        path = UNSORT+file # local file path
        if file in useful:
            newpath = f"{SORTED}{time}_{num}_sorted/useful"
            os.rename(path, newpath)
        else: # if its not in useful it goes in junk
            newpath = f"{SORTED}{time}_{num}_sorted/junk"
            os.rename(path, newpath)

def cleanup():
    """Makes sure nothing is left over in modfiles"""
    dir = os.listdir(UNSORT)
    if dir != 0:
        for file in dir:
            os.remove((os.path.join(UNSORT,file)))

if __name__ in "__main__":
    now = datetime.now()
    formated = now.strftime('%Y-%m-%d-%H%M')
    sort(formated)
    cleanup()