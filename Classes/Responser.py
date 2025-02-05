import requests
from bs4 import BeautifulSoup

class Responser:
    @staticmethod
    def get_soup(url, domain = None, token = None):

        session = requests.Session()

        if token and domain:
            session.cookies.set('PHPSESSID', token, domain=domain)

        request = session.get(url)

        if request.status_code == 200:
            return BeautifulSoup(request.text, "lxml")
        else:
            raise Exception(f"Не вдалося отримати сторінку. Код: {request.status_code}")