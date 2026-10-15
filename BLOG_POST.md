# Membuat Program Rekomendasi Kuliner Indonesia Sederhana dengan Python

## Latar Belakang

Saat mau makan, pertanyaan yang sering muncul biasanya simpel: "Mau makan apa ya, tapi budget cuma segini?". Daripada bingung bolak-balik, lebih gampang kalau ada saran yang langsung sesuai kantong.

Dari situ muncul ide untuk membuat program rekomendasi kuliner Indonesia berbasis terminal. Tujuannya simpel: menerima input jenis kuliner (makanan, minuman, atau camilan) dan budget, lalu memberikan daftar pilihan yang masuk budget, diurutkan dari yang paling murah.

Proyek ini juga jadi latihan untuk mengaplikasikan konsep dasar pemrograman Python: struktur data, algoritma pencarian dan pengurutan, serta penggunaan Git untuk version control.

## Masalah yang Ingin Diselesaikan

1. **Terlalu banyak pilihan** — daftar kuliner Indonesia buanyak, susah milih kalau nggak tahu harganya.
2. **Budget terbatas** — butuh filter otomatis biar nggak usah cek satu per satu.
3. **Butuh saran yang relevan** — kalau sudah nemu satu pilihan, biasanya pengen yang mirip-mirip.
4. **Mau hemat tapi tetap kenyang** — kadang butuh kombinasi (makan + minum) biar totalnya pas di budget.

## Struktur Data

Program ini menyimpan datanya dalam bentuk list berisi dictionary Python.

```python
{
    "nama": "Gudeg Jogja",
    "kategori": "makanan",
    "harga": 20000,
    "daerah": "DI Yogyakarta",
}
```

Pemilihan struktur ini cukup simpel dan fleksibel. Kita bisa langsung mengakses `item["harga"]`, `item["kategori"]`, atau `item["daerah"]` tanpa perlu parsing rumit.

Dataset berisi **35 item kuliner Indonesia** yang terbagi jadi: makanan (15), minuman (10), dan camilan (10). Semua harganya menggunakan angka bulat (rupiah) agar mudah difilter dan diurutkan.

## Algoritma yang Dipakai

### 1. Filter Berdasarkan Kategori dan Budget

Langkah pertama adalah menyaring data yang sesuai permintaan user. Ini dilakukan dengan list comprehension:

```python
hasil = [
    item for item in DATA_KULINER
    if item["kategori"] == kategori and item["harga"] <= budget
]
```

Logika ini simpel tapi efektif: ambil semua item yang jenisnya sesuai dan harganya nggak lebih dari budget yang dimasukkan user.

### 2. Pengurutan dari Termurah

Agar user langsung lihat opsi paling hemat dulu, hasil filter diurutkan berdasarkan harga naik.

```python
hasil.sort(key=lambda item: item["harga"])
```

### 3. Pencarian Kata Kunci

Selain filter berdasarkan kategori+budget, ada juga mode pencarian bebas berdasarkan potongan nama atau daerah.

```python
kata = kata.lower()
return [
    item for item in DATA_KULINER
    if kata in item["nama"].lower() or kata in item["daerah"].lower()
]
```

Dengan pencarian case-insensitive, user bisa ketik `"jogja"`, `"Jogja"`, atau `"JOGJA"` dan tetap dapat hasilnya.

### 4. Rekomendasi Serupa

Fitur ini jawab pertanyaan: "Kalau aku suka ini, apa lagi yang mirip?".

1. Ambil semua item dengan **kategori yang sama**, tapi **beda nama**.
2. Urutkan berdasarkan **selisih harga terkecil**.
3. Prioritaskan item yang **berasal dari daerah yang sama** dengan pilihan user.
4. Ambil 3 teratas sebagai saran.

```python
kandidat.sort(key=lambda lain: abs(lain["harga"] - item["harga"]))
satu_daerah = [l for l in kandidat if l["daerah"] == item["daerah"]]
daerah_lain = [l for l in kandidat if l["daerah"] != item["daerah"]]
return (satu_daerah + daerah_lain)[:3]
```

Pendekatan ini mirip dengan konsep *nearest neighbor*: cari item terdekat berdasarkan nilai numerik (harga), dengan bobot preferensi daerah.

### 5. Paket Hemat (Makan + Minum)

Ini fitur yang bikin program beda dari contoh-contoh tutorial biasa. Tujuannya: cari kombinasi **1 makanan + 1 minuman** yang totalnya bisa mentok semaksimal mungkin ke budget.

```python
for makan in makanan:
    for minum in minuman:
        total = makan["harga"] + minum["harga"]
        if total <= budget and (terbaik is None or total > terbaik["total"]):
            terbaik = {...}
```

Strateginya adalah **brute force** sederhana (makanan × minuman). Jumlah datanya kecil (15×10 = 150 kombinasi per pencarian), jadi nggak ada masalah performa.

Tambahan kecil biar makin hemat: kalau masih ada sisa budget setelah dapat kombinasi terbaik, program otomatis menambahkan **camilan termurah** yang masih muat di sisa uang tersebut.

```python
sisa = budget - terbaik["total"]
for cemil in camilan:
    if cemil["harga"] <= sisa:
        terbaik["camilan"] = cemil
        break
```

### 6. Sisa Budget dan Label Hemat

Biar user bisa langsung lihat nilai gunanya, tiap hasil ditampilkan lengkap dengan **sisa uang**.

```python
baris += f"  sisa {rupiah(budget - item['harga'])}"
if item["harga"] <= budget * 0.5:
    baris += "  (hemat)"
```

Label `(hemat)` muncul kalau harganya **≤ 50% dari budget**.

## Pengujian

Program bisa diuji otomatis lewat file input. Contohnya `test_input.txt`:

```text
1
makanan
20000
1
3
25000
2
Jogja
4
```

Alurnya: cari makanan budget 20.000 → pilih item #1 (lihat rekomendasi serupa) → mode paket hemat budget 25.000 → cari berdasarkan kata kunci "Jogja" → keluar.

## Pelajaran yang Dipetik

1. **Algoritma sederhana bisa sangat berguna**. Nggak harus AI atau rumit buat menyelesaikan masalah sehari-hari.
2. **Prioritas bikin pengalaman terasa natural**. Ide "utamakan daerah sama" di rekomendasi serupa membuat sarannya terasa lebih logis ketimbang acak.
3. **Fakta lebih baik dari asumsi**. Penyesuaian harga dan penentuan label `Nasional` vs daerah spesifik dilakukan setelah dicek ke sumber lapangan (2026).
4. **Kode yang jelas lebih penting dari kode yang pintar**. List comprehension, `sort()`, dan loop sederhana membuat alur program mudah dibaca.

## Kesimpulan

Program ini berhasil memenuhi tujuannya: memberikan rekomendasi kuliner Indonesia yang relevan sesuai budget, dilengkapi sisa uang, label hemat, rekomendasi serupa, dan paket hemat. Semua logika dibangun dari nol dengan pendekatan yang lugas.

## Referensi

- [Panduan Harga Makan Indonesia 2026 – Geokepo](https://www.geokepo.id/id/panduan/how-much-food-costs-indonesia-2026-price-guide)
- The Indonesia Guide – Warung Guide 2026
- Jakarta Tourism – Cheap Eats Jakarta (2026)
- Jakarta Guides – How Jakarta Eats on the Street (2026)
