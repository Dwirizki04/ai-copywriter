import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# --- 1. KONFIGURASI ---
st.set_page_config(
    page_title="AI Copywriter Pro",
    page_icon="🛍️",
    layout="centered"
)

# LOGIKA KUNCI RAHASIA (API KEY)
# Ini mencoba mengambil kunci baik dari komputer lokal (.env) maupun dari Cloud (Secrets)
try:
    # Coba ambil dari Streamlit Cloud Secrets
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    # Jika gagal, coba ambil dari file .env (Localhost)
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

# Konfigurasi Google Gemini
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ API Key hilang! Masukkan di .env atau Streamlit Secrets.")

# --- 2. FUNGSI LOGIKA (BACKEND) ---
def generate_description(nama_produk, fitur, tone_bahasa):
    try:
        # UPDATE PENTING: Menggunakan model yang valid dari daftar Anda
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""
        Bertindaklah sebagai ahli copywriting e-commerce profesional.
        Buatkan deskripsi produk yang menarik, persuasif, dan SEO friendly untuk marketplace (Shopee/Tokopedia) dalam Bahasa Indonesia.
        
        Detail Produk:
        - Nama Produk: {nama_produk}
        - Fitur/Spesifikasi Utama: {fitur}
        - Gaya Bahasa: {tone_bahasa}
        
        Output harus mengandung:
        1. Judul Produk yang 'Catchy' & mengandung kata kunci
        2. Paragraf pembuka yang emosional/menyentuh masalah
        3. Poin-poin keunggulan (Bullet points)
        4. Spesifikasi teknis singkat
        5. Call to Action (Ajakan membeli)
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Terjadi kesalahan koneksi: {e}"

# --- 3. TAMPILAN WEBSITE (FRONTEND) ---
st.title("🛍️ Generator Deskripsi Produk")
st.markdown("Buat deskripsi produk **laris manis** dengan AI Super Cepat (Gemini 2.5).")
st.divider()

col1, col2 = st.columns(2)

with col1:
    nama_produk = st.text_input("Nama Produk", placeholder="Contoh: Kripik Pisang Lumer")
    tone = st.selectbox("Gaya Bahasa", ["Profesional & Mewah", "Santai & Akrab", "Persuasif & Mendesak", "Lucu & Unik"])

with col2:
    target_pasar = st.text_input("Target Pembeli", placeholder="Contoh: Mahasiswa, Ibu Rumah Tangga")

fitur_produk = st.text_area("Fitur/Keunggulan Produk", 
                            placeholder="Contoh: Rasa coklat belgia, tanpa pengawet, kemasan ziplock, tahan 3 bulan.",
                            height=150)

if st.button("✨ Buat Deskripsi Sekarang", type="primary"):
    if not api_key:
        st.error("API Key belum disetting.")
    elif not nama_produk or not fitur_produk:
        st.warning("Mohon isi Nama Produk dan Fitur terlebih dahulu.")
    else:
        with st.spinner("Sedang meracik kata-kata sales terbaik..."):
            hasil = generate_description(nama_produk, fitur_produk, tone)
            
            st.success("Selesai! Silakan copy di bawah ini:")
            st.markdown("---")
            st.markdown(hasil)
            st.info("Tips: Anda bisa mengedit sedikit hasilnya agar lebih pas dengan toko Anda.")
