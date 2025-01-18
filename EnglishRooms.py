from datetime import datetime, timedelta
import pandas as pd
import json

class EnglishRooms:
    result = {}
    now = datetime.now()

    def __init__(self, path):
        self.path = path
        self.__pd = pd.read_excel('english.xlsx', header=1, sheet_name=None)
        self.__fix()

    # fix list def
    @staticmethod
    def __filter_list(key, dict):
        temp_room = []
        current_room = []

        if not isinstance(dict[key][0], list):
            dict[key][0] = ['']

        if not isinstance(dict[key][-1], list) and not isinstance(dict[key][-2], list):
            dict[key][-1] = ['']

        for index, item in enumerate(dict[key]):
            if not isinstance(item, list):
                if current_room:
                    temp_room.append(current_room)
                    current_room = []
                temp_room.append([])
            elif isinstance(item, list):
                current_room.extend(item)

        if current_room:
            temp_room.append(current_room)

        return [sublist for sublist in temp_room if sublist]

    def __fix(self):
        for key, value in self.__pd.items():
            value.columns = ['hour', 'group', 'teacher', 'room']

            dict = value.to_dict('list')
            del dict['group']

            # fix hour
            for index, item in enumerate(dict['hour']):
                if not pd.isna(item):
                    custom_hour = str(item).split('.')
                    dict['hour'][index] = f'{custom_hour[0]}:{custom_hour[1] + '0'}'

                    current_time = datetime.strptime(dict['hour'][index], "%H:%M")
                    plus_time = timedelta(hours=1, minutes=20)
                    time = (current_time + plus_time).strftime("%H:%M")

                    dict['hour'][index] = f'{dict['hour'][index]}-{time[1::] if time[0] == '0' else time}'


            dict['hour'] = [item for item in dict['hour'] if not pd.isna(item)]

            # fix teacher
            for index, item in enumerate(dict['teacher']):
                if not pd.isna(item):
                    dict['teacher'][index] = item.split(',\n')

            # fix room
            for index, item in enumerate(dict['room']):
                if not pd.isna(item):
                    dict['room'][index] = item.split('\n')

            dict['room'] = self.__filter_list('room', dict)
            dict['teacher'] = self.__filter_list('teacher', dict)

            key_name = key[0:-3].replace('ІІ', '2').replace('І', '1')
            self.result[key_name] = {}

            for index, item in enumerate(dict['hour']):
                self.result[key_name][item] = {'teacher': dict['teacher'][index], 'room': dict['room'][index], }

    def print_json(self):
        with open("english.json", "w", encoding='utf-8') as file:
            json.dump(self.result, file, ensure_ascii=False, indent=4)
