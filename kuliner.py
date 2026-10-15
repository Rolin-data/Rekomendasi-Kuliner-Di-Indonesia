"""Rekomendasi Kuliner Indonesia.

Program terminal sederhana. Kamu sebut jenis kuliner dan budget,
program nyariin yang masuk. Hasilnya diurutkan dari yang paling murah,
lengkap sama sisa uang, label hemat, dan saran yang mirip-mirip.

Cara jalan: python kuliner.py
"""

from data_kuliner import DATA_KULINER

KATEGORI_VALID = ["makanan", "minuman", "camilan"]
AMBANG_HEMAT = 0.5  # harga <= separuh budget dianggap hemat


def tanya(prompt):
    """input() yang nggak bikin program error kalau sesi dihentikan."""
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print("\nOke, sampai jumpa.")
        raise SystemExit(0)


def rupiah(angka):
    """Ubah 15000 jadi Rp15.000."""
    return f"Rp{angka:,}".replace(",", ".")


def cari_kuliner(kategori, budget):
    """Ambil kuliner sesuai jenis dengan harga yang masih masuk budget."""
    hasil = [
        item
        for item in DATA_KULINER
        if item["kategori"] == kategori and item["harga"] <= budget
    ]
    hasil.sort(key=lambda item: item["harga"])
    return hasil


def cari_kata_kunci(kata):
    """Cari dari potongan nama atau daerah."""
    kata = kata.lower()
    return [
        item
        for item in DATA_KULINER
        if kata in item["nama"].lower() or kata in item["daerah"].lower()
    ]


def rekomendasi_serupa(item, jumlah=3):
    """Cari yang jenisnya sama, harga paling dekat, dan utamakan satu daerah."""
    kandidat = [
        lain
        for lain in DATA_KULINER
        if lain["kategori"] == item["kategori"] and lain["nama"] != item["nama"]
    ]
    kandidat.sort(key=lambda lain: abs(lain["harga"] - item["harga"]))

    satu_daerah = [lain for lain in kandidat if lain["daerah"] == item["daerah"]]
    daerah_lain = [lain for lain in kandidat if lain["daerah"] != item["daerah"]]
    return (satu_daerah + daerah_lain)[:jumlah]


def paket_hemat(budget):
    """Cari 1 makanan + 1 minuman dengan total paling mentok ke budget.

    Kalau masih ada sisa, tambahin camilan paling murah yang muat.
    """
    makanan = [
        item
        for item in DATA_KULINER
        if item["kategori"] == "makanan" and item["harga"] <= budget
    ]
    minuman = [
        item
        for item in DATA_KULINER
        if item["kategori"] == "minuman" and item["harga"] <= budget
    ]
    camilan = sorted(
        [item for item in DATA_KULINER if item["kategori"] == "camilan"],
        key=lambda item: item["harga"],
    )

    terbaik = None
    for makan in makanan:
        for minum in minuman:
            total = makan["harga"] + minum["harga"]
            if total <= budget and (terbaik is None or total > terbaik["total"]):
                terbaik = {
                    "makanan": makan,
                    "minuman": minum,
                    "camilan": None,
                    "total": total,
                }

    if terbaik is None:
        return None

    sisa = budget - terbaik["total"]
    for cemil in camilan:
        if cemil["harga"] <= sisa:
            terbaik["camilan"] = cemil
            terbaik["total"] += cemil["harga"]
            break

    terbaik["sisa"] = budget - terbaik["total"]
    return terbaik


def tampilkan_daftar(daftar, budget=None):
    if not daftar:
        print("\nNggak ada yang cocok. Naikkan budget atau ganti jenisnya.")
        return

    print()
    for nomor, item in enumerate(daftar, start=1):
        baris = (
            f"{nomor}. {item['nama']:<24} {rupiah(item['harga']):>10}"
            f"  ({item['daerah']})"
        )
        if budget:
            baris += f"  sisa {rupiah(budget - item['harga'])}"
            if item["harga"] <= budget * AMBANG_HEMAT:
                baris += "  (hemat)"
        print("  " + baris)
    print()


def tampilkan_paket(paket, budget):
    if paket is None:
        print("\nBudget segitu belum cukup buat paket makan + minum.")
        print("Coba naikkan dikit, ya.")
        return

    print(f"\nPaket hemat buat budget {rupiah(budget)}:")
    print()
    print(
        f"  Makanan : {paket['makanan']['nama']} ({rupiah(paket['makanan']['harga'])})"
    )
    print(
        f"  Minuman : {paket['minuman']['nama']} ({rupiah(paket['minuman']['harga'])})"
    )
    if paket["camilan"]:
        print(
            f"  Camilan : {paket['camilan']['nama']}"
            f" ({rupiah(paket['camilan']['harga'])})"
        )
    else:
        print("  Camilan : belum muat")
    print()
    print(f"  Total   : {rupiah(paket['total'])}")
    print(f"  Sisa    : {rupiah(paket['sisa'])}")
    print()


def tanya_budget():
    while True:
        teks = tanya("  Budget sekali makan (contoh 20000): ").strip()
        try:
            budget = int(teks.replace(".", "").replace(",", ""))
        except ValueError:
            print("  Isinya harus angka, ya.\n")
            continue
        if budget <= 0:
            print("  Budget-nya harus lebih dari 0.\n")
            continue
        return budget


def tanya_kategori():
    while True:
        teks = tanya("  Jenis (makanan / minuman / camilan): ").strip().lower()
        if teks in KATEGORI_VALID:
            return teks
        print("  Pilih salah satu: makanan, minuman, atau camilan.\n")


def tampilkan_rekomendasi_serupa(item):
    print(f"\nKamu pilih {item['nama']} dari {item['daerah']}. Yang mirip ini:")
    for lain in rekomendasi_serupa(item):
        print(
            f"   - {lain['nama']:<24} {rupiah(lain['harga']):>10}  ({lain['daerah']})"
        )
    print()


def main():
    print("=" * 58)
    print("  REKOMENDASI KULINER INDONESIA")
    print(f"  {len(DATA_KULINER)} kuliner siap dipilih")
    print("=" * 58)

    while True:
        print("\nMau ngapain?")
        print("  1. Cari makanan / minuman / camilan sesuai budget")
        print("  2. Cari pakai nama atau daerah")
        print("  3. Cari paket hemat (makan + minum)")
        print("  4. Keluar")
        pilihan = tanya("  Pilih (1/2/3/4): ").strip()

        if pilihan == "1":
            kategori = tanya_kategori()
            budget = tanya_budget()
            hasil = cari_kuliner(kategori, budget)
            print(f"\n{kategori.capitalize()} yang muat {rupiah(budget)}:")
            tampilkan_daftar(hasil, budget)

            if hasil:
                jawab = tanya(
                    "  Mau lihat yang mirip? Ketik nomornya, atau Enter buat lanjut: "
                ).strip()
                if jawab.isdigit() and 1 <= int(jawab) <= len(hasil):
                    tampilkan_rekomendasi_serupa(hasil[int(jawab) - 1])

        elif pilihan == "2":
            kata = tanya("  Ketik nama atau daerah: ").strip()
            hasil = cari_kata_kunci(kata)
            print(f"\nHasil pencarian '{kata}':")
            tampilkan_daftar(hasil)

        elif pilihan == "3":
            budget = tanya_budget()
            tampilkan_paket(paket_hemat(budget), budget)

        elif pilihan == "4":
            print("\nSip, makasih. Selamat makan!\n")
            break

        else:
            print("  Nggak ada menu itu. Ketik 1, 2, 3, atau 4.")


if __name__ == "__main__":
    main()
