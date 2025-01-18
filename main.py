import json
import requests
from bs4 import BeautifulSoup
from EnglishRooms import EnglishRooms

def get_group(soup):
    return soup.find('h1').text.split()[2]

def update_result(my_group, subject, teacher, room, group, skip_vubirkovi = True):

    if subject and teacher and room:
        if 'Вибіркові дисципліни' not in subject.text and skip_vubirkovi:

            subject = subject.text
            teacher = teacher.text
            room = ' '.join(room.text.split())

            if group:
                group = group.text
                if group == '':
                    group = my_group


            if subject == 'Іноземна мова':
                pass


            if not hour in result[day]:
                print(f'if {result}')
                result[day].update({hour: [{'subject': subject, 'teacher': teacher, 'room': room, 'group': group}]})
            else:
                print(f'else {result}')
                result[day][hour].append({'subject': subject, 'teacher': teacher, 'room': room, 'group': group})

englishRooms = EnglishRooms('english.xlsx')
englishRooms.print_json()

ipz235 = 'https://rozklad.ztu.edu.ua/schedule/group/ІПЗ-23-5'
vt242 = 'https://rozklad.ztu.edu.ua/schedule/group/ВТ-24-2'

response = requests.get(ipz235)

if response.status_code == 200:

    result = {}

    soup = BeautifulSoup(response.text, "lxml")

    my_group = get_group(soup)

    for td in soup.find_all("td"):
        day = td.get('day')
        hour = td.get('hour')

        if day not in result:
            print(f'{day} not in {result}')
            result[day] = {}

        var = td.find('div', class_='variative')
        if var:
            subgroups = td.find('div', class_='subgroups')
            if subgroups:
                for div in subgroups.find_all('div', class_='one'):
                    subject = div.find("div", class_="subject")
                    teacher = div.find("div", class_="teacher")
                    room = div.find("span", class_="room")
                    group = div.find('div')

                    update_result(my_group, subject, teacher, room, group)
            else:
                subject = var.find("div", class_="subject")
                teacher = var.find("div", class_="teacher")
                room = var.find("span", class_="room")
                group = var.find("div")

                update_result(my_group, subject, teacher, room, group)

    print(result)

    with open("data.json", "w", encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False, indent=4)

else:
    print(f"Не вдалося отримати сторінку. Код: {response.status_code}")