(function () {
    const KEY = "omniwatch-lang";
    const SUPPORTED = ["en", "es", "pt"];

    function detect() {
        try {
            const saved = localStorage.getItem(KEY);
            if (saved && SUPPORTED.indexOf(saved) !== -1) return saved;
        } catch (e) {}

        const nav = (navigator.language || navigator.userLanguage || "en").toLowerCase();
        if (nav.startsWith("es")) return "es";
        if (nav.startsWith("pt")) return "pt";
        return "en";
    }

    window.omniwatchLang = {
        current: detect,
        set: function (lang) {
            if (SUPPORTED.indexOf(lang) === -1) lang = "en";
            try { localStorage.setItem(KEY, lang); } catch (e) {}
            document.cookie = "lang=" + lang + ";path=/;max-age=31536000";
            window.location.reload();
        }
    };

    document.addEventListener("DOMContentLoaded", function () {
        const sel = document.getElementById("lang-select");
        if (sel) sel.value = detect();
    });
})();
