"""Unit test buat logika di kuliner.py.

Jalanin dengan:  python -m unittest -v

Test ini nggak nyentuh file data_kuliner.json, jadi hasilnya selalu sama
dan nggak bakal ngerusak data asli.
"""

import unittest

import kuliner

# Data buatan khusus buat tes. Harganya sengaja dibikin gampang dihitung.
DATA = [
    {"nama": "A", "kategori": "makanan", "harga": 10000, "daerah": "X", "tempat": ""},
    {"nama": "B", "kategori": "makanan", "harga": 15000, "daerah": "X", "tempat": ""},
    {"nama": "C", "kategori": "makanan", "harga": 20000, "daerah": "Y", "tempat": ""},
    {"nama": "H", "kategori": "makanan", "harga": 16000, "daerah": "Y", "tempat": ""},
    {"nama": "D", "kategori": "minuman", "harga": 5000, "daerah": "X", "tempat": ""},
    {"nama": "E", "kategori": "minuman", "harga": 8000, "daerah": "Y", "tempat": ""},
    {"nama": "F", "kategori": "camilan", "harga": 3000, "daerah": "X", "tempat": ""},
    {"nama": "G", "kategori": "camilan", "harga": 7000, "daerah": "Y", "tempat": ""},
]

# Data kecil khusus buat nguji penambahan camilan di paket hemat.
DATA_KECIL = [
    {"nama": "M1", "kategori": "makanan", "harga": 10000, "daerah": "X", "tempat": ""},
    {"nama": "D1", "kategori": "minuman", "harga": 5000, "daerah": "X", "tempat": ""},
    {"nama": "F1", "kategori": "camilan", "harga": 2000, "daerah": "X", "tempat": ""},
    {"nama": "F2", "kategori": "camilan", "harga": 6000, "daerah": "Y", "tempat": ""},
]


class TestRupiah(unittest.TestCase):
    def test_format_ribuan(self):
        self.assertEqual(kuliner.rupiah(15000), "Rp15.000")

    def test_format_jutaan(self):
        self.assertEqual(kuliner.rupiah(1250000), "Rp1.250.000")

    def test_nol(self):
        self.assertEqual(kuliner.rupiah(0), "Rp0")


class TestParseBudget(unittest.TestCase):
    def test_angka_biasa(self):
        self.assertEqual(kuliner.parse_budget("20000"), 20000)

    def test_pakai_titik(self):
        self.assertEqual(kuliner.parse_budget("20.000"), 20000)

    def test_pakai_koma_dan_rupiah(self):
        self.assertEqual(kuliner.parse_budget("Rp25,000"), 25000)

    def test_ada_spasi(self):
        self.assertEqual(kuliner.parse_budget(" 30 000 "), 30000)

    def test_bukan_angka(self):
        self.assertIsNone(kuliner.parse_budget("abc"))

    def test_nol_ditolak(self):
        self.assertIsNone(kuliner.parse_budget("0"))

    def test_kosong_ditolak(self):
        self.assertIsNone(kuliner.parse_budget(""))


class TestCariKuliner(unittest.TestCase):
    def test_filter_kategori(self):
        hasil = kuliner.cari_kuliner(DATA, "minuman", 999999)
        self.assertEqual([i["nama"] for i in hasil], ["D", "E"])

    def test_hormati_budget(self):
        hasil = kuliner.cari_kuliner(DATA, "makanan", 16000)
        self.assertEqual([i["nama"] for i in hasil], ["A", "B", "H"])

    def test_urut_dari_termurah(self):
        hasil = kuliner.cari_kuliner(DATA, "makanan", 999999)
        harga = [i["harga"] for i in hasil]
        self.assertEqual(harga, sorted(harga))

    def test_budget_kekecilan(self):
        self.assertEqual(kuliner.cari_kuliner(DATA, "makanan", 100), [])


class TestCariKataKunci(unittest.TestCase):
    def test_case_insensitive(self):
        hasil = kuliner.cari_kata_kunci(DATA, "x")
        self.assertEqual([i["nama"] for i in hasil], ["A", "B", "D", "F"])

    def test_cari_dari_daerah(self):
        hasil = kuliner.cari_kata_kunci(DATA, "Y")
        self.assertEqual([i["nama"] for i in hasil], ["C", "H", "E", "G"])

    def test_cari_dari_tempat(self):
        data = [
            {
                "nama": "Z",
                "kategori": "makanan",
                "harga": 1000,
                "daerah": "X",
                "tempat": "Warung Bu Tini",
            }
        ]
        hasil = kuliner.cari_kata_kunci(data, "bu tini")
        self.assertEqual(len(hasil), 1)


class TestRekomendasiSerupa(unittest.TestCase):
    def test_nggak_balikin_dirinya_sendiri(self):
        item = DATA[1]  # B
        hasil = kuliner.rekomendasi_serupa(DATA, item)
        self.assertNotIn("B", [i["nama"] for i in hasil])

    def test_kategori_harus_sama(self):
        hasil = kuliner.rekomendasi_serupa(DATA, DATA[0])  # A = makanan
        self.assertTrue(all(i["kategori"] == "makanan" for i in hasil))

    def test_utamakan_daerah_sama(self):
        # Untuk B (harga 15000, daerah X): H (daerah Y) selisihnya cuma 1000,
        # tapi A (daerah X) selisihnya 5000. Yang se-daerah harus muncul duluan.
        hasil = kuliner.rekomendasi_serupa(DATA, DATA[1])  # B
        self.assertEqual(hasil[0]["nama"], "A")

    def test_batasi_jumlah(self):
        hasil = kuliner.rekomendasi_serupa(DATA, DATA[0], jumlah=2)
        self.assertEqual(len(hasil), 2)


class TestPaketHemat(unittest.TestCase):
    def test_ambil_total_terbesar(self):
        paket = kuliner.paket_hemat(DATA, 20000)
        self.assertEqual(paket["makanan"]["nama"], "B")
        self.assertEqual(paket["minuman"]["nama"], "D")
        self.assertEqual(paket["total"], 20000)
        self.assertEqual(paket["sisa"], 0)

    def test_tambah_camilan_kalau_muat(self):
        paket = kuliner.paket_hemat(DATA_KECIL, 18000)
        self.assertEqual(paket["total"], 17000)  # M1 + D1 + F1
        self.assertEqual(paket["camilan"]["nama"], "F1")
        self.assertEqual(paket["sisa"], 1000)

    def test_nggak_nambah_camilan_kalau_nggak_muat(self):
        paket = kuliner.paket_hemat(DATA_KECIL, 15000)
        self.assertIsNone(paket["camilan"])
        self.assertEqual(paket["total"], 15000)

    def test_budget_nggak_cukup(self):
        self.assertIsNone(kuliner.paket_hemat(DATA_KECIL, 14000))


if __name__ == "__main__":
    unittest.main()
