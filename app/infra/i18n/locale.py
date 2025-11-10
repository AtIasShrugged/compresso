"""Internationalization locale manager."""
import json
from pathlib import Path
from typing import Dict
from loguru import logger


class LocaleManager:
    """Manages locale translations."""
    
    def __init__(self, locales_dir: str = "locales", default_locale: str = "en"):
        self.locales_dir = Path(locales_dir)
        self.default_locale = default_locale
        self._translations: Dict[str, Dict[str, str]] = {}
        self._load_translations()
    
    def _load_translations(self) -> None:
        """Load all translation files."""
        if not self.locales_dir.exists():
            logger.warning(f"Locales directory not found: {self.locales_dir}")
            return
        
        for locale_file in self.locales_dir.glob("*.json"):
            locale = locale_file.stem
            try:
                with open(locale_file, "r", encoding="utf-8") as f:
                    self._translations[locale] = json.load(f)
                logger.info(f"Loaded translations for locale: {locale}")
            except Exception as e:
                logger.error(f"Failed to load translations for {locale}: {e}")
    
    def get(self, key: str, locale: str) -> str:
        """Get translation for key in specified locale.
        
        Args:
            key: Translation key
            locale: Locale code
            
        Returns:
            Translated string or key if not found
        """
        translations = self._translations.get(locale, {})
        if key in translations:
            return translations[key]
        
        # Fallback to default locale
        if locale != self.default_locale:
            default_translations = self._translations.get(self.default_locale, {})
            if key in default_translations:
                return default_translations[key]
        
        # Return key as fallback
        return key
    
    def get_available_locales(self) -> list[str]:
        """Get list of available locales."""
        return list(self._translations.keys())


# Global locale manager instance
locale_manager = LocaleManager()
