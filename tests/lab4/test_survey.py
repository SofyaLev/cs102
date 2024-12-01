import unittest
from src.lab4.py_files.survey import Survey, Respondent


class TestSurvey(unittest.TestCase):
    """Класс для тестирования Survey"""

    def setUp(self):
        """Установка тестовых данных"""
        # Границы возрастных групп
        self.limits = [18, 25, 35, 45, 60, 80, 100]

        # Создание экземпляра Survey с тестовыми границами
        self.processor = Survey(self.limits)

        # Пример респондентов
        self.respondents = [
            Respondent("Кошельков Захар Брониславович", 105),
            Respondent("Дьячков Нисон Иринеевич", 88),
            Respondent("Иванов Варлам Якунович", 88),
            Respondent("Старостин Ростислав Ермолаевич", 50),
            Respondent("Ярилова Розалия Трофимовна", 29),
            Respondent("Соколов Андрей Сергеевич", 15),
            Respondent("Егоров Алан Петрович", 7)
        ]

    def test_process(self):
        """Тестирование корректности распределения респондентов по возрастным группам"""
        self.processor.process(self.respondents)
        sorted_groups = self.processor.get_sorted_groups()

        # Проверка количества групп с респондентами
        self.assertEqual(len(sorted_groups), 5)

        # Проверка содержимого каждой группы
        group_labels = [group.label for group in sorted_groups]
        expected_labels = ["101+", "81-100", "46-60", "26-35", "0-18"]
        self.assertEqual(group_labels, expected_labels)

        # Проверка респондентов в каждой группе
        group_dict = {group.label: group.respondents for group in sorted_groups}

        self.assertEqual(len(group_dict["101+"]), 1)
        self.assertEqual(group_dict["101+"][0].name, "Кошельков Захар Брониславович")
        self.assertEqual(group_dict["101+"][0].age, 105)

        self.assertEqual(len(group_dict["81-100"]), 2)
        self.assertEqual(group_dict["81-100"][0].name, "Дьячков Нисон Иринеевич")
        self.assertEqual(group_dict["81-100"][0].age, 88)
        self.assertEqual(group_dict["81-100"][1].name, "Иванов Варлам Якунович")
        self.assertEqual(group_dict["81-100"][1].age, 88)

        self.assertEqual(len(group_dict["46-60"]), 1)
        self.assertEqual(group_dict["46-60"][0].name, "Старостин Ростислав Ермолаевич")
        self.assertEqual(group_dict["46-60"][0].age, 50)

        self.assertEqual(len(group_dict["26-35"]), 1)
        self.assertEqual(group_dict["26-35"][0].name, "Ярилова Розалия Трофимовна")
        self.assertEqual(group_dict["26-35"][0].age, 29)

        self.assertEqual(len(group_dict["0-18"]), 2)
        self.assertEqual(group_dict["0-18"][0].name, "Соколов Андрей Сергеевич")
        self.assertEqual(group_dict["0-18"][0].age, 15)
        self.assertEqual(group_dict["0-18"][1].name, "Егоров Алан Петрович")
        self.assertEqual(group_dict["0-18"][1].age, 7)

    def test_sorting_with_same_age(self):
        """Тестирование сортировки респондентов с одинаковым возрастом"""
        respondents = [
            Respondent("Борисов Алексей Иванович", 30),
            Respondent("Александрова Мария Сергеевна", 30),
            Respondent("Васильев Иван Петрович", 30)
        ]
        self.processor.process(respondents)
        sorted_groups = self.processor.get_sorted_groups()
        group = next((g for g in sorted_groups if g.label == "26-35"), None)
        self.assertIsNotNone(group)
        self.assertEqual(len(group.respondents), 3)
        # Проверка сортировки по ФИО при одинаковом возрасте
        expected_result = [
            "Александрова Мария Сергеевна",
            "Борисов Алексей Иванович",
            "Васильев Иван Петрович"
        ]
        actual_result = [r.name for r in group.respondents]
        self.assertEqual(actual_result, expected_result)

    def test_no_respondents_in_some_groups(self):
        """Тестирование того, что пустые группы не отображаются"""
        respondents = [
            Respondent("Иванов Иван Иванович", 20),
            Respondent("Петров Петр Петрович", 22)
        ]
        self.processor.process(respondents)
        sorted_groups = self.processor.get_sorted_groups()
        # Ожидаем только одну группу: 19-25
        self.assertEqual(len(sorted_groups), 1)
        self.assertEqual(sorted_groups[0].label, "19-25")

    def test_invalid_boundaries(self):
        """Тестирование обработки некорректных границ возрастных групп"""
        with self.assertRaises(ValueError):
            Survey([64, 16, 32])  # Границы расположены не по возрастанию

        with self.assertRaises(ValueError):
            Survey([16, 32, 64, 128])  # Верхняя граница превышает MAX_AGE

    def test_recommendation_with_invalid_respondents(self):
        """Тестирование того, что респонденты с некорректным возрастом не добавляются в группы"""
        respondents = [
            Respondent("Иванов Иван Иванович", -10),
            Respondent("Петров Петр Петрович", 121)
        ]
        # Обработка респондентов с некорректными возрастами
        self.processor.process(respondents)
        sorted_groups = self.processor.get_sorted_groups()
        # Респондент с возрастом -10 не попадет ни в одну группу
        # Респондент с возрастом 121 попадет в группу "101+"
        group = next((g for g in sorted_groups if g.label == "101+"), None)
        self.assertIsNotNone(group)
        self.assertEqual(len(group.respondents), 1)
        self.assertEqual(group.respondents[0].name, "Петров Петр Петрович")
        self.assertEqual(group.respondents[0].age, 121)


if __name__ == '__main__':
    unittest.main()
    