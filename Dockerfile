FROM python:3.13-slim


WORKDIR /app
COPY . /app/

# установка зависимостей
RUN pip install -r requirements-prod.txt

CMD sleep 7 \
    && python manage.py makemigrations \
    && python manage.py migrate \
    && python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='amarsana').exists() or User.objects.create_superuser('CashFlow', 'CashFlow@CashFlow.ru', 'Parolchik')" \
    && python manage.py collectstatic --noinput \
    && gunicorn main.wsgi:application --bind 0.0.0.0:8000
