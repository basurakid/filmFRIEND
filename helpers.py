import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from fuzzywuzzy import process
import requests


def create_x(df):
    """
    Generates a sparse matrix from ratings dataframe.

    Args:
        df: pandas dataframe containing 3 columns (userId, movieId, rating)

    Returns:
        X: sparse matrix
        user_mapper: dict that maps user id's to user indices
        user_inv_mapper: dict that maps user indices to user id's
        movie_mapper: dict that maps movie id's to movie indices
        movie_inv_mapper: dict that maps movie indices to movie id's
    """
    M = df['userId'].nunique()
    N = df['movieId'].nunique()

    user_mapper = dict(zip(np.unique(df["userId"]), list(range(M))))
    movie_mapper = dict(zip(np.unique(df["movieId"]), list(range(N))))

    user_inv_mapper = dict(zip(list(range(M)), np.unique(df["userId"])))
    movie_inv_mapper = dict(zip(list(range(N)), np.unique(df["movieId"])))

    user_index = [user_mapper[i] for i in df['userId']]
    item_index = [movie_mapper[i] for i in df['movieId']]

    X = csr_matrix((df["rating"], (user_index, item_index)), shape=(M, N))

    return X, user_mapper, movie_mapper, user_inv_mapper, movie_inv_mapper


def find_similar_movies(movie_id, X, movie_mapper, movie_inv_mapper, k, metric='cosine'):
    """
    Finds k-nearest neighbours for a given movie id.

    Args:
        movie_id: id of the movie of interest
        X: user-item utility matrix
        k: number of similar movies to retrieve
        metric: distance metric for kNN calculations

    Output: returns list of k similar movie ID's
    """
    X = X.T
    neighbour_ids = []

    movie_ind = movie_mapper[movie_id]
    movie_vec = X[movie_ind]
    if isinstance(movie_vec, (np.ndarray)):
        movie_vec = movie_vec.reshape(1, -1)
    # use k+1 since kNN output includes the movieId of interest
    kNN = NearestNeighbors(n_neighbors=k+1, algorithm="brute", metric=metric)
    kNN.fit(X)
    neighbour = kNN.kneighbors(movie_vec, return_distance=False)
    for i in range(0, k):
        n = neighbour.item(i)
        neighbour_ids.append(movie_inv_mapper[n])
    neighbour_ids.pop(0)
    return neighbour_ids


def movie_finder(title, movies):
    all_titles = movies['title'].tolist()
    closest_match = process.extractOne(title, all_titles)
    return closest_match[0]


def tmdb_data(tmdb_ids, id, title, is_tmdb_id, api_key="5e1f7a1a0d53bedb61f3b04e4da2d79a"):
    if not is_tmdb_id:
        movie_id = tmdb_ids[id]
    else:
        movie_id = id

    details_data = {}

    try:
        id_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
        details_response = requests.get(id_url)
        details_response.raise_for_status()
        details_data = details_response.json()

    except requests.exceptions.HTTPError as err:
        title_url = f'https://api.themoviedb.org/3/search/movie?query={title}&api_key={api_key}'
        search_response = requests.get(title_url)
        search_data = search_response.json()

        if search_data['results']:
            first_movie = search_data['results'][0]
            search_id = first_movie['id']
            id_url = f'https://api.themoviedb.org/3/movie/{search_id}?api_key={api_key}'
            details_response = requests.get(id_url)
            details_response.raise_for_status()
            details_data = details_response.json()

        else:
            details_data ={
                "title": "No movie found",
                "poster_path":"invalid_path",
                "id":"NotFound"
            }

    return details_data


def tmdb_cast(id, title, api_key="5e1f7a1a0d53bedb61f3b04e4da2d79a"):
    try:
        cast_id_url = f"https://api.themoviedb.org/3/movie/{id}/credits?api_key={api_key}"
        cast_response = requests.get(cast_id_url)
        cast_response.raise_for_status()
        details_cast_data = cast_response.json()

    except requests.exceptions.HTTPError as err:
        title_url = f'https://api.themoviedb.org/3/search/movie?query={title}&api_key={api_key}'
        search_response = requests.get(title_url)
        search_data = search_response.json()

        if search_data['results']:
            first_movie = search_data['results'][0]
            movie_id = first_movie['id']

            cast_id_url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}'

            cast_response = requests.get(cast_id_url)
            details_cast_response.raise_for_status()

            details_cast_data = details_response_cast.json()

    return details_cast_data



if __name__ == "__main__":
    main()