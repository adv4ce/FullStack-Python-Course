import requests
import os
from tqdm import tqdm


class YaUpload:
    def __init__(
        self,
        token,
        upload_url="https://cloud-api.yandex.net/v1/disk/resources",
    ):
        self.token = token
        self.upload_url = upload_url
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"OAuth {self.token}",
        }

    def create_folder(self, folder_name):
        try:
            requests.put(
                f"{self.upload_url}?path=disk%3A%2F{folder_name}",
                headers=self.headers,
            )
        except requests.RequestException as e:
            print(f"Ошибка создания папки: {e}")
            return requests.put(
                f"{self.upload_url}?path=disk%3A%2F{folder_name}",
                headers=self.headers,
            )

    def check_folder(self, folder_name):
        response = requests.get(
            f"{self.upload_url}?path=/{folder_name}",
            headers={"Authorization": f"OAuth {self.token}"},
        ).json()
        return True if "message" not in response.keys() else False

    def check_files(self, folder_name):
        response = requests.get(
            f"{self.upload_url}?path=/{folder_name}",
            headers={"Authorization": f"OAuth {self.token}"},
        ).json()
        return [items["name"] for items in response["_embedded"]["items"]]

    def upload_photos(self, folder_name, replace=False):
        for upload_photo in os.listdir("user_photos"):
            res = requests.get(
                f"{self.upload_url}/upload?path={folder_name}/{upload_photo}&overwrite={replace}",
                headers=self.headers,
            ).json()

            with open(f"user_photos/{upload_photo}", "rb") as file:
                try:
                    requests.put(res["href"], files={"file": file})
                except KeyError:
                    print(f"Upload error: {res}")


def response(token):
    url = "https://cloud-api.yandex.net/v1/disk"
    headers = {"Authorization": f"OAuth {token}"}

    return requests.get(url, headers=headers).status_code


def check_ya_token():
    token = input("Введите токен Яндекс диска: ")

    if response(token).status_code == 401:
        while response(token).status_code == 401:
            print("Проверьте правильность введенного токена")
            token = input("Введите правильный токен Яндекс диска: ")
    return token
