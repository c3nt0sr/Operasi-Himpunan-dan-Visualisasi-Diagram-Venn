"""Membuat Diagram Venn dari dataset (angka dihitung otomatis oleh matplotlib-venn)."""

import os
import subprocess
import sys
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output" / "venn"


class VennError(Exception):
    """Error saat membuat diagram (misalnya library belum terinstall)."""


def build_venn_figure(data):
    """Bangun objek Figure Diagram Venn 3 himpunan dari dataset.

    Dipakai bersama oleh CLI (disimpan sebagai PNG) dan versi web (ditampilkan
    langsung lewat st.pyplot). Angka tiap daerah dihitung dari himpunan A, B, C,
    bukan ditulis tetap.
    """
    try:
        import matplotlib
        matplotlib.use("Agg")  # render tanpa jendela GUI
        import matplotlib.pyplot as plt
        from matplotlib_venn import venn3
    except ImportError:
        raise VennError(
            "Library matplotlib / matplotlib-venn belum terinstall.\n"
            "  Jalankan: pip install -r requirements.txt"
        )

    labels = (data["label_A"], data["label_B"], data["label_C"])
    fig, ax = plt.subplots(figsize=(8, 6))
    # Angka di diagram dihitung dari set A, B, C -> tidak ada angka hardcode
    venn3([data["A"], data["B"], data["C"]], set_labels=labels, ax=ax)
    ax.set_title(f"{data['nama']}\n(Universal Set: {len(data['U'])} orang)")
    return fig


def create_venn(data, dataset_id):
    """Buat diagram Venn lalu simpan ke output/venn/<dataset_id>_venn.png.
    Mengembalikan path file hasil (dipakai oleh antarmuka CLI).
    """
    import matplotlib.pyplot as plt

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    file_path = OUTPUT_DIR / f"{dataset_id}_venn.png"
    fig = build_venn_figure(data)
    fig.savefig(file_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return file_path


def open_image(file_path):
    """Coba buka gambar secara otomatis. Return True jika berhasil."""
    try:
        if sys.platform.startswith("win"):
            os.startfile(file_path)
        elif sys.platform == "darwin":
            subprocess.run(["open", str(file_path)], check=True)
        else:
            subprocess.run(["xdg-open", str(file_path)], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except (OSError, subprocess.SubprocessError):
        return False
