import os
from datetime import datetime

class Logger:
    def __init__(self):
        """Инициализация логгера"""
        self.log_file = "logs/app.log"
        if not os.path.exists("logs"):
            os.makedirs("logs")
    
    def log(self, message):
        """Запись сообщения в лог"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")
    
    def get_logs(self):
        """Получение всех логов"""
        if os.path.exists(self.log_file):
            with open(self.log_file, "r", encoding="utf-8") as f:
                return f.readlines()
        return []