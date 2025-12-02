import streamlit as st
import google.generativeai as genai
import os

st.title("🔍 Cek Diagnosa Model & Versi")

# 1. Cek Versi Library yang terinstall di Server
try:
    st.info(f"Versi Library Google AI saat ini: {genai.__version__}")
except:
    st.warning("Versi library tidak terdeteksi.")

# 2. Cek Daftar Model yang Tersedia
try:
    # Ambil API Key dari Secrets
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        
        st.write("Sedang menghubungi server Google...")
        
        available_models = []
        # Meminta daftar model ke Google
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        
        if available_models:
            st.success("✅ BERHASIL! Google mengizinkan Anda memakai model berikut:")
            st.code(available_models)
            st.markdown("**Solusi:** Silakan copy salah satu nama di atas (misal `models/gemini-pro`) untuk mengganti kode di `main.py` nanti.")
        else:
            st.error("Koneksi nyambung, tapi tidak ada model yang tersedia. Cek API Key Anda.")
            
    else:
        st.error("API Key belum disetting di Secrets.")

except Exception as e:
    st.error(f"Terjadi Error Kritis: {e}")
    st.markdown("Jika errornya 'API key not valid', berarti salah copas di Secrets.")
