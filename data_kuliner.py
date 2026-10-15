"""Dataset kuliner Indonesia.

Setiap item adalah dictionary dengan kunci:
    nama     : str   -> nama kuliner
    kategori : str   -> "makanan" / "minuman" / "camilan"
    harga    : int   -> perkiraan harga dalam rupiah
    daerah   : str   -> daerah asal kuliner
"""

DATA_KULINER = [
    {
        "nama": "Nasi Goreng Kampung",
        "kategori": "makanan",
        "harga": 15000,
        "daerah": "Nasional",
    },
    {
        "nama": "Nasi Padang Rendang",
        "kategori": "makanan",
        "harga": 30000,
        "daerah": "Sumatera Barat",
    },
    {
        "nama": "Soto Betawi",
        "kategori": "makanan",
        "harga": 40000,
        "daerah": "DKI Jakarta",
    },
    {
        "nama": "Gudeg Jogja",
        "kategori": "makanan",
        "harga": 20000,
        "daerah": "DI Yogyakarta",
    },
    {
        "nama": "Rawon Surabaya",
        "kategori": "makanan",
        "harga": 25000,
        "daerah": "Jawa Timur",
    },
    {
        "nama": "Bakso Malang",
        "kategori": "makanan",
        "harga": 18000,
        "daerah": "Jawa Timur",
    },
    {"nama": "Mie Aceh", "kategori": "makanan", "harga": 22000, "daerah": "Aceh"},
    {
        "nama": "Pempek Palembang",
        "kategori": "makanan",
        "harga": 20000,
        "daerah": "Sumatera Selatan",
    },
    {
        "nama": "Sate Madura",
        "kategori": "makanan",
        "harga": 20000,
        "daerah": "Jawa Timur",
    },
    {
        "nama": "Nasi Liwet Solo",
        "kategori": "makanan",
        "harga": 17000,
        "daerah": "Jawa Tengah",
    },
    {
        "nama": "Papeda Kuah Kuning",
        "kategori": "makanan",
        "harga": 28000,
        "daerah": "Papua",
    },
    {
        "nama": "Coto Makassar",
        "kategori": "makanan",
        "harga": 27000,
        "daerah": "Sulawesi Selatan",
    },
    {
        "nama": "Ayam Betutu Bali",
        "kategori": "makanan",
        "harga": 40000,
        "daerah": "Bali",
    },
    {
        "nama": "Tinutuan Manado",
        "kategori": "makanan",
        "harga": 15000,
        "daerah": "Sulawesi Utara",
    },
    {
        "nama": "Kerak Telor",
        "kategori": "makanan",
        "harga": 12000,
        "daerah": "DKI Jakarta",
    },
    {
        "nama": "Es Teh Manis",
        "kategori": "minuman",
        "harga": 5000,
        "daerah": "Nasional",
    },
    {
        "nama": "Es Jeruk Peras",
        "kategori": "minuman",
        "harga": 8000,
        "daerah": "Nasional",
    },
    {
        "nama": "Kopi Tubruk",
        "kategori": "minuman",
        "harga": 10000,
        "daerah": "Nasional",
    },
    {"nama": "Kopi Kintamani", "kategori": "minuman", "harga": 25000, "daerah": "Bali"},
    {
        "nama": "Wedang Jahe",
        "kategori": "minuman",
        "harga": 10000,
        "daerah": "Jawa Tengah",
    },
    {
        "nama": "Es Dawet Ayu",
        "kategori": "minuman",
        "harga": 10000,
        "daerah": "Jawa Tengah",
    },
    {
        "nama": "Cendol Betawi",
        "kategori": "minuman",
        "harga": 12000,
        "daerah": "DKI Jakarta",
    },
    {
        "nama": "Es Kelapa Muda",
        "kategori": "minuman",
        "harga": 12000,
        "daerah": "Nasional",
    },
    {
        "nama": "Teh Tarik",
        "kategori": "minuman",
        "harga": 12000,
        "daerah": "Nasional",
    },
    {"nama": "Bajigur", "kategori": "minuman", "harga": 9000, "daerah": "Jawa Barat"},
    {
        "nama": "Pisang Goreng Keju",
        "kategori": "camilan",
        "harga": 10000,
        "daerah": "Nasional",
    },
    {"nama": "Tahu Isi", "kategori": "camilan", "harga": 5000, "daerah": "Nasional"},
    {
        "nama": "Cireng Bumbu Rujak",
        "kategori": "camilan",
        "harga": 8000,
        "daerah": "Jawa Barat",
    },
    {
        "nama": "Risoles Mayo",
        "kategori": "camilan",
        "harga": 8000,
        "daerah": "Jawa Barat",
    },
    {"nama": "Klepon", "kategori": "camilan", "harga": 7000, "daerah": "Jawa Tengah"},
    {
        "nama": "Lupis Ketan",
        "kategori": "camilan",
        "harga": 6000,
        "daerah": "Jawa Tengah",
    },
    {
        "nama": "Kue Cubit",
        "kategori": "camilan",
        "harga": 9000,
        "daerah": "DKI Jakarta",
    },
    {
        "nama": "Serabi Notosuman",
        "kategori": "camilan",
        "harga": 12000,
        "daerah": "Jawa Tengah",
    },
    {
        "nama": "Martabak Mini",
        "kategori": "camilan",
        "harga": 15000,
        "daerah": "Nasional",
    },
    {
        "nama": "Kacang Sihobuk",
        "kategori": "camilan",
        "harga": 13000,
        "daerah": "Sumatera Utara",
    },
]
