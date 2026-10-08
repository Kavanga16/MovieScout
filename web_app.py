import requests
from flask import Flask, render_template, request

from project import MOVIES_FILE, get_best_recommendation, scout_keyword

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    movie = None
    message = None
    
    if request.method == "POST":
        action = request.form.get("action")

        if action == "scout":
            query = request.form.get("query", "").strip()
            
            try:
                limit = int(request.form.get("limit", 10))

                if not 1 <= limit <= 20:
                    raise ValueError("Results must be between 1 and 20.")
                
                if not query:
                    raise ValueError("Enter a movie topic.")
                
                scout_keyword(query, MOVIES_FILE, limit=limit)
                message = f"Saved movies for: {query}"

            except ValueError as error:
                message = str(error)

            except requests.RequestException:
                message = "Movie services are temporarily unavailable. Try again later."

                


        elif action == "recommend":
            tags = request.form.get("tags", "").lower().split()
            
            try:
                max_runtime = int(request.form.get("max_runtime", 180))
                min_rating = float(request.form.get("min_rating", 0))

                if not 1 <= max_runtime <= 600:
                    raise ValueError("Runtime must be between 1 and 600 minutes.")
                
                if not 0 <= min_rating <= 10:
                    raise ValueError("Rating must be between 0 and 10.")
                
                movie = get_best_recommendation(
                    tags,
                    max_runtime,
                    min_rating,
                )

                if movie is None:
                    message = "No matching movies found. Try different filters."

            except ValueError as error:
                message = str(error)

            

        
    


            
    return render_template(
        "index.html",
        movie=movie,
        message=message,
    )

if __name__ == "__main__":
    app.run(debug=True)