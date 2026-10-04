(function () {
    const REFRESH_MS = 15000;

    function severityClass(sev) {
        if (sev === "critical") return "sev-critical";
        if (sev === "warning") return "sev-warning";
        return "sev-info";
    }

    function applyBarColor() {
        document.querySelectorAll(".server-card").forEach(function (card) {
            card.querySelectorAll(".bar-fill").forEach(function (fill) {
                const val = parseFloat(fill.dataset.value) || 0;
                fill.style.width = val + "%";
                if (val >= 90) {
                    fill.style.background = "#ef4444";
                } else if (val >= 75) {
                    fill.style.background = "#f59e0b";
                } else {
                    fill.style.background = "#22c55e";
                }
            });
        });
    }

    function buildAlertRow(a) {
        const tr = document.createElement("tr");
        tr.className = severityClass(a.severity);
        tr.innerHTML =
            '<td><span class="sev-dot"></span>' + a.severity + "</td>" +
            "<td>" + (a.server_name || "") + "</td>" +
            "<td>" + (a.server_location || "") + "</td>" +
            "<td>" + (a.message || "") + "</td>" +
            "<td>" + (a.timestamp ? a.timestamp.slice(0, 19) : "") + "</td>";
        return tr;
    }

    function refreshAlerts() {
        fetch("/api/alerts")
            .then(function (r) { return r.json(); })
            .then(function (alerts) {
                const tbody = document.querySelector(".alert-table tbody");
                if (!tbody) return;
                tbody.innerHTML = "";
                if (!alerts.length) {
                    const tr = document.createElement("tr");
                    tr.innerHTML = '<td colspan="5" class="empty">Sin alertas registradas</td>';
                    tbody.appendChild(tr);
                    return;
                }
                alerts.slice(0, 20).forEach(function (a) {
                    tbody.appendChild(buildAlertRow(a));
                });
            })
            .catch(function () {});
    }

    function refreshServerCards() {
        fetch("/api/servers")
            .then(function (r) { return r.json(); })
            .then(function (data) {
                data.forEach(function (item) {
                    const card = document.querySelector('a.server-card[href*="/server/' + item.server.id + '"]');
                    if (!card || !item.metrics) return;

                    const vals = card.querySelectorAll(".bar-val");
                    const fills = card.querySelectorAll(".bar-fill");

                    if (vals[0]) vals[0].textContent = item.metrics.cpu + "%";
                    if (vals[1]) vals[1].textContent = item.metrics.ram + "%";
                    if (vals[2]) vals[2].textContent = item.metrics.disk + "%";

                    if (fills[0]) fills[0].dataset.value = item.metrics.cpu;
                    if (fills[1]) fills[1].dataset.value = item.metrics.ram;
                    if (fills[2]) fills[2].dataset.value = item.metrics.disk;
                });
                applyBarColor();
            })
            .catch(function () {});
    }

    function refreshTimestamp() {
        const el = document.querySelector(".timestamp");
        if (!el) return;
        const now = new Date();
        el.textContent = "Actualizado: " + now.toISOString().slice(0, 19).replace("T", " ") + " UTC";
    }

    function tick() {
        refreshAlerts();
        refreshServerCards();
        refreshTimestamp();
    }

    document.addEventListener("DOMContentLoaded", function () {
        applyBarColor();
        setInterval(tick, REFRESH_MS);
    });
})();
