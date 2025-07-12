import csv
import os
from queue import Queue
from datetime import datetime

# Struktur data
antrian_transaksi = Queue()
kategori_map = {
    "makan": "Kebutuhan Pokok",
    "hiburan": "Non Pokok",
    "transport": "Kebutuhan Pokok",
    "lainnya": "Lainnya"
}

# File CSV
NAMA_FILE = "data.csv"

# Inisialisasi file CSV (jika belum ada)
def inisialisasi_csv():
    if not os.path.exists(NAMA_FILE):
        with open(NAMA_FILE, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["id", "tanggal", "jenis", "kategori", "jumlah", "keterangan"])

# Auto-generate ID transaksi
def generate_id():
    try:
        with open(NAMA_FILE, mode='r') as f:
            reader = list(csv.reader(f))
            if len(reader) <= 1:
                return 1
            last_id = int(reader[-1][0])
            return last_id + 1
    except:
        return 1

# CRUD: CREATE
def tambah_transaksi():
    id_transaksi = generate_id()
    tanggal = input("Tanggal (YYYY-MM-DD): ")
    jenis = input("Jenis (pemasukan/pengeluaran): ").lower()
    kategori = input("Kategori (makan/hiburan/transport/lainnya): ").lower()
    jumlah = float(input("Jumlah (Rp): "))
    keterangan = input("Keterangan: ")

    data = [str(id_transaksi), tanggal, jenis, kategori, str(jumlah), keterangan]
    antrian_transaksi.put(data)

    with open(NAMA_FILE, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)
    print("✅ Transaksi berhasil ditambahkan!")

# CRUD: READ
def tampilkan_data():
    try:
        with open(NAMA_FILE, mode='r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            print("\n📋 Data Transaksi:")
            print(f"{'ID':<5}{'Tanggal':<12}{'Jenis':<15}{'Kategori':<15}{'Jumlah':<12}{'Keterangan'}")
            print("-"*65)
            for row in reader:
                print(f"{row[0]:<5}{row[1]:<12}{row[2]:<15}{row[3]:<15}Rp{row[4]:<10}{row[5]}")
    except FileNotFoundError:
        print("❌ File tidak ditemukan.")

# CRUD: UPDATE
def update_transaksi():
    id_edit = input("Masukkan ID transaksi yang ingin diubah: ")
    data_baru = []

    updated = False
    with open(NAMA_FILE, mode='r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if row[0] == id_edit:
                print("Data ditemukan. Masukkan data baru:")
                tanggal = input("Tanggal (YYYY-MM-DD): ")
                jenis = input("Jenis (pemasukan/pengeluaran): ").lower()
                kategori = input("Kategori (makan/hiburan/transport/lainnya): ").lower()
                jumlah = input("Jumlah (Rp): ")
                keterangan = input("Keterangan: ")
                data_baru.append([id_edit, tanggal, jenis, kategori, jumlah, keterangan])
                updated = True
            else:
                data_baru.append(row)

    if updated:
        with open(NAMA_FILE, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(data_baru)
        print("✅ Transaksi berhasil diupdate.")
    else:
        print("❌ ID tidak ditemukan.")

# CRUD: DELETE
def hapus_transaksi():
    id_hapus = input("Masukkan ID transaksi yang ingin dihapus: ")
    data_baru = []

    deleted = False
    with open(NAMA_FILE, mode='r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if row[0] == id_hapus:
                deleted = True
                continue
            data_baru.append(row)

    if deleted:
        with open(NAMA_FILE, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(data_baru)
        print("🗑️ Transaksi berhasil dihapus.")
    else:
        print("❌ ID tidak ditemukan.")

# MENU UTAMA
def menu():
    inisialisasi_csv()
    while True:
        print("\n=== Aplikasi Manajemen Keuangan Pribadi ===")
        print("1. Tambah Transaksi")
        print("2. Lihat Semua Transaksi")
        print("3. Ubah Transaksi")
        print("4. Hapus Transaksi")
        print("5. Keluar")
        pilih = input("Pilih menu [1-5]: ")

        if pilih == "1":
            tambah_transaksi()
        elif pilih == "2":
            tampilkan_data()
        elif pilih == "3":
            update_transaksi()
        elif pilih == "4":
            hapus_transaksi()
        elif pilih == "5":
            print("Terima kasih telah menggunakan aplikasi!")
            break
        else:
            print("❗ Pilihan tidak valid.")

if __name__ == "__main__":
    menu()
