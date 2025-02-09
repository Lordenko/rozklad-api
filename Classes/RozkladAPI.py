from Classes.EnglishRooms import EnglishRooms
from Classes.EditorJSON import BuilderJSON
from Classes.Responser import Responser
from Classes.FileManager import FileManager
from configs.config import export_directory

from dataclasses import dataclass, asdict


@dataclass
class ScheduleEntry:
    group: str | None
    classes: int
    subject: str
    room: str
    teacher: str
                
    def is_elective(self):
        return 'Вибіркові дисципліни' in self.subject
    
    def is_english(self):
        return self.subject == 'Іноземна мова' and len(self.teacher.split()) > 3

class RozkladAPI:

    __json_name = 'rozklad'
    __result = {}
    __englishTeacher = None
    __englishRooms = EnglishRooms('EnglishXLSX/english.xlsx').result

    def __init__(self, url, englishTeacher):
        self.__url = url
        self.__englishTeacher = englishTeacher

        self.__soup = Responser.get_soup(self.__url, 'rozklad.ztu.edu.ua', 'huy')

        if FileManager.check_time(f'{export_directory}{self.__json_name}.json'):
            self.__extract_data(self.__soup)
            print(f'File {export_directory}{self.__json_name}.json recreate')


    def __fixup_entry(self, entry: ScheduleEntry, day, hour):
        self.__fixup_entry_group(entry)
        self.__fixup_entry_english(entry, day, hour)

    def __fixup_entry_group(self, entry: ScheduleEntry):
        if not entry.group:
            entry.group = self.__group_name

    def __fixup_entry_english(self, entry: ScheduleEntry, day, hour):
        if entry.is_english():
            try:
                englishId = self.__englishRooms[day][hour]['teacher'].index(self.__englishTeacher)
                entry.teacher = self.__englishRooms[day][hour]['teacher'][englishId]
                entry.room = self.__englishRooms[day][hour]['room'][englishId]
                entry.group = self.__group_name
            except ValueError:
                raise Exception('Вказаного викладача іноземної мови не було знайдено')

    def __update_result(self, entry: ScheduleEntry, day, hour):
        if not entry.is_elective():
            self.__result[day].setdefault(hour, []).append(asdict(entry))

    def __get_group(self, soup):
        return soup.find('h1').text.split()[2]

    def __check_day_in_result(self, day):
        if day not in self.__result:
            self.__result[day] = {}

    def __get_schedule_entry(self, tag):
        group = None
        if tag.find('div', class_='flow-groups'):
            group_tags = tag.find('div', class_='flow-groups').find_all('a')
            group = ', '.join([group.text.strip() for group in group_tags])
        classes = tag.find('div', class_='activity-tag').text.strip()
        subject = tag.find('div', class_='subject').text.strip()
        room = tag.find('div', class_='room').find('span').text.strip()
        teacher = tag.find('div', class_='teacher').find('a').text.strip()

        return ScheduleEntry(group, classes, subject, room, teacher)

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
                            day = self.__get_day_of_week(td_key, week_number)
                            entry = self.__get_schedule_entry(pair)
                            self.__fixup_entry(entry)
                            self.__update_result(entry, day, hour)

        BuilderJSON.create(self.__result, self.__json_name)
