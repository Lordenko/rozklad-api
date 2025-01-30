import json

class BuilderJSON:
    __directory = 'jsons/'

    def __init__(self, dictionary):
        self.dictionary = dictionary

    def get(self, name):
        with open(f'{self.__directory}{name}.json', "w", encoding='utf-8') as file:
            json.dump(self.dictionary, file, ensure_ascii=False, indent=4)