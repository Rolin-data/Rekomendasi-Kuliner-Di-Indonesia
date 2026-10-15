"""Rekomendasi Kuliner Indonesia - catatan warung pribadi.

Bedanya dari versi pertama: data nggak lagi ditanam di dalam kode.
Semua item disimpan di file data_kuliner.json, jadi bisa ditambah,
diubah harganya, atau dihapus langsung dari program.

Fitur:
    1. Cari makanan/minuman/camilan sesuai budget
    2. Cari pakai nama, daerah, atau nama warung
    3. Paket hemat (makan + minum)
    4. Kelola data (tambah / ubah harga / hapus)
    5. Lihat semua data
    6. Keluar

Cara jalan: python kuliner.py
"""

import json
import os

NAMA_FILE = "data_kuliner.json"
KATEGORI_VALID = ["makanan", "minuman", "camilan"]
AMBANG_HEMAT = 0.5  # harga <= separuh budget dianggap hemat


# ---------------------------------------------------------------------------
# Bagian data (baca / tulis file)
# ---------------------------------------------------------------------------


def muat_data(path=NAMA_FILE):
    """Baca data dari file JSON. Kalau file belum ada, balikin list kosong."""
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def simpan_data(data, path=NAMA_FILE):
    """Tulis data ke file JSON."""
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        file.write("\n")


# ---------------------------------------------------------------------------
# Bagian logika (murni, nggak nyentuh file - gampang dites)
# ---------------------------------------------------------------------------


def rupiah(angka):
    """Ubah 15000 jadi Rp15.000."""
    return f"Rp{angka:,}".replace(",", ".")


def parse_budget(teks):
    """Ubah input jadi angka. Terima '20000', '20.000', 'Rp25,000'. Salah -> None."""
    bersih = (
        teks.lower()
        .replace("rp", "")
        .replace(".", "")
        .replace(",", "")
        .replace(" ", "")
        .strip()
    )
    if not bersih.isdigit():
        return None
    nilai = int(bersih)
    return nilai if nilai > 0 else None


def cari_kuliner(data, kategori, budget):
    """Ambil kuliner sesuai jenis dengan harga yang masih masuk budget."""
    hasil = [
        item
        for item in data
        if item["kategori"] == kategori and item["harga"] <= budget
    ]
    hasil.sort(key=lambda item: item["harga"])
    return hasil


def cari_kata_kunci(data, kata):
    """Cari dari potongan nama, daerah, atau nama warung."""
    kata = kata.lower()
    return [
        item
        for item in data
        if kata in item["nama"].lower()
        or kata in item["daerah"].lower()
        or kata in item.get("tempat", "").lower()
    ]


def rekomendasi_serupa(data, item, jumlah=3):
    """Cari yang jenisnya sama, harga paling dekat, dan utamakan satu daerah."""
    kandidat = [
        lain
        for lain in data
        if lain["kategori"] == item["kategori"] and lain["nama"] != item["nama"]
    ]
    kandidat.sort(key=lambda lain: abs(lain["harga"] - item["harga"]))

    satu_daerah = [lain for lain in kandidat if lain["daerah"] == item["daerah"]]
    daerah_lain = [lain for lain in kandidat if lain["daerah"] != item["daerah"]]
    return (satu_daerah + daerah_lain)[:jumlah]


