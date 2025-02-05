import os
import datetime
from configs.config import update_check

class CheckFiles:
    @staticmethod
    def check(file_path):
        if os.path.exists(file_path):
            last_modified_timestamp = os.path.getmtime(file_path)
            last_modified_date = datetime.datetime.fromtimestamp(last_modified_timestamp)

            one_day_ago = datetime.datetime.now() - datetime.timedelta(hours=update_check)

            return last_modified_date < one_day_ago
        else:
            raise Exception("File does not exist!")
