from Classes.RozkladAPI import RozkladAPI
from configs import config

def main():

    url = f'https://rozklad.ztu.edu.ua/schedule/group/{config.group}'
    RozkladAPI(url, config.english_teacher)

if __name__ == '__main__':
    main()