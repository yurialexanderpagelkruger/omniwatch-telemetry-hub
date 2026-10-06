TRANSLATIONS = {
    "en": {
        "app_name": "OmniWatch",
        "app_tagline": "Centralized Telemetry",
        "nav_dashboard": "Dashboard",
        "nav_api": "API",
        "nav_health": "Health",
        "dashboard_title": "Centralized Panel",
        "demo_live": "LIVE DEMO",
        "updated": "Updated",
        "kpi_servers": "Servers",
        "kpi_healthy": "Healthy",
        "kpi_critical": "Critical Alerts",
        "kpi_warning": "Warnings",
        "servers_monitored": "Monitored Servers",
        "recent_alerts": "Recent Alerts",
        "col_severity": "Severity",
        "col_server": "Server",
        "col_location": "Location",
        "col_message": "Message",
        "col_date": "Date (UTC)",
        "no_alerts": "No alerts registered",
        "no_data": "No data",
        "services": "Services",
        "down": "Down",
        "critical": "critical",
        "warning": "warning",
        "info": "info",
        "healthy": "healthy",
        "back": "← Back to panel",
        "cpu": "CPU",
        "ram": "RAM",
        "disk": "DISK",
        "disco": "Disk",
        "uptime": "Uptime",
        "history_title": "CPU / RAM / Disk History",
        "server_alerts": "Server Alerts",
        "severity": "Severity",
        "message": "Message",
        "date_utc": "Date (UTC)",
        "no_alerts_server": "No alerts",
        "running": "running",
        "stopped": "stopped",
        "degraded": "degraded",
        "unknown": "unknown",
        "lang_es": "ES",
        "lang_en": "EN",
        "lang_pt": "PT",
        "theme_dark": "Dark",
        "theme_light": "Light",
        "footer": "OmniWatch © 2026 — Early Detection & Multi-Site Alerts",
    },
    "es": {
        "app_name": "OmniWatch",
        "app_tagline": "Telemetría Centralizada",
        "nav_dashboard": "Panel",
        "nav_api": "API",
        "nav_health": "Salud",
        "dashboard_title": "Panel Centralizado",
        "demo_live": "DEMO EN VIVO",
        "updated": "Actualizado",
        "kpi_servers": "Servidores",
        "kpi_healthy": "Saludables",
        "kpi_critical": "Alertas Críticas",
        "kpi_warning": "Advertencias",
        "servers_monitored": "Servidores Monitoreados",
        "recent_alerts": "Alertas Recientes",
        "col_severity": "Severidad",
        "col_server": "Servidor",
        "col_location": "Sede",
        "col_message": "Mensaje",
        "col_date": "Fecha (UTC)",
        "no_alerts": "Sin alertas registradas",
        "no_data": "Sin datos",
        "services": "Servicios",
        "down": "Caídos",
        "critical": "crítica",
        "warning": "advertencia",
        "info": "info",
        "healthy": "saludable",
        "back": "← Volver al panel",
        "cpu": "CPU",
        "ram": "RAM",
        "disk": "DISCO",
        "disco": "Disco",
        "uptime": "Uptime",
        "history_title": "Histórico de CPU / RAM / Disco",
        "server_alerts": "Alertas del Servidor",
        "severity": "Severidad",
        "message": "Mensaje",
        "date_utc": "Fecha (UTC)",
        "no_alerts_server": "Sin alertas",
        "running": "activo",
        "stopped": "detenido",
        "degraded": "degradado",
        "unknown": "desconocido",
        "lang_es": "ES",
        "lang_en": "EN",
        "lang_pt": "PT",
        "theme_dark": "Oscuro",
        "theme_light": "Claro",
        "footer": "OmniWatch © 2026 — Detección Temprana y Alertas Multi-Sede",
    },
    "pt": {
        "app_name": "OmniWatch",
        "app_tagline": "Telemetria Centralizada",
        "nav_dashboard": "Painel",
        "nav_api": "API",
        "nav_health": "Saúde",
        "dashboard_title": "Painel Centralizado",
        "demo_live": "DEMO AO VIVO",
        "updated": "Atualizado",
        "kpi_servers": "Servidores",
        "kpi_healthy": "Saudáveis",
        "kpi_critical": "Alertas Críticos",
        "kpi_warning": "Avisos",
        "servers_monitored": "Servidores Monitorados",
        "recent_alerts": "Alertas Recentes",
        "col_severity": "Severidade",
        "col_server": "Servidor",
        "col_location": "Local",
        "col_message": "Mensagem",
        "col_date": "Data (UTC)",
        "no_alerts": "Nenhum alerta registrado",
        "no_data": "Sem dados",
        "services": "Serviços",
        "down": "Fora do ar",
        "critical": "crítico",
        "warning": "aviso",
        "info": "info",
        "healthy": "saudável",
        "back": "← Voltar ao painel",
        "cpu": "CPU",
        "ram": "RAM",
        "disk": "DISCO",
        "disco": "Disco",
        "uptime": "Uptime",
        "history_title": "Histórico de CPU / RAM / Disco",
        "server_alerts": "Alertas do Servidor",
        "severity": "Severidade",
        "message": "Mensagem",
        "date_utc": "Data (UTC)",
        "no_alerts_server": "Sem alertas",
        "running": "ativo",
        "stopped": "parado",
        "degraded": "degradado",
        "unknown": "desconhecido",
        "lang_es": "ES",
        "lang_en": "EN",
        "lang_pt": "PT",
        "theme_dark": "Escuro",
        "theme_light": "Claro",
        "footer": "OmniWatch © 2026 — Detecção Precoce e Alertas Multi-Local",
    },
}

SPANISH_COUNTRIES = {"AR", "ES", "MX", "CO", "CL", "PE", "VE", "EC", "UY", "PY", "BO", "CR", "CU", "DO", "GT", "HN", "NI", "PA", "PR", "SV"}
PORTUGUESE_COUNTRIES = {"BR", "PT", "AO", "MZ", "CV", "GW", "ST", "TL"}

def detect_language(accept_language_header, country_code=None):
    if country_code:
        code = country_code.upper()
        if code in SPANISH_COUNTRIES:
            return "es"
        if code in PORTUGUESE_COUNTRIES:
            return "pt"

    if accept_language_header:
        langs = []
        for part in accept_language_header.split(","):
            part = part.strip()
            if not part:
                continue
            token = part.split(";")[0].strip().lower()
            langs.append(token)
        for lang in langs:
            if lang.startswith("es"):
                return "es"
            if lang.startswith("pt"):
                return "pt"
            if lang.startswith("en"):
                return "en"

    return "en"

def get_text(lang, key):
    lang = lang if lang in TRANSLATIONS else "en"
    return TRANSLATIONS[lang].get(key, TRANSLATIONS["en"].get(key, key))
