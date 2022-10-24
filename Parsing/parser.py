import csv
import os
import datetime
from time import time

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
            ">>"
            ]

fieldnames = ["Attacker No.", "Database", "Time Entered", "Time Spent (S)", "Commands Run", "Modification Attempts","Filename", "Database (Avgs)", "Avg Time Connected", "Avg Commands Run", "Avg File Modifications"]
data = {"atk": [], "DB": [], "etr": [], "time": [], "cmd": [], "mods": [], "filename": []}

logs = os.listdir("../Data Backups/")
logs.sort()

for i, file in enumerate(logs):
    data["atk"].append(i)
    DBnum = file.split("_")[2] # logs are formatted as DATE_DATABASE_NUMBER_log
    data["DB"].append(DBnum)
    data["filename"].append(file)
    with open(f"../Data Backups/{file}", "r") as log:
        conEpochms = 0
        cmds = 0
        mods = 0
        for line in log:
            if "Attacker connected" in line:
                connectTime = line.split("-")
                date = f"{connectTime[0]}-{connectTime[1]}-{connectTime[2].strip()}"
                data["etr"].append(date)
                parse = line.split(" ")
    
                dateReadable = parse[0].split('-') # split the date to convert to epoch
                timeReadable = parse[1].split(':')
                try:
                    connectEpoch = datetime.datetime(int(dateReadable[0]),int(dateReadable[1]),int(dateReadable[2]),int(timeReadable[0]),int(timeReadable[1]),int(timeReadable[2].split(".")[0])).timestamp()
                except:
                    print(file)
                    conEpochms = 0
                print("found connection")
                conEpochms = connectEpoch*1000+int(timeReadable[2].split(".")[1])
            if "Attacker closed" in line:
                parse = line.split(" ")
                dateReadable = parse[0].split('-') # split the date to convert to epoch
                timeReadable = parse[1].split(':')
                try:
                    disEpoch = datetime.datetime(int(dateReadable[0]),int(dateReadable[1]),int(dateReadable[2]),int(timeReadable[0]),int(timeReadable[1]),int(timeReadable[2].split(".")[0])).timestamp()
                except:
                    print(file)
                    conEpochms = 0
                print("Found disconnect")
                disEpochms = connectEpoch*1000+int(timeReadable[2].split(".")[1])
                deltaMS = 0
                if conEpochms == 0:
                    data["time"].append(0)
                else:
                    deltaMS = (disEpochms - conEpochms) # this is in ms
                    deltaS = deltaMS/1000 # leaving as s so we can do nice math for avgs later
                    data["time"].append(deltaS)
            if "line from reader" in line:
                cmds += 1
                for command in MOD_LIST:
                    words = line.split(" ")
                    for word in words:
                        if command in word:
                            mods += 1
        data["cmd"].append(cmds)
        data["mods"].append(mods)

# Finding averages for each database
DB_1_avg = {"atk": [], "etr": [], "time": [], "cmd": [], "mods": [], "time_avg": 0, "cmd_avg": 0, "mods_avg": 0,}
DB_2_avg = {"atk": [], "etr": [], "time": [], "cmd": [], "mods": [], "time_avg": 0, "cmd_avg": 0, "mods_avg": 0,}
DB_3_avg = {"atk": [], "etr": [], "time": [], "cmd": [], "mods": [], "time_avg": 0, "cmd_avg": 0, "mods_avg": 0,}
DB_4_avg = {"atk": [], "etr": [], "time": [], "cmd": [], "mods": [], "time_avg": 0, "cmd_avg": 0, "mods_avg": 0,}

for i in range(0, len(data["atk"])):
    db = int(data["DB"][i])
    if data["time"][i] <= 0:
        continue
    # once again this would look so much better with match case but ubuntu only really likes 3.8
    if db == 1:
        DB_1_avg["atk"].append(data["atk"][i])
        DB_1_avg["etr"].append(data["etr"][i])
        DB_1_avg["time"].append(data["time"][i])
        DB_1_avg["cmd"].append(data["cmd"][i])
        DB_1_avg["mods"].append(data["mods"][i])
    elif db == 2:
        DB_2_avg["atk"].append(data["atk"][i])
        DB_2_avg["etr"].append(data["etr"][i])
        DB_2_avg["time"].append(data["time"][i])
        DB_2_avg["cmd"].append(data["cmd"][i])
        DB_2_avg["mods"].append(data["mods"][i])
    elif db == 3:
        DB_3_avg["atk"].append(data["atk"][i])
        DB_3_avg["etr"].append(data["etr"][i])
        DB_3_avg["time"].append(data["time"][i])
        DB_3_avg["cmd"].append(data["cmd"][i])
        DB_3_avg["mods"].append(data["mods"][i])
    elif db == 4:
        DB_4_avg["atk"].append(data["atk"][i])
        DB_4_avg["etr"].append(data["etr"][i])
        DB_4_avg["time"].append(data["time"][i])
        DB_4_avg["cmd"].append(data["cmd"][i])
        DB_4_avg["mods"].append(data["mods"][i])
