![example workflow](https://github.com/expertnsk/foodgram-project-react/actions/workflows/main.yml/badge.svg)
# Foodgram - социальная сеть о кулинарии
### Делитесь рецептами и пробуйте новые
---
### Сервис доступен по адресу:
```
grocassist.sytes.net
```

### Логин и пароль администратора для проверки работоспособности
```
email: expertnsk89@gmail.com
password: Rfpfrjd10081989
```

### Возможности сервиса:
- делитесь своими рецептами
- смотрите рецепты других пользователей
- добавляйте рецепты в избранное
- быстро формируйте список покупок, добавляя рецепт в корзину
- следите за своими друзьями и коллегами

### Технологии:
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

### Запуск проекта:
1. Клонируйте проект:
```
git clone git@github.com:ExpertNSK/foodgram-project-react.git
```
2. Подготовьте сервер:
```
scp docker-compose.yml <username>@<host>:/home/<username>/
scp nginx.conf <username>@<host>:/home/<username>/
scp .env <username>@<host>:/home/<username>/
```
3. Установите docker и docker-compose:
```
sudo apt install docker.io 
sudo apt install docker-compose
```
4. Выполните миграции:
```
sudo docker-compose exec backend python manage.py migrate
```
5. Создайте суперюзера и соберите статику:
```
sudo docker-compose exec backend python manage.py createsuperuser
sudo docker-compose exec backend python manage.py collectstatic --no-input
```
6. Скопируйте предустановленные данные csv:
```
sudo docker-compose exec backend python manage.py load_data
```
