# Program Rekomendasi Kuliner Indonesia: Filter Budget, Paket Hemat, dan Cara Kerjanya

Rata-rata hari Sabtu malam aku selalu bingung milih makan. Bukan karena nggak ada pilihan — justru kebanyakan. Di satu sisi pengen yang murah, di sisi lain nggak mau asal murah tapi nggak kenyang. Akhirnya muter-muter di GoFood atau keliling kampung, capek sendiri.

Daripada kelamaan mikir, aku bikin program kecil di Python yang jawab pertanyaan simpel: **"Makan apa hari ini dengan budget segini?"** Programnya jalan di terminal, nggak pakai library tambahan, dan datanya 35 kuliner Indonesia dari sabang sampai merauke.

Namanya **Rekomendasi Kuliner Indonesia**. Repo-nya ada di [GitHub](https://github.com/Rolin-data/Rekomendasi-Kuliner-Di-Indonesia).

## Masalahnya kelihatan sepele, tapi nyebelin

Kalau lagi lapar dan buka aplikasi ojek online, yang muncul bukan "makan apa yang cocok", tapi justru "ini harganya masuk nggak ya budgetku?". Scroll bawah, klik item, lihat harga, tutup, scroll lagi. Capek. Belum lagi kalau mau sekalian nyari yang mirip sama makanan favoritku tapi versi lebih murah, atau lagi pengen hemat tapi tetap pengen makan + minum sekaligus.

Dari situ muncul ide bikin alat sederhana yang:

- Menerima input jenis kuliner (makanan, minuman, atau camilan) dan budget.
- Nge-filter yang harganya masih masuk.
- Ngeurutkan dari yang termurah.
- Kalau ada yang cocok, nyaranin yang mirip-mirip.
- Kalau budget-nya pas-pasan, cariin paket makan + minum yang totalnya nggak lebih dari budget.

## Data disimpan sebagai list of dictionary

Dataset ada di satu file `data_kuliner.py`, isinya list berisi 35 dictionary. Tiap dictionary punya empat kunci: `nama`, `kategori`, `harga`, dan `daerah`. Contohnya:

```python
{
    "nama": "Gudeg Jogja",
    "kategori": "makanan",
    "harga": 20000,
    "daerah": "DI Yogyakarta",
}
```

Harganya disimpan sebagai angka bulat, bukan string, biar gampang difilter dan diurutkan tanpa perlu parsing. `kategori` juga dipakai buat milih mode pencarian: makanan, minuman, atau camilan.

Yang bikin dataset ini beda dari dataset tutorial biasa: harganya bukan asal ketik. Sebelum di-commit, aku cek dulu harga kaki lima dan warung di beberapa sumber (Geokepo, Jakarta Tourism, The Indonesia Guide, dst.) buat tahun 2026. Hasilnya: nasi goreng kaki lima memang di kisaran Rp15.000–25.000, es teh manis Rp3.000–5.000, Soto Betawi di tempat legendaris bisa Rp40.000 ke atas. Angka-angka di dataset disesuaikan sama rentang itu, bukan dikarang.

Ada satu aturan tambahan: kalau sebuah hidangan sudah menyebar luas dan nggak bisa dibilang milik satu daerah lagi (kayak nasi goreng kampung, kopi tubruk, teh tarik, tahu isi), daerahnya ditulis `Nasional` — biar nggak ngaku-ngaku daerah orang.

## Algoritmanya nggak rumit, tapi nyambung sama masalahnya

### 1. Filter berdasarkan kategori dan budget

Ini inti dari program. Pakai list comprehension biasa:

```python
hasil = [
    item for item in DATA_KULINER
    if item["kategori"] == kategori and item["harga"] <= budget
]
```

Simpel, tapi cukup. Ambil yang jenisnya sesuai, harganya nggak lewat budget.

### 2. Diurutkan dari termurah

```python
hasil.sort(key=lambda item: item["harga"])
```

Biar user langsung lihat opsi paling hemat di paling atas. Nggak perlu algoritma sorting bikinan sendiri — `list.sort()` sudah cukup buat ukuran data segini.

### 3. Sisa uang dan label hemat

Tiap baris hasil nggak cuma nampilin nama dan harga, tapi juga sisa budget:

```python
baris += f"  sisa {rupiah(budget - item['harga'])}"
if item["harga"] <= budget * 0.5:
    baris += "  (hemat)"
```

Kalau harganya separuh budget atau kurang, diberi tanda `(hemat)`. Ini bantu user cepat ngenalin opsi yang paling irit tanpa harus hitung sendiri.

### 4. Pencarian bebas pakai kata kunci

Selain filter kategori+budget, ada mode cari dari potongan nama atau daerah. Case-insensitive, jadi ngetik `jogja`, `Jogja`, atau `JOGJA` hasilnya sama:

```python
kata = kata.lower()
return [
    item for item in DATA_KULINER
    if kata in item["nama"].lower() or kata in item["daerah"].lower()
]
```

### 5. Rekomendasi serupa: cari yang mirip, tapi utamakan satu daerah

Ini bagian yang paling aku suka. Logikanya: kalau user sudah nemu satu pilihan (misal Kerak Telor), program nyariin 3 item lain yang mirip. Tapi "mirip" di sini bukan sekadar kategori sama — ada bobot preferensi:

```python
kandidat.sort(key=lambda lain: abs(lain["harga"] - item["harga"]))
satu_daerah = [l for l in kandidat if l["daerah"] == item["daerah"]]
daerah_lain = [l for l in kandidat if l["daerah"] != item["daerah"]]
return (satu_daerah + daerah_lain)[:3]
```

Pertama, ambil semua item dengan kategori yang sama tapi beda nama. Kedua, urutkan berdasarkan selisih harga terkecil — ini konsep dasar *nearest neighbor*, cari yang paling dekat berdasarkan nilai numerik. Ketiga, pisahkan yang se-daerah sama yang beda daerah, lalu gabung dengan prioritas se-daerah duluan. Jadi kalau lagi cari yang mirip Kerak Telor, saran pertama yang muncul biasanya dari DKI Jakarta juga.

### 6. Paket hemat: makan + minum yang totalnya pas di budget

Ini fitur yang bikin program ini beda dari kebanyakan tutorial recommender. Tujuannya: cari kombinasi 1 makanan dan 1 minuman yang totalnya mentok semaksimal mungkin ke budget, tapi nggak lebih.

```python
for makan in makanan:
    for minum in minuman:
        total = makan["harga"] + minum["harga"]
        if total <= budget and (terbaik is None or total > terbaik["total"]):
            terbaik = {"makanan": makan, "minuman": minum, "total": total}
```

Ini brute force sederhana — makanan dikali minuman. Dengan 15 makanan dan 10 minuman, itu 150 kombinasi per pencarian. Jumlah kecil, jadi nggak ada masalah performa.

Kalau masih ada sisa budget setelah dapat kombinasi terbaik, program otomatis nambahin camilan termurah yang masih muat:

```python
sisa = budget - terbaik["total"]
for cemil in camilan:
    if cemil["harga"] <= sisa:
        terbaik["camilan"] = cemil
        break
```

Hasilnya: user dapat paket lengkap (makan, minum, kadang camilan) yang pemakaian budget-nya dimaksimalkan tanpa ada satu sen pun kelewat.

## Ngetes input "20.000" atau "20,000"

Waktu pertama kali demo, ada temen yang ngetik budget `20.000` (pakai titik) dan programnya error. Akhirnya ditambahin handling kecil di `tanya_budget()`:

```python
budget = int(teks.replace(".", "").replace(",", ""))
```

Jadi `20000`, `20.000`, dan `20,000` semuanya ke-parse jadi `20000`. Test input juga disiapin (`test_input.txt`) biar bisa diuji otomatis dari terminal tanpa harus ketik manual tiap kali:

```powershell
cmd /c "python kuliner.py < test_input.txt"
```

## Pelajaran dari project kecil ini

Tiga hal yang aku ambil:

**Algoritma sederhana bisa sangat berguna.** Nggak butuh machine learning buat masalah kayak gini. List comprehension, `sort()`, dan loop dua tingkat sudah cukup buat bikin program yang kepake sehari-hari.

**Prioritas bikin saran terasa logis.** Ide "utamakan daerah yang sama" di rekomendasi serupa bikin saranannya nggak terasa acak. Walaupun cuma bobot sederhana, dampaknya ke pengalaman user cukup besar.

**Fakta lebih baik dari asumsi.** Dataset yang kelihatan sederhana ternyata butuh riset juga — nggak asal ketik angka. Sekali salah harga, credibility program-nya langsung drop.

## Coba sendiri

Repo lengkap ada di [github.com/Rolin-data/Rekomendasi-Kuliner-Di-Indonesia](https://github.com/Rolin-data/Rekomendasi-Kuliner-Di-Indonesia). Clone, masuk foldernya, jalanin `python kuliner.py`, dan langsung bisa dipakai. Nggak perlu install apa-apa selain Python 3.
