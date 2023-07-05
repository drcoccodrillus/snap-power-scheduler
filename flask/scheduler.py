import os
import sys
import time
import json
import datetime
import schedule
import subprocess

def system_shutdown():
    #Write to log file that system shutdown was triggered
    file_path = os.path.join(os.environ['SNAP_COMMON'], 'latest_shutdown.log')
    with open(file_path, 'w') as file:
        date=datetime.datetime.now()
        file.write(str(date) + "\tSystem shutdown triggered\n")
    #Trigger system shutdown
    subprocess.run(['dbus-send --system --print-reply \
        --dest=org.freedesktop.login1 /org/freedesktop/login1 \
        "org.freedesktop.login1.Manager.PowerOff" boolean:true'], shell=True)

def setup_shutdown_scheduler(schedule_payload):
    days_of_week = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

    for day in days_of_week:
        if day in schedule_payload and schedule_payload[day] is not None:
            schedule_time = datetime.datetime.strptime(schedule_payload[day], "%H:%M:%S")
            if day == "sun":
                schedule.every().sunday.at(schedule_time.strftime("%H:%M")).do(system_shutdown)
            elif day == "mon":
                schedule.every().monday.at(schedule_time.strftime("%H:%M")).do(system_shutdown)
            elif day == "tue":
                schedule.every().tuesday.at(schedule_time.strftime("%H:%M")).do(system_shutdown)
            elif day == "wed":
                schedule.every().wednesday.at(schedule_time.strftime("%H:%M")).do(system_shutdown)
            elif day == "thu":
                schedule.every().thursday.at(schedule_time.strftime("%H:%M")).do(system_shutdown)
            elif day == "fri":
                schedule.every().friday.at(schedule_time.strftime("%H:%M")).do(system_shutdown)
            elif day == "sat":
                schedule.every().saturday.at(schedule_time.strftime("%H:%M")).do(system_shutdown)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    if(len(sys.argv) > 1):
        file_path = sys.argv[1]
    else:
        file_path = os.path.join(os.environ['SNAP_COMMON'], 'schedule_payload.json')
        #Create default empty schedule file if it doesn't exist
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            schedule_payload = {
                "mon": None,
                "tue": None,
                "wed": None,
                "thu": None,
                "fri": None,
                "sat": None,
                "sun": None
            }
            print(f"Writing to file: {file_path}")
            with open(file_path, 'w') as file:
                file.write(json.dumps(schedule_payload))

    with open(file_path, 'r') as file:
        schedule_payload = json.load(file)

    setup_shutdown_scheduler(schedule_payload)
