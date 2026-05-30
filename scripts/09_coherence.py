import pandas as pd
from gensim import corpora
from gensim.models import LdaModel, CoherenceModel

def main():

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
    # COHERENCE SCORE
    # =========================================

    coherence_model = CoherenceModel(
        model=lda,
        texts=texts,
        dictionary=dictionary,
        coherence='c_v'
    )

    score = coherence_model.get_coherence()

    print("\nCoherence Score:")
    print(score)

    # =========================================
    # SIMPAN HASIL
    # =========================================

    with open(
        "data/output/coherence_score.txt",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(f"Coherence Score: {score}")

    print("\nCoherence score berhasil disimpan!")

# =========================================
# MAIN
# =========================================

if __name__ == "__main__":
    main()