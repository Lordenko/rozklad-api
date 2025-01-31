from Classes.EnglishRooms import EnglishRooms
from Classes.BuilderJSON import BuilderJSON
from Classes.Responser import Responser

class RozkladAPI:

    __result = {}
    __englishTeacher = None
    __englishRooms = EnglishRooms('EnglishXLSX/english.xlsx').result

    def __init__(self, url, englishTeacher):
        self.__url = url
        self.__englishTeacher = englishTeacher

        self.__soup = Responser(self.__url).get_soup()
        self.__group_name = self.__get_group(self.__soup)
        self.__extract_data(self.__soup)

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


    def __check_day_in_result(self, day):
        if day not in self.__result:
            self.__result[day] = {}

    def __extract_data(self, soup):
        for td in soup.find_all("td"):
            day = td.get('day')
            hour = td.get('hour')

            self.__check_day_in_result(td.get('day'))

            var = td.find('div', class_='variative')
            subgroups = td.find('div', class_='subgroups')

            if not var:
                continue

            div = subgroups.find_all('div', class_='one') if subgroups else [var]

            for item in div:
                self.__update_result(self.__get_validate(item, day, hour))
