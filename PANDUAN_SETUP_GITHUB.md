# 📖 Panduan Setup GitHub Actions — Otomasi Scraping Skripsi

## Apa yang terjadi setelah setup ini?
Setiap hari jam **06:00 WIB** dan **18:00 WIB**, GitHub akan otomatis:
1. Scraping ulasan baru dari semua lokasi Google Maps
2. Hanya menambahkan ulasan yang **belum ada** di dataset
3. Menjalankan preprocessing → SVM → LDA → Distribusi Topik → Coherence
4. Menyimpan semua hasilnya ke repo — bisa kamu download kapan saja

---

## LANGKAH SETUP (ikuti urutan ini)

### LANGKAH 1 — Buat akun GitHub
1. Buka https://github.com
2. Klik **Sign up**
3. Isi email, password, username → verifikasi email

---

### LANGKAH 2 — Install Git di laptop kamu
1. Buka https://git-scm.com/downloads
2. Download untuk Windows → install (next-next-finish)
3. Buka **Git Bash** (klik kanan di folder mana saja → "Git Bash Here")

---

### LANGKAH 3 — Buat repository baru di GitHub
1. Login ke github.com
2. Klik tombol **+** (pojok kanan atas) → **New repository**
3. Nama repo: `skripsi-ulasan-wisata` (bebas, tapi jangan ada spasi)
4. Pilih **Private** (supaya tidak publik)
5. Klik **Create repository**
6. **Salin URL repo-nya** (contoh: `https://github.com/username-kamu/skripsi-ulasan-wisata.git`)

---

### LANGKAH 4 — Upload folder skripsi ke GitHub
Buka **Git Bash** lalu ketik satu per satu:

```bash
# Masuk ke folder skripsi kamu (sesuaikan path-nya!)
cd /c/Users/NamaKamu/Downloads/skripsi_muiz_auto

# Inisialisasi git
git init

# Set identitas (ganti dengan nama & email kamu)
git config user.email "emailkamu@gmail.com"
git config user.name "Nama Kamu"

# Tambahkan semua file
git add .

# Commit pertama
git commit -m "Upload awal skripsi"

# Hubungkan ke GitHub (ganti URL dengan URL repo kamu!)
git remote add origin https://github.com/username-kamu/skripsi-ulasan-wisata.git

# Push ke GitHub
git push -u origin main
```

> Saat diminta login, masukkan username GitHub dan password GitHub kamu.

---

### LANGKAH 5 — Aktifkan GitHub Actions
1. Buka repo kamu di github.com
2. Klik tab **Actions** (di menu atas)
3. Jika ada pesan "Workflows aren't being run on this repository", klik **I understand my workflows, go ahead and enable them**
4. Selesai! Workflow otomatis sudah aktif.

---

### LANGKAH 6 — Test jalankan manual (opsional tapi dianjurkan)
1. Di tab **Actions**, klik **Auto Scraping & Analisis Ulasan** (di sidebar kiri)
2. Klik tombol **Run workflow** → **Run workflow**
3. Tunggu sekitar 30-60 menit
4. Cek hasilnya: tab **Actions** → klik run yang baru → lihat log tiap step

---

### Cara download hasil terbaru
1. Buka repo di github.com
2. Masuk folder `data/output/`
3. Klik file yang mau didownload → klik tombol **Download**

Atau dari Git Bash:
```bash
git pull
```
Semua file terbaru akan tersync ke laptop kamu.

---

## CATATAN PENTING

⚠️ **Google Maps bisa memblokir scraping** — kalau step scraping gagal (merah), coba:
- Kurangi jumlah scroll (ubah `range(30)` jadi `range(15)` di skrip)
- Jalankan hanya 1x sehari bukan 2x

✅ **File yang diubah dari versi sebelumnya:**
- `scripts/01_scraping_maps.py` → headless=True, tambah ulasan baru saja (tidak hapus data lama)

✅ **File baru yang ditambahkan:**
- `.github/workflows/auto_scraping.yml` → jadwal otomatis GitHub Actions
- `PANDUAN_SETUP_GITHUB.md` → panduan ini

