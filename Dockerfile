FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install flask flask-cors waitress

EXPOSE 8000

CMD ["python", "app.py"]
