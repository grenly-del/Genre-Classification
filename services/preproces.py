import re
import nltk
from nltk.corpus import stopwords
from deep_translator import GoogleTranslator

# Download stopwords hanya sekali
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

def translate_to_english(text):
    return GoogleTranslator(source='auto', target='en').translate(text)

def process_text(text):
    # Lowercase dan hapus simbol
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Hapus stopwords
    filtered_text = ' '.join([word for word in text.split() if word not in stop_words])
    
    # Translate ke Bahasa Inggris
    translated_text = translate_to_english(filtered_text)
    
    print(translated_text)
    return translated_text
