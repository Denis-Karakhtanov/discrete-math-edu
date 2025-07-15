
# database.py
import psycopg2
import hashlib
from datetime import datetime

class Database:
    def __init__(self):
        """Инициализация подключения к PostgreSQL"""
        conn_string = "dbname=postgres user=postgres password=4BQT6r0VVWjo host=localhost port=5432"
        try:
            self.conn = psycopg2.connect(conn_string)
            self.cursor = self.conn.cursor()
            print("Подключение к базе данных успешно установлено")
        except psycopg2.Error as e:
            raise Exception(f"Ошибка подключения к базе данных: {str(e)}")
        except Exception as e:
            raise Exception(f"Неожиданная ошибка при подключении: {str(e)}")

    def create_tables(self):
        """Создание таблиц базы данных"""
        try:
            # Таблица пользователей
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    login VARCHAR(50) UNIQUE,
                    password VARCHAR(64),
                    role VARCHAR(20),
                    name VARCHAR(100)
                );
                CREATE INDEX IF NOT EXISTS idx_users_login ON users(login);
            """)
            # Таблица материалов
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS materials (
                    id SERIAL PRIMARY KEY,
                    topic VARCHAR(100),
                    content TEXT,
                    file_path VARCHAR(255),
                    category VARCHAR(50)
                );
                CREATE INDEX IF NOT EXISTS idx_materials_topic ON materials(topic);
            """)
            # Таблица вопросов
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS questions (
                    id SERIAL PRIMARY KEY,
                    topic VARCHAR(100),
                    question TEXT,
                    correct_answer VARCHAR(255),
                    wrong_answers TEXT[],
                    question_type VARCHAR(50),
                    category VARCHAR(50)
                );
                CREATE INDEX IF NOT EXISTS idx_questions_topic ON questions(topic);
            """)
            # Таблица результатов тестов
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS test_results (
                    id SERIAL PRIMARY KEY,
                    user_login VARCHAR(50),
                    topic VARCHAR(100),
                    category VARCHAR(50),
                    correct BOOLEAN,
                    timestamp TIMESTAMP
                );
                CREATE INDEX IF NOT EXISTS idx_test_results_user ON test_results(user_login);
            """)
            # Таблица категорий
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(50) UNIQUE
                );
            """)
            # Таблица прогресса пользователя
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_progress (
                    id SERIAL PRIMARY KEY,
                    user_login VARCHAR(50),
                    topic VARCHAR(100),
                    progress INTEGER
                );
            """)
            # Таблица логов
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id SERIAL PRIMARY KEY,
                    user_login VARCHAR(50),
                    action TEXT,
                    timestamp TIMESTAMP
                );
            """)
            self.conn.commit()
            print("Таблицы успешно созданы")
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception(f"Ошибка при создании таблиц: {str(e)}")

    def insert_test_data(self):
        """Вставка тестовых данных"""
        try:
            # Проверка и вставка пользователей
            self.cursor.execute("SELECT COUNT(*) FROM users")
            if self.cursor.fetchone()[0] == 0:
                self.cursor.execute("""
                    INSERT INTO users (login, password, role, name) VALUES
                    (%s, %s, %s, %s),
                    (%s, %s, %s, %s),
                    (%s, %s, %s, %s)
                """, (
                    'admin', hashlib.sha256("admin123".encode()).hexdigest(), 'Администратор', 'Админ Админов',
                    'teacher', hashlib.sha256("teacher123".encode()).hexdigest(), 'Преподаватель', 'Петр Петров',
                    'student', hashlib.sha256("student123".encode()).hexdigest(), 'Студент', 'Иван Иванов'
                ))

            # Проверка и вставка категорий
            self.cursor.execute("SELECT COUNT(*) FROM categories")
            if self.cursor.fetchone()[0] == 0:
                self.cursor.execute("""
                    INSERT INTO categories (name) VALUES
                    (%s), (%s), (%s), (%s)
                """, ('Логика', 'Теория множеств', 'Графы', 'Комбинаторика'))

            # Проверка и вставка материалов
            self.cursor.execute("SELECT COUNT(*) FROM materials")
            if self.cursor.fetchone()[0] == 0:
                self.cursor.execute("""
                    INSERT INTO materials (topic, content, file_path, category) VALUES
                    (%s, %s, %s, %s),
                    (%s, %s, %s, %s),
                    (%s, %s, %s, %s),
                    (%s, %s, %s, %s)
                """, (
                    'Логика высказываний', 'Основы математической логики...', 'data/logic.jpg', 'Логика',
                    'Операции над множествами', 'Множества и их свойства...', 'data/sets.mp4', 'Теория множеств',
                    'Основы теории графов', 'Графы и их применение...', 'data/graph.png', 'Графы',
                    'Комбинаторные задачи', 'Принципы подсчета...', 'data/combinatorics.pdf', 'Комбинаторика'
                ))

            # Проверка и вставка вопросов
            self.cursor.execute("SELECT COUNT(*) FROM questions")
            if self.cursor.fetchone()[0] == 0:
                self.cursor.execute("""
                    INSERT INTO questions (topic, question, correct_answer, wrong_answers, question_type, category) VALUES
                    (%s, %s, %s, %s, %s, %s),
                    (%s, %s, %s, %s, %s, %s),
                    (%s, %s, %s, %s, %s, %s),
                    (%s, %s, %s, %s, %s, %s)
                """, (
                    'Логика высказываний', 'Что такое дизъюнкция?', 'Логическое ИЛИ',
                    ['Логическое И', 'Логическое НЕ', 'Импликация'], 'Множественный выбор', 'Логика',
                    'Операции над множествами', 'Что такое объединение множеств?', 'Все элементы обоих множеств',
                    ['Пересечение', 'Разность', 'Дополнение'], 'Множественный выбор', 'Теория множеств',
                    'Основы теории графов', 'Что такое вершина графа?', 'Точка в графе',
                    ['Ребро', 'Цикл', 'Путь'], 'Множественный выбор', 'Графы',
                    'Комбинаторные задачи', 'Сколько способов выбрать 3 книги из 5?', '10',
                    [], 'Открытый вопрос', 'Комбинаторика'
                ))

            # Проверка и вставка прогресса пользователя
            self.cursor.execute("SELECT COUNT(*) FROM user_progress")
            if self.cursor.fetchone()[0] == 0:
                self.cursor.execute("""
                    INSERT INTO user_progress (user_login, topic, progress) VALUES
                    (%s, %s, %s),
                    (%s, %s, %s)
                """, ('student', 'Логика высказываний', 50, 'student', 'Операции над множествами', 70))

            self.conn.commit()
            print("Тестовые данные успешно вставлены")
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception(f"Ошибка при вставке тестовых данных: {str(e)}")

    def get_user(self, login, password, role):
        """Получение пользователя"""
        try:
            self.cursor.execute("SELECT * FROM users WHERE login=%s AND password=%s AND role=%s", 
                               (login, password, role))
            return self.cursor.fetchone()
        except psycopg2.Error as e:
            raise Exception(f"Ошибка при получении пользователя: {str(e)}")

    def get_user_info(self, login):
        """Получение информации о пользователе"""
        try:
            self.cursor.execute("SELECT * FROM users WHERE login=%s", (login,))
            return self.cursor.fetchone()
        except psycopg2.Error as e:
            raise Exception(f"Ошибка при получении информации о пользователе: {str(e)}")

    def add_user(self, login, password, role, name):
        """Добавление пользователя"""
        try:
            self.cursor.execute("INSERT INTO users (login, password, role, name) VALUES (%s, %s, %s, %s)", 
                               (login, password, role, name))
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception(f"Ошибка при добавлении пользователя: {str(e)}")

    def update_user(self, login, password, role, name):
        """Обновление пользователя"""
        try:
            query = "UPDATE users SET "
            params = []
            if password:
                query += "password=%s, "
                params.append(password)
            if role:
                query += "role=%s, "
                params.append(role)
            if name:
                query += "name=%s, "
                params.append(name)
            query = query.rstrip(", ") + " WHERE login=%s"
            params.append(login)
            self.cursor.execute(query, params)
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception(f"Ошибка при обновлении пользователя: {str(e)}")

    def delete_user(self, login):
        """Удаление пользователя"""
        try:
            self.cursor.execute("DELETE FROM users WHERE login=%s", (login,))
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception(f"Ошибка при удалении пользователя: {str(e)}")

    def get_all_users(self):
        """Получение всех пользователей"""
        try:
            self.cursor.execute("SELECT * FROM users")
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            raise Exception(f"Ошибка при получении списка пользователей: {str(e)}")

    def add_material(self, topic, content, file_path, category):
        """Добавление материала"""
        try:
            self.cursor.execute("INSERT INTO materials (topic, content, file_path, category) VALUES (%s, %s, %s, %s)", 
                               (topic, content, file_path, category))
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception(f"Ошибка при добавлении материала: {str(e)}")

    def update_material(self, topic, content, file_path, category):
        """Обновление материала"""
        try:
            self.cursor.execute("UPDATE materials SET content=%s, file_path=%s, category=%s WHERE topic=%s", 
                               (content, file_path, category, topic))
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception(f"Ошибка при обновлении материала: {str(e)}")

    def delete_material(self, topic):
        """Удаление материала"""
        try:
            self.cursor.execute("DELETE FROM materials WHERE topic=%s", (topic,))
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception(f"Ошибка при удалении материала: {str(e)}")

    def get_all_materials(self):
        """Получение всех материалов"""
        try:
            self.cursor.execute("SELECT * FROM materials")
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            raise Exception(f"Ошибка при получении материалов: {str(e)}")

    def get_materials_by_category(self, category):
        """Получение материалов по категории"""
        try:
            self.cursor.execute("SELECT * FROM materials WHERE category=%s", (category,))
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            raise Exception(f"Ошибка при получении материалов по категории: {str(e)}")

    def add_question(self, topic, question, correct_answer, wrong_answers, question_type, category):
        """Добавление вопроса"""
        try:
            self.cursor.execute("INSERT INTO questions (topic, question, correct_answer, wrong_answers, question_type, category) VALUES (%s, %s, %s, %s, %s, %s)", 
                               (topic, question, correct_answer, wrong_answers, question_type, category))
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception(f"Ошибка при добавлении вопроса: {str(e)}")

    def get_all_topics(self):
        """Получение всех тем"""
        try:
            self.cursor.execute("SELECT DISTINCT topic FROM questions")
            return [row[0] for row in self.cursor.fetchall()]
        except psycopg2.Error as e:
            raise Exception(f"Ошибка при получении тем: {str(e)}")

    def get_topics_by_category(self, category):
        """Получение тем по категории"""
        try:
            self.cursor.execute("SELECT DISTINCT topic FROM questions WHERE category=%s", (category,))
            return [row[0] for row in self.cursor.fetchall()]
        except psycopg2.Error as e:
            raise Exception(f"Ошибка при получении тем по категории: {str(e)}")

    def get_questions_by_topic(self, topic):
        """Получение вопросов по теме"""
        try:
            self.cursor.execute("SELECT * FROM questions WHERE topic=%s", (topic,))
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            raise Exception(f"Ошибка при получении вопросов: {str(e)}")

    def save_test_result(self, user_login, topic, category, correct):
        """Сохранение результата теста"""
        try:
            self.cursor.execute("INSERT INTO test_results (user_login, topic, category, correct, timestamp) VALUES (%s, %s, %s, %s, %s)", 
                               (user_login, topic, category, correct, datetime.now()))
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception(f"Ошибка при сохранении результата теста: {str(e)}")

    def get_user_results(self, user_login):
        """Получение результатов пользователя"""
        try:
            self.cursor.execute("SELECT * FROM test_results WHERE user_login=%s ORDER BY timestamp DESC", (user_login,))
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            raise Exception(f"Ошибка при получении результатов пользователя: {str(e)}")

    def get_weak_topics(self, user_login):
        """Получение слабых тем"""
        try:
            self.cursor.execute("""
                SELECT topic, AVG(correct::int) as success_rate
                FROM test_results
                WHERE user_login=%s
                GROUP BY topic
                HAVING AVG(correct::int) < 0.7
            """, (user_login,))
            return [row[0] for row in self.cursor.fetchall()]
        except psycopg2.Error as e:
            raise Exception(f"Ошибка при получении слабых тем: {str(e)}")

    def update_progress(self, user_login, topic, progress):
        """Обновление прогресса"""
        try:
            self.cursor.execute("INSERT INTO user_progress (user_login, topic, progress) VALUES (%s, %s, %s) "
                               "ON CONFLICT (user_login, topic) DO UPDATE SET progress=%s", 
                               (user_login, topic, progress, progress))
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            raise Exception(f"Ошибка при обновлении прогресса: {str(e)}")

    def get_progress(self, user_login):
        """Получение прогресса"""
        try:
            self.cursor.execute("SELECT topic, progress FROM user_progress WHERE user_login=%s", (user_login,))
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            raise Exception(f"Ошибка при получении прогресса: {str(e)}")

    def __del__(self):
        """Закрытие соединения"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
                print("Соединение с базой данных закрыто")
        except psycopg2.Error as e:
            print(f"Ошибка при закрытии соединения: {str(e)}")
