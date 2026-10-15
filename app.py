# -*- coding: utf-8 -*-
"""Versi web (Streamlit) — Sistem Klasifikasi Data dengan Himpunan.

Menjalankan:  streamlit run app.py
             lalu buka tautan Local URL yang muncul di terminal.

Logika himpunan tetap berada di src/ (dataset.py, set_operations.py,
inclusion_exclusion.py, venn.py) tanpa perubahan; berkas ini hanya
mengganti antarmuka main.py (CLI) menjadi antarmuka web. Untuk deploy,
cukup push repositori ke GitHub dan hubungkan ke Streamlit Community Cloud
(share.streamlit.io) dengan main file app.py.
"""

from pathlib import Path
import streamlit as st
import matplotlib.pyplot as plt

from src.dataset import DatasetError, load_dataset
from src.inclusion_exclusion import pie_three, pie_two
from src.set_operations import (complement_set, difference_set,
                                intersection_set, union_set)
from src.venn import VennError, build_venn_figure

ROOT = Path(__file__).resolve().parent
DATASET_FILES = {
    "dataset1": ("dataset_mahasiswa.csv", "Dataset 1 - Mahasiswa Kelas A"),
    "dataset2": ("dataset_mahasiswa_2.csv", "Dataset 2 - Mahasiswa Kelas B"),
}
DATASETS = {"1": "dataset1", "2": "dataset2"}
REPO_URL = "https://github.com/c3nt0sr/Operasi-Himpunan-dan-Visualisasi-Diagram-Venn"

st.set_page_config(
    page_title="Sistem Klasifikasi Data dengan Himpunan — PJBL-2",
    page_icon="◍",
    layout="wide",
)


@st.cache_data
def load_by_id(dataset_id: str):
    filename, title = DATASET_FILES[dataset_id]
    return load_dataset(ROOT / "data" / filename, title)


def nama_list(data, members):
    return sorted(data["names"][nim] for nim in members)


def format_anggota(nama_list_sorted):
    if not nama_list_sorted:
        return "— (kosong)"
    return ", ".join(nama_list_sorted)


# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("### Pengaturan")
    pilihan = st.selectbox(
        "Pilih Dataset",
        options=["dataset1", "dataset2"],
        format_func=lambda x: DATASET_FILES[x][1],
        index=0,
        help="Dataset 1 dan 2 masing-masing 15 mahasiswa dengan komposisi A/B/C berbeda.",
    )
    st.divider()
    st.markdown("**Kelompok 5 — PJBL-2 Matematika Diskrit**")
    st.caption(
        "Reva Sahira · Fachrul Razi Al Bahri · Ulfi Ufrijal · "
        "Adrian Maulana · Najwa Salmi"
    )
    st.link_button("Buka Repositori GitHub", REPO_URL)
    st.caption("Alternatif CLI tetap tersedia: `python main.py`")

# ---------- Load dataset ----------
try:
    data = load_by_id(pilihan)
except (DatasetError, VennError) as e:
    st.error(str(e))
    st.stop()

A, B, C, U = data["A"], data["B"], data["C"], data["U"]

# ---------- Header ----------
st.title("Sistem Klasifikasi Data dengan Himpunan")
st.caption(
    "PJBL-2 Matematika Diskrit — Memodelkan data mahasiswa sebagai himpunan, "
    "menghitung gabungan / irisan / selisih / komplemen, menggambar Diagram Venn, "
    "dan membuktikan Prinsip Inklusi-Eksklusi."
)
st.divider()

# ---------- Ringkasan himpunan (metrics) ----------
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("U (semesta)", len(U))
c2.metric("A — Semester 3", len(A))
c3.metric("B — Organisasi", len(B))
c4.metric("C — UKM", len(C))
c5.metric("A ∪ B ∪ C", len(A | B | C))
with st.expander("Aturan keanggotaan himpunan", expanded=False):
    st.markdown(
        "- **U** — seluruh mahasiswa pada dataset aktif (kunci unik: NIM; Nama hanya label).\n"
        "- **A** — mahasiswa Semester 3.\n"
        "- **B** — anggota organisasi (kolom `Organisasi` bukan `-`, yaitu BEM atau HMJ).\n"
        "- **C** — anggota UKM (kolom `UKM` bukan `-`)."
    )

