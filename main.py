"""Entry point: Sistem Klasifikasi Data dengan Himpunan (PJBL-2)."""

import io
import sys
import unittest
from pathlib import Path

from src import ui
from src.dataset import DatasetError, load_dataset
from src.inclusion_exclusion import pie_three, pie_two
from src.set_operations import (complement_set, difference_set,
                                intersection_set, union_set)
from src.venn import VennError, create_venn, open_image

ROOT = Path(__file__).resolve().parent
# id dataset -> (nama file CSV, judul)
DATASET_FILES = {
    "dataset1": ("dataset_mahasiswa.csv", "Dataset 1 - Mahasiswa Kelas A"),
    "dataset2": ("dataset_mahasiswa_2.csv", "Dataset 2 - Mahasiswa Kelas B"),
}
DATASETS = {"1": "dataset1", "2": "dataset2"}


def load_by_id(dataset_id):
    filename, title = DATASET_FILES[dataset_id]
    return load_dataset(ROOT / "data" / filename, title)


LEBAR_MAKS = 72  # batas lebar sebelum daftar nama dipecah menjadi satu per baris


def _format_daftar(nama):
    """Daftar nama apa adanya bila pendek; bila melebihi lebar, satu nama per baris."""
    satu_baris = str(nama)
    if len(satu_baris) <= LEBAR_MAKS:
        return satu_baris
    isi = "\n".join(f"    {n!r}," for n in nama)
    return f"\n[\n{isi}\n]"


def show_set(title, members, data):
    """Tampilkan jumlah anggota dan daftar NAMA (anggota himpunan = NIM)."""
    nama = sorted(data["names"][nim] for nim in members)
    print(f"\n{title}")
    print(f"Jumlah : {len(members)}")
    print(f"Data   : {_format_daftar(nama)}")


# ---------- Animasi pembukaan ----------
def intro_animation():
    ui.clear_screen()
    ui.show_banner()
    ui.loading_animation("[1/5] Memuat dataset...", 1.0)
    ui.show_check("Dataset berhasil dimuat.")
    ui.pause_session(0.8)

    ui.show_section("SESI 2 — MEMBENTUK HIMPUNAN")
    for item in ("Universal Set", "Set A", "Set B", "Set C"):
        ui.show_check(item)
    ui.pause_session(0.8)

    ui.show_section("SESI 3 — OPERASI HIMPUNAN")
    for item in ("Union", "Intersection", "Difference", "Complement"):
        ui.show_check(item)
    ui.pause_session(0.8)

    ui.show_section("SESI 4 — DIAGRAM VENN")
    ui.show_check("Membuat visualisasi...")
    ui.pause_session(0.8)

    ui.show_section("SESI 5 — INKLUSI-EKSKLUSI")
    ui.show_check("Menghitung jumlah data unik...")
    ui.pause_session(0.8)


# ---------- Fitur menu ----------
def show_data(data):
    print(f"\n{'=' * 16} DATA {'=' * 16}")
    print(data["nama"])
    print(f"\n{'NIM':<10} {'Nama':<18} {'Sem':<4} {'Organisasi':<11} UKM")
    print("-" * 56)
    for r in data["records"]:
        print(f"{r['nim']:<10} {r['nama']:<18} {r['semester']:<4} "
              f"{r['organisasi']:<11} {r['ukm']}")
    print("\nHimpunan dibentuk dari aturan keanggotaan:")
    show_set("Universal Set (U) = seluruh mahasiswa", data["U"], data)
    show_set(f"A = {data['label_A']}", data["A"], data)
    show_set(f"B = {data['label_B']}", data["B"], data)
    show_set(f"C = {data['label_C']}", data["C"], data)


def show_operations(data):
    A, B, C, U = data["A"], data["B"], data["C"], data["U"]

    while True:
        print(f"\n{'=' * 16} OPERASI HIMPUNAN {'=' * 16}")

        print(f"\nA = {data['label_A']}")
        print(f"B = {data['label_B']}")
        print(f"C = {data['label_C']}")

        print("\nPilih operasi:")
        print("1. Union (A ∪ B)")
        print("2. Intersection (A ∩ B)")
        print("3. Difference (A - B)")
        print("4. Difference (B - A)")
        print("5. Complement A (U - A)")
        print("6. Complement B (U - B)")
        print("7. Complement C (U - C)")
        # print("8. (A ∩ B) - C")
        print("8. Tampilkan Semua Operasi")
        print("0. Kembali")

        choice = input("\nPilihan: ").strip()

        if choice == "1":
            show_set(
                "A ∪ B",
                union_set(A, B),
                data
            )

        elif choice == "2":
            show_set(
                "A ∩ B",
                intersection_set(A, B),
                data
            )

        elif choice == "3":
            show_set(
                "A - B",
                difference_set(A, B),
                data
            )

        elif choice == "4":
            show_set(
                "B - A",
                difference_set(B, A),
                data
            )

        elif choice == "5":
            show_set(
                "U - A (komplemen A)",
                complement_set(U, A),
                data
            )

        elif choice == "6":
            show_set(
                "U - B (komplemen B)",
                complement_set(U, B),
                data
            )

        elif choice == "7":
            show_set(
                "U - C (komplemen C)",
                complement_set(U, C),
                data
            )

        # elif choice == "8":
        #     show_set(
        #         "(A ∩ B) - C",
        #         difference_set(
        #             intersection_set(A, B),
        #             C
        #         ),
        #         data
        #     )

        elif choice == "8":
            show_set("A ∪ B", union_set(A, B), data)
            show_set("A ∩ B", intersection_set(A, B), data)
            show_set("A - B", difference_set(A, B), data)
            show_set("B - A", difference_set(B, A), data)
            show_set(
                "U - A (komplemen A)",
                complement_set(U, A),
                data
            )
            show_set(
                "U - B (komplemen B)",
                complement_set(U, B),
                data
            )
            show_set(
                "U - C (komplemen C)",
                complement_set(U, C),
                data
            )
            # show_set(
            #     "(A ∩ B) - C",
            #     difference_set(
            #         intersection_set(A, B),
            #         C
            #     ),
            #     data
            # )

        elif choice == "0":
            return

        else:
            ui.show_error("Pilihan operasi tidak valid.")

        input("\nTekan Enter untuk melanjutkan...")


