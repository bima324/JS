import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
from colorama import Fore, Style, init

# Inisialisasi colorama (untuk Windows)
init(autoreset=True)

# Kota default: Jakarta Timur
kota = "jakarta-timur"

# URL halaman yang berisi jadwal sholat
url = f"https://www.umroh.com/jadwal-sholat/{kota}"

# Request ke website
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Cari tabel berdasarkan class-nya
table = soup.find("table", {"class": "table table-hover table-striped"})

if not table:
    print(Fore.RED + "❌ Gagal mengambil data. Website mungkin sedang tidak tersedia.")
    exit()

# List untuk menyimpan hasil scraping
jadwal_sholat = []

# Loop melalui setiap baris dalam tabel
for row in table.find_all("tr")[1:]:  # Lewati header tabel
    cols = row.find_all("td")
    if len(cols) > 0:
        tanggal = cols[0].text.strip()
        imsyak = cols[1].text.strip()
        subuh = cols[2].text.strip()
        dzuhur = cols[3].text.strip()
        ashar = cols[4].text.strip()
        maghrib = cols[5].text.strip()
        isya = cols[6].text.strip()

        jadwal_sholat.append([tanggal, imsyak, subuh, dzuhur, ashar, maghrib, isya])

# Cek apakah data berhasil diambil
if not jadwal_sholat:
    print(Fore.RED + "❌ Tidak ada data jadwal sholat yang ditemukan.")
    exit()

# Header tabel dengan warna
headers = [
    Fore.CYAN + "Tanggal" + Style.RESET_ALL,
    Fore.YELLOW + "Imsyak" + Style.RESET_ALL,
    Fore.GREEN + "Subuh" + Style.RESET_ALL,
    Fore.BLUE + "Dzuhur" + Style.RESET_ALL,
    Fore.MAGENTA + "Ashar" + Style.RESET_ALL,
    Fore.RED + "Maghrib" + Style.RESET_ALL,
    Fore.WHITE + "Isya" + Style.RESET_ALL,
]

# Cetak hasil dalam bentuk tabel
print("\n📅 Jadwal Sholat untuk:", Fore.CYAN + kota.upper() + Style.RESET_ALL)
print(tabulate(jadwal_sholat, headers=headers, tablefmt="fancy_grid"))
