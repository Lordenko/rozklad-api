from Classes.RozkladAPI import RozkladAPI

def main():
    url = 'https://rozklad.ztu.edu.ua/schedule/group/ІПЗ-23-5'
    englishTeacher = 'Вергун Тетяна Михайлівна'

    RozkladAPI(url, englishTeacher)

if __name__ == '__main__':
    main()