import pandas as pd
from gensim import corpora
from gensim.models import LdaModel

# =========================================
# LOAD DATA
# =========================================

df = pd.read_excel(
    "data/preprocessing/hasil_preprocessing.xlsx"
)

# =========================================
# HAPUS DATA KOSONG
# =========================================

df = df.dropna(subset=['stemming'])

# =========================================
# TOKENISASI
# =========================================

texts = [
    text.split()
    for text in df['stemming'].astype(str)
]

# =========================================
# DICTIONARY & CORPUS
# =========================================

dictionary = corpora.Dictionary(texts)

corpus = [
    dictionary.doc2bow(text)
    for text in texts
]

# =========================================
# MODEL LDA
# =========================================

lda = LdaModel(
    corpus=corpus,
    num_topics=5,
    id2word=dictionary,
    passes=10,
    random_state=42
)

# =========================================
# AMBIL TOPIK DOMINAN
# =========================================

dominant_topics = []

for doc in corpus:

    topics = lda.get_document_topics(doc)

    top_topic = max(
        topics,
        key=lambda x: x[1]
    )[0]

    dominant_topics.append(top_topic)

# =========================================
# MASUKKAN KE DATAFRAME
# =========================================

df['topik'] = dominant_topics

# =========================================
# DISTRIBUSI TOPIK
# =========================================

distribusi = (
    df['topik']
    .value_counts()
    .sort_index()
)

print("\nDistribusi Topik:\n")

print(distribusi)

# =========================================
# SIMPAN HASIL DISTRIBUSI
# =========================================

distribusi.to_excel(
    "data/output/distribusi_topik.xlsx"
)

# =========================================
# SIMPAN DATA TOPIK PER ULASAN
# =========================================

df.to_excel(
    "data/output/hasil_topik_per_ulasan.xlsx",
    index=False
)

print("\nDistribusi topik berhasil disimpan!")

# =========================================
# DISTRIBUSI TOPIK PER LOKASI
# =========================================

topik_lokasi = pd.crosstab(
    df['nama_tempat'],
    df['topik']
)

# =========================================
# GANTI NAMA TOPIK
# =========================================

topik_lokasi.columns = [
    'Topik 0 - Tempat Ibadah',
    'Topik 1 - Wisata Keluarga',
    'Topik 2 - Lokasi Wisata',
    'Topik 3 - Kualitas Lingkungan',
    'Topik 4 - Aktivitas Ekonomi'
]

# =========================================
# TAMPILKAN SEMUA DATA
# =========================================

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

print("\nDistribusi Topik Per Lokasi:\n")

print(topik_lokasi)

# =========================================
# SIMPAN HASIL
# =========================================

topik_lokasi.to_excel(
    "data/output/topik_per_lokasi.xlsx"
)

print("\nDistribusi topik per lokasi berhasil disimpan!")