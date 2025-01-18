import json
import requests
from bs4 import BeautifulSoup
from Classes.EnglishRooms import EnglishRooms

class RozkladAPI:

    __result = {}
    __group_name = None

    def __init__(self, url, englishTeacher):
        self.__url = url
        self.__response = requests.get(url)
        self.__englishTeacher = englishTeacher
        self.__englishRooms = EnglishRooms('EnglishXLSX/english.xlsx').result

        self.__start_response()

    @staticmethod
    def __get_validate(tag):
        return {
            'subject': tag.find("div", class_="subject"),
            'teacher': tag.find("div", class_="teacher"),
            'room': tag.find("span", class_="room"),
            'group': tag.find('div'),
            'classes': tag.find_all("div")
        }

    def __update_result(self, day, hour, validate, skip_vubirkovi=True):
        if validate['subject'] and validate['teacher'] and validate['room']:
            if 'Вибіркові дисципліни' not in validate['subject'].text and skip_vubirkovi:

                subject = validate['subject'].text
                teacher = validate['teacher'].text
                room = ' '.join(validate['room'].text.split())
                validate['classes'] = validate['classes'][2]
                classes = validate['classes'].text.split()[0][0:-5] if validate['classes'].text.split()[0][0:-5] == 'Практика' or \
                                                                       validate['classes'].text.split()[0][0:-5] == 'Лекція' else 'Практика'

                if validate['group']:
                    group = validate['group'].text
                    if group == '':
                        group = self.__group_name

                if subject == 'Іноземна мова' and len(teacher.split()) > 3:
                    try:
                        englishId = self.__englishRooms[day][hour]['teacher'].index(self.__englishTeacher)
                        teacher = self.__englishRooms[day][hour]['teacher'][englishId]
                        room = self.__englishRooms[day][hour]['room'][englishId]
                        group = self.__group_name
                    except ValueError:
                        print('Вказаного викладача іноземної мови не було знайдено')

                if not hour in self.__result[day]:
                    # print(f'if {result}')
                    self.__result[day].update({hour: [
                        {'subject': subject, 'teacher': teacher, 'room': room, 'group': group, 'classes': classes}]})
                else:
                    # print(f'else {result}')
                    self.__result[day][hour].append(
                        {'subject': subject, 'teacher': teacher, 'room': room, 'group': group, 'classes': classes})


    def __parsing(self, soup):
        for td in soup.find_all("td"):
            day = td.get('day')
            hour = td.get('hour')

            if day not in self.__result:
                # print(f'{day} not in {result}')
                self.__result[day] = {}

            var = td.find('div', class_='variative')
            if var:
                subgroups = td.find('div', class_='subgroups')
                if subgroups:
                    for div in subgroups.find_all('div', class_='one'):
                        self.__update_result(day, hour, self.__get_validate(div))
                else:
                    self.__update_result(day, hour, self.__get_validate(var))

    def __get_group(self, soup):
        return soup.find('h1').text.split()[2]

    def __start_response(self):
        if self.__response.status_code == 200:
            soup = BeautifulSoup(self.__response.text, "lxml")

            self.__group_name = self.__get_group(soup)
            self.__parsing(soup)

        else:
            raise Exception(f"Не вдалося отримати сторінку. Код: {self.__response.status_code}")

    def get_json(self):
        with open("jsons/rozklad.json", "w", encoding='utf-8') as file:
            json.dump(self.__result, file, ensure_ascii=False, indent=4)


