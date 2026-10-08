import argparse
import json
import os

import requests

MOVIES_FILE = "movies.json"
HISTORY_FILE = "history.json"
OMDB_URL = "http://www.omdbapi.com/"
TMDB_URL = "https://api.themoviedb.org/3"
OMDB_API_KEY_ENV = "OMDB_API_KEY"
TMDB_READ_TOKEN_ENV = "TMDB_READ_TOKEN"



DISCOVERY_TOPICS = {
    "space": {
        "queries": ["interstellar", "the martian", "gravity", "apollo 13", ]
    }
}
def main():
    args = parse_args()

    if args.command == "tonight":
        history = load_json(HISTORY_FILE)
        movies = load_movies(MOVIES_FILE)
        

        recommendations = recommend_movies(
            movies,
            tags=args.tags,
            max_runtime=args.max_runtime,
            min_rating=args.min_rating,
            history=history,
        )
        print_recommendation(recommendations)

        if recommendations:
            save_to_history(recommendations[0], HISTORY_FILE)

    elif args.command == "add":
        movie_data = search_movie(args.title)
        movie = parse_movie_data(movie_data)
        save_movie(movie, MOVIES_FILE)
    elif args.command == "discover":
        discover_movies(args.query, MOVIES_FILE)
    elif args.command == "scout":
        scout_keyword(args.query, MOVIES_FILE, limit=args.limit)
    elif args.command == "history":
        history = load_json(HISTORY_FILE)
        movies = load_movies(MOVIES_FILE)
        print_history(history, movies)
    elif args.command == "bot":
        bot_mode()
    else:
        print("Choose a command. Try: add, tonight, history, or bot")


def parse_args():
    parser = argparse.ArgumentParser(description="MovieScout: choose a movie to watch")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("history", help="Show recommendation history")

    

    add_parser = subparsers.add_parser("add", help="Search a movie through API and save it")
    add_parser.add_argument("title", help="Movie title, for example: The Matrix")

    discover_parser = subparsers.add_parser("discover", help="Find and save several movies by topic")
    discover_parser.add_argument("query", help="Search topic, for example: space or cyberpunk")

    scout_parser = subparsers.add_parser("scout", help="Find top movies by TMDb keyword")
    scout_parser.add_argument("query", help="Keyword, for example: space travel")
    scout_parser.add_argument("--limit", type=int, default=20, help="How many movies to save")

    tonight_parser = subparsers.add_parser("tonight", help="Recommend a movie for tonight")
    tonight_parser.add_argument("--tags", nargs="*", default=[], help="Mood tags, for example: cyberpunk action")
    tonight_parser.add_argument("--max-runtime", type=int, default=180, help="Maximum runtime in minutes")
    tonight_parser.add_argument("--min-rating", type=float, default=0.0, help="Minimum IMDb rating")

    subparsers.add_parser("bot", help="Start interactive bot mode")

    return parser.parse_args()


def get_api_key():
    key = os.getenv(OMDB_API_KEY_ENV)

    if not key:
        raise ValueError("Set OMDB_API_KEY in your environment.")

    return key

def get_tmdb_headers():
    token = os.getenv(TMDB_READ_TOKEN_ENV)

    if not token:
        raise ValueError("Set TMDB_API_KEY in your environment")
    return {
        "Authorization": f"Bearer {token}",
        "accept": "application/json",
    }
    
    

