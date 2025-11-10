// Locale management
(function() {
    const langSelect = document.getElementById('lang-select');
    
    if (langSelect) {
        langSelect.addEventListener('change', (e) => {
            const locale = e.target.value;
            // Set cookie and reload
            document.cookie = `lang=${locale}; path=/; max-age=31536000; SameSite=Lax`;
            window.location.reload();
        });
    }
})();
