import pandas as pd
from gensim import corpora
from gensim.models import LdaModel

# ========================
# 1. LOAD DATA HASIL PREPROCESSING
# ========================

df = pd.read_excel(
    "data/preprocessing/hasil_preprocessing.xlsx"
)

# ========================
# 2. AMBIL KOLOM STEMMING
# ========================

texts = df['stemming'].astype(str)

# ========================
# 3. TOKENISASI ULANG
# ========================

texts_token = [
    text.split()
    for text in texts
]

# ========================
# 4. BUAT DICTIONARY & CORPUS
# ========================

dictionary = corpora.Dictionary(texts_token)

corpus = [
    dictionary.doc2bow(text)
    for text in texts_token
]

# ========================
# 5. TENTUKAN JUMLAH TOPIK
# ========================

num_topics = 5

# ========================
# 6. TRAIN LDA
# ========================

lda_model = LdaModel(
    corpus=corpus,
    id2word=dictionary,
    num_topics=num_topics,
    passes=10,
    random_state=42
)

# ========================
# 7. TAMPILKAN TOPIK
# ========================

print("\nTopik yang ditemukan:\n")

hasil_topik = []

for i, topic in lda_model.print_topics(num_words=10):

    hasil = f"Topik {i+1}: {topic}"

    print(hasil)

    hasil_topik.append(hasil)

# ========================
# 8. SIMPAN HASIL TOPIK
# ========================

with open(
    "data/output/hasil_lda.txt",
    "w",
    encoding="utf-8"
) as f:

    for item in hasil_topik:
        f.write(item + "\n\n")

print("\nHasil LDA berhasil disimpan!")