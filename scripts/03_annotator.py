import pandas as pd
import random
import os

# =========================================
# LOAD DATASET
# =========================================

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
input_path = os.path.join(base_dir, "data", "labelling", "hasil_labeling.csv")

df = pd.read_csv(input_path, encoding='utf-8-sig')

# =========================================
# PILIH KOLOM
# =========================================

df = df[['nama_tempat', 'review', 'label_auto']]

# =========================================
# BUAT ID DATA
# =========================================

df['id_data'] = [
    f"UD-{str(i+1).zfill(4)}"
    for i in range(len(df))
]

# =========================================
# BUAT USER ID ANONIM
# =========================================

df['user_id_anonim'] = [
    f"User_{random.randint(100,999)}"
    for _ in range(len(df))
]

# =========================================
# GANTI NAMA KOLOM
# =========================================

df.rename(columns={
    'review': 'teks_ulasan',
    'label_auto': 'label'
}, inplace=True)

# =========================================
# AUTO CATATAN BERDASARKAN LABEL
# =========================================

def buat_catatan(label):
    notes = {
        "CONF": "Indikasi konflik sosial atau gangguan wisata",
        "GEND": "Indikasi pelecehan",
        "ECON": "Indikasi masalah ekonomi dan biaya",
        "INFRA": "Indikasi masalah fasilitas dan infrastruktur",
        "LAND": "Indikasi akses wisata",
        "DIGI": "Indikasi masalah fasilitas digital",
        "NEUT": "Ulasan positif atau netral tanpa keluhan sosial-ekonomi",
        "IRREL": "Ulasan tidak relevan atau tidak mengandung informasi penting"
    }
    return notes.get(label, "")

df['catatan'] = df['label'].apply(buat_catatan)

# =========================================
# URUTAN KOLOM FINAL
# =========================================

df = df[[
    'id_data',
    'user_id_anonim',
    'nama_tempat',
    'teks_ulasan',
    'label',
    'catatan'
]]

# =========================================
# SIMPAN EXCEL
# =========================================

save_path = os.path.join(base_dir, "data", "labelling", "lembar_kerja_anotator_final.xlsx")
df.to_excel(save_path, index=False)

print("Lembar kerja anotator final berhasil dibuat!")