def paket_hemat(data, budget):
    """Cari 1 makanan + 1 minuman dengan total paling mentok ke budget.

    Kalau masih ada sisa, tambahin camilan paling murah yang muat.
    Balikin None kalau budget-nya nggak cukup.
    """
    makanan = [
        item
        for item in data
        if item["kategori"] == "makanan" and item["harga"] <= budget
    ]
    minuman = [
        item
        for item in data
        if item["kategori"] == "minuman" and item["harga"] <= budget
    ]
    camilan = sorted(
        [item for item in data if item["kategori"] == "camilan"],
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


# ---------------------------------------------------------------------------
# Bagian tampilan
# ---------------------------------------------------------------------------


def tanya(prompt):
    """input() yang nggak bikin program error kalau sesi dihentikan."""
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print("\nOke, sampai jumpa.")
        raise SystemExit(0)


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
        tempat = item.get("tempat", "")
        if tempat:
            baris += f"  [{tempat}]"
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


def tampilkan_rekomendasi_serupa(data, item):
    print(f"\nKamu pilih {item['nama']} dari {item['daerah']}. Yang mirip ini:")
    for lain in rekomendasi_serupa(data, item):
        print(
            f"   - {lain['nama']:<24} {rupiah(lain['harga']):>10}  ({lain['daerah']})"
        )
    print()


# ---------------------------------------------------------------------------
# Bagian input
# ---------------------------------------------------------------------------


def tanya_budget():
    while True:
        teks = tanya("  Budget sekali makan (contoh 20000): ")
        budget = parse_budget(teks)
        if budget is None:
            print("  Isinya harus angka, ya.\n")
            continue
        return budget


def tanya_kategori():
    while True:
        teks = tanya("  Jenis (makanan / minuman / camilan): ").strip().lower()
        if teks in KATEGORI_VALID:
            return teks
        print("  Pilih salah satu: makanan, minuman, atau camilan.\n")


def tanya_angka(prompt, jumlah):
    """Minta nomor urut 1..jumlah. Balikin index (0-based) atau None."""
    jawab = tanya(prompt).strip()
    if jawab.isdigit() and 1 <= int(jawab) <= jumlah:
        return int(jawab) - 1
    return None


# ---------------------------------------------------------------------------
# Bagian kelola data
# ---------------------------------------------------------------------------


def tambah_data(data):
    print("\nCatat kuliner baru.")
    nama = tanya("  Nama kuliner: ").strip()
    if not nama:
        print("  Nama nggak boleh kosong.")
        return

    kategori = tanya_kategori()

    while True:
        budget = tanya_budget()
        if budget:
            break

    daerah = (
        tanya("  Daerah (contoh: DI Yogyakarta) [boleh kosong]: ").strip() or "Nasional"
    )
    tempat = tanya("  Nama warung / tempat (boleh kosong): ").strip()
    catatan = tanya("  Catatan (boleh kosong): ").strip()

    data.append(
        {
            "nama": nama,
            "kategori": kategori,
            "harga": budget,
            "daerah": daerah,
            "tempat": tempat,
            "catatan": catatan,
        }
    )
    simpan_data(data)
    print(f"\n  Tersimpan: {nama} ({rupiah(budget)}).")


def ubah_harga(data):
    if not data:
        print("\n  Belum ada data.")
        return
    tampilkan_daftar(data)
    pilih = tanya_angka("  Nomor yang mau diubah harganya: ", len(data))
    if pilih is None:
        print("  Nomornya nggak ada.")
        return
    item = data[pilih]
    print(f"  {item['nama']} sekarang {rupiah(item['harga'])}.")
    baru = tanya_budget()
    lama = item["harga"]
    item["harga"] = baru
    simpan_data(data)
    print(f"\n  Harga {item['nama']}: {rupiah(lama)} -> {rupiah(baru)}.")


def hapus_data(data):
    if not data:
        print("\n  Belum ada data.")
        return
    tampilkan_daftar(data)
    pilih = tanya_angka("  Nomor yang mau dihapus: ", len(data))
    if pilih is None:
        print("  Nomornya nggak ada.")
        return
    item = data[pilih]
    konfirmasi = tanya(f"  Hapus '{item['nama']}'? (y/n): ").strip().lower()
    if konfirmasi == "y":
        data.pop(pilih)
        simpan_data(data)
        print(f"\n  '{item['nama']}' udah dihapus.")
    else:
        print("\n  Batal, nggak jadi dihapus.")


def kelola_data(data):
    while True:
        print("\nKelola data saya:")
        print("  1. Tambah kuliner baru")
        print("  2. Ubah harga")
        print("  3. Hapus data")
        print("  4. Kembali")
        pilih = tanya("  Pilih (1/2/3/4): ").strip()

        if pilih == "1":
            tambah_data(data)
        elif pilih == "2":
            ubah_harga(data)
        elif pilih == "3":
            hapus_data(data)
        elif pilih == "4":
            return
        else:
            print("  Nggak ada menu itu. Ketik 1, 2, 3, atau 4.")


def lihat_semua(data):
    if not data:
        print("\n  Belum ada data. Pakai menu 4 buat nambah.")
        return
    makanan = [item for item in data if item["kategori"] == "makanan"]
    minuman = [item for item in data if item["kategori"] == "minuman"]
    camilan = [item for item in data if item["kategori"] == "camilan"]

    for judul, isi in (
        ("MAKANAN", makanan),
        ("MINUMAN", minuman),
        ("CAMILAN", camilan),
    ):
        print(f"\n{judul} ({len(isi)}):")
        kosong = f"  {'-' * 50}"
        print(kosong)
        for item in sorted(isi, key=lambda i: i["harga"]):
            baris = (
                f"  {item['nama']:<24} {rupiah(item['harga']):>10}  ({item['daerah']})"
            )
            if item.get("tempat"):
                baris += f"  [{item['tempat']}]"
            print(baris)
    print()


# ---------------------------------------------------------------------------
# Program utama
# ---------------------------------------------------------------------------


def main():
    data = muat_data()

    print("=" * 58)
    print("  CATATAN KULINER SAYA")
    print(f"  {len(data)} kuliner tercatat")
    print("=" * 58)

    if not data:
        print("\nData masih kosong. File data_kuliner.json belum ada isinya.")

    while True:
        print("\nMau ngapain?")
        print("  1. Cari makanan / minuman / camilan sesuai budget")
        print("  2. Cari pakai nama, daerah, atau warung")
        print("  3. Cari paket hemat (makan + minum)")
        print("  4. Kelola data saya")
        print("  5. Lihat semua data")
        print("  6. Keluar")
        pilihan = tanya("  Pilih (1-6): ").strip()

        if pilihan == "1":
            kategori = tanya_kategori()
            budget = tanya_budget()
            hasil = cari_kuliner(data, kategori, budget)
            print(f"\n{kategori.capitalize()} yang muat {rupiah(budget)}:")
            tampilkan_daftar(hasil, budget)

            if hasil:
                pilih = tanya_angka(
                    "  Mau lihat yang mirip? Ketik nomornya, atau Enter buat lanjut: ",
                    len(hasil),
                )
                if pilih is not None:
                    tampilkan_rekomendasi_serupa(data, hasil[pilih])

        elif pilihan == "2":
            kata = tanya("  Ketik nama / daerah / warung: ").strip()
            hasil = cari_kata_kunci(data, kata)
            print(f"\nHasil pencarian '{kata}':")
            tampilkan_daftar(hasil)

        elif pilihan == "3":
            budget = tanya_budget()
            tampilkan_paket(paket_hemat(data, budget), budget)

        elif pilihan == "4":
            kelola_data(data)

        elif pilihan == "5":
            lihat_semua(data)

        elif pilihan == "6":
            print("\nSip, makasih. Selamat makan!\n")
            break

        else:
            print("  Nggak ada menu itu. Ketik angka 1 sampai 6.")


if __name__ == "__main__":
    main()
