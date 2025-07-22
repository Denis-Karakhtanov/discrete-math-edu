import os
import shutil

class FileManager:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def save_file(self, source_path, destination_name):
        """Сохраняет файл source_path как destination_name в директории base_dir."""
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"Файл '{source_path}' не найден")
        destination_path = os.path.join(self.base_dir, destination_name)
        try:
            shutil.copy(source_path, destination_path)
        except Exception as e:
            raise IOError(f"Ошибка при копировании файла: {e}")
        return destination_path

    def get_file_path(self, file_name):
        """Возвращает абсолютный путь к файлу, если он существует."""
        path = os.path.join(self.base_dir, file_name)
        return path if os.path.exists(path) else None

    def delete_file(self, file_name):
        """Удаляет файл из директории, если он существует."""
        path = os.path.join(self.base_dir, file_name)
        if os.path.exists(path):
            os.remove(path)
            return True
        return False

    def list_files(self):
        """Возвращает список всех файлов в директории."""
        return [f for f in os.listdir(self.base_dir) if os.path.isfile(os.path.join(self.base_dir, f))]

    def exists(self, file_name):
        """Проверяет наличие файла в директории."""
        return os.path.exists(os.path.join(self.base_dir, file_name))
