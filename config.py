import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "omniwatch-dev-key")
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), "data", "omniwatch.db")
    DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
    SMTP_HOST = os.getenv("SMTP_HOST", "")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    ALERT_EMAIL_TO = os.getenv("ALERT_EMAIL_TO", "")
    COLLECT_INTERVAL_SECONDS = 30
    ALERT_CPU_THRESHOLD = 85.0
    ALERT_RAM_THRESHOLD = 90.0
    ALERT_DISK_THRESHOLD = 90.0
    ALERT_ALERT_COOLDOWN_SECONDS = 300
