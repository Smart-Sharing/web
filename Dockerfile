FROM python:3.10.0

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

COPY . .

CMD ["python", "app.py"]