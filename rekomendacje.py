import json
import numpy as np
from compute_scores import pearson_score
from compute_scores import euclidean_score

"""
Opracowanie:
    Autorzy: Jakub Prucnal
             Juliusz Orłowski
    Temat:   Silnik rekomendacji filmów lub seriali
Wejście:
    - plik movies.json zawierający listę ocen użytkowników wystawionych wybranym filmom lub serialom
Wyjście:
    Program wykorzystuje dwie metryki do liczenia odległości: Pearsona i Euklidesa.
    Na wyjściu wyświetlane są:
        1. Listy przy wykorzystaniu metryki Pearsona:
            a) rekomendowanych filmów lub seriali sortowana od najbardziej rekomendownanych
            b) odradzanych filmów lub seriali sortowana od najbardziej odradzanych
        1. Listy przy wykorzystaniu metryki Euklidesa:
            a) rekomendowanych filmów lub seriali sortowana od najbardziej rekomendownanych
            b) odradzanych filmów lub seriali sortowana od najbardziej odradzanych
Wykorzystywane biblioteki:
    NumPy - do tworzenia macierzy
Przygotowanie środowiska:
    W konsoli PyCharm po uprzedniej instalacji Pythona instalujemy niezbędne biblioteki:
    (1) instalacja NumPy -> pip install numpy
Dokumentacja kodu źródłowego:
    Python -> docstring (https://www.python.org/dev/peps/pep-0257/)
    NumPy -> https://numpy.org/doc/stable/user/whatisnumpy.html
    Prateek Joshi - Artificial Intelligence with Python
"""


# Znajdź rekomendacje dla podanego użytkownika
def get_recommendations(dataset, input_user, name_score):
    if input_user not in dataset:
        raise TypeError('Nie można znaleźć ' + input_user + ' w dataset')
    overall_scores = {}
    similarity_scores = {}
    
# Tworzenie 
    if name_score == "Pearson":
        for user in [x for x in dataset if x != input_user]:
            similarity_score = pearson_score(dataset, input_user, user)
            if similarity_score <= 0:
                continue
            filtered_list = [x for x in dataset[user] if x not in
                             dataset[input_user] or dataset[input_user][x] == 0]
            for item in filtered_list:
                overall_scores.update({item: dataset[user][item] * similarity_score})
                similarity_scores.update({item: similarity_score})
    elif name_score == "Euclidean":
        for user in [x for x in dataset if x != input_user]:
            similarity_score = euclidean_score(dataset, input_user, user)
            if similarity_score < 0.1:
                continue
            filtered_list = [x for x in dataset[user] if x not in
                             dataset[input_user] or dataset[input_user][x] == 0]
            for item in filtered_list:
                overall_scores.update({item: dataset[user][item] * similarity_score})
                similarity_scores.update({item: similarity_score})

    if len(overall_scores) == 0:
        return ['Brak możliwych rekomendacji']
    # Generowanie rankingu przez normalizację
    movie_scores = np.array([[score / similarity_scores[item], item]
                             for item, score in overall_scores.items()])
    # Sortowanie w porządku malejącym
    movie_scores = movie_scores[np.argsort(movie_scores[:, 0])[::-1]]
    # Uzyskanie rekomendacji
    movie_recommendations = [movie for _, movie in movie_scores]
    picks = movie_recommendations[:5]

    picks.extend(reversed(movie_recommendations[-5:]))

    return picks


def print_movies(list_movies):
    print('\nFilmy rekomendowane dla użytkownika ' + user + ':')
    for i, movie in enumerate(list_movies[:5]):
        print(str(i + 1) + '. ' + movie)
    print('\nFilmy nierekomendowane dla użytkownika ' + user + ':')
    for i, movie in enumerate(list_movies[-5:]):
        print(str(i + 1) + '. ' + movie)


if __name__ == '__main__':
    user = 'Paweł Czapiewski'
    ratings_file = 'movies.json'
    with open(ratings_file, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())

    print('\n\nRekomendacja przy użyciu metryki liczenia odległości Pearsona')

    movies = get_recommendations(data, user, 'Pearson')
    print_movies(movies)

    print('\n\nRekomendacja przy użyciu metryki liczenia odległości Euklidesowej')

    movies = get_recommendations(data, user, 'Euclidean')
    print_movies(movies)