def show_venn(data, dataset_id):
    ui.show_check("Dataset berhasil diproses")
    try:
        path = create_venn(data, dataset_id)
    except VennError as error:
        ui.show_error(str(error))
        return
    ui.show_check("Diagram Venn berhasil dibuat")
    print(f"✓ File:\n  {path.relative_to(ROOT).as_posix()}")
    if not open_image(path):
        print("  (Gambar tidak bisa dibuka otomatis, silakan buka manual.)")


def show_pie(data):
    A, B, C = data["A"], data["B"], data["C"]
    print(f"\n{'=' * 16} Prinsip Inklusi-Eksklusi (PIE) {'=' * 16}")

    print("\n--- Dua Himpunan (A dan B) ---\n")
    two = pie_two(A, B)
    print("\n".join(two["lines"]))
    print(f"\nJumlah data unik = {two['result']}")
    cocok = "SESUAI ✓" if two["result"] == len(A | B) else "TIDAK SESUAI ✗"
    print(f"Cek langsung len(A ∪ B) = {len(A | B)} -> {cocok}")

    print("\n--- Tiga Himpunan (A, B, dan C) ---\n")
    three = pie_three(A, B, C)
    print("\n".join(three["lines"]))
    print(f"\nJumlah data unik = {three['result']}")
    cocok = "SESUAI ✓" if three["result"] == len(A | B | C) else "TIDAK SESUAI ✗"
    print(f"Cek langsung len(A ∪ B ∪ C) = {len(A | B | C)} -> {cocok}")


class _ResultPrinter(unittest.TextTestResult):
    """Cetak '✓ Test ... PASSED' untuk tiap test."""

    def addSuccess(self, test):
        super().addSuccess(test)
        print(f"✓ {test.shortDescription() or test.id()} PASSED")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        print(f"✗ {test.shortDescription() or test.id()} FAILED")

    def addError(self, test, err):
        super().addError(test, err)
        print(f"✗ {test.shortDescription() or test.id()} ERROR")


def run_tests():
    print(f"\n{'=' * 16} HASIL TESTING {'=' * 16}\n")
    suite = unittest.defaultTestLoader.discover(
        str(ROOT / "tests"), top_level_dir=str(ROOT))
    runner = unittest.TextTestRunner(stream=io.StringIO(), resultclass=_ResultPrinter)
    result = runner.run(suite)
    if result.wasSuccessful():
        print("\nSemua testing berhasil.")
    else:
        print("\nAda testing yang gagal. Jalankan: python -m unittest discover -s tests")


# ---------- Menu utama ----------
def show_menu(current_name):
    print(f"\n{'=' * 50}\nMENU UTAMA\n{'=' * 50}")
    print(f"Dataset aktif: {current_name}\n")
    print("1. Pilih Dataset")
    print("2. Tampilkan Data")
    print("3. Operasi Himpunan")
    print("4. Diagram Venn")
    print("5. Prinsip Inklusi-Eksklusi")
    print("6. Tampilkan Semua Hasil")
    print("7. Jalankan Testing")
    print("8. Keluar")


def choose_dataset(current_id):
    print("\n1. Dataset 1 (Mahasiswa Kelas A)\n2. Dataset 2 (Mahasiswa Kelas B)")
    choice = input("Pilih dataset (1/2): ").strip()
    if choice not in DATASETS:
        ui.show_error("Pilihan dataset tidak valid.")
        return current_id
    return DATASETS[choice]


def main():
    # Pastikan simbol ∪ ∩ █ ✓ tampil benar di terminal Windows
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    intro_animation()
    dataset_id = "dataset1"

    while True:
        try:
            data = load_by_id(dataset_id)
        except DatasetError as error:
            ui.show_error(str(error))
            return

        show_menu(data["nama"])
        try:
            choice = input("\nPilihan: ").strip()

            if choice == "1":
                dataset_id = choose_dataset(dataset_id)
                data = load_by_id(dataset_id)
                ui.show_check(f"Dataset aktif: {data['nama']}")
            elif choice == "2":
                show_data(data)
            elif choice == "3":
                show_operations(data)
            elif choice == "4":
                show_venn(data, dataset_id)
            elif choice == "5":
                show_pie(data)
            elif choice == "6":
                show_data(data)
                show_operations(data)
                show_venn(data, dataset_id)
                show_pie(data)
            elif choice == "7":
                run_tests()
            elif choice == "8":
                print("\nTerima kasih! Sampai jumpa.")
                return
            else:
                ui.show_error("Pilihan tidak valid.")
                print("  Silakan pilih menu yang tersedia.")

            ui.wait_enter()
        except DatasetError as error:
            ui.show_error(str(error))
        except (EOFError, KeyboardInterrupt):
            print("\nSampai jumpa!")
            return


if __name__ == "__main__":
    main()
