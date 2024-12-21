from unittest import TestCase
from task_2 import solution


class Test_task2(TestCase):
    def test_answer(self):
        test_data = {
            (1, -3, 2): [1.0, 2.0],
            (2, -4, -6): [-1.0, 3.0],
            (1, 2, 5): ["корней нет"],
            (1, 0, -9): [3.0, -3.0],
            (1, 1, 3): ["корней нет"],
            (1, -2, 1): [1.0],
            (3, -15, 12): [4.0, 1.0],
            (1, 4, 5): ["корней нет"],
            (4, -4, 1): [0.5],
            (1, -6, 8): [4.0, 2.0],
        }
        for kats, answ in test_data.items():
            with self.subTest(kats=kats, answ=answ):
                self.assertCountEqual(
                    solution(*kats),
                    answ,
                    msg=f"Ошибка при данных kats = {kats}, answ = {answ}, правильный ответ: {solution(*kats)}",
                )
