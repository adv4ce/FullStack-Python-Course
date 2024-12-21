from unittest import TestCase
from yaDisk import YaUpload, response
from data import token, yandex
import os

class Test_YaDisk(TestCase):
    def test_connection(self):
        self.assertEqual(response(token), 200, msg="Нет соединения с сервером")

    def test_create_folder(self):
        # folder_name
        test_data = ["test" + str(i) for i in range(1, 6)]
        for name in test_data:
            yandex.create_folder(name)

        for name in test_data:
            with self.subTest(name=name):
                self.assertTrue(
                    yandex.check_folder(name), msg=f"Папки {name} не существует"
                )

    def test_upload_files(self):
        folder = "test_upload_photos"
        yandex.create_folder(folder)
        yandex.upload_photos(folder)

        get_photos_name_with_disk = yandex.check_files(folder)
        user_photos = os.listdir("user_photos")

        self.assertCountEqual(get_photos_name_with_disk, user_photos, msg="Ошибка")
