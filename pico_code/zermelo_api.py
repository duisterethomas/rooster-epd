from json import loads
from requests import get

class Client():
    def __init__(self, school=""):
        if school != "":
            self.endpoint = f"https://{school}.zportal.nl/api"
        else:
            raise ValueError("School is not defined.")

    def get_user(self, token=""):
        if token == "":
            raise ValueError("Token is not defined.")

        url = f"{self.endpoint}/v3/users/~me?access_token={token}"

        res = get(url)

        if res.status_code == 401:
            raise ValueError("Token not active.")
        elif res.status_code == 200:
            return loads(res.text)

    def get_appointments(self, token="", start_unix="", end_unix=""):
        if token == "":
            raise ValueError("Token is not defined.")
        elif start_unix == "":
            raise ValueError("Start unix timestamp is not defined.")
        elif end_unix == "":
            raise ValueError("End unix timestamp is not defined.")

        url = f"{self.endpoint}/v3/appointments?access_token={token}&user=~me&start={start_unix}&end={end_unix}"

        res = get(url)

        if res.status_code == 403:
            raise ValueError(
                "Start unix timestamp and / or end unix timestamp make no sense.")
        elif res.status_code == 401:
            raise ValueError("Token not active.")
        elif res.status_code == 200:
            return loads(res.text)

    def get_liveschedule(self, token="", week: str = None, usercode: str = None):
        if token == "":
            raise ValueError("Token is not defined.")

        if week == None:
            raise ValueError("Week is not defined.")

        if usercode == None:
            raise ValueError("Usercode is not defined.")

        url = f"{self.endpoint}/v3/liveschedule?access_token={token}&student={usercode}&week={week}"

        res = get(url)

        if res.status_code == 401:
            raise ValueError("Token not active.")
        elif res.status_code == 200:
            return loads(res.text)
