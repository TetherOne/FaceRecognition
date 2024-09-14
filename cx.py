import requests

url = "https://backend.facecloud.tevian.ru/api/v1/detect"
file_path = "my-image.jpeg"
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3MjYyOTU3ODYsIm5iZiI6MTcyNjI5NTc4NiwianRpIjoiMTQwM2RlNTgtOTdkNS00MGQ0LWI4NGUtODVmMmRmYjYwNDUwIiwic3ViIjo0NzQsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.rqjYkjOGhbOe9qm4WuNsg5ynWGnGjqGd1H75X-w9nTM"

# Открытие файла изображения
with open(file_path, "rb") as image_file:
    headers = {
        "Content-Type": "image/jpeg",  # MIME-тип изображения
        "Authorization": f"Bearer {token}",  # Заголовок авторизации
    }

    # Отправка POST-запроса с изображением
    response = requests.post(url, headers=headers, data=image_file)

# Проверка ответа сервера
print(response.status_code)
print(response.json())
