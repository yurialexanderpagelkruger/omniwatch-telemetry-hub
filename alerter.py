import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import database
from config import Config

def send_telegram(message):
    if not Config.TELEGRAM_BOT_TOKEN or not Config.TELEGRAM_CHAT_ID:
        return False
    url = f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        resp = requests.post(
            url,
            json={"chat_id": Config.TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"},
            timeout=10,
        )
        return resp.status_code == 200
    except Exception:
        return False

def send_email(subject, body):
    if not Config.SMTP_HOST or not Config.SMTP_USER:
        return False
    try:
        msg = MIMEMultipart()
        msg["From"] = Config.SMTP_USER
        msg["To"] = Config.ALERT_EMAIL_TO
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html"))
        with smtplib.SMTP(Config.SMTP_HOST, Config.SMTP_PORT) as server:
            server.starttls()
            server.login(Config.SMTP_USER, Config.SMTP_PASSWORD)
            server.send_message(msg)
        return True
    except Exception:
        return False

def dispatch(server, severity, message):
    prefix = message[:40]
    if database.get_recent_alert_exists(
        server["id"], severity, prefix, Config.ALERT_ALERT_COOLDOWN_SECONDS
    ):
        return

    database.insert_alert(server["id"], severity, message)

    icon = {"critical": "🔴", "warning": "🟠", "info": "🔵"}.get(severity, "⚪")
    text = (
        f"{icon} <b>OmniWatch — {severity.upper()}</b>\n"
        f"<b>Servidor:</b> {server['name']}\n"
        f"<b>Sede:</b> {server['location']}\n"
        f"<b>Detalle:</b> {message}"
    )
    send_telegram(text)
    send_email(
        f"[OmniWatch] {severity.upper()} en {server['name']}",
        f"<p>{message}</p><p>Servidor: {server['name']} ({server['location']})</p>",
    )

def evaluate_metrics(server, metrics):
    if metrics["cpu"] >= Config.ALERT_CPU_THRESHOLD:
        dispatch(server, "critical", f"CPU al {metrics['cpu']}% (umbral {Config.ALERT_CPU_THRESHOLD}%)")
    elif metrics["cpu"] >= Config.ALERT_CPU_THRESHOLD - 10:
        dispatch(server, "warning", f"CPU elevado al {metrics['cpu']}%")

    if metrics["ram"] >= Config.ALERT_RAM_THRESHOLD:
        dispatch(server, "critical", f"RAM al {metrics['ram']}% (umbral {Config.ALERT_RAM_THRESHOLD}%)")
    elif metrics["ram"] >= Config.ALERT_RAM_THRESHOLD - 10:
        dispatch(server, "warning", f"RAM elevada al {metrics['ram']}%")

    if metrics["disk"] >= Config.ALERT_DISK_THRESHOLD:
        dispatch(server, "critical", f"Disco al {metrics['disk']}% (umbral {Config.ALERT_DISK_THRESHOLD}%)")
    elif metrics["disk"] >= Config.ALERT_DISK_THRESHOLD - 10:
        dispatch(server, "warning", f"Disco al {metrics['disk']}%")

def evaluate_services(server, services):
    for svc in services:
        if svc["status"] == "stopped":
            dispatch(server, "critical", f"Servicio {svc['name']} caído")
        elif svc["status"] == "degraded":
            dispatch(server, "warning", f"Servicio {svc['name']} degradado")

def run_alert_cycle():
    for server in database.get_servers():
        metrics = database.get_latest_metrics(server["id"])
        if metrics:
            evaluate_metrics(server, metrics)
        services = database.get_latest_services(server["id"])
        if services:
            evaluate_services(server, services)
