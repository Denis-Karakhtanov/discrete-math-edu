import random

class TestGenerator:
    def __init__(self, db):
        """Инициализация генератора тестов"""
        self.db = db
    
    def generate_test(self, topic):
        """Генерация теста по теме"""
        questions = self.db.get_questions_by_topic(topic)
        if len(questions) < 5:
            return questions
        return random.sample(questions, 5)
    
    def generate_mixed_test(self, category):
        """Генерация смешанного теста по категории"""
        questions = []
        topics = self.db.get_topics_by_category(category)
        for topic in topics:
            topic_questions = self.db.get_questions_by_topic(topic)
            if topic_questions:
                questions.extend(random.sample(topic_questions, min(len(topic_questions), 2)))
        return random.sample(questions, min(len(questions), 5))