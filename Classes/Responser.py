import requests
from bs4 import BeautifulSoup

class Responser:
    def __init__(self, url):
        self.url = url

    def get_soup(self):
        request = requests.get(self.url)
        if request.status_code == 200:
            return BeautifulSoup(request.text, "lxml")
        else:
            raise Exception(f"Не вдалося отримати сторінку. Код: {request.status_code}")