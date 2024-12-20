from .consts import MAX_AGE
from typing import Optional


class Respondent:
    """
    Представление респондента по ФИО и возрасту
    """
    def __init__(self, name, age):
        """
        Инициализация респондента
        """
        self.name = name
        self.age = age

    def __repr__(self):
        """
        Возврат данных респондента в виде нужной строки
        """
        return f'{self.name} ({self.age})'


class AgeGroup:
    """
    Представление возрастной группы (с границами и списком респондентов)
    """
    def __init__(self, label, lower, upper: Optional[int]):
        self.label = label
        self.lower = lower
        self.upper = upper
        self.respondents = []

    def add_respondent(self, respondent):
        """
        Добавление респондента в возрастную группу
        """
        self.respondents.append(respondent)

    def has_respondents(self):
        """
        Проверка на то, что в группе есть респонденты
        """
        return len(self.respondents) > 0

    def sort_respondents(self):
        """
        Сортировка респондентов по убыванию возраста и возрастанию ФИО в случае совпадения возраста
        """
        self.respondents.sort(key=lambda x: (-x.age, x.name))

    def __repr__(self):
        """
        Возврат группы респондентов в нужном виде
        """
        respondents_str = ', '.join([f'{resp.name} ({resp.age})' for resp in self.respondents])
        return f'{self.label}: {respondents_str}'


class Survey:
    """
    Обработка списка респондентов и распределение их по возрастным группам
    """
    def __init__(self, limits):
        """
        Инициализация обработки заданных границ возрастных групп
        """
        if not self.valid_limits(limits):
            raise ValueError(f'Границы групп должны быть возрастающими числами от 1 до {MAX_AGE} включительно')
        self.limits = limits
        self.age_groups = self.create_age_groups()

    def valid_limits(self, limits):
        """
        Проверка корректности границ возрастных групп
        """
        previous = -1
        for limit in limits:
            if not (0 < limit <= MAX_AGE):
                return False
            if limit <= previous:
                return False
            previous = limit
        return True

    def create_age_groups(self):
        """
        Создание списка возрастных групп
        """
        groups = []
        lower = 0
        for limit in self.limits:
            label = f'{lower}-{limit}'
            groups.append(AgeGroup(label, lower, limit))
            lower = limit + 1
        label = f'{lower}+'
        groups.append(AgeGroup(label, lower, None))
        groups.sort(key=lambda x: x.lower, reverse=True)
        return groups

    def add_respondent(self, respondent):
        """
        Добавление респондента в возрастную группу
        """
        age = respondent.age
        for group in self.age_groups:
            if group.upper is not None:
                if group.lower <= age <= group.upper:
                    group.add_respondent(respondent)
                    return
            else:
                if age >= group.lower:
                    group.add_respondent(respondent)
                    return

    def process(self, respondents):
        """
        Обработка списка респондентов и распределение их по возрастным группам
        """
        for respondent in respondents:
            self.add_respondent(respondent)
        for group in self.age_groups:
            if group.has_respondents():
                group.sort_respondents()

    def get_sorted_groups(self):
        """
        Возврат списка возрастных групп и их респондентов, отсортированного от наибольшего возраста к наименьшему
        """
        return [group for group in self.age_groups if group.has_respondents()]

    def print_groups(self):
        """
        Вывод групп в требуемом формате
        """
        sorted_groups = self.get_sorted_groups()
        for group in sorted_groups:
            print(group)
            