class MovieRecommender:
    """
    Загрузка данных о фильмах и истории просмотров. Составление рекомендаций для пользователя
    """
    def __init__(self, movies_file=None, history_file=None, movies=None, histories=None):
        """
        Инициализация класса, загрузка данных и фильмах и истории просмотров
        """
        if movies:
            self.movies = movies
        else:
            self.movies_file = movies_file
            self.movies = dict()
            self.load_movies()
        if histories:
            self.histories = histories
        else:
            self.history_file = history_file
            self.histories = list()
            self.load_history()

    def load_movies(self):
        """
        Загрузка списка фильмов из файла
        """
        try:
            with open(self.movies_file, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        movie_id, movie_name = line.split(',', 1)
                        movie_id = int(movie_id)
                        self.movies[movie_id] = movie_name
        except FileNotFoundError:
            print(f'Файл {self.movies_file} не найден')

    def load_history(self):
        """
        Загрузка историй просмотров пользователей из файла
        """
        try:
            with open(self.history_file, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        movie_ids = list(map(int, line.split(',')))
                        self.histories.append(movie_ids)
        except FileNotFoundError:
            print(f'Файл {self.history_file} не найден')

    def recommend(self, movies):
        """
        Составление рекомендаций на основе истории просмотров пользователя
        """
        if not movies:
            return None
        user_movies = set(movies)
        matching_movies = list()

        for history in self.histories:
            history_set = set(history)
            common_movies = user_movies & history_set
            ratio = len(common_movies) / len(user_movies)
            if ratio >= 0.5:
                matching_movies.append((history, ratio))

        recommended_movies = dict()
        for history, weight in matching_movies:
            for movie_id in history:
                if movie_id not in user_movies:
                    if movie_id in recommended_movies:
                        recommended_movies[movie_id] += weight
                    else:
                        recommended_movies[movie_id] = weight
        if not recommended_movies:
            return None

        max_weight = max(recommended_movies.values())
        top_movies = [movie_id for movie_id, weight in recommended_movies.items() if weight == max_weight]

        recommended_movie_id = top_movies[0]
        return self.movies.get(recommended_movie_id, None)
