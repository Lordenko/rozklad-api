from Classes.EnglishRooms import EnglishRooms
from Classes.EditorJSON import BuilderJSON
from Classes.Responser import Responser
from Classes.CheckFiles import CheckFiles
from configs.config import export_directory

class RozkladAPI:

    __json_name = 'rozklad'
    __result = {}
    __englishTeacher = None
    __englishRooms = EnglishRooms('EnglishXLSX/english.xlsx').result

    def __init__(self, url, englishTeacher):
        self.__url = url
        self.__englishTeacher = englishTeacher

        self.__soup = Responser.get_soup(self.__url, 'rozklad.ztu.edu.ua', 'huy')

        if CheckFiles.check(f'{export_directory}{self.__json_name}.json'):
            self.__extract_data(self.__soup)
            print(f'File {export_directory}{self.__json_name}.json recreate')


    def __check_validate(self, validate):
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
                raise Exception('Вказаного викладача іноземної мови не було знайдено')

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

    def __get_validate(self, tag, day, hour):
        validate = {
            'day': day,
            'hour': hour,
            'group': ', '.join([group.text.strip() for group in tag.find('div', class_='flow-groups').find_all('a')]) if tag.find('div', class_='flow-groups') else None,
            'classes': tag.find('div', class_='activity-tag').text.strip(),
            'subject': tag.find('div', class_='subject').text.strip(),
            'room': tag.find('div', class_='room').find('span').text.strip(),
            'teacher': tag.find('div', class_='teacher').find('a').text.strip(),
        }

        self.__check_validate(validate)

        return validate

    @staticmethod
    def __get_day_of_week(day, week_number):
        DAYS_OF_WEEK = {
            0: 'Понеділок',
            1: 'Вівторок',
            2: 'Середа',
            3: 'Четвер',
            4: 'П\'ятниця',
            5: 'Субота',
            6: 'Неділя'
        }

        return f'{DAYS_OF_WEEK[day]} {week_number}'

    def __extract_data(self, soup):

        self.__group_name = self.__get_group(self.__soup)

        for wrapper in soup.find_all('div', class_='wrapper'):
            week_number = wrapper.find('h2').text.strip()[-1]

            for tr in wrapper.find_all('tr')[1::]:
                hour = tr.find('th', class_='hour-name').find('div', class_='full-name').text

                for td_key, td in enumerate(tr.find_all('td')):
                    self.__check_day_in_result(self.__get_day_of_week(td_key, week_number))

                    for pair in td.find_all('div', class_='pair'):
                        if pair:
                            self.__update_result(self.__get_validate(pair, self.__get_day_of_week(td_key, week_number), hour))

        BuilderJSON.create(self.__result, self.__json_name)
