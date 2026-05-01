import streamlit as st
from fpdf import FPDF

# 1. Sayfa Ayarları
st.set_page_config(page_title="Canlı Özgeçmişim", layout="wide")

# 2. Sol Panel: Bilgi Giriş Alanları
with st.sidebar:
    st.header("📝 Bilgilerini Düzenle")
    ad = st.text_input("Ad Soyad", "John Doe")
    unvan = st.text_input("Ünvan", "Full Stack Developer")
    email = st.text_input("E-posta", "merhaba@site.com")
    linkedin = st.text_input("LinkedIn", "johndoe")
    st.divider()
    ozet = st.text_area("Hakkımda", "Teknoloji tutkunu bir geliştiriciyim...")
    yetenekler = st.text_input("Yetenekler", "Python, Streamlit, SQL")
    st.divider()
    deneyim = st.text_area("Deneyimler", "A Şirketi - Geliştirici (2020-2024)")

# 3. Sağ Panel: Web Sitesi Görünümü
st.title("🌐 Özgeçmiş Web Sitem")
st.markdown(f"""
    <div style="background-color: white; padding: 30px; border-radius: 15px; color: #333; border: 1px solid #eee;">
        <h1 style="color: #007bff;">{ad}</h1>
        <h3>{unvan}</h3>
        <p>📧 {email} | 🔗 {linkedin}</p>
        <hr>
        <h4>🚀 Özet</h4><p>{ozet}</p>
        <h4>🛠 Yetenekler</h4><p>{yetenekler}</p>
        <h4>💼 İş Deneyimi</h4><p style="white-space: pre-line;">{deneyim}</p>
    </div>
""", unsafe_allow_html=True)

# 4. PDF OLUŞTURMA FONKSİYONU
def generate_pdf():
    pdf = FPDF()
    pdf.add_page()
    
    # Türkçe karakterleri İngilizceye çeviren fonksiyon
    def fix_text(text):
        mapping = {
            "ş":"s", "Ş":"S", "ğ":"g", "Ğ":"G", "ü":"u", "Ü":"U", 
            "ı":"i", "İ":"I", "ö":"o", "Ö":"O", "ç":"c", "Ç":"C"
        }
        for tr, en in mapping.items():
            text = text.replace(tr, en)
        return text

    # Başlık ve İletişim Bilgileri
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, fix_text(ad), ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, fix_text(unvan), ln=True)
    pdf.cell(0, 10, f"Email: {email}", ln=True)
    pdf.ln(10)
    
    # Özet Bölümü
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Ozet", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 8, fix_text(ozet))
    pdf.ln(5)

    # Yetenekler Bölümü (Bu kısım eklendi)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Yetenekler", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 8, fix_text(yetenekler))
    pdf.ln(5)
    
    # Deneyim Bölümü
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Deneyimler", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 8, fix_text(deneyim))
    
    return pdf.output()

# 5. PDF İndirme Butonu İşlemleri
try:
    pdf_output = generate_pdf()
    pdf_bytes = bytes(pdf_output) # Streamlit formatı için dönüşüm

    st.sidebar.divider()
    st.sidebar.download_button(
        label="📄 Özgeçmişi PDF İndir",
        data=pdf_bytes,
        file_name="ozgecmis.pdf",
        mime="application/pdf"
    )
except Exception as e:
    st.sidebar.error(f"Hata oluştu: {e}")
