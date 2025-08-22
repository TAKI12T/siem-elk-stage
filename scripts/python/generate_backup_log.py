import random
from datetime import datetime, timedelta
import os

LOG_PATH = "/var/log/test-logs/plesk/backup.log"
DOMAINS = ["example.com", "mon-site.fr", "test.org", "shop.dev"]

SHARED_USERS = {
    "alice": "92.184.100.22",
    "bob": "5.135.183.146",
    "eve": "185.199.110.153"
}
IPS_SUSPECTS = ["203.0.113.77", "123.45.67.89"]

NORMAL_RESULTS = [
    "INFO: Backup of domain '{}' completed successfully by user '{}'.",
    "WARNING: Backup skipped for domain '{}' by user '{}' (no changes detected)"
]

SUSPICIOUS_RESULTS = [
    "ERROR: Backup failed for domain '{}' by user '{}' (Disk full)",
    "CRITICAL: Backup corrupted for domain '{}' (checksum mismatch, user '{}')",
    "ALERT: Unauthorized backup access attempt from IP {} on domain '{}'",
    "ERROR: Backup aborted for domain '{}' by user '{}' (unexpected I/O error)"
]

def generate_backup_log(timestamp: datetime) -> str:
    if random.random() < 0.5:
        user = random.choice(list(SHARED_USERS.keys()))
        result = random.choice(NORMAL_RESULTS)
        log_line = f"[{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {result.format(random.choice(DOMAINS), user)}\n"
    else:
        type_attack = random.choice(SUSPICIOUS_RESULTS)
        domain = random.choice(DOMAINS)
        if "Unauthorized" in type_attack:
            ip = random.choice(IPS_SUSPECTS)
            log_line = f"[{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {type_attack.format(ip, domain)}\n"
        else:
            user = random.choice(list(SHARED_USERS.keys()))
            log_line = f"[{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {type_attack.format(domain, user)}\n"
    return log_line

def write_backup_logs(log_count: int = 50):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    now = datetime.now()
    with open(LOG_PATH, "a") as f:
        for _ in range(log_count):
            #
            now -= timedelta(seconds=random.randint(5, 60))
            f.write(generate_backup_log(now))
    print(f"✔️ {log_count} logs de sauvegarde générés dans {LOG_PATH}")

if __name__ == "__main__":
    write_backup_logs(100)
