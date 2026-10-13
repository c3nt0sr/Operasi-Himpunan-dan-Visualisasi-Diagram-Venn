# Operasi Himpunan dan Visualisasi Diagram Venn

Operasi Himpunan dan Visualisasi Diagram Venn, PJBL-2 Matematika Diskrit, Kelompok 5 ex-1mphn3n

PJBL-2 Matematika Diskrit, Kelompok 5 ex-1mphn3n

## Kelompok

| No | Nama | NIM | Peran |
|---|---|---|---|
| 1 | Reva Sahira | 25210112 | Dokumentasi, laporan akhir, dan pengumpulan (PDF, SPADA) |
| 2 | Fachrul Razi Al Bahri | 25210205 | Pemrogram utama dan pengelola repositori (main.py) |
| 3 | Ulfi Ufrijal | 25210155 | Pemrogram operasi himpunan (set_operations.py) dan pengujian |
| 4 | Adrian Maulana | 25210220 | Perancang model himpunan dan kurator dataset |
| 5 | Najwa Salmi | 25210131 | Video demonstrasi dan presentasi |

## Tujuan

Menerapkan konsep himpunan pada data nyata: membentuk himpunan dari aturan keanggotaan, menghitung gabungan, irisan, selisih, dan komplemen, memvisualisasikannya dengan Diagram Venn, serta membuktikan Prinsip Inklusi-Eksklusi (PIE) sama dengan hasil union yang dihitung langsung.

## Model Himpunan

Himpunan semesta **U** = seluruh mahasiswa dalam dataset (15 sampel). Anggota himpunan memakai **NIM** (kunci unik); **Nama** hanya dipakai sebagai label saat hasil ditampilkan.

| Himpunan | Aturan keanggotaan |
|---|---|
| **A** | mahasiswa Semester 3 |
| **B** | anggota organisasi (kolom `Organisasi` bukan `-`) |
| **C** | anggota UKM (kolom `UKM` bukan `-`) |

Ketiga himpunan saling beririsan sehingga operasi himpunan menghasilkan keluaran yang bermakna.

## Fitur

- Union, Intersection, Difference, Complement (A<sup>c</sup> = U - A)
- Menu "Tampilkan Semua Operasi" untuk menampilkan ketujuh operasi sekaligus
- Daftar nama panjang dirapikan satu nama per baris agar tidak terpotong di terminal
- Diagram Venn otomatis (disimpan sebagai gambar)
- Prinsip Inklusi-Eksklusi (2 dan 3 himpunan, lengkap dengan langkah hitung)
- Dua dataset CSV
- Animasi CLI
- Pengujian otomatis (27 kasus uji dengan unittest)

## Teknologi

- Python 3 (CLI dengan `input()` dan `print()`)
- Tipe `set` Python (operator `|`, `&`, `-`)
- Modul `csv` bawaan Python
- Matplotlib dan Matplotlib-Venn (Diagram Venn)
- unittest
- Git dan GitHub

## Struktur Project

```
pjbl-2-himpunan/
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   ├── dataset_mahasiswa.csv       (Dataset 1)
│   └── dataset_mahasiswa_2.csv     (Dataset 2)
├── src/
│   ├── __init__.py
│   ├── dataset.py
│   ├── set_operations.py
│   ├── inclusion_exclusion.py
│   ├── venn.py
│   └── ui.py
├── tests/
│   ├── __init__.py
│   └── test_set_operations.py
└── output/
    └── venn/
        └── .gitkeep
```

## Dataset

Format CSV dengan lima kolom: `NIM` (kunci unik), `Nama`, `Semester`, `Organisasi`, `UKM`. Kolom `Organisasi` dan `UKM` bernilai `-` bila mahasiswa tidak mengikuti.

```
NIM,Nama,Semester,Organisasi,UKM
21101001,Ahmad Fadli,3,BEM,-
21101002,Siti Nurhaliza,5,-,UKM Futsal
21101003,Budi Santoso,3,HMJ TI,UKM Basket
```

