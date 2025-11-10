# Localization

- `infra/i18n/locale.py` — loads JSON dictionaries `locales/en.json`, `locales/ru.json`.
- Locale selection: cookie lang, then Accept-Language, then default.
- In templates: filter `{{ _("Summary") }}`.
- JS locale switcher — writes cookie, redirects.

## Dark/Light Theme

- CSS variables in `:root` and `[data-theme="dark"]`.
- `prefers-color-scheme` as default; UI switcher saves to localStorage and (opt.) cookie.
