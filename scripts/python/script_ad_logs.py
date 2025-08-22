import os
import random
from datetime import datetime, timedelta

# === Configuration ===
LOG_DIR = "/var/log/test-logs"
LOG_FILE = os.path.join(LOG_DIR, "Active_Directory.log")
os.makedirs(LOG_DIR, exist_ok=True)

# === Paramètres ===
USERS = ["admin", "user1", "webmaster", "client1", "noreply"]
DOMAINS = ["CORP.LOCAL"]
HOSTS = ["DC1.CORP.LOCAL"]
SOURCE_IPS = ["192.168.1.10", "10.0.0.1", "203.0.113.42", "123.45.67.89"]
ATTACKER_IP = "203.0.113.50"
LOG_LEVELS = {"success": "INFO", "fail": "WARN"}

# ID et messages
EVENTS = {
    "4624": ("AUTH", "Connexion réussie pour l'utilisateur {user}"),
    "4625": ("AUTH", "Échec de connexion pour l'utilisateur {user}"),
    "4771": ("KERBEROS", "Échec de pré-authentification pour {user}"),
    "4769": ("KERBEROS", "Ticket Service délivré à {user}"),
    "4728": ("GROUP_CHANGE", "Ajout de {user} à un groupe"),
    "4729": ("GROUP_CHANGE", "Suppression de {user} d’un groupe")
}

# === Fonction de génération de ligne ===
def generate_log(timestamp, event_id, logon_type, user, domain, ip, host, level):
    log_type, message_template = EVENTS[event_id]
    message = message_template.format(user=user)
    return f"{timestamp},{event_id},{logon_type},{user},{domain},{ip},{host},{level},{log_type},{message}\n"

# === Génération ===
start_time = datetime.now() - timedelta(minutes=30)
current_time = start_time

with open(LOG_FILE, "w") as f:
    f.write("timestamp,event_id,logon_type,username,domain,source_ip,hostname,log_level,log_type,message\n")

    for _ in range(50):
        user = random.choice(USERS)
        domain = DOMAINS[0]
        ip = random.choice(SOURCE_IPS)
        host = random.choice(HOSTS)
        logon_type = random.choice(["2", "3", ""])  # interactive / réseau / groupe

        event_id = random.choices(
            ["4624", "4625", "4771", "4728", "4729", "4769"],
            weights=[5, 3, 2, 1, 1, 2],
            k=1
        )[0]
        level = LOG_LEVELS["success"] if event_id in ["4624", "4769", "4728", "4729"] else LOG_LEVELS["fail"]

        timestamp = current_time.isoformat()
        log = generate_log(timestamp, event_id, logon_type, user, domain, ip, host, level)
        f.write(log)
        current_time += timedelta(seconds=random.randint(5, 60))

    # Brute-force ciblé
    brute_user = "user_brute"
    for _ in range(10):
        timestamp = current_time.isoformat()
        log = generate_log(timestamp, "4625", "3", brute_user, DOMAINS[0], ATTACKER_IP, HOSTS[0], LOG_LEVELS["fail"])
        f.write(log)
        current_time += timedelta(seconds=5)

    # Connexion finale réussie
    log = generate_log(current_time.isoformat(), "4624", "3", brute_user, DOMAINS[0], ATTACKER_IP, HOSTS[0], LOG_LEVELS["success"])
    f.write(log)

print(f"✅ Logs Active Directory générés dans : {LOG_FILE}")
