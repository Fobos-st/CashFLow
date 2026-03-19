FROM python:3.13-slim


WORKDIR /app
COPY . /app/

# установка зависимостей
RUN pip install -r requirements-prod.txt

CMD sleep 7 \
    && python manage.py makemigrations \
    && python manage.py migrate \
    && python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(email='CashFlow@CashFlow.ru').exists() or User.objects.create_superuser(first_name='Super', last_name='CashFlow', email='CashFlow@CashFlow.ru', password='Parolchik')" \
    && python manage.py collectstatic --noinput \
    && gunicorn core.wsgi:application --bind 0.0.0.0:8000
