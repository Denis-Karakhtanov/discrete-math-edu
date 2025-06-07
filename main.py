import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import psycopg2
import os
import sys
import random
import hashlib
from datetime import datetime
import json
from PIL import Image, ImageTk
import vlc
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Импорт модулей приложения
from gui import MainGUI
from database import Database
from test_generator import TestGenerator
from video_player import VideoPlayer
from animation import AnimationManager
from file_manager import FileManager
from report_generator import ReportGenerator
from settings import SettingsManager
from logger import Logger

# Основной класс приложения
class DiscreteMathApp:
    def __init__(self, root):
        """Инициализация приложения"""
        self.root = root
        self.root.title("Обучающее приложение по дискретной математике")
        self.root.geometry("1000x700")
        self.db = Database()
        self.file_manager = FileManager("data")  
        self.logger = Logger()
        self.current_user = None
        self.current_role = None
        self.settings = SettingsManager(self)
        self.gui = MainGUI(self)
        self.test_generator = TestGenerator(self.db)
        self.video_player = VideoPlayer(self.root)
        self.animation_manager = AnimationManager(self)
        self.report_generator = ReportGenerator()
        
        # Роли пользователей
        self.roles = ["Администратор", "Преподаватель", "Студент"]
        self.setup_database()
        self.apply_settings()
        self.show_login_screen()
        self.logger.log("Приложение запущено")
    
    def setup_database(self):
        """Инициализация базы данных"""
        try:
            self.db.create_tables()
            self.db.insert_test_data()
            self.logger.log("База данных успешно инициализирована")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось инициализировать базу данных: {str(e)}")
            self.logger.log(f"Ошибка инициализации базы данных: {str(e)}")
    
    def apply_settings(self):
        """Применение настроек интерфейса"""
        theme = self.settings.get_setting("theme")
        if theme == "dark":
            self.root.configure(bg="#333333")
        else:
            self.root.configure(bg="white")
    
    def show_login_screen(self):
        """Экран входа"""
        self.gui.clear_frame()
        tk.Label(self.gui.main_frame, text="Вход в систему", font=("Arial", 18, "bold")).pack(pady=30)
        
        tk.Label(self.gui.main_frame, text="Логин:", font=("Arial", 12)).pack()
        login_entry = tk.Entry(self.gui.main_frame, font=("Arial", 12))
        login_entry.pack(pady=10)
        
        tk.Label(self.gui.main_frame, text="Пароль:", font=("Arial", 12)).pack()
        password_entry = tk.Entry(self.gui.main_frame, show="*", font=("Arial", 12))
        password_entry.pack(pady=10)
        
        tk.Label(self.gui.main_frame, text="Роль:", font=("Arial", 12)).pack()
        role_combobox = ttk.Combobox(self.gui.main_frame, values=self.roles, state="readonly", font=("Arial", 12))
        role_combobox.set("Студент")
        role_combobox.pack(pady=10)
        
        tk.Button(self.gui.main_frame, text="Войти", font=("Arial", 12), 
                 command=lambda: self.login(login_entry.get(), password_entry.get(), role_combobox.get())).pack(pady=20)
        tk.Button(self.gui.main_frame, text="Настройки", font=("Arial", 12), 
                 command=self.show_settings).pack(pady=10)
        self.logger.log("Открыт экран входа")
    
    def login(self, login, password, role):
        """Аутентификация пользователя"""
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user = self.db.get_user(login, hashed_password, role)
        if user:
            self.current_user = user[1]
            self.current_role = user[3]
            self.logger.log(f"Успешный вход: {self.current_user} ({self.current_role})")
            self.show_main_menu()
        else:
            messagebox.showerror("Ошибка", "Неверный логин, пароль или роль")
            self.logger.log(f"Неуспешная попытка входа: {login}, роль: {role}")
    
    def show_main_menu(self):
        """Главное меню"""
        self.gui.clear_frame()
        tk.Label(self.gui.main_frame, text=f"Добро пожаловать, {self.current_user} ({self.current_role})", 
                font=("Arial", 18, "bold")).pack(pady=30)
        
        if self.current_role == "Администратор":
            tk.Button(self.gui.main_frame, text="Панель администратора", font=("Arial", 12), 
                     command=self.show_admin_panel).pack(pady=10)
        if self.current_role in ["Администратор", "Преподаватель"]:
            tk.Button(self.gui.main_frame, text="Управление материалами", font=("Arial", 12), 
                     command=self.show_material_management).pack(pady=10)
            tk.Button(self.gui.main_frame, text="Создать тест", font=("Arial", 12), 
                     command=self.show_test_creation).pack(pady=10)
            tk.Button(self.gui.main_frame, text="Аналитика результатов", font=("Arial", 12), 
                     command=self.show_analytics).pack(pady=10)
        tk.Button(self.gui.main_frame, text="Просмотр материалов", font=("Arial", 12), 
                 command=self.show_materials).pack(pady=10)
        tk.Button(self.gui.main_frame, text="Пройти тест", font=("Arial", 12), 
                 command=self.show_test_selection).pack(pady=10)
        tk.Button(self.gui.main_frame, text="Видеоуроки", font=("Arial", 12), 
                 command=self.show_video_player).pack(pady=10)
        tk.Button(self.gui.main_frame, text="Анимации", font=("Arial", 12), 
                 command=self.show_animations).pack(pady=10)
        tk.Button(self.gui.main_frame, text="Личный кабинет", font=("Arial", 12), 
                 command=self.show_user_profile).pack(pady=10)
        tk.Button(self.gui.main_frame, text="Настройки", font=("Arial", 12), 
                 command=self.show_settings).pack(pady=10)
        tk.Button(self.gui.main_frame, text="Справка", font=("Arial", 12), 
                 command=self.show_help).pack(pady=10)
        tk.Button(self.gui.main_frame, text="Выйти", font=("Arial", 12), 
                 command=self.show_login_screen).pack(pady=10)
        self.logger.log("Открыто главное меню")
    
    def show_admin_panel(self):
        """Панель администратора"""
        self.gui.clear_frame()
        tk.Label(self.gui.main_frame, text="Панель администратора", font=("Arial", 18, "bold")).pack(pady=30)
        
        tk.Button(self.gui.main_frame, text="Добавить пользователя", font=("Arial", 12), 
                 command=self.show_add_user).pack(pady=10)
        tk.Button(self.gui.main_frame, text="Редактировать пользователя", font=("Arial", 12), 
                 command=self.show_edit_user).pack(pady=10)
        tk.Button(self.gui.main_frame, text="Удалить пользователя", font=("Arial", 12), 
                 command=self.show_delete_user).pack(pady=10)
        tk.Button(self.gui.main_frame, text="Список пользователей", font=("Arial", 12), 
                 command=self.show_user_list).pack(pady=10)
        tk.Button(self.gui.main_frame, text="Логи системы", font=("Arial", 12), 
                 command=self.show_logs).pack(pady=10)
        tk.Button(self.gui.main_frame, text="Назад", font=("Arial", 12), 
                 command=self.show_main_menu).pack(pady=10)
        self.logger.log("Открыта панель администратора")
    
    def show_add_user(self):
        """Добавление пользователя"""
        self.gui.clear_frame()
        tk.Label(self.gui.main_frame, text="Добавить пользователя", font=("Arial", 18, "bold")).pack(pady=30)
        
        tk.Label(self.gui.main_frame, text="Логин:", font=("Arial", 12)).pack()
        login_entry = tk.Entry(self.gui.main_frame, font=("Arial", 12))
        login_entry.pack(pady=10)
        
        tk.Label(self.gui.main_frame, text="Пароль:", font=("Arial", 12)).pack()
        password_entry = tk.Entry(self.gui.main_frame, show="*", font=("Arial", 12))
        password_entry.pack(pady=10)
        
        tk.Label(self.gui.main_frame, text="Роль:", font=("Arial", 12)).pack()
        role_combobox = ttk.Combobox(self.gui.main_frame, values=self.roles, state="readonly", font=("Arial", 12))
        role_combobox.set("Студент")
        role_combobox.pack(pady=10)
        
        tk.Label(self.gui.main_frame, text="Имя:", font=("Arial", 12)).pack()
        name_entry = tk.Entry(self.gui.main_frame, font=("Arial", 12))
        name_entry.pack(pady=10)
        
        tk.Button(self.gui.main_frame, text="Сохранить", font=("Arial", 12), 
                 command=lambda: self.add_user(login_entry.get(), password_entry.get(), role_combobox.get(), name_entry.get())).pack(pady=20)
        tk.Button(self.gui.main_frame, text="Назад", font=("Arial", 12), 
                 command=self.show_admin_panel).pack(pady=10)
        self.logger.log("Открыт экран добавления пользователя")
    
    def add_user(self, login, password, role, name):
        """Сохранение нового пользователя"""
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        try:
            self.db.add_user(login, hashed_password, role, name)
            messagebox.showinfo("Успех", "Пользователь добавлен")
            self.logger.log(f"Добавлен пользователь: {login}")
            self.show_admin_panel()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить пользователя: {str(e)}")
            self.logger.log(f"Ошибка добавления пользователя {login}: {str(e)}")
    
    def show_edit_user(self):
        """Редактирование пользователя"""
        self.gui.clear_frame()
        tk.Label(self.gui.main_frame, text="Редактировать пользователя", font=("Arial", 18, "bold")).pack(pady=30)
        
        users = self.db.get_all_users()
        tk.Label(self.gui.main_frame, text="Выберите пользователя:", font=("Arial", 12)).pack()
        user_combobox = ttk.Combobox(self.gui.main_frame, values=[u[1] for u in users], state="readonly", font=("Arial", 12))
        user_combobox.pack(pady=10)
        
        tk.Label(self.gui.main_frame, text="Новый пароль:", font=("Arial", 12)).pack()
        password_entry = tk.Entry(self.gui.main_frame, show="*", font=("Arial", 12))
        password_entry.pack(pady=10)
        
        tk.Label(self.gui.main_frame, text="Новая роль:", font=("Arial", 12)).pack()
        role_combobox = ttk.Combobox(self.gui.main_frame, values=self.roles, state="readonly", font=("Arial", 12))
        role_combobox.set("Студент")
        role_combobox.pack(pady=10)
        
        tk.Label(self.gui.main_frame, text="Новое имя:", font=("Arial", 12)).pack()
        name_entry = tk.Entry(self.gui.main_frame, font=("Arial", 12))
        name_entry.pack(pady=10)
        
        tk.Button(self.gui.main_frame, text="Сохранить", font=("Arial", 12), 
                 command=lambda: self.edit_user(user_combobox.get(), password_entry.get(), role_combobox.get(), name_entry.get())).pack(pady=20)
        tk.Button(self.gui.main_frame, text="Назад", font=("Arial", 12), 
                 command=self.show_admin_panel).pack(pady=10)
        self.logger.log("Открыт экран редактирования пользователя")
    
    def edit_user(self, login, password, role, name):
        """Сохранение изменений пользователя"""
        hashed_password = hashlib.sha256(password.encode()).hexdigest() if password else None
        try:
            self.db.update_user(login, hashed_password, role, name)
            messagebox.showinfo("Успех", "Пользователь обновлен")
            self.logger.log(f"Обновлен пользователь: {login}")
            self.show_admin_panel()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить пользователя: {str(e)}")
            self.logger.log(f"Ошибка обновления пользователя {login}: {str(e)}")
    
    def show_delete_user(self):
        """Удаление пользователя"""
        self.gui.clear_frame()
        tk.Label(self.gui.main_frame, text="Удалить пользователя", font=("Arial", 18, "bold")).pack(pady=30)
        
        users = self.db.get_all_users()
        tk.Label(self.gui.main_frame, text="Выберите пользователя:", font=("Arial", 12)).pack()
        user_combobox = ttk.Combobox(self.gui.main_frame, values=[u[1] for u in users], state="readonly", font=("Arial", 12))
        user_combobox.pack(pady=10)
        
        tk.Button(self.gui.main_frame, text="Удалить", font=("Arial", 12), 
                 command=lambda: self.delete_user(user_combobox.get())).pack(pady=20)
        tk.Button(self.gui.main_frame, text="Назад", font=("Arial", 12), 
                 command=self.show_admin_panel).pack(pady=10)
        self.logger.log("Открыт экран удаления пользователя")
    
    def delete_user(self, login):
        """Удаление пользователя"""
        try:
            self.db.delete_user(login)
            messagebox.showinfo("Успех", "Пользователь удален")
            self.logger.log(f"Удален пользователь: {login}")
            self.show_admin_panel()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить пользователя: {str(e)}")
            self.logger.log(f"Ошибка удаления пользователя {login}: {str(e)}")
    
    def show_user_list(self):
        """Список пользователей"""
        self.gui.clear_frame()
        tk.Label(self.gui.main_frame, text="Список пользователей", font=("Arial", 18, "bold")).pack(pady=30)
        
        users = self.db.get_all_users()
        tree = ttk.Treeview(self.gui.main_frame, columns=("Login", "Role", "Name"), show="headings")
        tree.heading("Login", text="Логин")
        tree.heading("Role", text="Роль")
        tree.heading("Name", text="Имя")
        tree.pack(fill="both", expand=True, pady=10)
        
        for user in users:
            tree.insert("", "end", values=(user[1], user[3], user[2]))
        
        tk.Button(self.gui.main_frame, text="Назад", font=("Arial", 12), 
                 command=self.show_admin_panel).pack(pady=10)
        self.logger.log("Открыт список пользователей")
    
    def show_logs(self):
        """Просмотр логов системы"""
        self.gui.clear_frame()
        tk.Label(self.gui.main_frame, text="Логи системы", font=("Arial", 18, "bold")).pack(pady=30)
        
        logs = self.logger.get_logs()
        text_area = tk.Text(self.gui.main_frame, height=20, width=80, font=("Arial", 10))
        text_area.pack(pady=10)
        for log in logs:
            text_area.insert(tk.END, f"{log}\n")
        text_area.config(state="disabled")
        
        tk.Button(self.gui.main_frame, text="Назад", font=("Arial", 12), 
                 command=self.show_admin_panel).pack(pady=10)
        self.logger.log("Открыт просмотр логов")
    
    def show_material_management(self):
        """Управление учебными материалами"""
        self.gui.clear_frame()
        tk.Label(self.gui.main_frame, text="Управление материалами", font=("Arial", 18, "bold")).pack(pady=30)
        
        tk.Button(self.gui.main_frame, text="Добавить материал", font=("Arial", 12), 
                 command=self.show_add_material).pack(pady=10)
        tk.Button(self.gui.main_frame, text="Редактировать материал", font=("Arial", 12), 
                 command=self.show_edit_material).pack(pady=10)
        tk.Button(self.gui.main_frame, text="Удалить материал", font=("Arial", 12), 
                 command=self.show_delete_material).pack(pady=10)
        tk.Button(self.gui.main_frame, text="Список материалов", font=("Arial", 12), 
                 command=self.show_material_list).pack(pady=10)
        tk.Button(self.gui.main_frame, text="Назад", font=("Arial", 12), 
                 command=self.show_main_menu).pack(pady=10)
        self.logger.log("Открыт экран управления материалами")
    
    def show_add_material(self):
        """Добавление материала"""
        self.gui.clear_frame()
        tk.Label(self.gui.main_frame, text="Добавить материал", font=("Arial", 18, "bold")).pack(pady=30)
        
        tk.Label(self.gui.main_frame, text="Тема:", font=("Arial", 12)).pack()
        topic_entry = tk.Entry(self.gui.main_frame, font=("Arial", 12))
        topic_entry.pack(pady=10)
        
        tk.Label(self.gui.main_frame, text="Содержание:", font=("Arial", 12)).pack()
        content_text = tk.Text(self.gui.main_frame, height=10, width=60, font=("Arial", 12))
        content_text.pack(pady=10)
        
        tk.Label(self.gui.main_frame, text="Путь к файлу (видео/изображение):", font=("Arial", 12)).pack()
        file_entry = tk.Entry(self.gui.main_frame, font=("Arial", 12))
        file_entry.pack(pady=10)
        tk.Button(self.gui.main_frame, text="Выбрать файл", font=("Arial", 12), 
                 command=lambda: file_entry.insert(0, filedialog.askopenfilename())).pack(pady=10)
        
        tk.Label(self.gui.main_frame, text="Категория:", font=("Arial", 12)).pack()
        category_combobox = ttk.Combobox(self.gui.main_frame, values=["Логика", "Теория множеств", "Графы", "Комбинаторика"], 
                                        state="readonly", font=("Arial", 12))
        category_combobox.pack(pady=10)
        
        tk.Button(self.gui.main_frame, text="Сохранить", font=("Arial", 12), 
                 command=lambda: self.add_material(topic_entry.get(), content_text.get("1.0", tk.END), 
                                                  file_entry.get(), category_combobox.get())).pack(pady=20)
        tk.Button(self.gui.main_frame, text="Назад", font=("Arial", 12), 
                 command=self.show_material_management).pack(pady=10)
        self.logger.log("Открыт экран добавления материала")
    
    def add_material(self, topic, content, file_path, category):
        """Сохранение материала"""
        try:
            saved_path = self.file_manager.save_file(file_path, os.path.basename(file_path)) if file_path else ""
            self.db.add_material(topic, content, saved_path, category)
            messagebox.showinfo("Успех", "Материал добавлен")
            self.logger.log(f"Добавлен материал: {topic}")
            self.show_material_management()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить материал: {str(e)}")
            self.logger.log(f"Ошибка добавления материала {topic}: {str(e)}")
    
    def show_edit_material(self):
        """Редактирование материала"""
        self.gui.clear_frame()
        tk.Label(self.gui.main_frame, text="Редактировать материал", font=("Arial", 18, "bold")).pack(pady=30)
        
        materials = self.db.get_all_materials()
        tk.Label(self.gui.main_frame, text="Выберите материал:", font=("Arial", 12)).pack()
        material_combobox = ttk.Combobox(self.gui.main_frame, values=[m[1] for m in materials], state="readonly", font=("Arial", 12))
        material_combobox.pack(pady=10)
        
        tk.Label(self.gui.main_frame, text="Новое содержание:", font=("Arial", 12)).pack()
        content_text = tk.Text(self.gui.main_frame, height=10, width=60, font=("Arial", 12))
        content_text.pack(pady=10)
        
        tk.Label(self.gui.main_frame, text="Новый путь к файлу:", font=("Arial", 12)).pack()
        file_entry = tk.Entry(self.gui.main_frame, font=("Arial", 12))
        file_entry.pack(pady=10)
        tk.Button(self.gui.main_frame, text="Выбрать файл", font=("Arial", 12), 
                 command=lambda: file_entry.insert(0, filedialog.askopenfilename())).pack(pady=10)
        
        tk.Label(self.gui.main_frame, text="Категория:", font=("Arial", 12)).pack()
        category_combobox = ttk.Combobox(self.gui.main_frame, values=["Логика", "Теория множеств", "Графы", "Комбинаторика"], 
                                        state="readonly", font=("Arial", 12))
        category_combobox.pack(pady=10)
        
        tk.Button(self.gui.main_frame, text="Сохранить", font=("Arial", 12), 
                 command=lambda: self.edit_material(material_combobox.get(), content_text.get("1.0", tk.END), 
                                                  file_entry.get(), category_combobox.get())).pack(pady=20)
        tk.Button(self.gui.main_frame, text="Назад", font=("Arial", 12), 
                 command=self.show_material_management).pack(pady=10)
        self.logger.log("Открыт экран редактирования материала")
    
    def edit_material(self, topic, content, file_path, category):
        """Сохранение изменений материала"""
        try:
            saved_path = self.file_manager.save_file(file_path, os.path.basename(file_path)) if file_path else ""
            self.db.update_material(topic, content, saved_path, category)
            messagebox.showinfo("Успех", "Материал обновлен")
            self.logger.log(f"Обновлен материал: {topic}")
            self.show_material_management()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить материал: {str(e)}")
            self.logger.log(f"Ошибка обновления материала {topic}: {str(e)}")
    
    def show_delete_material(self):
        """Удаление материала"""
        self.gui.clear_frame()
        tk.Label(self.gui.main_frame, text="Удалить материал", font=("Arial", 18, "bold")).pack(pady=30)
        
        materials = self.db.get_all_materials()
        tk.Label(self.gui.main_frame, text="Выберите материал:", font=("Arial", 12)).pack()
        material_combobox = ttk.Combobox(self.gui.main_frame, values=[m[1] for m in materials], state="readonly", font=("Arial", 12))
        material_combobox.pack(pady=10)
        
        tk.Button(self.gui.main_frame, text="Удалить", font=("Arial", 12), 
                 command=lambda: self.delete_material(material_combobox.get())).pack(pady=20)
        tk.Button(self.gui.main_frame, text="Назад", font=("Arial", 12), 
                 command=self.show_material_management).pack(pady=10)
        self.logger.log("Открыт экран удаления материала")
    
    def delete_material(self, topic):
        """Удаление материала"""
        try:
            self.db.delete_material(topic)
            messagebox.showinfo("Успех", "Материал удален")
            self.logger.log(f"Удален материал: {topic}")
            self.show_material_management()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить материал: {str(e)}")
            self.logger.log(f"Ошибка удаления материала {topic}: {str(e)}")
    
    def show_material_list(self):
        """Список материалов"""
        self.gui.clear_frame()
        tk.Label(self.gui.main_frame, text="Список материалов", font=("Arial", 18, "bold")).pack(pady=30)
        
        materials = self.db.get_all_materials()
        tree = ttk.Treeview(self.gui.main_frame, columns=("Topic", "Category"), show="headings")
        tree.heading("Topic", text="Тема")
        tree.heading("Category", text="Категория")
        tree.pack(fill="both", expand=True, pady=10)
        
        for material in materials:
            tree.insert("", "end", values=(material[1], material[4]))
        
        tk.Button(self.gui.main_frame, text="Назад", font=("Arial", 12), 
                 command=self.show_material_management).pack(pady=10)
        self.logger.log("Открыт список материалов")
    
    def show_materials(self):
        """Просмотр учебных материалов"""
        self.gui.clear_frame()
        tk.Label(self.gui.main_frame, text="Учебные материалы", font=("Arial", 18, "bold")).pack(pady=30)
        
        tk.Label(self.gui.main_frame, text="Фильтр по категории:", font=("Arial", 12)).pack()
        category_combobox = ttk.Combobox(self.gui.main_frame, values=["Все", "Логика", "Теория множеств", "Графы", "Комбинаторика"], 
                                        state="readonly", font=("Arial", 12))
        category_combobox.set("Все")
        category_combobox.pack(pady=10)
        
        materials_frame = tk.Frame(self.gui.main_frame)
        materials_frame.pack(fill="both", expand=True)
        
        def update_materials():
            for widget in materials_frame.winfo_children():
                widget.destroy()
            materials = self.db.get_all_materials() if category_combobox.get() == "Все" else self.db.get_materials_by_category(category_combobox.get())
            for material in materials:
                frame = tk.Frame(materials_frame)
                frame.pack(fill="x", pady=5)
                tk.Label(frame, text=f"Тема: {material[1]} ({material[4]})", font=("Arial", 12)).pack(side="left")
                tk.Button(frame, text="Открыть", font=("Arial", 12), 
                         command=lambda m=material: self.show_material_content(m)).pack(side="right")
        
        category_combobox.bind("<<ComboboxSelected>>", lambda e: update_materials())
        update_materials()
        
        tk.Button(self.gui.main_frame, text="Назад", font=("Arial", 12), 
                 command=self.show_main_menu).pack(pady=10)
        self.logger.log("Открыт экран просмотра материалов")
    
    def show_material_content(self, material):
        """Отображение содержания материала"""
        self.gui.clear_frame()
        tk.Label(self.gui.main_frame, text=f"Тема: {material[1]}", font=("Arial", 18, "bold")).pack(pady=30)
        tk.Label(self.gui.main_frame, text=f"Категория: {material[4]}", font=("Arial", 12)).pack()
        content_text = tk.Text(self.gui.main_frame, height=15, width=80, font=("Arial", 12))
        content_text.insert(tk.END, material[2])
        content_text.config(state="disabled")
        content_text.pack(pady=10)
        
        if material[3] and os.path.exists(material[3]):
            if material[3].endswith((".jpg", ".png")):
                img = Image.open(material[3])
                img = img.resize((300, 300), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                tk.Label(self.gui.main_frame, image=photo).pack(pady=10)
                tk.Label(self.gui.main_frame, image=photo).image = photo
            elif material[3].endswith((".mp4", ".avi")):
                tk.Button(self.gui.main_frame, text="Воспроизвести видео", font=("Arial", 12), 
                         command=lambda: self.video_player.play_video(material[3])).pack(pady=10)
        
        tk.Button(self.gui.main_frame, text="Назад", font=("Arial", 12), 
                 command=self.show_materials).pack(pady=10)
        self.logger.log(f"Открыт материал: {material[1]}")
    
    def show_test_creation(self):
        """Создание теста"""
        self.gui.clear_frame()
        tk.Label(self.gui.main_frame, text="Создать тест", font=("Arial", 18, "bold")).pack(pady=30)
        
        tk.Label(self.gui.main_frame, text="Тема:", font=("Arial", 12)).pack()
        topic_entry = tk.Entry(self.gui.main_frame, font=("Arial", 12))
        topic_entry.pack(pady=10)
        
        tk.Label(self.gui.main_frame, text="Тип вопроса:", font=("Arial", 12)).pack()
        type_combobox = ttk.Combobox(self.gui.main_frame, values=["Множественный выбор", "Открытый вопрос"], 
                                    state="readonly", font=("Arial", 12))
        type_combobox.set("Множественный выбор")
        type_combobox.pack(pady=10)
        
        tk.Label(self.gui.main_frame, text="Вопрос:", font=("Arial", 12)).pack()
        question_text = tk.Text(self.gui.main_frame, height=5, width=60, font=("Arial", 12))
        question_text.pack(pady=10)
        
        tk.Label(self.gui.main_frame, text="Правильный ответ:", font=("Arial", 12)).pack()
        correct_answer_entry = tk.Entry(self.gui.main_frame, font=("Arial", 12))
        correct_answer_entry.pack(pady=10)
        
        tk.Label(self.gui.main_frame, text="Неправильные ответы (через запятую, для множественного выбора):", font=("Arial", 12)).pack()
        wrong_answers_entry = tk.Entry(self.gui.main_frame, font=("Arial", 12))
        wrong_answers_entry.pack(pady=10)
        
        tk.Label(self.gui.main_frame, text="Категория:", font=("Arial", 12)).pack()
        category_combobox = ttk.Combobox(self.gui.main_frame, values=["Логика", "Теория множеств", "Графы", "Комбинаторика"], 
                                        state="readonly", font=("Arial", 12))
        category_combobox.pack(pady=10)
        
        tk.Button(self.gui.main_frame, text="Добавить вопрос", font=("Arial", 12), 
                 command=lambda: self.add_question(topic_entry.get(), question_text.get("1.0", tk.END), 
                                                  correct_answer_entry.get(), wrong_answers_entry.get(), 
                                                  type_combobox.get(), category_combobox.get())).pack(pady=20)
        tk.Button(self.gui.main_frame, text="Назад", font=("Arial", 12), 
                 command=self.show_main_menu).pack(pady=10)
        self.logger.log("Открыт экран создания теста")
    
    def add_question(self, topic, question, correct_answer, wrong_answers, question_type, category):
        """Добавление вопроса"""
        try:
            wrong_answers = wrong_answers.split(",") if question_type == "Множественный выбор" else []
            self.db.add_question(topic, question.strip(), correct_answer, wrong_answers, question_type, category)
            messagebox.showinfo("Успех", "Вопрос добавлен")
            self.logger.log(f"Добавлен вопрос: {topic}, тип: {question_type}")
            self.show_test_creation()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить вопрос: {str(e)}")
            self.logger.log(f"Ошибка добавления вопроса {topic}: {str(e)}")
    
    def show_test_selection(self):
        """Выбор теста"""
        self.gui.clear_frame()
        tk.Label(self.gui.main_frame, text="Выберите тест", font=("Arial", 18, "bold")).pack(pady=30)
        
        tk.Label(self.gui.main_frame, text="Категория:", font=("Arial", 12)).pack()
        category_combobox = ttk.Combobox(self.gui.main_frame, values=["Все", "Логика", "Теория множеств", "Графы", "Комбинаторика"], 
                                        state="readonly", font=("Arial", 12))
        category_combobox.set("Все")
        category_combobox.pack(pady=10)
        
        tk.Label(self.gui.main_frame, text="Тема:", font=("Arial", 12)).pack()
        topic_combobox = ttk.Combobox(self.gui.main_frame, state="readonly", font=("Arial", 12))
        topic_combobox.pack(pady=10)
        
        def update_topics():
            topics = self.db.get_all_topics() if category_combobox.get() == "Все" else self.db.get_topics_by_category(category_combobox.get())
            topic_combobox["values"] = topics
            if topics:
                topic_combobox.set(topics[0])
        
        category_combobox.bind("<<ComboboxSelected>>", lambda e: update_topics())
        update_topics()
        
        tk.Button(self.gui.main_frame, text="Начать тест", font=("Arial", 12), 
                 command=lambda: self.start_test(topic_combobox.get())).pack(pady=20)
        tk.Button(self.gui.main_frame, text="Назад", font=("Arial", 12), 
                 command=self.show_main_menu).pack(pady=10)
        self.logger.log("Открыт экран выбора теста")
    
    def start_test(self, topic):
        """Запуск теста"""
        if not topic:
            messagebox.showerror("Ошибка", "Выберите тему")
            self.logger.log("Ошибка: не выбрана тема для теста")
            return
        questions = self.test_generator.generate_test(topic)
        if not questions:
            messagebox.showerror("Ошибка", "Нет вопросов по данной теме")
            self.logger.log(f"Ошибка: нет вопросов для темы {topic}")
            return
        
        self.gui.clear_frame()
        tk.Label(self.gui.main_frame, text=f"Тест по теме: {topic}", font=("Arial", 18, "bold")).pack(pady=30)
        
        self.current_question = 0
        self.correct_answers = 0
        self.questions = questions
        
        self.show_question()
        self.logger.log(f"Начало теста по теме: {topic}")
    
    def show_question(self):
        """Отображение вопроса"""
        if self.current_question >= len(self.questions):
            self.show_test_results()
            return
        
        question = self.questions[self.current_question]
        self.gui.clear_frame()
        tk.Label(self.gui.main_frame, text=f"Вопрос {self.current_question + 1}: {question[2]} ({question[5]})", 
                font=("Arial", 14), wraplength=800).pack(pady=20)
        
        if question[4] == "Множественный выбор":
            answers = [question[3]] + question[4]
            random.shuffle(answers)
            self.selected_answer = tk.StringVar()
            
            for answer in answers:
                tk.Radiobutton(self.gui.main_frame, text=answer, value=answer, variable=self.selected_answer, 
                              font=("Arial", 12)).pack(anchor="w", padx=20, pady=5)
        else:
            tk.Label(self.gui.main_frame, text="Введите ответ:", font=("Arial", 12)).pack()
            self.selected_answer = tk.StringVar()
            tk.Entry(self.gui.main_frame, textvariable=self.selected_answer, font=("Arial", 12)).pack(pady=10)
        
        tk.Button(self.gui.main_frame, text="Ответить", font=("Arial", 12), 
                 command=self.check_answer).pack(pady=20)
        tk.Button(self.gui.main_frame, text="Пропустить", font=("Arial", 12), 
                 command=self.skip_question).pack(pady=10)
    
    def check_answer(self):
        """Проверка ответа"""
        question = self.questions[self.current_question]
        is_correct = self.selected_answer.get().strip().lower() == question[3].lower()
        if is_correct:
            self.correct_answers += 1
            messagebox.showinfo("Правильно", "Ответ верный!")
        else:
            messagebox.showerror("Ошибка", f"Правильный ответ: {question[3]}")
        
        self.db.save_test_result(self.current_user, question[1], question[5], is_correct)
        self.logger.log(f"Ответ на вопрос {question[2][:30]}...: {'верный' if is_correct else 'неверный'}")
        self.current_question += 1
        self.show_question()
    
    def skip_question(self):
        """Пропуск вопроса"""
        self.current_question += 1
        self.logger.log(f"Пропущен вопрос {self.current_question}")
        self.show_question()
    
    def show_test_results(self):
        """Результаты теста"""
        self.gui.clear_frame()
        score = (self.correct_answers / len(self.questions)) * 100
        tk.Label(self.gui.main_frame, text=f"Результат: {self.correct_answers}/{len(self.questions)} ({score:.2f}%)", 
                font=("Arial", 18, "bold")).pack(pady=30)
        
        weak_topics = self.db.get_weak_topics(self.current_user)
        if weak_topics:
            tk.Label(self.gui.main_frame, text="Слабые темы:", font=("Arial", 14, "bold")).pack(pady=10)
            for topic in weak_topics:
                tk.Label(self.gui.main_frame, text=topic, font=("Arial", 12), fg="red").pack()
        
        tk.Button(self.gui.main_frame, text="Экспорт в .docx", font=("Arial", 12), 
                 command=lambda: self.report_generator.export_to_docx(self.current_user, score, weak_topics)).pack(pady=10)
        tk.Button(self.gui.main_frame, text="Экспорт в .xlsx", font=("Arial", 12), 
                 command=lambda: self.report_generator.export_to_xlsx(self.current_user, score, weak_topics)).pack(pady=10)
        tk.Button(self.gui.main_frame, text="Посмотреть статистику", font=("Arial", 12), 
                 command=self.show_test_stats).pack(pady=10)
        tk.Button(self.gui.main_frame, text="Назад", font=("Arial", 12), 
                 command=self.show_main_menu).pack(pady=10)
        self.logger.log(f"Тест завершен, результат: {score:.2f}%")
    
    def show_test_stats(self):
        """Статистика тестов"""
        self.gui.clear_frame()
        tk.Label(self.gui.main_frame, text="Статистика тестов", font=("Arial", 18, "bold")).pack(pady=30)
        
        results = self.db.get_user_results(self.current_user)
        topics = list(set([r[2] for r in results]))
        success_rates = []
        
        for topic in topics:
            topic_results = [r[3] for r in results if r[2] == topic]
            success_rate = sum(1 for r in topic_results if r) / len(topic_results) * 100 if topic_results else 0
            success_rates.append(success_rate)
        
        fig, ax = plt.subplots()
        ax.bar(topics, success_rates)
        ax.set_ylabel("Успешность (%)")
        ax.set_title("Успешность по темам")
        plt.xticks(rotation=45)
        
        canvas = FigureCanvasTkAgg(fig, master=self.gui.main_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)
        
        tk.Button(self.gui.main_frame, text="Назад", font=("Arial", 12), 
                 command=self.show_test_results).pack(pady=10)
        self.logger.log("Открыта статистика тестов")
    
    def show_video_player(self):
        """Воспроизведение видео"""
        self.gui.clear_frame()
        tk.Label(self.gui.main_frame, text="Видеоуроки", font=("Arial", 18, "bold")).pack(pady=30)
        
        materials = self.db.get_all_materials()
        videos = [m for m in materials if m[3] and m[3].endswith((".mp4", ".avi"))]
        
        for video in videos:
            frame = tk.Frame(self.gui.main_frame)
            frame.pack(fill="x", pady=5)
            tk.Label(frame, text=video[1], font=("Arial", 12)).pack(side="left")
            tk.Button(frame, text="Воспроизвести", font=("Arial", 12), 
                     command=lambda v=video[3]: self.video_player.play_video(v)).pack(side="right")
        
        tk.Button(self.gui.main_frame, text="Назад", font=("Arial", 12), 
                 command=self.show_main_menu).pack(pady=10)
        self.logger.log("Открыт экран видеоуроков")
    
    def show_animations(self):
        """Запуск анимаций"""
        self.gui.clear_frame()
        tk.Label(self.gui.main_frame, text="Анимации", font=("Arial", 18, "bold")).pack(pady=30)
        
        tk.Button(self.gui.main_frame, text="Анимация графа", font=("Arial", 12), 
                 command=self.animation_manager.animate_graph).pack(pady=10)
        tk.Button(self.gui.main_frame, text="Анимация множества", font=("Arial", 12), 
                 command=self.animation_manager.animate_set).pack(pady=10)
        tk.Button(self.gui.main_frame, text="Анимация логики", font=("Arial", 12), 
                 command=self.animation_manager.animate_logic).pack(pady=10)
        tk.Button(self.gui.main_frame, text="Назад", font=("Arial", 12), 
                 command=self.show_main_menu).pack(pady=10)
        self.logger.log("Открыт экран анимаций")
    
    def show_user_profile(self):
        """Личный кабинет"""
        self.gui.clear_frame()
        tk.Label(self.gui.main_frame, text="Личный кабинет", font=("Arial", 18, "bold")).pack(pady=30)
        
        user_info = self.db.get_user_info(self.current_user)
        tk.Label(self.gui.main_frame, text=f"Логин: {user_info[1]}", font=("Arial", 12)).pack(pady=5)
        tk.Label(self.gui.main_frame, text=f"Роль: {user_info[3]}", font=("Arial", 12)).pack(pady=5)
        tk.Label(self.gui.main_frame, text=f"Имя: {user_info[4]}", font=("Arial", 12)).pack(pady=5)
        
        results = self.db.get_user_results(self.current_user)
        tk.Label(self.gui.main_frame, text="Результаты тестов:", font=("Arial", 14, "bold")).pack(pady=10)
        tree = ttk.Treeview(self.gui.main_frame, columns=("Topic", "Correct", "Date"), show="headings")
        tree.heading("Topic", text="Тема")
        tree.heading("Correct", text="Правильно")
        tree.heading("Date", text="Дата")
        tree.pack(fill="both", expand=True, pady=10)
        
        for result in results:
            tree.insert("", "end", values=(result[2], "Да" if result[3] else "Нет", result[4]))
        
        tk.Button(self.gui.main_frame, text="Изменить пароль", font=("Arial", 12), 
                 command=self.show_change_password).pack(pady=10)
        tk.Button(self.gui.main_frame, text="Назад", font=("Arial", 12), 
                 command=self.show_main_menu).pack(pady=10)
        self.logger.log("Открыт личный кабинет")
    
    def show_change_password(self):
        """Изменение пароля"""
        self.gui.clear_frame()
        tk.Label(self.gui.main_frame, text="Изменить пароль", font=("Arial", 18, "bold")).pack(pady=30)
        
        tk.Label(self.gui.main_frame, text="Новый пароль:", font=("Arial", 12)).pack()
        password_entry = tk.Entry(self.gui.main_frame, show="*", font=("Arial", 12))
        password_entry.pack(pady=10)
        
        tk.Label(self.gui.main_frame, text="Подтвердите пароль:", font=("Arial", 12)).pack()
        confirm_entry = tk.Entry(self.gui.main_frame, show="*", font=("Arial", 12))
        confirm_entry.pack(pady=10)
        
        tk.Button(self.gui.main_frame, text="Сохранить", font=("Arial", 12), 
                 command=lambda: self.change_password(password_entry.get(), confirm_entry.get())).pack(pady=20)
        tk.Button(self.gui.main_frame, text="Назад", font=("Arial", 12), 
                 command=self.show_user_profile).pack(pady=10)
        self.logger.log("Открыт экран изменения пароля")
    
    def change_password(self, password, confirm):
        """Сохранение нового пароля"""
        if password != confirm:
            messagebox.showerror("Ошибка", "Пароли не совпадают")
            self.logger.log("Ошибка: пароли не совпадают при изменении")
            return
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        try:
            self.db.update_user(self.current_user, hashed_password, None, None)
            messagebox.showinfo("Успех", "Пароль изменен")
            self.logger.log(f"Изменен пароль для {self.current_user}")
            self.show_user_profile()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось изменить пароль: {str(e)}")
            self.logger.log(f"Ошибка изменения пароля для {self.current_user}: {str(e)}")
    
    def show_settings(self):
        """Настройки приложения"""
        self.gui.clear_frame()
        tk.Label(self.gui.main_frame, text="Настройки", font=("Arial", 18, "bold")).pack(pady=30)
        
        tk.Label(self.gui.main_frame, text="Тема интерфейса:", font=("Arial", 12)).pack()
        theme_combobox = ttk.Combobox(self.gui.main_frame, values=["light", "dark"], state="readonly", font=("Arial", 12))
        theme_combobox.set(self.settings.get_setting("theme"))
        theme_combobox.pack(pady=10)
        
        tk.Label(self.gui.main_frame, text="Размер шрифта:", font=("Arial", 12)).pack()
        font_size_entry = tk.Entry(self.gui.main_frame, font=("Arial", 12))
        font_size_entry.insert(0, self.settings.get_setting("font_size"))
        font_size_entry.pack(pady=10)
        
        tk.Label(self.gui.main_frame, text="Язык интерфейса:", font=("Arial", 12)).pack()
        language_combobox = ttk.Combobox(self.gui.main_frame, values=["Русский", "Английский"], state="readonly", font=("Arial", 12))
        language_combobox.set(self.settings.get_setting("language"))
        language_combobox.pack(pady=10)
        
        tk.Button(self.gui.main_frame, text="Сохранить", font=("Arial", 12), 
                 command=lambda: self.save_settings(theme_combobox.get(), font_size_entry.get(), language_combobox.get())).pack(pady=20)
        tk.Button(self.gui.main_frame, text="Назад", font=("Arial", 12), 
                 command=self.show_main_menu).pack(pady=10)
        self.logger.log("Открыт экран настроек")
    
    def save_settings(self, theme, font_size, language):
        """Сохранение настроек"""
        try:
            self.settings.update_setting("theme", theme)
            self.settings.update_setting("font_size", int(font_size))
            self.settings.update_setting("language", language)
            messagebox.showinfo("Успех", "Настройки сохранены")
            self.apply_settings()
            self.logger.log("Настройки сохранены")
            self.show_main_menu()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить настройки: {str(e)}")
            self.logger.log(f"Ошибка сохранения настроек: {str(e)}")
    
    def show_analytics(self):
        """Аналитика результатов"""
        self.gui.clear_frame()
        tk.Label(self.gui.main_frame, text="Аналитика результатов", font=("Arial", 18, "bold")).pack(pady=30)
        
        users = self.db.get_all_users()
        tk.Label(self.gui.main_frame, text="Выберите пользователя:", font=("Arial", 12)).pack()
        user_combobox = ttk.Combobox(self.gui.main_frame, values=[u[1] for u in users], state="readonly", font=("Arial", 12))
        user_combobox.pack(pady=10)
        
        def show_user_stats():
            results = self.db.get_user_results(user_combobox.get())
            topics = list(set([r[2] for r in results]))
            success_rates = []
            
            for topic in topics:
                topic_results = [r[3] for r in results if r[2] == topic]
                success_rate = sum(1 for r in topic_results if r) / len(topic_results) * 100 if topic_results else 0
                success_rates.append(success_rate)
            
            fig, ax = plt.subplots()
            ax.bar(topics, success_rates)
            ax.set_ylabel("Успешность (%)")
            ax.set_title(f"Успешность по темам для {user_combobox.get()}")
            plt.xticks(rotation=45)
            
            for widget in self.gui.main_frame.winfo_children():
                if isinstance(widget, FigureCanvasTkAgg):
                    widget.destroy()
            
            canvas = FigureCanvasTkAgg(fig, master=self.gui.main_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=10)
        
        tk.Button(self.gui.main_frame, text="Показать статистику", font=("Arial", 12), 
                 command=show_user_stats).pack(pady=10)
        tk.Button(self.gui.main_frame, text="Назад", font=("Arial", 12), 
                 command=self.show_main_menu).pack(pady=10)
        self.logger.log("Открыт экран аналитики")
    
    def show_help(self):
        """Справка по системе"""
        self.gui.clear_frame()
        tk.Label(self.gui.main_frame, text="Справка", font=("Arial", 18, "bold")).pack(pady=30)
        tk.Label(self.gui.main_frame, text="Обучающее приложение по дискретной математике\n"
                                         "Автор: Иванов Иван Иванович\n"
                                         "Версия: 1.0\n"
                                         "Описание: Приложение для изучения дисциплины 'Дискретная математика'\n"
                                         "Функции:\n"
                                         "- Просмотр учебных материалов\n"
                                         "- Прохождение тестов\n"
                                         "- Просмотр видеоуроков\n"
                                         "- Анимации для визуализации\n"
                                         "- Управление пользователями (для администратора)\n"
                                         "- Аналитика результатов (для преподавателя)\n"
                                         "- Личный кабинет и настройки", 
                font=("Arial", 12), wraplength=800, justify="left").pack(pady=20)
        tk.Button(self.gui.main_frame, text="Назад", font=("Arial", 12), 
                 command=self.show_main_menu).pack(pady=10)
        self.logger.log("Открыт экран справки")

if __name__ == "__main__":
    root = tk.Tk()
    app = DiscreteMathApp(root)
    root.mainloop()
