import socket
import psutil
from datetime import datetime
import database
from config import Config

SERVICES_TO_MONITOR = ["nginx", "postgresql", "redis", "docker", "ssh"]

def collect_local_metrics():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent

    net = psutil.net_io_counters()
    net_in = round(net.bytes_recv / 1024 / 1024, 2)
    net_out = round(net.bytes_sent / 1024 / 1024, 2)

    boot_time = psutil.boot_time()
    uptime = int((datetime.now() - datetime.fromtimestamp(boot_time)).total_seconds())

    return {
        "cpu": round(cpu, 2),
        "ram": round(ram, 2),
        "disk": round(disk, 2),
        "net_in": net_in,
        "net_out": net_out,
        "uptime": uptime,
    }

def check_services():
    results = []
    for svc in SERVICES_TO_MONITOR:
        try:
            proc = next(
                (p for p in psutil.process_iter(["name"]) if svc in (p.info["name"] or "").lower()),
                None,
            )
            status = "running" if proc else "stopped"
        except Exception:
            status = "unknown"
        results.append({"name": svc, "status": status})
    return results

def check_port(host, port=22, timeout=2):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False

def run_collection_cycle():
    servers = database.get_servers()
    for server in servers:
        metrics = collect_local_metrics()
        database.insert_metric(
            server["id"],
            metrics["cpu"],
            metrics["ram"],
            metrics["disk"],
            metrics["net_in"],
            metrics["net_out"],
            metrics["uptime"],
        )
        for svc in check_services():
            database.insert_service(server["id"], svc["name"], svc["status"])
