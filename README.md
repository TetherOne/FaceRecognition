# Сервис по распознованию лиц

### Функционал
- GET http://127.0.0.1:8015/api/v1/tasks - просмотр списка заданий
- GET http://127.0.0.1:8015/api/v1/tasks/{task_id} - просмотр заданий по id
- CREATE http://127.0.0.1:8015/api/v1/tasks/create - создание задания
- DELETE http://127.0.0.1:8015/api/v1/tasks/{task_id}/delete - удаление задание по id
- CREATE http://127.0.0.1:8015/api/v1/tasks/{task_id}/add-image/ - добавление изображения к заданию, передается название и изображение
