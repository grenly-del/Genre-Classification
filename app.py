from flask import Flask, render_template, request
from services.preproces import process_text
from services.checkGenre import check_genres, classify_genre_with_llm


# Genres
allowed_genres = [
    "Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary",
    "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Mystery",
    "Romance", "Science Fiction", "TV Movie", "Thriller", "War", "Western"
]

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])    
def hello_world():
    status = False
    result = []  # Inisialisasi awal dengan array kosong
    model_choice = "TDF"
    if request.method == "POST":
        inputan = request.form['inputan']
        model_choice = request.form['model_choice']
        # Preprocess dan prediksi
        print(model_choice)
        cleaned = process_text(inputan)  
        predicted = check_genres(cleaned)
        if model_choice == "LLM":
            genre_string = classify_genre_with_llm(cleaned, allowed_genres)
            result = genre_string
            print(f"result LLM : {result}") 
        else:
            predicted = check_genres(cleaned, 'model', 'vectorizer2')
            if predicted and isinstance(predicted[0], (list, tuple)):
                    result = predicted[0]
            print(f"result TDF : {result}")

    return render_template("hello.html", genres=result, status=status) 

if __name__ == '__main__':  
    app.run(debug=True, port=3301)  