import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC

from sklearn.metrics import (
    accuracy_score,
    classification_report
)

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
# FITUR DAN LABEL
# =========================================

X = df['stemming']

y = df['label']

# =========================================
# TF-IDF
# =========================================

tfidf = TfidfVectorizer()

X_tfidf = tfidf.fit_transform(X)

# =========================================
# TRAIN TEST SPLIT
# =========================================

X_train, X_test, y_train, y_test = train_test_split(
    X_tfidf,
    y,
    test_size=0.2,
    random_state=42
)

# =========================================
# MODEL SVM
# =========================================

model = LinearSVC()

# training model
model.fit(X_train, y_train)

# =========================================
# TESTING / PREDIKSI
# =========================================

y_pred = model.predict(X_test)

# =========================================
# AKURASI
# =========================================

accuracy = accuracy_score(y_test, y_pred)

print("Akurasi Model:")
print(round(accuracy * 100, 2), "%")

# =========================================
# EVALUASI MODEL
# =========================================

print("\nClassification Report:\n")

print(classification_report(
    y_test,
    y_pred
))

# =========================================
# STRATIFIED K-FOLD CROSS VALIDATION
# =========================================

skf = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

scores = cross_val_score(
    model,
    X_tfidf,
    y,
    cv=skf
)

print("\nCross Validation Score:")

print(scores)

print("\nRata-rata Cross Validation:")

print(round(scores.mean() * 100, 2), "%")

# =========================================
# HYPERPARAMETER TUNING
# =========================================

param_grid = {
    'C': [0.1, 1, 10],
    'gamma': [1, 0.1, 0.01],
    'kernel': ['rbf']
}

grid = GridSearchCV(
    SVC(),
    param_grid,
    refit=True,
    verbose=1
)

grid.fit(X_train, y_train)

print("\nBest Parameter:")

print(grid.best_params_)

print("\nBest Accuracy:")

print(round(grid.best_score_ * 100, 2), "%")

# =========================================
# ERROR ANALYSIS
# =========================================

# ambil index data test
test_index = y_test.index

# ambil data asli dari dataframe
error_df = df.loc[test_index].copy()

# tambahkan label actual dan prediksi
error_df['actual'] = y_test.values
error_df['predicted'] = y_pred

# ambil yang salah saja
error = error_df[
    error_df['actual'] != error_df['predicted']
]

print("\nJumlah Salah Klasifikasi:")
print(len(error))

# =========================================
# SIMPAN ERROR ANALYSIS
# =========================================

error.to_excel(
    "data/output/error_analysis.xlsx",
    index=False
)

print("\nFile error_analysis.xlsx berhasil disimpan")

model = LinearSVC(
    class_weight='balanced'
)

print(classification_report(
    y_test,
    y_pred,
    zero_division=0
))