import pandas as pd
import os

# =========================================
# KEYWORD LABEL 
# =========================================

label_keywords = {

    # -------------------------------------
    # CONF = Konflik Sosial 
    # -------------------------------------
    "CONF": [
        "dilarang",
        "diusir",
        "tidak boleh masuk",
        "khusus tamu",
        "pagar hotel",
        "preman",
        "pengamen",
        "ribut",
        "berantem",
        "parkir liar",
        "oknum",
    ],

    # -------------------------------------
    # LAND = Ketimpangan Lahan
    # -------------------------------------
    "LAND": [
        "sewa",
        "privatisasi",
        "dipagar",
        "lahan diambil",
        "penggusuran",
        "tanah dijual",
        "akses ditutup",
        "milik pribadi",
        "resort",
        "hotel menutup",
        "pantai ditutup"
    ],

    # -------------------------------------
    # GEND = Isu Gender
    # -------------------------------------
    "GEND": [
        "pelecehan",
        "tidak aman",
        "catcalling",
        "diganggu",
        "bahasa kotor",
        "ejekan",
        "bahaya",
        "ngeri",
        "berisik",
        "pacaran"
    ],

    # -------------------------------------
    # ECON = Ekonomi dan Modal
    # -------------------------------------
    "ECON": [
        "mahal",
        "murah",
        "palak",
        "pungli",
        "tarif",
        "parkir",
    ],

    # -------------------------------------
    # DIGI = Kesenjangan Digital
    # -------------------------------------
    "DIGI": [
        "sinyal",
        "signal",
        "internet",
        "wifi",
        "qris",
        "atm",
        "susah sinyal",
        "tidak ada jaringan",
        "e-money"
    ],

    # -------------------------------------
    # INFRA = Infrastruktur 
    # -------------------------------------
    "INFRA": [
        "jalan",
        "rusak",
        "berlubang",
        "sampah",
        "kotor",
        "toilet",
        "gelap",
        "becek",
        "bau",
    ],

    # -------------------------------------
    # NEUT = Netral / Positif
    # -------------------------------------
    "NEUT": [
        "bagus",
        "indah",
        "keren",
        "mantap",
        "rekomendasi",
        "sunset",
        "juara"
    ]
}

# =========================================
# PRIORITAS LABEL
# =========================================

priority = [
    "CONF",
    "ECON",
    "INFRA",
    "LAND",
    "GEND",
    "DIGI",
    "NEUT"
]

# =========================================
# FUNCTION AUTO LABEL
# =========================================

def auto_label(text):
    text = str(text).lower()
    found_labels = []
    for label, keywords in label_keywords.items():
        for word in keywords:
            if word in text:
                found_labels.append(label)
    for p in priority:
        if p in found_labels:
            return p
    return "IRREL"

# =========================================
# LOAD DATASET
# =========================================

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dataset_path = os.path.join(base_dir, "data", "raw", "dataset_final.csv")

df = pd.read_csv(
    dataset_path,
    sep=',',
    encoding='latin1',
    on_bad_lines='skip'
)

# =========================================
# BERSIHKAN NAMA KOLOM
# =========================================

df.columns = df.columns.str.strip()
print(df.columns.tolist())

# =========================================
# CLEANING REVIEW RINGAN
# =========================================

df['review'] = df['review'].astype(str)
df['review'] = df['review'].str.replace('\n', ' ', regex=False)
df['review'] = df['review'].str.replace('\r', ' ', regex=False)
df['review'] = df['review'].str.strip()

# =========================================
# AUTO LABELING
# =========================================

df['label_auto'] = df['review'].apply(auto_label)

# =========================================
# TAMBAHAN KOLOM VALIDASI MANUAL
# =========================================

df['label_final'] = df['label_auto']
df['catatan'] = ""

# =========================================
# SIMPAN HASIL
# =========================================

save_path = os.path.join(base_dir, "data", "labelling", "hasil_labeling.csv")
df.to_csv(save_path, index=False, encoding='utf-8')

# =========================================
# CEK DISTRIBUSI LABEL
# =========================================

print("\nDistribusi Label:\n")
print(df['label_auto'].value_counts())
print("\nFile berhasil disimpan: hasil_labeling.csv")
