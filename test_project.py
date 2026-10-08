from project import (
    find_movie_by_id,
    match_score,
    movie_exists,
    parse_movie_data,
    recommend_movies,
)

# Tests will be written step by step while the project grows.
# Start with pure functions first: match_score() and recommend_movies().


def test_match_score_rejects_long_movie():
    movie = {
        "runtime": 180,
        "imdb_rating": 8.0,
        "tags": ["sci-fi", "adventure"],
    }

    result = match_score(
        movie,
        tags=["sci-fi"],
        max_runtime=120,
        min_rating=7.0,
    )

    assert result == 0

def test_match_score_rejects_low_rating():
    movie = {
        "runtime": 160,
        "imdb_rating": 6.5,
        "tags": ["sci-fi", "adventure"],
    }

    result = match_score(
        movie, 
        tags=[],
        max_runtime=180,
        min_rating=7,
    )

    assert result == 0

def test_match_score_counts_matching_tags():
    movie = {
        "runtime": 165,
        "imdb_rating": 8.0,
        "tags": ["sci-fi", "adventure"],
    }

    result = match_score(
        movie,
        tags=["sci-fi", "adventure"],
        max_runtime=180,
        min_rating=7,
    )
    
    assert result == 3
    
def test_recommend_movies_includes_matching_movie():
    movie = {
        "imdb_id": "tt001",
        "runtime": 120,
        "imdb_rating": 8.0,
        "tags":["sci-fi"],
    }

    movies = [movie]
    result = recommend_movies(movies, tags=["sci-fi"], max_runtime=180, min_rating=7.0, history=[])
 
    assert len(result) == 1
    assert result[0]["score"] == 2

def test_recommend_movies_excludes_history():
    movie = {
        "imdb_id": "tt001",
        "runtime": 120,
        "imdb_rating": 8.0,
        "tags":[],
    }

    movies = [movie]
    result = recommend_movies(movies, tags=[], max_runtime=180, min_rating=7.0, history=["tt001"])

    assert len(result) == 0

def test_movie_exists_returns_true_for_same_imdb_id():
    new_movie = {"imdb_id": "tt001"}
    saved_movies = [{"imdb_id": "tt001"}]

    result = movie_exists(new_movie, saved_movies)
    assert result is True

def test_movie_exists_returns_false_for_different_imdb_id():
    new_movie = {"imdb_id": "tt002"}
    saved_movies = [{"imdb_id": "tt001"}]

    result = movie_exists(new_movie, saved_movies)
    assert result is False

def test_find_movie_by_id_returns_matching_movie():
    movie = {
        "imdb_id": "tt001",
        "runtime": 145,
        "imdb_rating": 8.0,
        "tags": ["sci-fi"],
    }
    
    imdb_id = movie["imdb_id"]
    movies = [movie]
    result = find_movie_by_id(movies, imdb_id)

    assert result == movie

def test_find_movie_by_id_returns_none_when_missing():
    movie = {
        "imdb_id": "tt001",
        "runtime": 145,
        "imdb_rating": 8.0,
        "tags": ["sci-fi"],
    }
    
    movies = [movie]
    result = find_movie_by_id(movies, "tt999")

    assert result is None


def test_parse_movie_data():
    data = {
        "Title": "Test Movie",
        "Year": "1999",
        "imdbID": "tt001",
        "imdbRating": "8.0",
        "Runtime": "136 min",
        "Genre": "Action, Sci-Fi"
    }

    result = parse_movie_data(data)
    assert result["runtime"] == 136
    assert result["year"] == 1999
    assert result["imdb_rating"] == 8.0
    assert result["genres"] == ["Action", "Sci-Fi"]
    assert result["tags"] == ["action", "sci-fi"]



