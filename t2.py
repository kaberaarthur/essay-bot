from datetime import datetime

def log_activity(activity):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp}: {activity}\n"
    
    with open("activity_log.txt", "a") as log_file:
        log_file.write(log_entry)


log_activity("Activity 1")
