import os
import random
from datetime import datetime

# Chemin du fichier
log_dir = "/var/log/test-logs/"
log_file = os.path.join(log_dir, "fortimail-syslog.log")
os.makedirs(log_dir, exist_ok=True)

# Données partagées entre les logs
domains = ["example.com", "demo.org", "securemail.net"]
users = ["alice", "bob", "eve", "admin", "noreply"]
subjects = [
    "Réunion reportée", "Facture disponible", "Nouvelle offre", "Mise à jour urgente", "Alerte de sécurité"
]
normal_msgs = [
    "SPF validation passed", "DMARC check passed", "Mail delivered successfully"
]
suspicious_msgs = [
    "SPF validation failed", "Virus signature detected", "Spoofing attempt",
    "Phishing link detected", "Spam score exceeded threshold", "Attachment blocked", "Malicious macro detected"
]

client_ips = ["203.0.113.77", "92.184.100.22", "123.45.67.89", "185.199.110.153"]
dst_ips = ["192.168.100.1", "192.168.100.20", "10.0.0.1"]
device_ids = ["FEVM01TM24000907", "FEVM01TM99999999"]
log_ids = ["0300024614", "0200024614"]

def generate_random_log():
    now = datetime.now()
    date_str = now.strftime("date=%Y-%m-%d,time=%H:%M:%S.%f")[:-3]
    is_suspicious = random.random() < 0.4  # 40% de trafic suspect

    base_fields = {
        "device_id": random.choice(device_ids),
        "log_id": random.choice(log_ids),
        "type": "spam",
        "subtype": "smtp",
        "pri": "information" if not is_suspicious else "warning",
        "session_id": f"{random.randint(100000,999999)}-{random.randint(100000,999999)}",
        "client_name": f"mail-{random.randint(1,5)}.{random.choice(domains)}",
        "client_ip": random.choice(client_ips),
        "dst_ip": random.choice(dst_ips),
        "from": f"{random.choice(users)}@{random.choice(domains)}",
        "to": f"{random.choice(users)}@{random.choice(domains)}",
        "subject": random.choice(subjects),
        "msg": random.choice(suspicious_msgs if is_suspicious else normal_msgs),
        "action": "blocked" if is_suspicious else "delivered",
        "spam_score": round(random.uniform(5.0, 9.9), 1) if is_suspicious else round(random.uniform(0.1, 4.5), 1)
    }

    log_parts = [date_str] + [f'{k}="{v}"' for k, v in base_fields.items()]
    return "<190>" + ",".join(log_parts)

# Écriture des logs
with open(log_file, "a") as f:
    for _ in range(20):  # 20 logs pour plus de variété
        f.write(generate_random_log() + "\n")

print(f"✅ 20 logs FortiMail générés dans : {log_file}")
