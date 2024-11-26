from py_files.movie_recommender import MovieRecommender
from py_files.consts import MOVIES_FILE, HISTORY_FILE


def main():
    """
    Основная функция для MovieRecommender
    """
    recommender = MovieRecommender(movies_file=MOVIES_FILE, history_file=HISTORY_FILE)
    user_input = input('Введите список идентификаторов просмотренных фильмов, разделяя их запятыми без пробелов:\n')
    user_movies = list(map(int, user_input.split(',')))

    recommendation = recommender.recommend(user_movies)

    if recommendation:
        print(recommendation)
    else:
        print('Нет подходящих рекоммендаций')


if __name__ == '__main__':
    main()
