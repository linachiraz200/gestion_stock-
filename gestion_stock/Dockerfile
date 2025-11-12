FROM python:3.11-slim

# تحديد مجلد العمل داخل الحاوية
WORKDIR /app

# نسخ ملفات المشروع
COPY . .

# تثبيت المكتبات
RUN pip install --upgrade pip
RUN pip install django djongo pymongo

# تشغيل السيرفر
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
