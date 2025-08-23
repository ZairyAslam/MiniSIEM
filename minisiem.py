import time
import os
from datetime import datetime

LOG_FILE = "logs/fake.log"
failed_logins = {}  # store failed login attempts by user


def parse_log_line(line):
    """
    Takes a raw log line and breaks it into structured fields.
    Example line: "2025-08-19 12:34:56 LOGIN_FAIL user=alice ip=192.168.1.5"
    """
    parts = line.strip().split()
    if len(parts) < 3:
        return None  # skip malformed lines

    timestamp_str = parts[0] + " " + parts[1]  # combine date + time
    event_type = parts[2]

    # convert timestamp string -> datetime object
    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

    data = {"timestamp": timestamp, "event_type": event_type}

    for part in parts[3:]:
        if "=" in part:
            key, value = part.split("=", 1)
            data[key] = value

    return data


def follow_log(file_path):
    """Continuously read new lines from the log file (tail -f style)."""
    with open(file_path, "r") as f:
        f.seek(0, os.SEEK_END)  # go to end of file

        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue

            event = parse_log_line(line)
            if event:
                process_event(event)  # <--- handle detection here


def process_event(event):
    """Detect suspicious patterns like multiple failed logins."""
    if event["event_type"] == "LOGIN_FAIL":
        user = event.get("user", "UNKNOWN")
        timestamp = event["timestamp"]

        if user not in failed_logins:
            failed_logins[user] = []

        failed_logins[user].append(timestamp)

        # keep only failures within the last 60 seconds
        failed_logins[user] = [
            t for t in failed_logins[user] if (timestamp - t).total_seconds() <= 60
        ]

        if len(failed_logins[user]) >= 3:
            print(f"🚨 ALERT: Multiple failed logins for user {user}")


if __name__ == "__main__":
    print("[*] Starting MiniSIEM log reader...")
    follow_log(LOG_FILE)