DB_1_avg["time_avg"] = sum(DB_1_avg["time"])/len(DB_1_avg["time"])
DB_2_avg["time_avg"] = sum(DB_2_avg["time"])/len(DB_2_avg["time"])
DB_3_avg["time_avg"] = sum(DB_3_avg["time"])/len(DB_3_avg["time"])
DB_4_avg["time_avg"] = sum(DB_4_avg["time"])/len(DB_4_avg["time"])

DB_1_avg["cmd_avg"] = sum(DB_1_avg["cmd"])/len(DB_1_avg["cmd"])
DB_2_avg["cmd_avg"] = sum(DB_2_avg["cmd"])/len(DB_2_avg["cmd"])
DB_3_avg["cmd_avg"] = sum(DB_3_avg["cmd"])/len(DB_3_avg["cmd"])
DB_4_avg["cmd_avg"] = sum(DB_4_avg["cmd"])/len(DB_4_avg["cmd"])

DB_1_avg["mods_avg"] = sum(DB_1_avg["mods"])/len(DB_1_avg["mods"])
DB_2_avg["mods_avg"] = sum(DB_2_avg["mods"])/len(DB_2_avg["mods"])
DB_3_avg["mods_avg"] = sum(DB_3_avg["mods"])/len(DB_3_avg["mods"])
DB_4_avg["mods_avg"] = sum(DB_4_avg["mods"])/len(DB_4_avg["mods"])

last = logs[-1].split("_")[0]
with open(f"STATS_AS_OF_{last}.csv", "w+", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for i in range(0, len(data["atk"])):
        # once again this would look so much better with match case but ubuntu only really likes 3.8
        if i == 0:
            writer.writerow({"Attacker No.": data["atk"][i],"Database": data["DB"][i],"Time Entered": data["etr"][i],"Time Spent (S)": data["time"][i],
            "Commands Run": data["cmd"][i],"Modification Attempts": data["mods"][i],"Filename": data["filename"][i], "Database (Avgs)": 1, "Avg Time Connected": DB_1_avg["time_avg"], 
            "Avg Commands Run": DB_1_avg["cmd_avg"], "Avg File Modifications": DB_1_avg["mods_avg"]})
        elif i == 1:
            writer.writerow({"Attacker No.": data["atk"][i],"Database": data["DB"][i],"Time Entered": data["etr"][i],"Time Spent (S)": data["time"][i],
            "Commands Run": data["cmd"][i],"Modification Attempts": data["mods"][i],"Filename": data["filename"][i], "Database (Avgs)": 2, "Avg Time Connected": DB_2_avg["time_avg"], 
            "Avg Commands Run": DB_2_avg["cmd_avg"], "Avg File Modifications": DB_2_avg["mods_avg"]})
        elif i == 2:
            writer.writerow({"Attacker No.": data["atk"][i],"Database": data["DB"][i],"Time Entered": data["etr"][i],"Time Spent (S)": data["time"][i],
            "Commands Run": data["cmd"][i],"Modification Attempts": data["mods"][i],"Filename": data["filename"][i], "Database (Avgs)": 3, "Avg Time Connected": DB_3_avg["time_avg"], 
            "Avg Commands Run": DB_3_avg["cmd_avg"], "Avg File Modifications": DB_3_avg["mods_avg"]})
        elif i == 3:
            writer.writerow({"Attacker No.": data["atk"][i],"Database": data["DB"][i],"Time Entered": data["etr"][i],"Time Spent (S)": data["time"][i],
            "Commands Run": data["cmd"][i],"Modification Attempts": data["mods"][i],"Filename": data["filename"][i], "Database (Avgs)": 4, "Avg Time Connected": DB_4_avg["time_avg"], 
            "Avg Commands Run": DB_4_avg["cmd_avg"], "Avg File Modifications": DB_4_avg["mods_avg"]})
        else:
            writer.writerow({"Attacker No.": data["atk"][i],"Database": data["DB"][i],"Time Entered": data["etr"][i],"Time Spent (S)": data["time"][i],
            "Commands Run": data["cmd"][i],"Modification Attempts": data["mods"][i],"Filename": data["filename"][i]})