import json
import os

class SettingsManager:
    def __init__(self, app):
        """Инициализация менеджера настроек"""
        self.app = app
        self.settings_file = "settings.json"
        self.default_settings = {
            "theme": "light",
            "font_size": 12,
            "language": "Русский"
        }
        self.settings = self.load_settings()
    
    def load_settings(self):
        """Загрузка настроек из файла"""
        if os.path.exists(self.settings_file):
            with open(self.settings_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return self.default_settings
    
    def save_settings(self):
        """Сохранение настроек в файл"""
        with open(self.settings_file, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=4)
    
    def get_setting(self, key):
        """Получение настройки"""
        return self.settings.get(key, self.default_settings[key])
    
    def update_setting(self, key, value):
        """Обновление настройки"""
        self.settings[key] = value
        self.save_settings()