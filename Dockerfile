FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install "django<4" djongo pymongo pytz

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]






