import json
from configs.config import export_directory
from Classes.FileManager import FileManager

class BuilderJSON:

    @staticmethod
    def create(dictionary, name):

        FileManager.create_dir(export_directory)

        with open(f'{export_directory}{name}.json', 'w', encoding='utf-8') as file:
            json.dump(dictionary, file, ensure_ascii=False, indent=4)

    @staticmethod
    def get(name):
        with open(f'{export_directory}{name}.json', 'r', encoding='utf-8') as file:
            return json.load(file)
