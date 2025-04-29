import joblib
import google.generativeai as genai
# Load model dan vectorizer


# Konfigurasi API key (ganti dengan milikmu)
genai.configure(api_key="AIzaSyCNgUQQgeIu1bEQ8RrIuL6WzfmFtg_FvDk")

def check_genres(sample_text, path_model='model', path_vector='vectorizer2'):
    model = joblib.load(f'models/{path_model}.pkl') # Ganti Model (model.pkl---> LogisticRegression, model_MLP.pkl---> MLPClassifier)
    mlb = joblib.load('models/mlb.pkl')
    vectorizer = joblib.load(f'models/{path_vector}.pkl') # Ganti Vectorizer (vectorizer2.pkl---> LogisticRegression, vectorizer.pkl---> MLPClassifier)
    print(sample_text)
    sample_vec = vectorizer.transform([sample_text]) 
    # Dapatkan probabilitas untuk semua label
    probas = model.predict_proba(sample_vec)[0]  # ambil baris pertama (karena hanya satu input)
    # Ambil label genre dari MultiLabelBinarizer
    genre_labels = mlb.classes_

    # Gabungkan label dan proba-nya
    genre_probas = list(zip(genre_labels, probas))

    # Filter hanya label yang diprediksi aktif (threshold-nya default 0.5)
    predicted = [(genre, prob) for genre, prob in genre_probas if prob >= 0.5]

    # Urutkan berdasarkan confidence score (dari yang paling tinggi)
    predicted_sorted = sorted(predicted, key=lambda x: x[1], reverse=True)

    # Tampilkan
    print("Predicted genres with confidence scores:")
    for genre, score in predicted_sorted:
        print(f"{genre}: {score:.4f}")


    pred = model.predict(sample_vec)
    print(pred)
    return mlb.inverse_transform(pred)



# Fungsi klasifikasi menggunakan Gemini Pro (LLM)
def classify_genre_with_llm(sinopsis, allowed_genres): 
    prompt = f"""
Tugas kamu adalah mengklasifikasikan genre film berdasarkan sinopsis yang diberikan.
Berikan 1 sampai 3 genre yang paling sesuai dari daftar berikut:

{', '.join(allowed_genres)}

Sinopsis:
\"\"\"{sinopsis}\"\"\" 

Genre yang cocok:
"""

    # Gunakan model Gemini
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(prompt)
    print(response.text.strip().split(','))
    return response.text.strip().split(",")  # Membagi hasil genre dengan koma