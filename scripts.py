import sqlite3
import requests
from datetime import datetime


def connect_base():
    base = sqlite3.connect('db/base.db')
    cursor = base.cursor()
    return base, cursor


def check_user(login, password):
    base, cursor = connect_base()
    user = cursor.execute(
        f"""SELECT * FROM users WHERE login = '{login}' AND password = '{password}'""").fetchall()
    base.close()
    if len(user) != 0:
        return user[0][0]
    return 0


def isvalid_login(login):
    base = sqlite3.connect('db/base.db')
    cursor = base.cursor()
    all_login = cursor.execute(f"""SELECT * FROM users WHERE login = '{login}'""").fetchall()
    base.close()
    if len(all_login) != 0:
        return False

    return True


def isvalid_password(first, second):
    if first == second:
        return True
    return False

def isvalid_value(*value):
    for i in value:
        if len(i) == 0:
            return False
    else:
        return True
    
def get_id(login):
    base = sqlite3.connect('db/base.db')
    cursor = base.cursor()
    id = cursor.execute(f"""SELECT * FROM users WHERE login = '{login}'""").fetchall()[0][0]
    base.close()
    return id
    

def get_name_street(x, y):
    geocoder_request = f"https://geocode-maps.yandex.ru/1.x/?apikey=06ac2964-1c74-4510-ba0f-4bd4b962a22a&geocode={y},{x}&format=json"
    response = requests.get(geocoder_request)

    if response:
        # Преобразуем ответ в json-объект
        json_response = response.json()
        print(response)
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"]["Components"]

        final = ""
        for i in toponym[3:]:
            final += i["name"] + ", "
        return final[:-2]
    return ""

def change_date(date):
    n = datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S.%f").strftime('%H:%M %d.%m.%Y')
    return n


def get_firts_ticket():
    base = sqlite3.connect('db/base.db')
    cursor = base.cursor()
    return cursor.execute("""SELECT * FROM tickets WHERE status = 'new'""").fetchall()

def get_close_tickets():
    base = sqlite3.connect('db/base.db')
    cursor = base.cursor()
    return cursor.execute("""SELECT * FROM tickets WHERE status = 'closed'""").fetchall()


def parse_jsons(data):
    final = []
    for i in data:
        print(i)
        final.append({
            "id": i[0],
            "address": i[1],
            "status": i[2],
            "created_at": i[3],
            "description": i[4] if i[4] else "",
            "distric": i[5],
            "resolution": i[6] if len(i) > 6 else None,
            "execution_date": i[7] if len(i) > 7 else None,
            "executor_id": i[8] if len(i) > 8 else None,
            "final_status_at": i[9] if len(i) > 9 else None,
            "complaint_id": i[10] if len(i) > 10 else None
        })
    return final