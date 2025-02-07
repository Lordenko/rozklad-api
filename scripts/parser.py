import json
import requests

def parse_data():
    url = "https://jsonplaceholder.typicode.com/posts"  # Тут можна замінити на інше джерело
    response = requests.get(url)
    data = response.json()

    # Зберігаємо в JSON-файл
    with open("api/data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    print(json.dumps({"message": "Парсинг завершено"}))  # Вивід для Node.js

parse_data()
