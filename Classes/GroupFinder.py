from Classes.EditorJSON import BuilderJSON
from Classes.Responser import Responser
from Classes.FileManager import FileManager
from configs.config import rozklad_list, rozklad_domen, export_directory

class GroupFinder:
    __json_name = 'group_links'
    __soup = Responser.get_soup(rozklad_list)
    __dictionary = {}

    def __get_groups(self):
        for group in self.__soup.find('div', class_='accordion-item').find_all('a'):
            self.__dictionary[group.text] = f'{rozklad_domen}{group.get('href')}'

        BuilderJSON.create(self.__dictionary, self.__json_name)

    def find(self, name_group):
        if FileManager.check_time(f'{export_directory}{self.__json_name}.json'):
            self.__get_groups()
            print(f'File {export_directory}{self.__json_name}.json recreate')

        try:
            return BuilderJSON.get(self.__json_name)[name_group]
        except KeyError:
            raise Exception(f'Group {name_group} not found')