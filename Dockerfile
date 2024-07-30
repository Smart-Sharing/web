FROM python:3.10.0

WORKDIR /app

# Копируем файл requirements.txt в контейнер
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]