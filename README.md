# Rekomendasi Kuliner Indonesia

Program rekomendasi kuliner berbasis terminal. Kamu sebut jenis kuliner dan budget,
program carikan yang muat, urutkan dari yang termurah, lalu tawarkan pilihan yang mirip.
Ada juga mode paket hemat: satu makanan + satu minuman yang totalnya mentok ke budget.

Proyek ini portfolio project untuk latihan **struktur data**, **algoritma pencarian dan
pengurutan**, serta **Git version control**.

## Fitur

1. **Cari sesuai jenis + budget** — pilih makanan/minuman/camilan, isi harga maksimal.
2. **Tampil sisa uang** — tiap item langsung kelihatan sisa budgetnya.
3. **Label hemat** — item yang harganya separuh budget atau kurang ditandai `(hemat)`.
4. **Cari pakai nama atau daerah** — mis. ketik `Jogja` atau `rendang`.
5. **Paket hemat** — cari kombinasi 1 makanan + 1 minuman dengan total paling mendekati
   budget tapi tidak lewat. Kalau masih ada sisa, camilan termurah ikut ditambahkan.
6. **Rekomendasi serupa** — dari item yang kamu pilih, program saranin item lain dengan
   jenis sama, utamakan daerah yang sama, urut dari harga terdekat.

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

### Sumber harga

Harga di atas bukan angka karangan. Acuan yang dipakai:

| Sumber | Yang diambil |
|---|---|
| Panduan harga makan Indonesia 2026 (geokepo.id) | Jajanan kaki lima Rp5.000–15.000; makan kaki lima Rp15.000–25.000; warung Rp20.000–40.000 |
| The Indonesia Guide — Warung Guide 2026 | Nasi goreng Rp15.000–30.000; kopi Rp5.000–15.000; es teh Rp5.000–10.000 |
| Jakarta Tourism — Cheap Eats Jakarta (2026) | Bakso Rp25.000–40.000; Soto Betawi Rp45.000–75.000; nasi goreng Rp20.000–40.000 |
| Jakarta Guides — How Jakarta Eats on the Street (2026) | Soto Betawi di tempat legendaris Rp40.000–70.000 |
| The Indonesia Guide | Harga di Bali 30–50% lebih tinggi dari Jawa (dasar penyesuaian Ayam Betutu) |

Catatan: harga bervariasi menurut kota dan tingkat pedagang. Angka di dataset adalah
**perkiraan tingkat warung/kaki lima**, bukan harga restoran.

Aturan penamaan `daerah`: kalau sebuah hidangan sudah menyebar dan tidak lagi milik satu
daerah tertentu (mis. nasi goreng kampung, kopi tubruk, tahu isi, teh tarik), daerahnya
ditulis `Nasional`.

## Algoritma

| Kebutuhan | Implementasi |
|---|---|
| Pencarian (filter) | List comprehension: cocokkan `kategori` dan `harga <= budget` |
| Pencarian kata kunci | Substring match pada `nama` dan `daerah` (case-insensitive) |
| Pengurutan | `list.sort()` dengan `key=lambda item: item["harga"]` |
| Rekomendasi serupa | Urut berdasarkan selisih harga (`abs(harga_a - harga_b)`), lalu prioritaskan daerah yang sama |
| Paket hemat | Cek semua kombinasi (makanan × minuman), ambil yang total paling besar tapi ≤ budget, lalu tambahkan camilan termurah yang masih muat sisa |
| Label hemat | Ditandai kalau `harga <= 0.5 * budget` |

## Cara Menjalankan

Butuh Python 3 (tanpa library tambahan).

```powershell
cd kuliner-recommender
python kuliner.py
```

## Contoh Penggunaan

Output contoh (dari `test_input.txt`):

```
==========================================================
  REKOMENDASI KULINER INDONESIA
  35 kuliner siap dipilih
==========================================================

Mau ngapain?
  1. Cari makanan / minuman / camilan sesuai budget
  2. Cari pakai nama atau daerah
  3. Cari paket hemat (makan + minum)
  4. Keluar
  Pilih (1/2/3/4):   Jenis (makanan / minuman / camilan):   Budget sekali makan (contoh 20000): 

Makanan yang muat Rp20.000:

  1. Kerak Telor                Rp12.000  (DKI Jakarta)  sisa Rp8.000
  2. Nasi Goreng Kampung        Rp15.000  (Nasional)  sisa Rp5.000
  3. Tinutuan Manado            Rp15.000  (Sulawesi Utara)  sisa Rp5.000
  4. Nasi Liwet Solo            Rp17.000  (Jawa Tengah)  sisa Rp3.000
  5. Bakso Malang               Rp18.000  (Jawa Timur)  sisa Rp2.000
  6. Gudeg Jogja                Rp20.000  (DI Yogyakarta)  sisa Rp0
  7. Pempek Palembang           Rp20.000  (Sumatera Selatan)  sisa Rp0
  8. Sate Madura                Rp20.000  (Jawa Timur)  sisa Rp0

  Mau lihat yang mirip? Ketik nomornya, atau Enter buat lanjut: 

Kamu pilih Kerak Telor dari DKI Jakarta. Yang mirip ini:
   - Soto Betawi                Rp40.000  (DKI Jakarta)
   - Nasi Goreng Kampung        Rp15.000  (Nasional)
   - Tinutuan Manado            Rp15.000  (Sulawesi Utara)

Paket hemat (budget Rp25.000): makanan Nasi Goreng Kampung + minuman Kopi Tubruk, total Rp25.000
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
