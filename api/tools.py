import requests


def open_door(login: str, password: str):
    url = "https://dom.ufanet.ru/api/v0/skud/shared/41967/open/"
    # "http://dom.ufanet.ru/api/v0/skud/shared/41967/open/"
    url_login = "https://dom.ufanet.ru/login/"

    headers = {
    "Accept": "*/*",
    "User-Agent": "Thunder Client (https://www.thunderclient.com)",
    "Content-Type": "multipart/form-data; boundary=kljmyvW1ndjXaOEAg4vPm6RBUqO6MC5A" 
    }

    payload = "--kljmyvW1ndjXaOEAg4vPm6RBUqO6MC5A\r\nContent-Disposition: form-data; "
    payload += f"name=\"contract\"\r\n\r\n{login}\r\n--kljmyvW1ndjXaOEAg4vPm6RBUqO6MC5A\r\n"
    payload += f"Content-Disposition: form-data; name=\"password\"\r\n\r\n{password}\r\n--kljmyvW1ndjXaOEAg4vPm6RBUqO6MC5A--\r\n"

    if login is None or password is None:
        raise Exception("Creds is wrong!")

    with requests.Session() as s:
        s.post(url_login, data=payload,  headers=headers)
        return s.get(url).reason

