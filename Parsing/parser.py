import csv
import os
from datetime import datetime

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

fieldnames = ["Attacker No.", "Database", "Time entered", "Time Spent", "Commands run", "Modification attempts"]
data = {"atk": [], "DB": [], "etr": [], "time": [], "cmd": [], "mods": []}

logs = os.listdir("../Data Backups/")
logs.sort()

for i, file in enumerate(logs):
    data["atk"].append(i)
    with open(file, "r") as log:


