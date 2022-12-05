import os
import gzip
from re import L
from time import time
import datetime
import csv


MOD_LIST = ["rm",
            "cp",
            "mv",
            "mkdir",
            "nano",
            "vim",
            "vi",
            "touch",
            "wget",
            "curl",
            "apt",
            "apt-get",
            ">>",
            "chmod",
            "tftp",
            "scp"
            ]
fieldnames = ["Database", "IP address","Time Entered", "Time Spent (S)", "Commands Run", "Modification Attempts", "Logname"]
AnalNames = ["DB1 Times","DB2 Times","DB3 Times","DB4 Times","_","DB1 Cmds", "DB2 Cmds","DB3 Cmds","DB4 Cmds", "__","DB1 Mods", "DB2 Mods","DB3 Mods","DB4 Mods"]
total_data = {"DB": [], "filename": []} # this is really just hear in case we need it later
interactive_data = {"DB": [], "IP": [],"etr": [], "time": [], "cmd": [], "mods": [], "filename": []}
PATH = "/home/student/MITM/logs/session_streams/"
logs = os.listdir(PATH)
logs.sort()
zipped_logs = [log for log in logs if log[-2:]=="gz"] # this gets rid of any non log files in the directory
zipped_logs.sort()
# now we have a list of all logs
# logs that we care about have the line:
#-------- Attacker Keystrokes ----------
# so we can use gzip to look for that in the file
# Make sure to minimize verbosity to maintain performance since we're storing over 60k entries

print("parsing...")
for compressed in zipped_logs:
    try:
        #with gzip.open(f"{PATH}{compressed}", "rt", encoding="utf-8") as contents:
        with gzip.open(compressed, mode="rt") as contents:
            total_data["filename"].append(compressed)
            keystrokes = False
            for line in contents.readlines():
                if "Container Name:" in line:
                    container  = line.split(":")
                    splits = container[1].split("_")
                    db = splits[1].strip("\n")  
                    total_data["DB"].append(db)
                if "Attack Timestamp:" in line: # timestamp
                    timestamp = line.split("Attack Timestamp:")[1].strip(" ").strip("\n")
                if "Attacker IP:" in line: # address
                    IP = line.split(":")[1].strip(" ").strip("\n")  
                if "Attacker Keystrokes" in line:
                    keystrokes = True # keystrokes being equal to true means we should be looking for commands and whatnot now
                    # Its in interactive mode:
                    # add the info we got from before
                    interactive_data["etr"].append(timestamp)
                    interactive_data["IP"].append(IP)
                    interactive_data["DB"].append(db)
                    interactive_data["filename"].append(compressed)
                    # at this point we need total time in container, total commands run
                    # and total number of file modifications
                

            else:
                continue
    except:
        continue
print("sorting through important files...")
for i, file in enumerate(interactive_data["filename"]):
    with gzip.open(file, mode="rt") as tarball:
        stream = False
        times = False
        commands = 0
        mods = 0
        timeDelta = None
        bot = False
        for line in tarball.readlines():
            if "Attacker Stream Below" in line:
                stream = True
                times = False
            if "Attacker Keystrokes" in line:
                stream = False
                times = True
            if "$" in line and stream:
                    # now we get the last three things
                    line_split = line.split("$")
                    # now formatted as date[SPACE]hour, minute, second.milisecond, commands
                    line_commands = line_split[1].replace("||",";").replace("&&",";")
                    line_commands = line_commands.split(";")
                    commands += len(line_commands)
                    for command in line_commands:
                        for mod in MOD_LIST:
                            if mod in command:
                                mods+= 1
            if times:
                splits = line.split(":")
                date  =  splits[0].split(" ")
                date_p = date[0].split("-")

                if timeDelta == None: # looking for bots
                    timeDelta = datetime.datetime(int(date_p[0]),int(date_p[1]),int(date_p[2]),int(date[1]),int(splits[1]),int(splits[2].split(".")[0])).timestamp()
                else:
                    currentCMD = datetime.datetime(int(date_p[0]),int(date_p[1]),int(date_p[2]),int(date[1]),int(splits[1]),int(splits[2].split(".")[0])).timestamp()
                    if abs(timeDelta-currentCMD) <= 0.1:
                        bot = True
                        break # we dont need to look through the rest of the file if we know its a bot
                    else:
                        continue

        ts = interactive_data["etr"][i]
        last_cmdTime = datetime.datetime(int(date_p[0]),int(date_p[1]),int(date_p[2]),int(date[1]),int(splits[1]),int(splits[2].split(".")[0])).timestamp()
        conT = ts.replace("-", ":").replace(" ", ":").split(":")
        connect = datetime.datetime(int(conT[0]),int(conT[1]),int(conT[2]),int(conT[3]),int(conT[4]),int(conT[5].split(".")[0])).timestamp()
        t_total = last_cmdTime-connect # this is in seconds
        if not bot:
            interactive_data["cmd"].append(commands)
            interactive_data["mods"].append(mods)
            interactive_data["time"].append(t_total)
