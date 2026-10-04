import os
from datetime import datetime
from flask import Flask, render_template, jsonify, abort
from apscheduler.schedulers.background import BackgroundScheduler
from config import Config
import database
import simulator
import collector
import alerter

app = Flask(__name__)
app.config.from_object(Config)

database.init_db()
database.seed_servers()

def collection_job():
    if Config.DEMO_MODE:
        simulator.run_simulation_cycle()
    else:
        collector.run_collection_cycle()
    alerter.run_alert_cycle()

def maintenance_job():
    database.prune_old_data(days=7)

scheduler = BackgroundScheduler()
scheduler.add_job(collection_job, "interval", seconds=Config.COLLECT_INTERVAL_SECONDS, id="collection")
scheduler.add_job(maintenance_job, "interval", hours=6, id="maintenance")
if not scheduler.running:
    scheduler.start()

@app.route("/")
def dashboard():
    servers = database.get_servers()
    enriched = []
    for s in servers:
        metrics = database.get_latest_metrics(s["id"])
        services = database.get_latest_services(s["id"])
        down_services = [svc["name"] for svc in services if svc["status"] != "running"]
        health = "healthy"
        if metrics:
            if metrics["cpu"] >= 85 or metrics["ram"] >= 90 or metrics["disk"] >= 90 or down_services:
                health = "critical"
            elif metrics["cpu"] >= 75 or metrics["ram"] >= 80 or metrics["disk"] >= 80:
                health = "warning"
        enriched.append({
            "server": s,
            "metrics": metrics,
            "health": health,
            "down_services": down_services,
            "service_count": len(services),
        })
    alerts = database.get_recent_alerts(20)
    alert_counts = database.get_alert_count_by_severity()
    total_servers = len(servers)
    healthy = sum(1 for e in enriched if e["health"] == "healthy")

    return render_template(
        "dashboard.html",
        servers=enriched,
        alerts=alerts,
        alert_counts=alert_counts,
        total_servers=total_servers,
        healthy_count=healthy,
        demo_mode=Config.DEMO_MODE,
        generated_at=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
    )

@app.route("/server/<int:server_id>")
def server_detail(server_id):
    server = database.get_server(server_id)
    if not server:
        abort(404)
    metrics = database.get_latest_metrics(server_id)
    history = database.get_metrics_history(server_id, limit=60)
    services = database.get_latest_services(server_id)
    alerts = [a for a in database.get_recent_alerts(100) if a["server_id"] == server_id]
    return render_template(
        "detail.html",
        server=server,
        metrics=metrics,
        history=history,
        services=services,
        alerts=alerts,
    )

@app.errorhandler(404)
def not_found(e):
    return render_template("base.html", error="Recurso no encontrado"), 404

@app.route("/api/servers")
def api_servers():
    result = []
    for s in database.get_servers():
        metrics = database.get_latest_metrics(s["id"])
        result.append({"server": s, "metrics": metrics})
    return jsonify(result)

@app.route("/api/server/<int:server_id>/history")
def api_history(server_id):
    return jsonify(database.get_metrics_history(server_id, limit=60))

@app.route("/api/alerts")
def api_alerts():
    return jsonify(database.get_recent_alerts(50))

@app.route("/api/summary")
def api_summary():
    return jsonify({
        "servers": len(database.get_servers()),
        "alerts_by_severity": database.get_alert_count_by_severity(),
        "generated_at": datetime.utcnow().isoformat(),
    })

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "omniwatch"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
