import string
from collections import defaultdict

# Читаем содержимое файла
with open("resource_1.txt", "r", encoding="utf-8") as file:
    text = file.read().lower()

# Убираем пунктуацию и разбиваем на слова
translator = str.maketrans('', '', string.punctuation)
text = text.translate(translator)
words = text.split()

# Подсчитываем количество встреч каждого слова
word_counts = defaultdict(int)
for word in words:
    word_counts[word] += 1

# Сортируем слова по убыванию частоты и алфавиту
sorted_words = sorted(word_counts.items(), key=lambda item: (-item[1], item[0]))

# Записываем результат в файл
with open("result_1.txt", "w", encoding="utf-8") as result_file:
    for word, count in sorted_words:
        result_file.write(f"{word} {count}\n")

# Выводим результат в консоль
for word, count in sorted_words:
    print(f"{word} {count}")