# ---------- Tabs ----------
tab_data, tab_operasi, tab_venn, tab_pie, tab_uji = st.tabs(
    ["Data", "Operasi Himpunan", "Diagram Venn", "Inklusi-Eksklusi", "Pengujian"]
)

# ---- Tab: Data ----
with tab_data:
    st.subheader(f"{data['nama']} — {len(data['records'])} mahasiswa")
    # Tabel data
    import pandas as pd

    df = pd.DataFrame(
        [
            {
                "NIM": r["nim"],
                "Nama": r["nama"],
                "Semester": r["semester"],
                "Organisasi": r["organisasi"],
                "UKM": r["ukm"],
            }
            for r in data["records"]
        ]
    )
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.markdown("**Anggota tiap himpunan**")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown(f"**A — Semester 3** ({len(A)} orang)")
        st.write(format_anggota(nama_list(data, A)))
    with col_b:
        st.markdown(f"**B — Organisasi** ({len(B)} orang)")
        st.write(format_anggota(nama_list(data, B)))
    with col_c:
        st.markdown(f"**C — UKM** ({len(C)} orang)")
        st.write(format_anggota(nama_list(data, C)))
    st.markdown(f"**U — Semesta** ({len(U)} orang)")
    st.write(format_anggota(nama_list(data, U)))

# ---- Tab: Operasi ----
with tab_operasi:
    st.subheader("Operasi Himpunan")
    st.caption("Gabungan, irisan, selisih, dan komplemen dihitung dengan tipe `set` Python; daftar nama diurutkan alfabetis.")
    operasi = [
        ("A ∪ B — Gabungan", len(A | B), union_set(A, B), "Mahasiswa Semester 3 atau anggota organisasi."),
        ("A ∩ B — Irisan", len(A & B), intersection_set(A, B), "Semester 3 sekaligus anggota organisasi."),
        ("A − B — Selisih", len(A - B), difference_set(A, B), "Anggota A yang tidak ada di B."),
        ("B − A — Selisih", len(B - A), difference_set(B, A), "Anggota B yang tidak ada di A."),
        ("U − A — Komplemen A", len(U - A), complement_set(U, A), "Mahasiswa yang bukan Semester 3."),
        ("U − B — Komplemen B", len(U - B), complement_set(U, B), "Mahasiswa yang bukan anggota organisasi."),
        ("U − C — Komplemen C", len(U - C), complement_set(U, C), "Mahasiswa yang bukan anggota UKM."),
        ("A ∩ B ∩ C", len(A & B & C), A & B & C, "Ketiga kategori sekaligus."),
    ]
    # Opsi ringkas vs rinci
    mode = st.radio("Tampilan", ["Ringkas (tabel)", "Rinci (per operasi)"], horizontal=True, label_visibility="collapsed")
    if mode.startswith("Ringkas"):
        import pandas as pd

        tdf = pd.DataFrame(
            [
                {"Operasi": nama, "Jumlah": jml, "Anggota": format_anggota(nama_list(data, himp))}
                for nama, jml, himp, _ in operasi
            ]
        )
        st.dataframe(tdf, use_container_width=True, hide_index=True)
    else:
        for nama, jml, himp, ket in operasi:
            with st.expander(f"{nama} — {jml} orang", expanded=False):
                st.caption(ket)
                st.write(f"**Jumlah:** {jml}")
                st.write(format_anggota(nama_list(data, himp)))

