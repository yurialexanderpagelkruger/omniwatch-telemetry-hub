import sqlite3
import os
from datetime import datetime, timedelta
from config import Config

def get_connection():
    os.makedirs(os.path.dirname(Config.DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS servers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            location TEXT NOT NULL,
            host TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            server_id INTEGER NOT NULL,
            cpu REAL NOT NULL,
            ram REAL NOT NULL,
            disk REAL NOT NULL,
            net_in REAL NOT NULL,
            net_out REAL NOT NULL,
            uptime INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (server_id) REFERENCES servers (id)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            server_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            status TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (server_id) REFERENCES servers (id)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            server_id INTEGER NOT NULL,
            severity TEXT NOT NULL,
            message TEXT NOT NULL,
            acknowledged INTEGER NOT NULL DEFAULT 0,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (server_id) REFERENCES servers (id)
        )
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_metrics_server_time ON metrics(server_id, timestamp)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_alerts_time ON alerts(timestamp)")
    conn.commit()
    conn.close()

def seed_servers():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) as count FROM servers")
    if cur.fetchone()["count"] > 0:
        conn.close()
        return
    servers = [
        ("srv-core-01", "Casa Central - Buenos Aires", "10.0.1.10"),
        ("srv-core-02", "Casa Central - Buenos Aires", "10.0.1.11"),
        ("srv-app-01", "Sucursal Córdoba", "10.0.2.20"),
        ("srv-db-01", "Sucursal Rosario", "10.0.3.30"),
        ("srv-edge-01", "Sucursal Mendoza", "10.0.4.40"),
        ("srv-cache-01", "Datacenter Cloud", "172.16.0.5"),
    ]
    now = datetime.utcnow().isoformat()
    for name, location, host in servers:
        cur.execute(
            "INSERT INTO servers (name, location, host, created_at) VALUES (?, ?, ?, ?)",
            (name, location, host, now),
        )
    conn.commit()
    conn.close()

def get_servers():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM servers ORDER BY name").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_server(server_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM servers WHERE id = ?", (server_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def insert_metric(server_id, cpu, ram, disk, net_in, net_out, uptime, timestamp=None):
    ts = timestamp or datetime.utcnow().isoformat()
    conn = get_connection()
    conn.execute(
        "INSERT INTO metrics (server_id, cpu, ram, disk, net_in, net_out, uptime, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (server_id, cpu, ram, disk, net_in, net_out, uptime, ts),
    )
    conn.commit()
    conn.close()

def insert_service(server_id, name, status):
    conn = get_connection()
    conn.execute(
        "INSERT INTO services (server_id, name, status, timestamp) VALUES (?, ?, ?, ?)",
        (server_id, name, status, datetime.utcnow().isoformat()),
    )
    conn.commit()
    conn.close()

def insert_alert(server_id, severity, message):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO alerts (server_id, severity, message, timestamp) VALUES (?, ?, ?, ?)",
        (server_id, severity, message, datetime.utcnow().isoformat()),
    )
    conn.commit()
    alert_id = cur.lastrowid
    conn.close()
    return alert_id

def get_latest_metrics(server_id):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM metrics WHERE server_id = ? ORDER BY timestamp DESC LIMIT 1",
        (server_id,),
    ).fetchone()
    conn.close()
    return dict(row) if row else None

def get_metrics_history(server_id, limit=60):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM metrics WHERE server_id = ? ORDER BY timestamp DESC LIMIT ?",
        (server_id, limit),
    ).fetchall()
    conn.close()
    return [dict(r) for r in reversed(rows)]

def get_latest_services(server_id):
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT s.name, s.status, s.timestamp FROM services s
        INNER JOIN (
            SELECT name, MAX(timestamp) as maxts FROM services WHERE server_id = ? GROUP BY name
        ) t ON s.name = t.name AND s.timestamp = t.maxts
        WHERE s.server_id = ?
        """,
        (server_id, server_id),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_recent_alerts(limit=50):
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT a.*, s.name as server_name, s.location as server_location
        FROM alerts a JOIN servers s ON a.server_id = s.id
        ORDER BY a.timestamp DESC LIMIT ?
        """,
        (limit,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_alert_count_by_severity():
    conn = get_connection()
    rows = conn.execute(
        "SELECT severity, COUNT(*) as count FROM alerts WHERE acknowledged = 0 GROUP BY severity"
    ).fetchall()
    conn.close()
    result = {"critical": 0, "warning": 0, "info": 0}
    for r in rows:
        result[r["severity"]] = r["count"]
    return result

def get_recent_alert_exists(server_id, severity, message_prefix, cooldown_seconds):
    since = (datetime.utcnow() - timedelta(seconds=cooldown_seconds)).isoformat()
    conn = get_connection()
    row = conn.execute(
        "SELECT COUNT(*) as count FROM alerts WHERE server_id = ? AND severity = ? AND message LIKE ? AND timestamp > ?",
        (server_id, severity, message_prefix + "%", since),
    ).fetchone()
    conn.close()
    return row["count"] > 0

def prune_old_data(days=7):
    cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()
    conn = get_connection()
    conn.execute("DELETE FROM metrics WHERE timestamp < ?", (cutoff,))
    conn.execute("DELETE FROM services WHERE timestamp < ?", (cutoff,))
    conn.execute("DELETE FROM alerts WHERE timestamp < ? AND acknowledged = 1", (cutoff,))
    conn.commit()
    conn.close()
