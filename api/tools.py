import json
import requests

from api.config import ufanet_user, ufanet_pass

session = None


def ufanet_login(func):
    def wrapper(*args):
        global session
        url_login = "https://dom.ufanet.ru/login/"
        headers = {
            "Accept": "*/*",
            "User-Agent": "Thunder Client (https://www.thunderclient.com)",
            "Content-Type": "multipart/form-data; boundary=kljmyvW1ndjXaOEAg4vPm6RBUqO6MC5A"
        }
        payload = "--kljmyvW1ndjXaOEAg4vPm6RBUqO6MC5A\r\nContent-Disposition: form-data; "
        payload += f"name=\"contract\"\r\n\r\n{ufanet_user}\r\n--kljmyvW1ndjXaOEAg4vPm6RBUqO6MC5A\r\n"
        payload += f"Content-Disposition: form-data; name=\"password\"\r\n\r\n{ufanet_pass}\r\n--kljmyvW1ndjXaOEAg4vPm6RBUqO6MC5A--\r\n"
        session = requests.Session()
        session.post(url_login, data=payload,  headers=headers)
        return func(*args)
    return wrapper


@ufanet_login
def get_my_doors():
    url = "https://dom.ufanet.ru/api/v0/skud/shared/"
    return json.loads(session.get(url).content)


@ufanet_login
def open_door(door: int):
    url = f"https://dom.ufanet.ru/api/v0/skud/shared/{door}/open/"
    return json.loads(session.get(url).content)
