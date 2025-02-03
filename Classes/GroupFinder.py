from Classes.EditorJSON import BuilderJSON
from Classes.Responser import Responser
from Classes.CheckFiles import CheckFiles
from configs.config import rozklad_list, rozklad_domen, export_directory

class GroupFinder:
    __json_name = 'group_links'
    __soup = Responser(rozklad_list).get_soup()
    __dictionary = {}

    def __get_groups(self):
        for group in self.__soup.find('div', class_='accordion-item').find_all('a'):
            self.__dictionary[group.text] = f'{rozklad_domen}{group.get('href')}'

        BuilderJSON.create(self.__dictionary, self.__json_name)

    def find(self, name_group):
        if CheckFiles.check(f'{export_directory}{self.__json_name}.json'):
            self.__get_groups()

        return BuilderJSON.get(self.__json_name)[name_group]
