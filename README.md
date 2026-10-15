# Rekomendasi Kuliner Indonesia

Catatan kuliner berbasis terminal. Data nggak ditanam di dalam kode, tapi disimpan di
file `data_kuliner.json` — jadi bisa ditambah, diubah harganya, atau dihapus langsung
dari program. Ini bukan pura-pura jadi aplikasi nasional, tapi catatan warung buat
dipakai sendiri.

Kamu sebut jenis kuliner dan budget, program carikan yang muat, urutkan dari yang
termurah, lalu tawarkan pilihan yang mirip. Ada juga mode paket hemat: satu makanan +
satu minuman yang totalnya mentok ke budget.

Proyek ini portfolio project untuk latihan **struktur data**, **algoritma pencarian dan
pengurutan**, **penanganan file (JSON)**, **unit testing**, serta **Git version control**.

## Fitur

1. **Cari sesuai jenis + budget** — pilih makanan/minuman/camilan, isi harga maksimal.
2. **Tampil sisa uang** — tiap item langsung kelihatan sisa budgetnya.
3. **Label hemat** — item yang harganya separuh budget atau kurang ditandai `(hemat)`.
4. **Cari pakai nama, daerah, atau warung** — mis. ketik `Jogja` atau `Bu Tini`.
5. **Paket hemat** — cari kombinasi 1 makanan + 1 minuman dengan total paling mendekati
   budget tapi tidak lewat. Kalau masih ada sisa, camilan termurah ikut ditambahkan.
6. **Rekomendasi serupa** — dari item yang kamu pilih, program saranin item lain dengan
   jenis sama, utamakan daerah yang sama, urut dari harga terdekat.
7. **Kelola data** — tambah kuliner baru, ubah harga, atau hapus, langsung tersimpan ke
   `data_kuliner.json`.
8. **Lihat semua data** — semua isi catatan, dikelompokkan per kategori.

## Data

Data disimpan di `data_kuliner.json` sebagai array JSON. Tiap item bentuknya begini:

```json
{
  "nama": "Gudeg Jogja",
  "kategori": "makanan",
  "harga": 20000,
  "daerah": "DI Yogyakarta",
  "tempat": "",
  "catatan": ""
}
```

| Field | Isi |
|---|---|
| `nama` | nama kuliner |
| `kategori` | `makanan`, `minuman`, atau `camilan` |
| `harga` | perkiraan harga per porsi (rupiah) |
| `daerah` | daerah asal, atau `Nasional` kalau sudah menyebar |
| `tempat` | nama warung/tempat, boleh kosong |
| `catatan` | catatan bebas, boleh kosong |

Jumlah awal **35 item** (15 makanan, 10 minuman, 10 camilan). Field `tempat` dan
`catatan` sengaja dikosongin — isi sendiri lewat menu **Kelola data** biar jadi catatan
yang beneran punya kamu (harga di warung langgananmu, bukan kira-kira).

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
| Pencarian kata kunci | Substring match pada `nama`, `daerah`, dan `tempat` (case-insensitive) |
| Pengurutan | `list.sort()` dengan `key=lambda item: item["harga"]` |
| Rekomendasi serupa | Urut berdasarkan selisih harga (`abs(harga_a - harga_b)`), lalu prioritaskan daerah yang sama |
| Paket hemat | Cek semua kombinasi (makanan × minuman), ambil yang total paling besar tapi ≤ budget, lalu tambahkan camilan termurah yang masih muat sisa |
| Label hemat | Ditandai kalau `harga <= 0.5 * budget` |
| Baca/tulis data | `json.load()` dan `json.dump()` ke `data_kuliner.json` |
| Parsing input budget | Buang `Rp`, titik, koma, dan spasi lalu `int()`. Jadi `20.000` maupun `Rp25,000` tetap valid |

## Cara Menjalankan

Butuh Python 3 (tanpa library tambahan).

```powershell
cd Rekomendasi-Kuliner-Di-Indonesia
python kuliner.py
```

Data dibaca dari `data_kuliner.json` di folder yang sama. Kalau file itu nggak ada,
program tetap jalan tapi daftarnya kosong (bisa diisi lewat menu Kelola data).

## Versi Web

Ada juga versi webnya (`index.html`) yang baca `data_kuliner.json` yang sama — enak buat
dibuka dari HP. Logikanya sama persis dengan versi Python (cari, paket hemat, rekomendasi
serupa), tapi **read-only**: buat nambah atau ngubah data tetap lewat versi terminal, atau
edit JSON-nya langsung.

Buka pakai server lokal — browser nggak boleh ambil file lain kalau halaman dibuka lewat
`file://`:

```powershell
python -m http.server 8000
# lalu buka http://localhost:8000
```

Bisa juga diaktifkan GitHub Pages-nya di repo ini (Settings → Pages → branch `main`,
folder `/`) biar langsung bisa dibuka online.

## Contoh Penggunaan

Output contoh (dari `test_input.txt`):

```
==========================================================
  CATATAN KULINER SAYA
  35 kuliner tercatat
==========================================================

Mau ngapain?
  1. Cari makanan / minuman / camilan sesuai budget
  2. Cari pakai nama, daerah, atau warung
  3. Cari paket hemat (makan + minum)
  4. Kelola data saya
  5. Lihat semua data
  6. Keluar
  Pilih (1-6):   Jenis (makanan / minuman / camilan):   Budget sekali makan (contoh 20000): 

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
Rekomendasi-Kuliner-Di-Indonesia/
├── kuliner.py         # program utama + logika (CLI)
├── data_kuliner.json  # isi catatan (dipakai CLI dan versi web)
├── index.html         # versi web (Tailwind, read-only)
├── test_kuliner.py    # unit test
├── test_input.txt     # contoh input buat uji CLI
├── BLOG_POST.md       # tulisan teknis
├── BLOG_POST.html     # versi HTML-nya
├── convert_blog.py    # ubah BLOG_POST.md jadi HTML
└── README.md
```

## Pengujian

Unit test (nggak nyentuh `data_kuliner.json`, pakai data buatan):

```powershell
python -m unittest -v test_kuliner
```

Uji program CLI pakai contoh input:

```powershell
cmd /c "python kuliner.py < test_input.txt"
```

Versi web diuji manual di browser: hasil pencarian, paket hemat, dan daftar semua data
dicek sama dengan output versi Python.
