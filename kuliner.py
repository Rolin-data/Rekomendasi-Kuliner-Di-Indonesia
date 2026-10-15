"""Rekomendasi Kuliner Indonesia.

Program sederhana berbasis terminal:
    1. Pengguna memasukkan jenis kuliner (makanan / minuman / camilan)
       dan budget maksimal per porsi.
    2. Program mencari kuliner yang cocok dari data_kuliner.DATA_KULINER.
    3. Hasil diurutkan dari harga termurah.
    4. Pengguna bisa memilih salah satu untuk melihat rekomendasi serupa
       (kategori sama, daerah sama, harga terdekat).

Jalankan dengan:  python kuliner.py
"""

from data_kuliner import DATA_KULINER

KATEGORI_VALID = ["makanan", "minuman", "camilan"]


def tanya(prompt):
    """input() yang tidak crash saat sesi dihentikan (Ctrl+C / Ctrl+D)."""
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print("\n  Sesi diakhiri.")
        raise SystemExit(0)


def rupiah(angka):
    """Ubah 15000 menjadi 'Rp15.000'."""
    return "Rp{:,}".format(angka).replace(",", ".")


def cari_kuliner(kategori, budget):
    """Filter berdasarkan kategori dan budget, lalu urutkan dari termurah."""
    hasil = [
        item
        for item in DATA_KULINER
        if item["kategori"] == kategori and item["harga"] <= budget
    ]
    hasil.sort(key=lambda item: item["harga"])
    return hasil


def cari_kata_kunci(kata):
    """Cari kuliner dari potongan nama atau daerah."""
    kata = kata.lower()
    return [
        item
        for item in DATA_KULINER
        if kata in item["nama"].lower() or kata in item["daerah"].lower()
    ]


def rekomendasi_serupa(item, jumlah=3):
    """Rekomendasi lain dengan kategori sama, diurutkan dari harga terdekat."""
    kandidat = [
        lain
        for lain in DATA_KULINER
        if lain["kategori"] == item["kategori"] and lain["nama"] != item["nama"]
    ]
    kandidat.sort(key=lambda lain: abs(lain["harga"] - item["harga"]))

    # Utamakan yang satu daerah, sisanya dari daerah lain.
    satu_daerah = [lain for lain in kandidat if lain["daerah"] == item["daerah"]]
    daerah_lain = [lain for lain in kandidat if lain["daerah"] != item["daerah"]]
    return (satu_daerah + daerah_lain)[:jumlah]


def tampilkan_daftar(daftar):
    if not daftar:
        print(
            "\n  Tidak ada kuliner yang cocok. Coba naikkan budget atau ganti jenis.\n"
        )
        return
    print("")
    for nomor, item in enumerate(daftar, start=1):
        print(
            "  {}. {:<24} {:>10}  ({})".format(
                nomor, item["nama"], rupiah(item["harga"]), item["daerah"]
            )
        )
    print("")


def minta_budget():
    while True:
        teks = tanya("  Budget maksimal per porsi (contoh 20000): ").strip()
        try:
            budget = int(teks.replace(".", "").replace(",", ""))
        except ValueError:
            print("  Masukkan angka saja, ya.\n")
            continue
        if budget <= 0:
            print("  Budget harus lebih dari 0.\n")
            continue
        return budget


def tanya_kategori():
    while True:
        teks = tanya("  Jenis (makanan / minuman / camilan): ").strip().lower()
        if teks in KATEGORI_VALID:
            return teks
        print("  Pilihan harus salah satu dari: makanan, minuman, camilan.\n")


def tampilkan_rekomendasi_serupa(item):
    print(
        "\n  Karena kamu tertarik pada {} dari {}, coba juga:".format(
            item["nama"], item["daerah"]
        )
    )
    for lain in rekomendasi_serupa(item):
        print(
            "   - {:<24} {:>10}  ({})".format(
                lain["nama"], rupiah(lain["harga"]), lain["daerah"]
            )
        )
    print("")


def main():
    print("=" * 58)
    print("  REKOMENDASI KULINER INDONESIA")
    print("  Total data: {} kuliner".format(len(DATA_KULINER)))
    print("=" * 58)

    while True:
        print("\nMenu:")
        print("  1. Cari rekomendasi berdasarkan jenis + budget")
        print("  2. Cari berdasarkan nama / daerah")
        print("  3. Keluar")
        pilihan = tanya("  Pilih menu (1/2/3): ").strip()

        if pilihan == "1":
            kategori = tanya_kategori()
            budget = minta_budget()
            hasil = cari_kuliner(kategori, budget)
            print(
                "\n  Hasil untuk {} dengan harga <= {}:".format(
                    kategori, rupiah(budget)
                )
            )
            tampilkan_daftar(hasil)

            if hasil:
                jawab = tanya(
                    "  Lihat rekomendasi serupa? Masukkan nomor, atau Enter untuk lewati: "
                ).strip()
                if jawab.isdigit() and 1 <= int(jawab) <= len(hasil):
                    tampilkan_rekomendasi_serupa(hasil[int(jawab) - 1])

        elif pilihan == "2":
            kata = tanya("  Kata kunci (nama atau daerah): ").strip()
            hasil = cari_kata_kunci(kata)
            print("\n  Hasil pencarian '{}':".format(kata))
            tampilkan_daftar(hasil)

        elif pilihan == "3":
            print("\n  Terima kasih. Selamat menikmati kuliner Indonesia!\n")
            break

        else:
            print("  Menu tidak dikenal. Ketik 1, 2, atau 3.")


if __name__ == "__main__":
    main()
