import os
import datetime
from configs.config import update_check

class FileManager:
    @staticmethod
    def check_time(path):

        if FileManager.check_exist(path):
            last_modified_timestamp = os.path.getmtime(path)
            last_modified_date = datetime.datetime.fromtimestamp(last_modified_timestamp)

            one_day_ago = datetime.datetime.now() - datetime.timedelta(seconds=update_check)

            return last_modified_date < one_day_ago
        else:
            return True


    @staticmethod
    def check_exist(path):
        return os.path.exists(path)

    @staticmethod
    def create_dir(path):
        if not FileManager.check_exist(path):
            os.makedirs(path)

    @staticmethod
    def create_file(path):
        if not FileManager.check_exist(path):
            fix_path = '/'.join(path.split('/')[0:-1])

            if not FileManager.check_time(fix_path):
                FileManager.create_dir(fix_path)

            with open(path, 'w'):
                pass

