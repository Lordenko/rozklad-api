import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv('../configs/login.env')
login = os.getenv("LOGIN")
password = os.getenv("PASSWORD")

login_url = "https://cabinet.ztu.edu.ua/site/login"
schedule_url = "https://cabinet.ztu.edu.ua/site/schedule"

session = requests.Session()

response = session.get(login_url)

# session.cookies.set('advanced-frontend', '8v8jjqh9snk98j16m9lkmt8tei', domain='cabinet.ztu.edu.ua')

# print(session.cookies.get('advanced-frontend'))

soup = BeautifulSoup(response.text, 'html.parser')

csrf_token = soup.find("input", {"name": "_csrf-frontend"}).get("value")

payload = {
    "LoginForm[username]": login,
    "LoginForm[password]": password,
    "_csrf-frontend": csrf_token
}

login_response = session.post(login_url, data=payload)

if login_response.status_code == 200 and "logout" in login_response.text.lower():
    print("Login successful!")
else:
    print("Login failed!")


schedule_response = session.get(schedule_url)

if schedule_response.status_code == 200:
    soup = BeautifulSoup(schedule_response.content, 'html.parser')
    print(soup.prettify())
else:
    print("Failed to access the schedule page!")
