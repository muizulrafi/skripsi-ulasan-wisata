import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.svm import SVC

from sklearn.metrics import (
    classification_report,
    accuracy_score
)

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
# FITUR & LABEL
# =========================================

X = df['stemming'].astype(str)

y = df['label']

# =========================================
# SPLIT DATA
# 70% TRAINING
# 30% DATA BARU
# =========================================

X_train, X_new, y_train, y_new = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42,
    stratify=y
)

# =========================================
# TF-IDF
# =========================================

tfidf = TfidfVectorizer(
    max_features=3000
)

X_train_tfidf = tfidf.fit_transform(X_train)

X_new_tfidf = tfidf.transform(X_new)

# =========================================
# MODEL SVM
# =========================================

model = SVC(
    kernel='rbf',
    C=1,
    gamma='scale',
    class_weight='balanced'
)

# training
model.fit(
    X_train_tfidf,
    y_train
)

# =========================================
# PREDIKSI
# =========================================

y_pred = model.predict(
    X_new_tfidf
)

# =========================================
# AKURASI
# =========================================

accuracy = accuracy_score(
    y_new,
    y_pred
)

print("\n=== UJI GENERALISASI ===\n")

print("Accuracy:")
print(round(accuracy * 100, 2), "%")

# =========================================
# CLASSIFICATION REPORT
# =========================================

report = classification_report(
    y_new,
    y_pred
)

print("\nClassification Report:\n")

print(report)

# =========================================
# SIMPAN HASIL
# =========================================

with open(
    "data/output/uji_generalisasi.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write("=== UJI GENERALISASI ===\n\n")

    f.write(
        f"Accuracy: {round(accuracy * 100, 2)}%\n\n"
    )

    f.write(report)

print("\nHasil uji generalisasi berhasil disimpan!")