import time
import os

LOG_FILE = "logs/fake.log"

def parse_log_line(line):
    """
    Takes a raw log line and breaks it into structured fields.
    Example line: "2025-08-19 12:34:56 LOGIN_SUCCESS user=alice ip=192.168.1.5"
    """
    parts = line.strip().split()  # split by spaces
    if len(parts) < 3:
        return None  # skip malformed lines

    timestamp = parts[0] + " " + parts[1]  # combine date + time
    event_type = parts[2]

    # store extra fields as key=value pairs
    data = {"timestamp": timestamp, "event_type": event_type}

    for part in parts[3:]:
        if "=" in part:
            key, value = part.split("=", 1)  # split only at first "="
            data[key] = value

    return data


def follow_log(file_path):
    """Continuously read new lines from the log file (tail -f style)."""
    with open(file_path, "r") as f:
        # Move to the end of the file (we only want new logs)
        f.seek(0, os.SEEK_END)

        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)  # wait for new lines
                continue

            event = parse_log_line(line)
            if event:
                print(event)


if __name__ == "__main__":
    print("[*] Starting MiniSIEM log reader...")
    follow_log(LOG_FILE)
