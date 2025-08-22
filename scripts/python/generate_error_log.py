import random
from datetime import datetime, timedelta
import os

LOG_PATH = "/var/log/test-logs/plesk/httpsd_error.log"

# IP partagées entre tous les logs
SHARED_IPS = [
    "192.168.1.30",      # machine locale
    "203.0.113.77",      # IP attaquant récurrent
    "123.45.67.89",      # autre source suspecte
    "92.184.100.22",     # IP de alice
    "5.135.183.146",     # IP de bob
    "185.199.110.153"    # IP de eve
]

NORMAL_ERRORS = [
    "PHP Fatal error: Uncaught Exception: Database connection failed for user 'alice'",
    "Permission denied: Could not open /var/www/vhosts/example.com/htdocs/index.php",
    "PleskException: Invalid credentials for user 'admin'",
    "Deprecated: Function mysql_connect() is deprecated in /var/www/html/db.php"
]

SUSPICIOUS_ERRORS = [
    "Segmentation fault at address 0xdeadbeef",
    "Unauthorized access attempt detected from IP 203.0.113.77",
    "Warning: SQL Injection attempt blocked for user 'root'",
    "Critical: Multiple failed login attempts detected for user 'bob'",
    "Kernel panic - not syncing: Fatal exception",
    "Suspicious script execution in /tmp/tmpXYZ.sh"
]

def generate_error_log(timestamp: datetime) -> str:
    ip = random.choice(SHARED_IPS)
    if random.random() < 0.5:
        error_msg = random.choice(NORMAL_ERRORS)
    else:
        error_msg = random.choice(SUSPICIOUS_ERRORS)
    log = f"[{timestamp.strftime('%a %b %d %H:%M:%S %Y')}] [error] [client {ip}] {error_msg}\n"
    return log

def write_error_logs(count: int = 50):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    now = datetime.now()
    with open(LOG_PATH, "a") as f:
        for _ in range(count):
            now -= timedelta(seconds=random.randint(5, 60))
            f.write(generate_error_log(now))
    print(f"✔️ {count} logs d’erreur générés dans {LOG_PATH}")

if __name__ == "__main__":
    write_error_logs(50)
