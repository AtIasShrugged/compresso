# Templates

## Base Layout

- **base.html**: container, header with locale/theme switchers, footer.
- **CSS**:
  - grid/flex, max-width container, typography via CSS variables,
  - dark theme `[data-theme="dark"]`,
  - responsive: one column → two on tablet → three on desktop where needed.

## Components

- **form_controls.html**: radio for detail, select for model, input/url/textarea per active tab.
- **JS**: `theme.js` (toggle + persist), `i18n.js` (cookie lang).
