import pandas as pd
import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# =========================================
# LOAD DATASET
# =========================================

df = pd.read_excel(
    "data/labelling/lembar_kerja_anotator_final.xlsx"
)
# =========================================
# PILIH KOLOM
# =========================================

df = df[['nama_tempat', 'teks_ulasan', 'label']]

# =========================================
# CLEANING TEXT
# =========================================

def cleaning_text(text):

    text = str(text).lower()

    # hapus url
    text = re.sub(r'http\S+', '', text)

    # hapus mention
    text = re.sub(r'@\w+', '', text)

    # hapus hashtag
    text = re.sub(r'#\w+', '', text)

    # hapus angka
    text = re.sub(r'\d+', '', text)

    # hapus tanda baca
    text = re.sub(r'[^\w\s]', '', text)

    # hapus spasi berlebih
    text = re.sub(r'\s+', ' ', text).strip()

    return text

df['cleaning'] = df['teks_ulasan'].apply(cleaning_text)

# =========================================
# TOKENIZING
# =========================================

df['tokenizing'] = df['cleaning'].apply(word_tokenize)

# =========================================
# STOPWORD REMOVAL
# =========================================

stop_words = set(stopwords.words('indonesian'))

def remove_stopwords(tokens):

    return [
        word for word in tokens
        if word not in stop_words
    ]

df['stopword'] = df['tokenizing'].apply(remove_stopwords)

# =========================================
# STEMMING
# =========================================

factory = StemmerFactory()
stemmer = factory.create_stemmer()

def stemming(tokens):

    kalimat = ' '.join(tokens)

    return stemmer.stem(kalimat)

df['stemming'] = df['stopword'].apply(stemming)

# =========================================
# SIMPAN HASIL
# =========================================

df.to_excel(
    "data/preprocessing/hasil_preprocessing.xlsx",
    index=False
)

print("Preprocessing selesai!")