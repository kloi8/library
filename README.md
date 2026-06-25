# Школьная библиотека — проект (минимальная версия)

В проекте реализована простая веб‑система для хранения и просмотра учебных материалов.

## Требования
- Python 3.9+
- pip

## Установка (локально)
1. Создайте виртуальное окружение и активируйте его:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux / macOS
   venv\Scripts\activate    # Windows
   ```
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Выполните миграции и создайте суперпользователя:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
4. Запустите сервер:
   ```bash
   python manage.py runserver
   ```
5. Откройте http://127.0.0.1:8000/ в браузере.

## Описание
- Админ-панель: /admin (для добавления дисциплин, классов, материалов и пользователей)
- Учёт ролей реализован через модель Profile 


