import requests
from bs4 import BeautifulSoup

login_url = "https://cabinet.ztu.edu.ua/site/login"
schedule_url = "https://cabinet.ztu.edu.ua/site/schedule"

session = requests.Session()

response = session.get(login_url)

soup = BeautifulSoup(response.text, 'html.parser')

csrf_token = soup.find("input", {"name": "_csrf-frontend"}).get("value")

payload = {
    "LoginForm[username]": "1",
    "LoginForm[password]": "1",
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
