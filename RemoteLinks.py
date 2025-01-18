import requests
from bs4 import BeautifulSoup

# URL для логіну та сторінки розкладу
login_url = "https://cabinet.ztu.edu.ua/site/login"
schedule_url = "https://cabinet.ztu.edu.ua/site/schedule"

# Створюємо сесію
session = requests.Session()

# Завантажуємо сторінку логіну для отримання CSRF
response = session.get(login_url)

# Парсимо HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Отримуємо значення CSRF токена
csrf_token = soup.find("input", {"name": "_csrf-frontend"}).get("value")

# Дані для авторизації
payload = {
    "LoginForm[username]": "1",  # заміни на свій логін
    "LoginForm[password]": "1",  # заміни на свій пароль
    "_csrf-frontend": csrf_token
}

# Виконуємо POST-запит для авторизації
login_response = session.post(login_url, data=payload)

# Перевіряємо успішність авторизації
if login_response.status_code == 200 and "logout" in login_response.text.lower():
    print("Login successful!")
else:
    print("Login failed!")

# Завантажуємо сторінку розкладу
schedule_response = session.get(schedule_url)

# Перевіряємо доступ до розкладу
if schedule_response.status_code == 200:
    # Парсимо сторінку розкладу
    soup = BeautifulSoup(schedule_response.content, 'html.parser')
    print(soup.prettify())
else:
    print("Failed to access the schedule page!")
