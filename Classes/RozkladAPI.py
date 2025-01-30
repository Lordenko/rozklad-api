from Classes.EnglishRooms import EnglishRooms
from Classes.BuilderJSON import BuilderJSON
import requests
from bs4 import BeautifulSoup

class RozkladAPI:

    __result = {}
    __group_name = None
    __englishRooms = None
    __englishTeacher = None

    def __init__(self, url, englishTeacher):
        self.__url = url
        self.__response = requests.get(url)
        self.__englishTeacher = englishTeacher
        self.__englishRooms = EnglishRooms('EnglishXLSX/english.xlsx').result

        self.__start_response()
        BuilderJSON(self.__result).get('rozklad')

    def __get_validate(self, tag, day, hour):
        validate = {
            'day': day,
            'hour': hour,
            'subject': tag.find("div", class_="subject").text if tag.find("div", class_="subject") else None,
            'teacher': tag.find("div", class_="teacher").text if tag.find("div", class_="teacher") else None,
            'room': ' '.join(tag.find("span", class_="room").text.split()) if tag.find("span", class_="room") else None,
            'group': tag.find('div').text if tag.find("div") else None,
        }

        self.__add_classes(validate, tag)
        self.__check_validate(validate)

        return validate if all(validate.values()) else None

    @staticmethod
    def __add_classes(validate, tag):
        if all(validate.values()):
            validate['classes'] = tag.find_all("div")[2].text.split()[0][0:-5] if tag.find_all("div")[2].text.split()[0][0:-5] == 'Практика' or tag.find_all("div")[2].text.split()[0][0:-5] == 'Лекція' else 'Практика'

    def __check_validate(self, validate):
        if all(validate.values()):
            self.__check_group(validate)
            self.__english_check(validate)

    def __check_group(self, validate):
        if not validate['group']:
            validate['group'] = self.__group_name

    def __english_check(self, validate):
        if validate['subject'] == 'Іноземна мова' and len(validate['teacher'].split()) > 3:
            try:
                englishId = self.__englishRooms[validate['day']][validate['hour']]['teacher'].index(self.__englishTeacher)
                validate['teacher'] = self.__englishRooms[validate['day']][validate['hour']]['teacher'][englishId]
                validate['room'] = self.__englishRooms[validate['day']][validate['hour']]['room'][englishId]
                validate['group'] = self.__group_name
            except ValueError:
                print('Вказаного викладача іноземної мови не було знайдено')

    def __update_result(self, validate, skip_selective = True):
        if validate and 'Вибіркові дисципліни' not in validate['subject'] and skip_selective:

            self.__result[validate['day']].setdefault(validate['hour'], []).append(
                {'subject': validate['subject'], 'teacher': validate['teacher'], 'room': validate['room'], 'group': validate['group'], 'classes': validate['classes']}
            )

    def __get_group(self, soup):
        return soup.find('h1').text.split()[2]




    # will be fixed in issue2 and issue3 :)


    def __parsing(self, soup):
        for td in soup.find_all("td"):
            day = td.get('day')
            hour = td.get('hour')

            if day not in self.__result:
                self.__result[day] = {}

            var = td.find('div', class_='variative')
            if var:
                subgroups = td.find('div', class_='subgroups')
                if subgroups:
                    for div in subgroups.find_all('div', class_='one'):
                        self.__update_result(self.__get_validate(div, day, hour))
                else:
                    self.__update_result(self.__get_validate(var, day, hour))


    def __start_response(self):
        if self.__response.status_code == 200:
            soup = BeautifulSoup(self.__response.text, "lxml")

            self.__group_name = self.__get_group(soup)
            self.__parsing(soup)

        else:
            raise Exception(f"Не вдалося отримати сторінку. Код: {self.__response.status_code}")