# ---- Tab: Venn ----
with tab_venn:
    st.subheader("Diagram Venn")
    st.caption("Angka tiap daerah dihitung otomatis dari himpunan A, B, C (bukan hardcode) melalui `matplotlib-venn`.")
    try:
        fig = build_venn_figure(data)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
        # Tombol unduh
        import io

        buf = io.BytesIO()
        fig2 = build_venn_figure(data)
        fig2.savefig(buf, format="png", dpi=150, bbox_inches="tight")
        plt.close(fig2)
        st.download_button(
            "Unduh Diagram Venn (PNG)",
            data=buf.getvalue(),
            file_name=f"{pilihan}_venn.png",
            mime="image/png",
        )
    except VennError as e:
        st.error(str(e))
        st.info("Pastikan `matplotlib` dan `matplotlib-venn` terpasang (`pip install -r requirements.txt`).")

# ---- Tab: PIE ----
with tab_pie:
    st.subheader("Prinsip Inklusi-Eksklusi (PIE)")
    st.caption("PIE menghitung jumlah data unik tanpa menghitung ganda; hasilnya dibandingkan dengan pencacahan langsung `len(gabungan)`.")
    dua = pie_two(A, B)
    tiga = pie_three(A, B, C)
    col2, col3 = st.columns(2)
    with col2:
        st.markdown("**Dua himpunan** — |A ∪ B| = |A| + |B| − |A ∩ B|")
        st.code("\n".join(dua["lines"]), language="text")
        st.write(f"**Hasil:** {dua['result']} orang")
        cek2 = len(A | B)
        if dua["result"] == cek2:
            st.success(f"SESUAI — len(A ∪ B) = {cek2}")
        else:
            st.error(f"TIDAK SESUAI — len(A ∪ B) = {cek2}")
    with col3:
        st.markdown("**Tiga himpunan** — |A ∪ B ∪ C| = |A|+|B|+|C| − |A∩B|−|A∩C|−|B∩C| + |A∩B∩C|")
        st.code("\n".join(tiga["lines"]), language="text")
        st.write(f"**Hasil:** {tiga['result']} orang")
        cek3 = len(A | B | C)
        if tiga["result"] == cek3:
            st.success(f"SESUAI — len(A ∪ B ∪ C) = {cek3}")
        else:
            st.error(f"TIDAK SESUAI — len(A ∪ B ∪ C) = {cek3}")

# ---- Tab: Pengujian ----
with tab_uji:
    st.subheader("Pengujian")
    st.caption("27 kasus uji (`unittest`) — dijalankan tanpa keluar dari web. CLI: `python -m unittest discover -s tests`.")
    if st.button("Jalankan Pengujian", type="primary"):
        import io
        import unittest

        buf = io.StringIO()
        # Jalankan discovery
        loader = unittest.defaultTestLoader
        suite = loader.discover(str(ROOT / "tests"), top_level_dir=str(ROOT))

        class _StreamResult(unittest.TextTestResult):
            def addSuccess(self, test):
                super().addSuccess(test)
                buf.write(f"✓ {test.shortDescription() or test.id()} — PASSED\n")

            def addFailure(self, test, err):
                super().addFailure(test, err)
                buf.write(f"✗ {test.shortDescription() or test.id()} — FAILED\n")

            def addError(self, test, err):
                super().addError(test, err)
                buf.write(f"✗ {test.shortDescription() or test.id()} — ERROR\n")

        runner = unittest.TextTestRunner(stream=io.StringIO(), resultclass=_StreamResult, verbosity=0)
        result = runner.run(suite)
        st.code(buf.getvalue(), language="text")
        if result.wasSuccessful():
            st.success(f"Semua {result.testsRun} pengujian lulus.")
        else:
            st.error(f"{len(result.failures)} gagal, {len(result.errors)} error dari {result.testsRun} uji.")
    else:
        st.info("Tekan tombol di atas untuk menjalankan 27 pengujian dan melihat hasilnya di sini.")

st.divider()
st.caption(
    "Kode sumber, dataset, dan laporan ada di repositori GitHub (tautan di sidebar). "
    "Versi CLI tetap tersedia: `python main.py`."
)
