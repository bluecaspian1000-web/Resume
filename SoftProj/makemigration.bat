@echo off
echo Applying migrations...
python manage.py makemigrations courses
python manage.py makemigrations Professor
python manage.py makemigrations Student
python manage.py makemigrations accounts
python manage.py migrate