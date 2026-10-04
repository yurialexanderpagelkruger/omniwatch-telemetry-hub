import random
import math
import time
from datetime import datetime
import database

SERVER_PROFILES = {
    "srv-core-01": {"cpu": 45, "ram": 60, "disk": 55, "bias": 1.0},
    "srv-core-02": {"cpu": 30, "ram": 50, "disk": 45, "bias": 0.9},
    "srv-app-01": {"cpu": 55, "ram": 70, "disk": 65, "bias": 1.1},
    "srv-db-01": {"cpu": 70, "ram": 80, "disk": 85, "bias": 1.2},
    "srv-edge-01": {"cpu": 25, "ram": 40, "disk": 35, "bias": 0.8},
    "srv-cache-01": {"cpu": 60, "ram": 75, "disk": 50, "bias": 1.0},
}

SERVICES = ["nginx", "postgresql", "redis", "docker", "ssh"]

_phase = time.time()

def _wave(base, amplitude, period, phase_offset=0):
    global _phase
    return base + amplitude * math.sin((_phase + phase_offset) / period)

def _clamp(value, low=1.0, high=99.0):
    return max(low, min(high, value))

def _random_service_status():
    r = random.random()
    if r < 0.02:
        return "stopped"
    if r < 0.05:
        return "degraded"
    return "running"

def generate_and_store(server):
    profile = SERVER_PROFILES.get(server["name"], {"cpu": 40, "ram": 50, "disk": 50, "bias": 1.0})

    cpu = _clamp(_wave(profile["cpu"], 20, 40, profile["bias"] * 5) + random.uniform(-5, 5))
    ram = _clamp(_wave(profile["ram"], 15, 60, profile["bias"] * 8) + random.uniform(-3, 3))
    disk = _clamp(profile["disk"] + random.uniform(-1, 2), high=98.0)

    net_in = round(abs(_wave(120, 80, 30) + random.uniform(-20, 20)), 2)
    net_out = round(abs(_wave(90, 60, 35) + random.uniform(-15, 15)), 2)

    uptime = int(time.time()) - random.randint(3600, 864000)

    database.insert_metric(
        server["id"],
        round(cpu, 2),
        round(ram, 2),
        round(disk, 2),
        net_in,
        net_out,
        uptime,
    )

    for svc in SERVICES:
        status = _random_service_status()
        if svc == "postgresql" and server["name"] == "srv-db-01":
            status = "running" if random.random() > 0.08 else "stopped"
        database.insert_service(server["id"], svc, status)

def run_simulation_cycle():
    global _phase
    _phase = time.time()
    servers = database.get_servers()
    for server in servers:
        generate_and_store(server)
