.PHONY: install migrate createsuperuser runserver


install:
	pip install -r requiremen.txt
 
migrate:
	python manage.py makemigrations
	python manage.py migrate
 
createsuperuser:
	python manage.py createsuperuser
 
runserver:
	python manage.py runserver