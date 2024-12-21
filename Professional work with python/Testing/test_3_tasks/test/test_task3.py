from unittest import TestCase
from task_3 import check_month

class Test_task3(TestCase):
  def test_answer(self):
    test_data = {
      1: "Зима",
      12: "Зима",
      
      3: "Весна",
      5: "Весна",

      6: "Лето",
      8: "Лето",

      9: "Осень",
      11: "Осень",

      0: "Некорректный номер месяца",
      13: "Некорректный номер месяца",
    }
    for kats, answ in test_data.items():
      with self.subTest(kats=kats, answ=answ):
        self.assertEqual(check_month(kats), answ, msg=f"Ошибка, входные данные:\nkats={kats}\nansw={answ}\nвызов функции={check_month(kats)}")
    