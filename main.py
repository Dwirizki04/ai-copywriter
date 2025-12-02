import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# --- 1. KONFIGURASI ---
# Memuat API Key dari file .env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="AI Copywriter Pro",
    page_icon="🛍️",
    layout="centered"
)

# Konfigurasi Google Gemini AI
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("API Key belum ditemukan. Pastikan file .env sudah dibuat.")

# --- 2. FUNGSI LOGIKA (BACKEND) ---
def generate_description(nama_produk, fitur, tone_bahasa):
    """
    Fungsi ini mengirim data ke AI dan menerima teks balasan.
    """
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        # Prompt Engineering: Ini adalah 'resep rahasia' agar hasilnya bagus
        prompt = f"""
        Bertindaklah sebagai ahli copywriting e-commerce profesional.
        Buatkan deskripsi produk yang menarik, persuasif, dan SEO friendly untuk marketplace (Shopee/Tokopedia).
        
        Detail Produk:
        - Nama Produk: {nama_produk}
        - Fitur/Spesifikasi Utama: {fitur}
        - Gaya Bahasa: {tone_bahasa}
        
        Output harus mengandung:
        1. Judul Produk yang 'Catchy'
        2. Paragraf pembuka yang menyentuh masalah pembeli
        3. Poin-poin keunggulan (Bullet points)
        4. Spesifikasi teknis
        5. Call to Action (Ajakan membeli)
        
        Gunakan Bahasa Indonesia yang natural.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Terjadi kesalahan: {e}"

# --- 3. TAMPILAN WEBSITE (FRONTEND) ---

# Header
st.title("🛍️ Generator Deskripsi Produk")
st.markdown("Buat deskripsi produk **laris manis** dalam hitungan detik dengan AI.")
st.divider()

# Kolom Input (Kiri dan Kanan)
col1, col2 = st.columns(2)

with col1:
    nama_produk = st.text_input("Nama Produk", placeholder="Contoh: Sepatu Lari Pria Titan X")
    tone = st.selectbox("Gaya Bahasa", ["Profesional & Mewah", "Santai & Gaul", "Persuasif & Mendesak"])

with col2:
    target_pasar = st.text_input("Target Pembeli", placeholder="Contoh: Pria usia 20-30 tahun")

# Input Area Besar
fitur_produk = st.text_area("Fitur/Keunggulan Produk (Penting)", 
                            placeholder="Contoh: Bahan mesh bernapas, sol karet anti-slip, ringan, cocok untuk marathon.",
                            height=150)

# Tombol Eksekusi
buat_deskripsi = st.button("✨ Buat Deskripsi Sekarang", type="primary")

# --- 4. MENAMPILKAN HASIL ---
if buat_deskripsi:
    if not api_key:
        st.error("API Key error. Cek konfigurasi.")
    elif not nama_produk or not fitur_produk:
        st.warning("Mohon isi Nama Produk dan Fitur terlebih dahulu.")
    else:
        with st.spinner("Sedang meracik kata-kata ajaib..."):
            # Memanggil fungsi logika di atas
            hasil_teks = generate_description(nama_produk, fitur_produk, tone)
            
            st.success("Selesai! Berikut deskripsinya:")
            st.markdown("---")
            st.markdown(hasil_teks)
            
            # Tambahan tombol copy (opsional logic)
            st.caption("Tips: Copy teks di atas dan paste ke Shopee/Tokopedia Anda.")