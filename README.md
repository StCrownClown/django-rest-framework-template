# marketplace/flowers script

python manage.py makemigrations

python manage.py makemigrations accounts flowers

python manage.py migrate

python manage.py migrate --run-syncdb

python manage.py createsuperuser

docker build -t marketplace .
