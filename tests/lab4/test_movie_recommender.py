import unittest
from src.lab4.py_files.movie_recommender import MovieRecommender


class TestMovieRecommender(unittest.TestCase):
    """Класс для тестирования MovieRecommender"""

    def setUp(self):
        """Установка тестовых данных"""
        # Данные фильмов
        self.movies = {
            1: 'Мстители: Финал',
            2: 'Хатико',
            3: 'Дюна',
            4: 'Унесенные призраками'
        }

        # История просмотров пользователей
        self.histories = [
            [2, 1, 3],
            [1, 4, 3],
            [2, 2, 2, 2, 2, 3]
        ]

        # Создание экземпляра MovieRecommender с тестовыми данными
        self.recommender = MovieRecommender(movies=self.movies, histories=self.histories)

    def test_recommendation(self):
        """Тестирование работы функции recommend"""
        # Пример из задания
        user_movies = [2, 4]
        recommended_movie = self.recommender.recommend(user_movies)
        self.assertEqual(recommended_movie, 'Дюна')

    def test_no_recommendation(self):
        """Тестирование случая, когда нет рекомендаций"""
        # Пользователь посмотрел все фильмы
        user_movies = [1, 2, 3, 4]
        recommended_movie = self.recommender.recommend(user_movies)
        self.assertIsNone(recommended_movie)

    def test_edge_case_half_movies(self):
        """Тестирование случая, когда совпадает ровно половина фильмов"""
        user_movies = [1, 2]
        recommended_movie = self.recommender.recommend(user_movies)
        # Рекомендация должна быть из оставшихся фильмов
        self.assertEqual(recommended_movie, 'Дюна')

    def test_empty_user_movies(self):
        """Тестирование случая, когда пользователь не смотрел ни одного фильма"""
        user_movies = list()
        recommended_movie = self.recommender.recommend(user_movies)
        self.assertIsNone(recommended_movie)

    def test_recommendation_with_weights(self):
        """Тестирование верного подсчета веса рекомендаций"""
        user_movies = [1, 3]
        recommended_movie = self.recommender.recommend(user_movies)
        # Проверка на то, что рекомендован фильм с максимальным весом
        self.assertEqual(recommended_movie, 'Хатико')


if __name__ == '__main__':
    unittest.main()
