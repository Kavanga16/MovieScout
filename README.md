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
