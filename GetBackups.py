#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = "Noy."
__version__ = "0.1"


from ftplib import FTP
import os, time, json
from datetime import datetime, timedelta


"""
NEEDS:
Python 3 - to install : go on the website https://www.python.org/
ftplib - to install : pip install pyftpdlib
"""

# exemple of file name : Backup_2023-07-19.zip
print("Starting " + os.path.basename(__file__) + "...")

days_before_removing_backup = 7

try :
    with open("ini.json", 'r') as configFile:
        d = json.load(configFile)
except:
    print("Error loading ini.json creating another")
    try:
        os.rename("ini.json", "OLD-ini.json")
    except:
        pass
    with open("ini.json", 'w') as configFile:
        configFile.write("""
{
    "server": "yourServer", 
    "username": "yourUsername", 
    "password": "yourPassw0rd", 
    "remote_path": "yourRemotePath", 
    "local_path": "yourLocalPath", 
    "backup_Hour": "XX:XX"
}
""")
    exit()
try:
    server = d["server"]
    username = d["username"]
    password = d["password"]
    remote_path = d["remote_path"]
    local_path = d["local_path"]
    backup_Hour = d["backup_Hour"]
except:
    print("Error Please make sure the ini.json file is valid")
    exit()

while True:
    try:
        given_time = datetime.strptime(backup_Hour, "%H:%M")
    except ValueError:
        raise ValueError("Invalid input format. Please provide time in 'HH:MM' format.")
    current_time = datetime.now()
    target_time = current_time.replace(hour=given_time.hour, minute=given_time.minute, second=0, microsecond=0)

    # If the target time is already in the past, set it to the next day
    if target_time <= current_time:
        target_time += timedelta(days=1)

    time_difference = (target_time - current_time).total_seconds()
    if time_difference - 100 > 0:
        time.sleep(time_difference - 100)
    do = True
    while do :
        if datetime.now().strftime("%H:%M") == backup_Hour:

            print("Starting" + datetime.now().strftime(" %m/%d ") + "backup...")
            try:
                ftp = FTP(server)
                ftp.login(username, password)
                ftp.cwd(remote_path)

                # Take only the files that are not already on the local path
                files = [f for f in ftp.nlst() if f not in os.listdir(local_path)]

                for file in files:
                    with open(local_path + file, 'wb') as f:
                        ftp.retrbinary('RETR ' + file, f.write)
                ftp.quit()

                # Remove the files that are older than 7 days
                for file in os.listdir(local_path):
                    if os.path.isfile(local_path + file) and file.startswith("Backup_"):
                        date = datetime.strptime(file[7:17], "%Y-%m-%d")
                        if ((datetime.now() - date).days) > days_before_removing_backup:
                            os.remove(local_path + file)
                print("Backup" + datetime.now().strftime(" %m/%d ") + "done !")
            except FileNotFoundError as e:
                print("FileNotFoundError during" + datetime.now().strftime(" %m/%d ") + "backup, error = ", e)
            except:
                print("Error during" + datetime.now().strftime(" %m/%d ") + "backup")
            do = False
            time.sleep(60)