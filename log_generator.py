import os
import time
import random
from datetime import datetime

os.makedirs("logs", exist_ok=True)

LOG_FILE = "logs/fake.log"

users = ["alice", "bob", "carol", "dave"]
ips = ["192.168.1.10", "192.168.1.15", "10.0.0.5", "172.16.0.3"]
files = ["/etc/passwd", "/var/log/syslog", "/home/alice/.ssh/id_rsa"]

events = [
    "LOGIN SUCCESS user={user} ip={ip}",
    "LOGIN FAIL user={user} ip={ip}",
    "FILE READ user={user} file={file}",
    "CONNECTION user={user} dst_ip={ip} port={port}",
]

def generate_log():
    """Create a single fake log entry."""
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user = random.choice(users)
        ip = random.choice(ips)
        file = random.choice(files)
        port = random.randint(20, 8080)

        event = random.choice(events).format(user=user, ip=ip, file=file, port=port)

        return f"{now} {event}"
    
    except Exception as e:
        # If something breaks in generating the log, return an error log instead
        return f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ERROR generating log: {e}"

def main():
    print(f"Writing logs to {LOG_FILE}... Press Ctrl+C to stop.")
    try:
        with open(LOG_FILE, "a") as f:
            while True:
                try:
                    log_entry = generate_log()
                    f.write(log_entry + "\n")
                    f.flush()
                    print(log_entry)
                    time.sleep(1)
                
                except Exception as e:
                    # Handles errors in writing to file or printing
                    print(f"[ERROR] Failed to write log: {e}")
                    time.sleep(1)  # wait before retrying

    except KeyboardInterrupt:
        print("\n[INFO] Program stopped by user. Goodbye!")

    except Exception as e:
        print(f"[FATAL] Could not open log file {LOG_FILE}: {e}")

if __name__ == "__main__":
    main()