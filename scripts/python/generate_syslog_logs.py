import time
import random
from datetime import datetime
import os

# Chemin du fichier
log_path = "/var/log/test-logs/syslog.log"
os.makedirs(os.path.dirname(log_path), exist_ok=True)

# Données communes avec les autres scripts
IPS = ["192.168.1.10", "10.0.0.1", "203.0.113.42", "123.45.67.89"]
USERS = ["admin", "user1", "webmaster", "client1", "noreply"]
HOSTNAMES = ["webserver1", "dbserver", "firewall", "myhost"]
PROCESSES = ["sshd", "nginx", "kernel", "systemd", "cron", "dockerd"]
LOG_LEVELS = ["INFO", "WARNING", "ERROR", "DEBUG"]

# Messages normaux
NORMAL_MESSAGES = [
    "Accepted password for {user} from {ip} port 22 ssh2",
    "Session opened for user {user}",
    "User {user} logged out",
    "Started Session 123 of user {user}",
    "Reloading configuration files",
    "Configuration file updated successfully",
    "Firewall allowed connection from {ip} to port 443",
    "Permission denied while accessing /etc/shadow"
]

# Messages suspects pour détection SIEM
SUSPICIOUS_MESSAGES = [
    "Multiple failed password attempts for {user} from {ip}",
    "Unauthorized access to root shell",
    "Brute-force attack detected from {ip}",
    "Segmentation fault at address 0xdeadbeef",
    "Kernel panic - not syncing: Fatal exception",
    "Malicious process detected: /tmp/malware.sh"
]

def generate_syslog_line():
    timestamp = datetime.now().strftime("%b %d %H:%M:%S")
    hostname = random.choice(HOSTNAMES)
    process = random.choice(PROCESSES)
    pid = random.randint(100, 9999)
    level = random.choice(LOG_LEVELS)

    user = random.choice(USERS)
    ip = random.choice(IPS)

    if random.random() < 0.3:  # 30% de logs suspects
        message_template = random.choice(SUSPICIOUS_MESSAGES)
    else:
        message_template = random.choice(NORMAL_MESSAGES)

    message = message_template.format(user=user, ip=ip)

    return f"{timestamp} {hostname} {process}[{pid}]: {level}: {message}\n"

# Générer 100 lignes
with open(log_path, "a") as f:
    for _ in range(100):
        f.write(generate_syslog_line())
        time.sleep(0.1)

print(f"✅ 100 logs syslog générés dans : {log_path}")
