# Сервис по распознованию лиц

### Функционал
- GET http://127.0.0.1:8015/api/v1/tasks - просмотр списка заданий
- GET http://127.0.0.1:8015/api/v1/tasks/{task_id} - просмотр заданий по id
- CREATE http://127.0.0.1:8015/api/v1/tasks/create - создание задания
- DELETE http://127.0.0.1:8015/api/v1/tasks/{task_id}/delete - удаление задание по id
- CREATE http://127.0.0.1:8015/api/v1/tasks/{task_id}/add-image/ - добавление изображения к заданию, передается название и изображение

### Запуск проекта
#### 1. Клонируйте репозиторий
```
git clone https://github.com/TetherOne/FaceRecognition.git
```
#### 2. Соберите проект
```
docker-compose build
docker-compose up
```
#### 3. Перейдите в браузер по ссылке:
```
http://127.0.0.1:8015/docs
```
