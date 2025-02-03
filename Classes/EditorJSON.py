import json
from configs.config import export_directory

class BuilderJSON:

    @staticmethod
    def create(dictionary, name):
        with open(f'{export_directory}{name}.json', 'w', encoding='utf-8') as file:
            json.dump(dictionary, file, ensure_ascii=False, indent=4)

    @staticmethod
    def get(name):
        with open(f'{export_directory}{name}.json', 'r', encoding='utf-8') as file:
            return json.load(file)
