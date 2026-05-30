import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# =========================================
# LOAD DATA
# =========================================

df = pd.read_excel(
    "data/preprocessing/hasil_preprocessing.xlsx"
)
# =========================================
# HAPUS DATA KOSONG
# =========================================

df = df.dropna()

# =========================================
# AMBIL TEKS STEMMING
# =========================================

texts = df['stemming']

# =========================================
# TF-IDF
# =========================================

tfidf = TfidfVectorizer()
X_tfidf = tfidf.fit_transform(texts)

# =========================================
# UBAH KE DATAFRAME
# =========================================

tfidf_df = pd.DataFrame(
    X_tfidf.toarray(),
    columns=tfidf.get_feature_names_out()
)

#tambah label
tfidf_df['label'] = df['label'].values

# =========================================
# SIMPAN KE FLASHDISK (E:)
# =========================================

tfidf_df.to_excel("E:/hasil_tfidf.xlsx", index=False)

# =========================================
# LIHAT HASIL
# =========================================

print("Jumlah Data:")
print(X_tfidf.shape)

print("\nContoh Feature:")
print(tfidf.get_feature_names_out()[:20])

print("\nTF-IDF berhasil dibuat dan disimpan ke E:/hasil_tfidf.xlsx")