# MovieScout

MovieScout is a Python and Flask application that helps users discover, save, and recommend movies using the OMDb and TMDb APIs with local JSON storage.

## Overview

MovieScout was built as a practical Python automation project. It reduces manual movie searching by combining keyword-based movie discovery, API data, local JSON storage, recommendation filters, and a simple Flask interface. Users can search for movie topics, save matching movies, filter recommendations by tags, runtime, and rating, and avoid repeated suggestions through a local history file.

## Features

- Keyword-based movie discovery using TMDb
- Movie details enrichment using OMDb
- Local JSON storage for saved movies and recommendation history
- Recommendation filtering by tags, runtime, and IMDb rating
- Duplicate detection based on IMDb IDs for saved movies and recommendation history
- Command-line interface for search, recommendation, and history commands
- Flask web interface for searching and recommendations
- Pytest coverage for parsing, filtering, recommendation, and lookup logic

## Tech Stack

- Python
- Flask
- Requests
- Pytest
- JSON
- HTML/CSS
- OMDb API
- TMDb API

## Project Structure
 
- `project.py` - core CLI, API, parsing, storage, and recommendation logic
- `web_app.py` - Flask web application
- `templates/` - HTML templates for the web interface
- `static/` - CSS styles
- `movies.example.json` - example local movie data structure
- `history.example.json` - example recommendation history structure
- `test_project.py` - pytest test suite
- `.env.example` - example environment variables

## Local Data Files

The app uses local JSON files for saved movies and recommendation history. These files are ignored by Git because they are local working data.

Before running the app, copy the example files:

```bash
cp movies.example.json movies.json
cp history.example.json history.json
```

## Setup

Clone the repository and install the dependencies:

```bash
git clone https://github.com/Kavanga16/MovieScout.git
cd MovieScout
python -m pip install -r requirements.txt
```

## Environment Variables

MovieScout requires API credentials for OMDb and TMDb.

Create a local `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Then fill in your own API keys:

```env
OMDB_API_KEY="your_omdb_api_key_here"
TMDB_READ_TOKEN="your_tmdb_read_token_here"
```

The `.env` file is ignored by Git and should not be committed.

## Usage

Run the Flask web interface:

```bash
python web_app.py
```

Use the command-line interface:

```bash
python project.py add "The Matrix"
python project.py discover "space"
python project.py scout "space travel" --limit 20
python project.py tonight --tags sci-fi adventure --max-runtime 180 --min-rating 7.0
python project.py history
python project.py bot
```

Main commands:

- `add` - search for a movie by title and save it locally
- `discover` - find and save movies from a topic query
- `scout` - find top movies by TMDb keyword search
- `tonight` - recommend a movie using tags, runtime, rating, and history 
- `history` - show previously recommended movies
- `bot` - start the interactive recommendation mode

## Running Tests 

Run the test suite with pytest:

```bash
python -m pytest
```

The tests cover movie parsing, recommendation scoring, duplicate detection, history filtering, and movie lookup logic.

## What I Learned

This project helped me practice:

- Working with external APIs and JSON responses
- Designing a local data format for saved movies and history
- Building command-line tools with Python
- Creating a simple Flask web interfaceа
- Writing tests for parsing, filtering, lookup, and recommendation logic
- Separating local secrets and working data from public repository files

## Roadmap

Possible future improvements:

- Improve the Flask interface with better movie cards and loading states
- Add pagination or sorting for larger movie lists
- Add more precise recommendation scoring
- Store movies and history in PostgreSQL instead of JSON files
- Add deployment instructions
