(function () {
    const KEY = "omniwatch-theme";

    function getSaved() {
        try { return localStorage.getItem(KEY); } catch (e) { return null; }
    }

    function getPreferred() {
        if (window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches) {
            return "light";
        }
        return "dark";
    }

    function apply(theme) {
        document.documentElement.setAttribute("data-theme", theme);
        document.documentElement.classList.toggle("light", theme === "light");
        try { localStorage.setItem(KEY, theme); } catch (e) {}
        const btn = document.getElementById("theme-toggle");
        if (btn) btn.textContent = theme === "light" ? "🌙" : "☀️";
    }

    window.omniwatchTheme = {
        current: function () { return getSaved() || getPreferred(); },
        toggle: function () {
            const next = (getSaved() || getPreferred()) === "light" ? "dark" : "light";
            apply(next);
        },
        init: function () { apply(getSaved() || getPreferred()); }
    };

    window.omniwatchTheme.init();
})();
