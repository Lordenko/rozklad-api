from datetime import datetime, timedelta
import pandas as pd
import json

class EnglishRooms:
    result = {}
    now = datetime.now()

    def __init__(self, path):
        self.path = path
        self.__pd = pd.read_excel(path, header=1, sheet_name=None)
        self.__global_fix()

        self.get_json()

    def __global_fix(self):
        for key, value in self.__pd.items():
            dict = self.__get_dict(value)

            self.__fix_hour(dict)
            self.__fix_teacher(dict)
            self.__fix_room(dict)

            self.__global_filter(dict)

            self.__update_result(dict, key)


    @staticmethod
    def __fix_teacher(dict):
        for index, item in enumerate(dict['teacher']):
            if not pd.isna(item):
                dict['teacher'][index] = item.split(',\n')

    @staticmethod
    def __fix_room(dict):
        for index, item in enumerate(dict['room']):
            if not pd.isna(item):
                dict['room'][index] = item.split('\n')

    @staticmethod
    def __normalize_time(dict, item, index):
        custom_hour = str(item).split('.')
        dict['hour'][index] = f'{custom_hour[0]}:{custom_hour[1] + '0'}'

    @staticmethod
    def __get_last_time(dict, index):
        current_time = datetime.strptime(dict['hour'][index], "%H:%M")
        plus_time = timedelta(hours=1, minutes=20)
        return (current_time + plus_time).strftime("%H:%M")


    def __fix_hour(self, dict):
        for index, item in enumerate(dict['hour']):
            if not pd.isna(item):
                self.__normalize_time(dict, item, index)
                time = self.__get_last_time(dict, index)

                dict['hour'][index] = f'{dict['hour'][index]}-{time[1::] if time[0] == '0' else time}'

        dict['hour'] = [item for item in dict['hour'] if not pd.isna(item)]

    def __fix_roman(self, key):
        key_name = key[0:-3].replace('ІІ', '2').replace('І', '1')
        self.result[key_name] = {}
        print(self.result)
        return key_name

    def __global_filter(self, dict):
        dict['room'] = self.__filter_list('room', dict)
        dict['teacher'] = self.__filter_list('teacher', dict)

    def __update_result(self, dict, key):
        day = self.__fix_roman(key)
        for index, item in enumerate(dict['hour']):
            self.result[day][item] = {'teacher': dict['teacher'][index], 'room': dict['room'][index]}

    def __get_dict(self, value):
        value.columns = ['hour', 'group', 'teacher', 'room']
        dict = value.to_dict('list')
        del dict['group']

        return dict



    def __filter_list(self, key, dict):
        temp_room = []
        current_room = []

        self.__check_first_element_filter(dict, key)
        self.__check_last_and_pre_last_element_filter(dict, key)

        self.__split_non_list_elements(dict, key, current_room, temp_room)
        self.__group_list_elements(current_room, temp_room)

        return [sublist for sublist in temp_room if sublist]

    @staticmethod
    def __split_non_list_elements(dict, key, current_room, temp_room):
        for index, item in enumerate(dict[key]):
            if not isinstance(item, list):
                if current_room:
                    temp_room.append(current_room)
                    current_room = []
                temp_room.append([])
            elif isinstance(item, list):
                current_room.extend(item)

    @staticmethod
    def __group_list_elements(current_room, temp_room):
        if current_room:
            temp_room.append(current_room)

    @staticmethod
    def __check_first_element_filter(dict, key):
        if not isinstance(dict[key][0], list):
            dict[key][0] = ['']

    @staticmethod
    def __check_last_and_pre_last_element_filter(dict, key):
        if not isinstance(dict[key][-1], list) and not isinstance(dict[key][-2], list):
            dict[key][-1] = ['']





    # will be fixed in issue2 :)

    def get_json(self):
        with open("jsons/english.json", "w", encoding='utf-8') as file:
            json.dump(self.result, file, ensure_ascii=False, indent=4)
