import os
import shutil
import sys
import datetime

# This finds modified files on the host machine and copies them off to the LXC host
# This gets run on the host
# This must be run as sudo
# file path to get to containers are /var/lib/lxc/[CONTAINER NAME]/rootfs
#   puts you at / in the container

# keep the time formatted exactly as the log file(year-month-day hour:minute:second.millisecond)

# Script takes 1 command line argument, being the container name.
# expects to be called as python3 gatherer.py [Container Name]

n = len(sys.argv)
if n != 2: # the calling of the script counts as an argument
    print("Usage: gatherer.py [Container Name]")
    sys.exit(1)

BASEPATH = f"/var/lib/lxc/{sys.argv[1]}/rootfs/"
PATHTODUMP = "/home/student/data/modfiles"

# getting the latest logfile
logs = os.listdir("/home/student/data")
greatest = 0
for log in logs:
    if "DATABASE" in log:
        num = log.split("_")[1]
        if int(num) > greatest:
            greatest = num
    else:
        continue
MITMLOG = f"/home/student/data/DATABASE_{greatest}_log"

# get login time
# attacker login is defined by [LXC-Auth] in a line
def main():
    with open(MITMLOG, "r") as logs:
        for line in logs:
            if "[LXC-Auth]" in line:
                # Example date
                # 2022-09-29 05:27:01.486
                parse = line.split(' ') # relevant parts are the date and the time
                dateReadable = parse[0].split('-') # split the date to convert to epoch
                timeReadable = parse[1].split(':')
                connectEpoch = datetime.datetime(dateReadable[0],dateReadable[1],dateReadable[2],timeReadable[0],timeReadable[1],int(timeReadable[2])).strftime('%s')
                # Basically converts a pretty date into time since epoch which makes it easy to do math

    # Now that we have the time the attacker connected we can see what gets modified after

    for path, files, dirs in os.walk(BASEPATH):
        for file in files:
            stats = os.stats(os.path.join(path,file))
            modTime = stats.st_mtime # modified time in seconds since epoch
            if modTime >= connectEpoch: # if the file was modified more than 1 minute after attacker connected
                #os.rename(os.path.join(path,file), os.path.join(PATHTODUMP, file)) # move to the unsorted dir
                shutil.copy(os.path.join(path,file), PATHTODUMP) # move to the unsorted dir
            else:
                continue



if __name__ in "__main__":
    main()
