from Classes.RozkladAPI import RozkladAPI
from Classes.GroupFinder import GroupFinder
from configs.config import group, english_teacher

def main():

    url = GroupFinder().find(group)

    RozkladAPI(url, english_teacher)

if __name__ == '__main__':
    main()