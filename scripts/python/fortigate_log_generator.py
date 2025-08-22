import time
import random
from datetime import datetime

log_path = "/var/log/test-logs/fortigate.log"

firewalls = ["FortiGate01", "FortiGate02"]


shared_ips = {
    "alice": "92.184.100.22",   # France (Orange)
    "bob": "5.135.183.146",     # OVH (France)
    "eve": "185.199.110.153"    # GitHub Pages
}
src_ips_normal = list(shared_ips.values())

dst_ips = ["10.0.0.10", "10.0.0.20", "10.0.0.30"]  # cibles communes
attacker_ip = "203.0.113.77"  # IP utilisée dans les attaques

usernames = list(shared_ips.keys())

services = {
    "HTTP": 80, "HTTPS": 443, "DNS": 53, "SSH": 22, "SMB": 445
}
proto_map = {"TCP": 6, "UDP": 17}


def generate_fortigate_log(log_type="traffic_normal"):
    now = datetime.now()
    base = f'date={now.strftime("%Y-%m-%d")} time={now.strftime("%H:%M:%S")}'
    devname = f'devname="{random.choice(firewalls)}"'
    devid = 'devid="FGT60FTK21012345"'
    vd = 'vd="root"'

    if log_type == "traffic_normal":
        user = random.choice(usernames)
        src = shared_ips[user]
        dst = random.choice(dst_ips)
        service_name, dstport = random.choice(list(services.items()))
        proto = random.choice(list(proto_map.values()))
        log = (
            f'{base} {devname} {devid} logid="0000000013" type="traffic" subtype="forward" '
            f'level="notice" {vd} srcip={src} dstip={dst} srcport={random.randint(1024, 65535)} '
            f'dstport={dstport} proto={proto} action="accept" policyid=1 policytype="policy" '
            f'service="{service_name}" user="{user}" srccountry="France" dstcountry="Morocco"'
        )

    elif log_type == "traffic_attack":
        log = (
            f'{base} {devname} {devid} logid="0000000013" type="traffic" subtype="forward" '
            f'level="warning" {vd} srcip={attacker_ip} dstip=10.0.0.10 srcport={random.randint(1024, 65535)} '
            f'dstport=445 proto=6 action="deny" policyid=2 policytype="policy" '
            f'service="SMB" srccountry="Unknown" dstcountry="Morocco"'
        )

    elif log_type == "auth_fail":
        user = random.choice(usernames)
        src = shared_ips[user]
        log = (
            f'{base} {devname} {devid} logid="0100032002" type="event" subtype="user" '
            f'level="warning" logdesc="User login failed" user="{user}" action="login" '
            f'status="failed" srcip={src} reason="Invalid password"'
        )

    elif log_type == "antivirus":
        src = shared_ips["eve"]
        dst = dst_ips[1]
        log = (
            f'{base} {devname} {devid} logid="0200008200" type="utm" subtype="virus" eventtype="virus" '
            f'level="warning" severity="medium" {vd} srcip={src} dstip={dst} '
            f'virus="EICAR_TEST_FILE" action="blocked" msg="file infected"'
        )

    elif log_type == "ips":
        log = (
            f'{base} {devname} {devid} logid="0419016384" type="utm" subtype="ips" eventtype="signature" '
            f'level="alert" {vd} severity="high" srcip={attacker_ip} dstip=10.0.0.30 '
            f'attack="MS.Windows.SMBv1.Buffer.Overflow" action="dropped"'
        )

    else:
        log = f"{base} type=event msg='Unknown log type'"

    return log + "\n"


# Écriture dans le fichier
with open(log_path, "a") as f:
    for _ in range(30):
        f.write(generate_fortigate_log("traffic_normal"))
        time.sleep(0.1)

    for _ in range(10):
        f.write(generate_fortigate_log("traffic_attack"))
        time.sleep(0.1)

    for _ in range(5):
        f.write(generate_fortigate_log("auth_fail"))
        time.sleep(0.05)

    for _ in range(5):
        f.write(generate_fortigate_log("antivirus"))
        time.sleep(0.05)

    for _ in range(5):
        f.write(generate_fortigate_log("ips"))
        time.sleep(0.05)
