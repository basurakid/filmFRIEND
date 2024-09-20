from flask import Flask, redirect, render_template, request, jsonify, url_for
import pandas as pd
from helpers import create_x, find_similar_movies, movie_finder, tmdb_data, tmdb_cast
from urllib.parse import unquote


app = Flask(__name__)

print()
# Load dataframes from csv files
movies = pd.read_csv("ml-latest-small/movies.csv")
ratings = pd.read_csv("ml-latest-small/ratings.csv")
tmdb = pd.read_csv("ml-latest-small/links.csv")

# Drop unused columns
ratings.drop(columns=['timestamp'], inplace=True)
tmdb.drop(columns=["imdbId"], inplace=True)

# Create X grid and mappers
X, user_mapper, movie_mapper, user_inv_mapper, movie_inv_mapper = create_x(ratings)

# Map movieId to titles
movie_titles = dict(zip(movies['movieId'], movies['title']))
movie_ids = dict(zip(movies['title'], movies['movieId']))
tmdb_ids = dict(zip(tmdb['movieId'], tmdb['tmdbId']))


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if not request.form.get("q"):
            return jsonify({"error": "No query provided"}), 400

        else:
            movie_query = request.form.get("q")
            return redirect(url_for('results', query=movie_query))

    return render_template("home.html")


@app.route("/results", methods=["GET", "POST"])
def results():
    query = request.args.get("query")
    if not query:
        return "No query provided", 400

    query = unquote(query)

    if request.method == "POST":
        if not request.form.get("q"):
            return jsonify({"error": "No query provided"}), 400

        else:
            movie_query = request.form.get("q")
            return redirect(url_for('results', query=movie_query))

    try:
        movie_id = movie_ids[query]

    except KeyError:
        print("KeyError has been caught, using fuzzywuzzy")
        query = movie_finder(query, movies)
        movie_id = movie_ids[query]

    similar_movies = find_similar_movies(movie_id, X, movie_mapper, movie_inv_mapper, metric='cosine', k=26)
    similar_movies_data = []
    for s in similar_movies:
        search_title = movie_titles[s]
        similar_movies_data.append(tmdb_data(tmdb_ids, s, search_title, is_tmdb_id=False))

    return render_template("results.html", search_term=query, movies=similar_movies_data)


@app.route('/movie', methods=["GET", "POST"])
def movie():
    tmdb_movie_id = request.args.get("id")
    tmdb_movie_title = request.args.get("title")
    tmdb_movie_title = unquote(tmdb_movie_title)

    if not tmdb_movie_id:
        return "No id provided", 400
    elif not tmdb_movie_title:
        return "No title provided", 400

    if request.method == "POST":
        if not request.form.get("q"):
            return jsonify({"error": "No query provided"}), 400

        else:
            movie_query = request.form.get("q")
            return redirect(url_for('results', query=movie_query))

    movie_data = tmdb_data(tmdb_ids, tmdb_movie_id, tmdb_movie_title, is_tmdb_id=True)
    movie_credits = tmdb_cast(tmdb_movie_id, tmdb_movie_title)

    for crewmember in movie_credits["crew"]:
        if crewmember["job"] == "Director":
            movie_director = crewmember["name"]

    movie_cast = ""
    for i, actor in enumerate(movie_credits['cast']):
        if i >= 10:
            movie_cast += f"{actor['name']}"
            break
        movie_cast += f"{actor['name']}, "

    return render_template("movie.html", movie_data=movie_data, movie_director=movie_director, movie_cast=movie_cast)


@app.route('/search')
def search():
    query = request.args.get('query')

    if not query:
        return jsonify({"error": "No query provided"}), 400

        # Perform the search
    search = search_movies(query)

    # If no results are found
    if len(search) == 0:
        return jsonify({"message": "No movies found"}), 404

    return jsonify(search)


def search_movies(query, limit=10):
    # Connect to your database and perform a search
    global movies
    search = movies[movies['title'].str.contains(query, case=False, na=False, regex=False)][['title']].head(limit)
    # Return a list of matching movie titles
    return search['title'].head(limit).tolist()


if __name__ == "__main__":
    app.run(debug=True)
