run:
	docker-compose up --build
test:
	docker-compose up --build -d app
	docker exec -it app python manage.py test

migrations:
	docker exec -it app python manage.py makemigrations take_home
	docker exec -it app python manage.py migrate