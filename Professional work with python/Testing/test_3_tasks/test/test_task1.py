from unittest import TestCase
from task_1 import check_triangle


class Test_task1(TestCase):
    def test_answer(self):
        test_data = {
            "Равносторонний треугольник": (5, 5, 5),
            "Равнобедренный треугольник": (6, 6, 4),
            "Разносторонний треугольник": (7, 8, 9),
            "Треугольник не существует": (2, 3, 6),
        }
        for key, value in test_data.items():
            with self.subTest(key=key, value=value):
                self.assertEqual(
                    check_triangle(*value), key, msg=f"Ошибка, {value} - {key}"
                )
