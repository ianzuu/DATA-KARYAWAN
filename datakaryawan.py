import streamlit as st
import sqlite3
import pandas as pd

# --- Koneksi ke database ---
conn = sqlite3.connect('data_karyawan.db', check_same_thread=False)
cursor = conn.cursor()

# Buat tabel kalau belum ada
cursor.execute('''
CREATE TABLE IF NOT EXISTS stok (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_karyawan TEXT,
    tempattanggallahir_karyawan TEXT,
    umur_karyawan INTEGER,
    alamat_karyawan TEXT
)
''')
conn.commit()

st.title("Data Karyawan - by ian")

# --- Form input ---
st.subheader("Input Data Karyawan")
with st.form("form_input"):
    nama_karyawan = st.text_input("Nama Karyawan")
    tempattanggallahir_karyawan = st.text_input("Tempat Tanggal Lahir")
    umur_karyawan = st.number_input("Umur", 0)
    alamat_karyawan = st.text_input("Alamat Karyawan")

    submitted = st.form_submit_button("Simpan Data")
    if submitted:
        cursor.execute('''
            INSERT INTO stok (
                nama_karyawan, tempattanggallahir_karyawan, umur_karyawan, alamat_karyawan
            ) VALUES (?, ?, ?, ?)
        ''', (nama_karyawan, tempattanggallahir_karyawan, umur_karyawan, alamat_karyawan))
        conn.commit()
        st.success("✅ Data berhasil disimpan!")

# --- Menampilkan data ---
# --- Menampilkan data ---
st.subheader("Data Karyawan")
df = pd.read_sql_query("SELECT * FROM stok", conn)

# Ubah header jadi lebih rapi
df.rename(columns={
    'nama_karyawan': 'Nama Karyawan',
    'tempattanggallahir_karyawan': 'Tempat & Tanggal Lahir',
    'umur_karyawan': 'Umur',
    'alamat_karyawan': 'Alamat'
}, inplace=True)

st.dataframe(df)


# --- Export Excel ---
def export_excel():
    df.to_excel("hasil_karyawan.xlsx", index=False)
    with open("hasil_karyawan.xlsx", "rb") as f:
        st.download_button("📥 Download Excel", f, file_name="hasil_karyawan.xlsx")

export_excel()

