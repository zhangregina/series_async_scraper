sleep 20

python manage.py makemigrations --no-input # --no-input

python manage.py migrate --no-input

python manage.py collectstatic --no-input

exec gunicorn main.wsgi:application -c gunicorn_config.py --reload   #c - config file. это как runserver запускается под коробкой