def search_movie(title):
    params = {
        "apikey": get_api_key(),
        "t": title,
    }

    response = requests.get(OMDB_URL, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    if data.get("Response") == "False":
        raise ValueError(data.get("Error", "Movie not found"))

    return data

def search_movies(query):
    params = {
        "apikey": get_api_key(),
        "s": query,
        "type": "movie",
    }

    response = requests.get(OMDB_URL, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    if data.get("Response") == "False":
        raise ValueError(data.get("Error", "No movies found"))
    
    return data["Search"]

def get_movie_by_id(imdb_id):
    params = {
        "apikey": get_api_key(),
        "i": imdb_id,
    }

    response = requests.get(OMDB_URL, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    if data.get("Response") == "False":
        raise ValueError(data.get("Error", "Movie not found"))
    
    return data

def discover_movies(query, filename):
    results = search_movies(query)

    for result in results:
        imdb_id = result["imdbID"]
        full_data = get_movie_by_id(imdb_id)
        movie = parse_movie_data(full_data)
        save_movie(movie, filename)
    

def discover_tmdb_movies(keyword_ids, limit=20):
    params = {
        "with_keywords": "|".join(str(keyword_id) for keyword_id in keyword_ids),
        "sort_by": "vote_average.desc",
        "vote_count.gte": 1000,
        "include_adult": "false",
        "page": 1,
    }

    response = requests.get(
        f"{TMDB_URL}/discover/movie",
        headers=get_tmdb_headers(),
        params=params,
        timeout=10
    )
    response.raise_for_status()

    data = response.json()
    return data.get("results", [])[:limit]


def find_tmdb_keyword_ids(query):
    words = query.lower().split()
    keyword_ids = []

    for word in words:
        response = requests.get(
            f"{TMDB_URL}/search/keyword",
            headers=get_tmdb_headers(),
            params={"query": word},
            timeout=10,
        )
        response.raise_for_status()

        results = response.json().get("results", [])

        if results:
            keyword_ids.append(results[0]["id"])

    if not keyword_ids:
        raise ValueError(f"No TMDb keywords found for: {query}")
    
    return keyword_ids

def get_imdb_id_from_tmdb(tmdb_id):
    response = requests.get(
        f"{TMDB_URL}/movie/{tmdb_id}/external_ids",
        headers=get_tmdb_headers(),
        timeout=10,
    )
    response.raise_for_status()

    data = response.json()
    return data.get("imdb_id")

def scout_keyword(query, filename, limit=20):
    keyword_id = find_tmdb_keyword_ids(query)
    tmdb_movies = discover_tmdb_movies(keyword_id, limit=limit)

    saved = 0

    for tmdb_movie in tmdb_movies:
        imdb_id = get_imdb_id_from_tmdb(tmdb_movie["id"])

        if not imdb_id:
            continue

        full_data = get_movie_by_id(imdb_id)
        movie = parse_movie_data(full_data)
        save_movie(movie, filename)
        saved += 1

    print(f"Scout saved {saved} movies for keyword: {query}")

def parse_movie_data(data):
    title = data["Title"]
    year = int(data["Year"])
    imdb_id = data["imdbID"]
    imdb_rating = float(data["imdbRating"])

    runtime_text = data["Runtime"]
    runtime = int(runtime_text.replace(" min", ""))

    genres_text = data["Genre"]
    genres = genres_text.split(", ")

    tags = [genre.lower() for genre in genres]
    imdb_url = f"https://www.imdb.com/title/{imdb_id}/"


    return {
        "title": title,
        "year": year,
        "imdb_id": imdb_id,
        "imdb_rating": imdb_rating,
        "runtime": runtime,
        "genres": genres,
        "tags": tags,
        "imdb_url": imdb_url,

    }


def scout_topic(topic_name, max_runtime, min_rating):
    pass

def load_json(filename):
    with open(filename, "r", encoding="utf-8-sig") as file:
        data = json.load(file)

    return data


def save_json(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)
    


def load_movies(filename):
    return load_json(filename)


def save_movie(movie, filename):
    movies = load_json(filename)

    if movie_exists(movie, movies):
        print(f"{movie['title']} is already saved.")
        return
    movies.append(movie)
    save_json(movies, filename)
    print(f"{movie['title']} saved.")


def match_score(movie, tags, max_runtime, min_rating):
    if movie["runtime"] > max_runtime:
        return 0 
    
    if movie["imdb_rating"] < min_rating:
        return 0
    
    score = 0

    for tag in tags:
        if tag in movie["tags"]:
            score += 1
    
    score += 1
    return score
    


def recommend_movies(movies, tags, max_runtime, min_rating, history=None):
    if history is None:
        history = []

    recommendations = []

    for movie in movies:
        if was_recommended(movie, history):
            continue

        score = match_score(movie, tags, max_runtime, min_rating)

        if score > 0:
            movie_with_score = movie.copy()
            movie_with_score["score"] = score
            recommendations.append(movie_with_score)

    recommendations.sort(key=lambda movie: movie["score"], reverse=True)

    return recommendations

def movie_exists(movie, movies):
    for saved_movie in movies:
        if saved_movie["imdb_id"] == movie["imdb_id"]:
            return True
    
    return False

def print_recommendation(recommendations):
    if not recommendations:
        print("No movies found.")
        return

    movie = recommendations[0]

    print("Tonight's pick:")
    print(f"{movie['title']} ({movie['year']})")
    print(f"Rating: {movie['imdb_rating']}")
    print(f"Runtime: {movie['runtime']} min")
    print(f"Genres: {', '.join(movie['genres'])}")
    print(f"IMDb: {movie['imdb_url']}")


def get_best_recommendation(tags, max_runtime, min_rating):
    movies = load_movies(MOVIES_FILE)
    history = load_json(HISTORY_FILE)

    recommendations = recommend_movies(
        movies,
        tags=tags,
        max_runtime=max_runtime,
        min_rating=min_rating,
        history=history,
    )

    if not recommendations:
        return None
    
    best_movie = recommendations[0]
    save_to_history(best_movie, HISTORY_FILE)

    return best_movie

def save_to_history(movie, filename):
    history = load_json(filename)
    history.append(movie["imdb_id"])
    save_json(history, filename)

def was_recommended(movie, history):
    return movie["imdb_id"] in history

def print_history(history, movies):
    if not history:
        print("History is empty.")
        return
    
    print("Recommendation history:")

    for imdb_id in history:
        movie = find_movie_by_id(movies, imdb_id)

        if movie is None:
            print(imdb_id)
        else:
            print(f"{movie['title']} ({movie['year']}) - {movie['imdb_rating']}")

def find_movie_by_id(movies, imdb_id):
    for movie in movies:
        if movie["imdb_id"] == imdb_id:
            return movie
        
        
    return None

def bot_mode():
    print("MovieScout bot")

    tags_text = input("Mood tags: ")
    max_runtime = int(input("Max runtime: "))
    min_rating = float(input("Min rating: "))

    tags = tags_text.split()

    movies = load_movies(MOVIES_FILE)   
    history = load_json(HISTORY_FILE)

    recommendations = recommend_movies(
        movies,
        tags=tags,
        max_runtime=max_runtime,
        min_rating=min_rating,
        history=history,
    )

    print_recommendation(recommendations)

    if recommendations:
        save_to_history(recommendations[0], HISTORY_FILE)



if __name__ == "__main__":
    main()