# Now exporting to the csv
print("writing to a csv...")
with open(f"analysis.csv", "w+", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=AnalNames)
    # putting things into nice arrays
    db1dict = {"time": [], "cmd": [], "mods": []}
    db2dict = {"time": [], "cmd": [], "mods": []}
    db3dict = {"time": [], "cmd": [], "mods": []}
    db4dict = {"time": [], "cmd": [], "mods": []}
    for idx, database in enumerate(interactive_data["DB"]):
        if database == "1":
            db1dict["time"].append(interactive_data["time"][idx])
            db1dict["cmd"].append(interactive_data["cmd"][idx])
            db1dict["mods"].append(interactive_data["mods"][idx])
        elif database == "2":
            db2dict["time"].append(interactive_data["time"][idx])
            db2dict["cmd"].append(interactive_data["cmd"][idx])
            db2dict["mods"].append(interactive_data["mods"][idx])
        elif database == "3":
            db3dict["time"].append(interactive_data["time"][idx])
            db3dict["cmd"].append(interactive_data["cmd"][idx])
            db3dict["mods"].append(interactive_data["mods"][idx])
        elif database == "4":
            db4dict["time"].append(interactive_data["time"][idx])
            db4dict["cmd"].append(interactive_data["cmd"][idx])
            db4dict["mods"].append(interactive_data["mods"][idx])
        else:
            continue                        
    writer.writeheader()

    # Doing the Kushkal Wallis test:
    db1n = len(db1dict["time"])
    db2n = len(db2dict["time"])
    db3n = len(db3dict["time"])
    db4n = len(db4dict["time"])

    

    for i in range(0, max([len(db1dict["time"]),len(db2dict["time"]),len(db3dict["time"]),len(db4dict["time"])])):
        if i+1 >= len(db1dict["time"]):
            db1dict["time"].append(None)
            db1dict["cmd"].append(None)
            db1dict["mods"].append(None)
        if i+1 >= len(db2dict["time"]):
            db2dict["time"].append(None)
            db2dict["cmd"].append(None)
            db2dict["mods"].append(None)
        if i+1 >= len(db3dict["time"]):
            db3dict["time"].append(None)
            db3dict["cmd"].append(None)
            db3dict["mods"].append(None)
        if i+1 >= len(db4dict["time"]):
            db4dict["time"].append(None)
            db4dict["cmd"].append(None)
            db4dict["mods"].append(None)

        writer.writerow({"DB1 Times": db1dict["time"][i], "DB2 Times": db2dict["time"][i], "DB3 Times": db3dict["time"][i], "DB4 Times": db4dict["time"][i], "DB1 Cmds": db1dict["cmd"][i],"DB2 Cmds": db2dict["cmd"][i],"DB3 Cmds": db3dict["cmd"][i],"DB4 Cmds": db4dict["cmd"][i],"DB1 Mods": db1dict["mods"][i],"DB2 Mods": db2dict["mods"][i],"DB3 Mods": db3dict["mods"][i],"DB4 Mods": db4dict["mods"][i]})

