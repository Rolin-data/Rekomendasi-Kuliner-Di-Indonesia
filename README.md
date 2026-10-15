# Rekomendasi Kuliner Indonesia

Program rekomendasi kuliner berbasis terminal. Pengguna memasukkan jenis kuliner dan budget,
program mencari pilihan yang cocok, mengurutkannya dari yang termurah, lalu menawarkan
rekomendasi serupa.

Proyek ini dikerjakan sebagai portfolio project untuk latihan **struktur data**, **algoritma
pencarian dan pengurutan**, serta **Git version control**.

## Fitur

1. **Rekomendasi berbasis kategori + budget** — filter jenis (makanan/minuman/camilan) dan harga maksimal.
2. **Pencarian kata kunci** — cari dari potongan nama atau daerah.
3. **Pengurutan harga** — hasil selalu diurutkan dari termurah.
4. **Rekomendasi serupa** — dari satu item yang dipilih, program menyarankan item lain
   dengan kategori sama, memprioritaskan daerah yang sama, diurutkan dari harga terdekat.

## Data

| Kategori | Jumlah item |
|---|---:|
| makanan | 15 |
| minuman | 10 |
| camilan | 10 |
| **Total** | **35** |

Tiap item disimpan sebagai dictionary:

```python
{
    "nama": "Gudeg Jogja",
    "kategori": "makanan",
    "harga": 20000,
    "daerah": "DI Yogyakarta",
}
```

Data lengkap ada di `data_kuliner.py`.

## Algoritma

| Kebutuhan | Implementasi |
|---|---|
| Pencarian (filter) | List comprehension: cocokkan `kategori` dan `harga <= budget` |
| Pencarian kata kunci | Substring match pada `nama` dan `daerah` (case-insensitive) |
| Pengurutan | `list.sort()` dengan `key=lambda item: item["harga"]` |
| Rekomendasi serupa | Urut berdasarkan selisih harga (`abs(harga_a - harga_b)`), lalu prioritaskan daerah yang sama |

## Cara Menjalankan

Butuh Python 3 (tanpa library tambahan).

```powershell
cd kuliner-recommender
python kuliner.py
```

## Contoh Penggunaan

Input: jenis `makanan`, budget `20000`, lalu pilih nomor `1`.

```
==========================================================
  REKOMENDASI KULINER INDONESIA
  Total data: 35 kuliner
==========================================================

  Hasil untuk makanan dengan harga <= Rp20.000:

  1. Kerak Telor                Rp12.000  (DKI Jakarta)
  2. Nasi Goreng Kampung        Rp15.000  (DKI Jakarta)
  3. Tinutuan Manado            Rp15.000  (Sulawesi Utara)
  4. Nasi Liwet Solo            Rp17.000  (Jawa Tengah)
  5. Bakso Malang               Rp18.000  (Jawa Timur)
  6. Gudeg Jogja                Rp20.000  (DI Yogyakarta)
  7. Pempek Palembang           Rp20.000  (Sumatera Selatan)
  8. Sate Madura                Rp20.000  (Jawa Timur)

  Karena kamu tertarik pada Kerak Telor dari DKI Jakarta, coba juga:
   - Nasi Goreng Kampung        Rp15.000  (DKI Jakarta)
   - Soto Betawi                Rp25.000  (DKI Jakarta)
   - Tinutuan Manado            Rp15.000  (Sulawesi Utara)
```

## Struktur Folder

```
kuliner-recommender/
├── kuliner.py        # program utama (CLI)
├── data_kuliner.py   # dataset kuliner
├── test_input.txt    # contoh input untuk pengujian otomatis
└── README.md
```

## Pengujian

```powershell
cmd /c "python kuliner.py < test_input.txt"
```
