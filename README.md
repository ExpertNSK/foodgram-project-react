![example workflow](https://github.com/expertnsk/foodgram-project-react/actions/workflows/main.yml/badge.svg)
# Foodgram - социальная сеть о кулинарии
### Делитесь рецептами и пробуйте новые
---
### Сервис доступен по адресу:
```
grocassist.sytes.net
```

### Возможности сервиса:
- делитесь своими рецептами
- смотрите рецепты других пользователей
- добавляйте рецепты в избранное
- быстро формируйте список покупок, добавляя рецепт в корзину
- следите за своими друзьями и коллегами

### Технологии:
- Django
- Python
- Docker

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