| | Dataset 1 | Dataset 2 |
|---|---|---|
| File | dataset_mahasiswa.csv | dataset_mahasiswa_2.csv |
| U | 15 | 15 |
| A (Semester 3) | 7 | 6 |
| B (Organisasi) | 7 | 7 |
| C (UKM) | 7 | 7 |
| A ∩ B | 4 | 4 |
| A ∩ B ∩ C | 2 | 2 |
| A ∪ B ∪ C | 13 | 12 |

Kedua dataset berisi mahasiswa berbeda dan menghasilkan hasil operasi yang berbeda.

## Operasi Himpunan

- **Union (A ∪ B)**: mahasiswa yang ada di A atau B.
- **Intersection (A ∩ B)**: mahasiswa yang ada di A dan B sekaligus.
- **Difference (A - B)**: anggota A yang tidak ada di B.
- **Complement (U - A)**: mahasiswa yang bukan anggota A.

## Diagram Venn

`src/venn.py` memakai `matplotlib-venn` (`venn3`). Himpunan A, B, C langsung diambil dari dataset aktif, sehingga semua angka dihitung otomatis (tidak ada angka hardcode).

## Prinsip Inklusi-Eksklusi

- Dua himpunan: `|A ∪ B| = |A| + |B| - |A ∩ B|`
- Tiga himpunan: `|A ∪ B ∪ C| = |A| + |B| + |C| - |A ∩ B| - |A ∩ C| - |B ∩ C| + |A ∩ B ∩ C|`

Program menampilkan setiap langkah hitung dan membandingkannya dengan `len()` dari union Python set.

## Instalasi

```
git clone <URL_REPOSITORY>
cd <NAMA_PROJECT>
python -m venv .venv
```

Windows:

```
.venv\Scripts\activate
```

Kemudian:

```
pip install -r requirements.txt
```

## Menjalankan Program

```
python main.py
```

## Menjalankan Testing

```
python -m unittest discover -s tests
```

## Output

Diagram Venn tersimpan di `output/venn/` (mis. `dataset1_venn.png`). File PNG tidak di-commit ke Git.

## Pengujian

Total 27 kasus uji (`unittest`) yang seluruhnya lulus, terbagi dalam empat kelompok:

- **Operasi dasar**: union, intersection, difference, dan complement pada himpunan contoh.
- **Sifat aljabar himpunan**: komutatif, idempoten, identitas, komplemen ganda dan lengkap, hukum De Morgan, distributif, serta hubungan `|A| = |A ∩ B| + |A - B|`.
- **Dataset nyata**: jumlah A/B/C/U tiap dataset, kecocokan PIE dengan `len()` union, komplemen dataset, irisan tiga himpunan, dan perbedaan kedua dataset.
- **Penanganan galat**: file tidak ditemukan, kolom hilang, data kosong, NIM duplikat, dan Semester bukan angka.

## Kendala Teknis

- `matplotlib-venn` belum terinstall -> program menampilkan pesan, tidak crash.
- Validasi CSV: kolom hilang, data kosong, NIM duplikat, atau Semester bukan angka ditolak dengan pesan yang jelas.
- Union vs PIE: PIE menghitung jumlah (bukan daftar anggota), sehingga hasilnya harus sama dengan `len(A | B | C)`.
- Gambar Venn tidak selalu bisa dibuka otomatis (tergantung OS); jika gagal, buka manual dari `output/venn/`.

## Status Penyelesaian (Pertemuan 7)

- [x] Daftar nama dirapikan satu per baris agar tidak terpotong di terminal
- [x] Menu "Tampilkan Semua Operasi" (tombol 8) diperbaiki
- [x] Dataset diperiksa ulang dan kasus uji ditambah (27 uji)
- [x] Laporan akhir disusun
- [x] Perekaman video demonstrasi
