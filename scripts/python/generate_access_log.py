import time
import random
from datetime import datetime
import os

LOG_PATH = "/var/log/test-logs/plesk/httpsd_access.log"

# IPs publiques cohérentes entre tous les scripts
SHARED_USERS = {
    "alice": "92.184.100.22",    # France (Orange)
    "bob": "5.135.183.146",      # OVH
    "eve": "185.199.110.153"     # GitHub Pages
}
USERS = list(SHARED_USERS.keys())
IPS = list(SHARED_USERS.values()) + ["203.0.113.77", "123.45.67.89"]  # inclut IP d'attaque

DOMAINS = ["example.com", "mon-site.fr", "test.org", "shop.dev"]
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari.537.36",
    "curl/7.68.0",
    "sqlmap/1.4.12#stable (http://sqlmap.org)"  # attaque
]
HTTP_METHODS = ["GET", "POST", "HEAD"]
STATUS_CODES = [200, 301, 404, 500]

def generate_access_log():
    now = datetime.now().strftime("%d/%b/%Y:%H:%M:%S +0000")

    if random.random() < 0.5:
        # Log normal
        user = random.choice(USERS)
        ip = SHARED_USERS[user]
        path = random.choice(["smb/web", "login", "api", "plesk-status"])
        log = (
            f'{ip} - {user} [{now}] '
            f'"{random.choice(HTTP_METHODS)} /{path} HTTP/1.1" '
            f'{random.choice(STATUS_CODES)} {random.randint(200, 5000)} '
            f'"http://{random.choice(DOMAINS)}" "{random.choice(USER_AGENTS)}"\n'
        )
    else:
        # Log suspect (attaque)
        suspicious_paths = [
            "/../../etc/passwd",
            "/wp-login.php",
            "/phpmyadmin/index.php",
            "/admin/config.php",
            "/api/v1/users?name=' OR 1=1 --",
            "/login.php?user=admin' --",
            "/robots.txt",
            "/etc/shadow"
        ]
        suspicious_user_agents = [
            "sqlmap/1.4.12#stable (http://sqlmap.org)",
            "nmap",
            "masscan",
            "Nikto",
            "python-requests/2.25.1"
        ]
        log = (
            f'203.0.113.77 - - [{now}] '
            f'"{random.choice(HTTP_METHODS)} {random.choice(suspicious_paths)} HTTP/1.1" '
            f'{random.choice([404, 403, 500])} {random.randint(0, 1000)} '
            f'"http://{random.choice(DOMAINS)}" "{random.choice(suspicious_user_agents)}"\n'
        )
    return log

def write_access_logs():
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a") as f:
        for _ in range(random.randint(5, 10)):
            f.write(generate_access_log())
            time.sleep(0.1)
    print(f"✔️ Logs d'accès générés dans {LOG_PATH}")

if __name__ == "__main__":
    write_access_logs()

