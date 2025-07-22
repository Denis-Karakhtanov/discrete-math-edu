import os
import shutil

class FileManager:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def save_file(self, source_path, destination_name):
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"Файл {source_path} не найден")
        destination_path = os.path.join(self.base_dir, destination_name)
        shutil.copy(source_path, destination_path)
        return destination_path

    def get_file_path(self, file_name):
        file_path = os.path.join(self.base_dir, file_name)
        if os.path.exists(file_path):
            return file_path
        return None

    def delete_file(self, file_name):
        file_path = os.path.join(self.base_dir, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False

    def list_files(self):
        return [f for f in os.listdir(self.base_dir) if os.path.isfile(os.path.join(self.base_dir, f))]
