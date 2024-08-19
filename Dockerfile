# Используем официальный Python-образ как базовый
FROM python:3.10.0

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt requirements.txt

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем остальной код приложения
COPY . .

# Определяем переменную окружения для Flask
ENV FLASK_APP=app.py

# Открываем порт, на котором будет работать приложение
EXPOSE 5000

# Запускаем приложение
CMD ["flask", "run", "--host=0.0.0.0"]
