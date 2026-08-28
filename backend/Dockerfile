FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=wsgi.py

RUN chmod +x start.sh

EXPOSE 5000

CMD ["./start.sh"]
