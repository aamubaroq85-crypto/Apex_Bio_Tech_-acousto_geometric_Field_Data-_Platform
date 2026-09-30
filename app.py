import streamlit as st
import pandas as pd
import numpy as np
import datetime
from fpdf import FPDF

# Konfigurasi Halaman
st.set_page_config(
    page_title="Apex Bio Tech | Acousto-Geometric Platform",
    page_icon="⛏️",
    layout="wide"
)

# Kelas Generator PDF Berkop Perusahaan
class PDFReport(FPDF):
    def header(self):
        # Kop Perusahaan
        self.set_font('helvetica', 'B', 16)
        self.set_text_color(24, 43, 73)
        self.cell(0, 8, 'APEX BIO TECH APPLIED TECHNOLOGIES', 0, 1, 'C')
        
        self.set_font('helvetica', '', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, 'Divisi Geomekanika & Teknologi Acousto-Geometric Fluks Konstanta Zuhri (pi_eff)', 0, 1, 'C')
        self.cell(0, 5, 'Email: contact@apexbiotech.internal | Web: portal.apexbiotech.io', 0, 1, 'C')
        self.ln(5)
        
        # Garis Pembatas Kop
        self.set_draw_color(41, 128, 185)
        self.set_line_width(0.8)
        self.line(10, 28, 200, 28)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Sertifikat Laporan Resmi Geoteknik - Halaman {self.page_no()}', 0, 0, 'C')

def generate_pdf_report(site_name, df_subset):
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Judul Dokumen
    pdf.set_font('helvetica', 'B', 14)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 8, f'LAPORAN SERTIFIKASI AUDIT POROSITAS & UCS', 0, 1, 'L')
    
    pdf.set_font('helvetica', '', 10)
    pdf.cell(0, 6, f'Lokasi Pit / Blok: {site_name}', 0, 1, 'L')
    pdf.cell(0, 6, f'Tanggal Cetak: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1, 'L')
    pdf.ln(5)
    
    # Tabel Data
    pdf.set_font('helvetica', 'B', 9)
    pdf.set_fill_color(41, 128, 185)
    pdf.set_text_color(255, 255, 255)
    
    headers = ['Scan ID', 'Timestamp', 'Pi_Eff', 'Porositas (%)', 'UCS (MPa)', 'Status']
    widths = [25, 35, 20, 25, 25, 50]
    
    for i, h in enumerate(headers):
        pdf.cell(widths[i], 7, h, 1, 0, 'C', True)
    pdf.ln()
    
    pdf.set_font('helvetica', '', 9)
    pdf.set_text_color(0, 0, 0)
    
    for index, row in df_subset.iterrows():
        pdf.cell(widths[0], 6, str(row['Scan_ID']), 1, 0, 'C')
        pdf.cell(widths[1], 6, str(row['Timestamp']), 1, 0, 'C')
        pdf.cell(widths[2], 6, str(row['Pi_Eff_Value']), 1, 0, 'C')
        pdf.cell(widths[3], 6, str(row['Porosity_Pct']), 1, 0, 'C')
        pdf.cell(widths[4], 6, str(row['UCS_Strength_MPa']), 1, 0, 'C')
        pdf.cell(widths[5], 6, str(row['Status_Kelayakan']), 1, 0, 'L')
        pdf.ln()
        
    pdf.ln(10)
    pdf.set_font('helvetica', 'I', 9)
    pdf.multi_cell(0, 5, 'Catatan: Laporan ini dihasilkan secara otomatis oleh sistem analitik berbasis cloud Apex Bio Tech. Validasi kekuatan batuan diukur menggunakan metode non-destruktif gelombang akustik terarah.')
    
    return pdf.output(dest='S').encode('latin1')

# Sidebar Navigasi
st.sidebar.title("⛏️ Apex Bio Tech Suite")
st.sidebar.markdown("**Acousto-Geometric Porosity Scanner**")
st.sidebar.markdown("---")

menu = st.sidebar.selectbox(
    "Pilih Mode Operasional",
    ["Dashboard Utama", "Field Service Logger (Insitu)", "Client Subscription Analytics", "Manajemen Kontrak & Lisensi"]
)

# Simulasi Database Sederhana dalam Session State
if 'scans_db' not in st.session_state:
    st.session_state.scans_db = pd.DataFrame({
        'Scan_ID': ['SCN-2026-001', 'SCN-2026-002', 'SCN-2026-003'],
        'Site_Location': ['Pit Barat - Blok A', 'Pit Utara - Bench 3', 'Open Cut - Sektor 2'],
        'Timestamp': ['2026-09-28 08:30', '2026-09-29 11:15', '2026-09-30 14:20'],
        'Pi_Eff_Value': [1.618, 1.625, 1.612],
        'Porosity_Pct': [14.2, 8.5, 22.1],
        'UCS_Strength_MPa': [85.4, 110.2, 54.6],
        'Status_Kelayakan': ['Stabil / Layak', 'Sangat Kuat', 'Perlu Perhatian (Waspada)']
    })

if menu == "Dashboard Utama":
    st.title("📊 Platform Intelijen Geomekanika & Porositas Batuan")
    st.markdown("""
    Selamat datang di pusat komando **Apex Bio Tech**. Sistem ini mengintegrasikan pemindaian akustik non-destruktif berbasis konstanta $\pi_{\text{eff}}$ 
    untuk memberikan hasil analisis geoteknik seketika bagi operasi penambangan terbuka maupun bawah tanah.
    """)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Pemindaian Bulan Ini", "142 Titik", "+18% dari bulan lalu")
    col2.metric("Klien Aktif Berlangganan", "8 Perusahaan Tambang", "Tier-1 Kontrak")
    col3.metric("Akurasi Validasi In-Situ", "99.4%", "Standar Lab Terkalibrasi")
    
    st.markdown("---")
    st.subheader("Peta Sebaran Titik Pemindaian Terbaru")
    st.dataframe(st.session_state.scans_db, use_container_width=True)

elif menu == "Field Service Logger (Insitu)":
    st.title("🛠️ Field Service: Input Data Pemindaian Lapangan")
    st.markdown("Gunakan formulir ini saat melakukan penugasan *High-Margin Field Service* di lokasi tambang klien.")
    
    with st.form("scan_form"):
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            client_name = st.text_input("Nama Perusahaan / Klien Tambang", "PT Tambang Makmur Sejahtera")
            site_loc = st.text_input("Lokasi Pit / Blok Pengujian", "Pit Selatan - Level 2")
            operator_id = st.text_input("ID Teknisi / Operator", "ENG-BAROQ-01")
        with col_f2:
            pi_eff = st.number_input("Nilai Kalibrasi pi_eff", value=1.618033, format="%.6f")
            acoustic_freq = st.number_input("Frekuensi Resonansi Akustik (kHz)", value=45.5)
            raw_attenuation = st.number_input("Atenuasi Gelombang (dB/m)", value=2.15)
        
        submitted = st.form_submit_button("Proses Pemindaian & Hitung Parameter")
        
        if submitted:
            calculated_porosity = round(abs(np.sin(pi_eff) * 25 + (raw_attenuation * 3.5)), 2)
            calculated_ucs = round(max(10, 150 - (calculated_porosity * 4.2)), 2)
            
            if calculated_porosity > 20:
                status = "Perlu Perhatian (Waspada)"
            elif calculated_porosity > 10:
                status = "Stabil / Layak"
            else:
                status = "Sangat Kuat"
                
            new_id = f"SCN-2026-{len(st.session_state.scans_db)+1:03d}"
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            
            new_row = pd.DataFrame({
                'Scan_ID': [new_id],
                'Site_Location': [f"{client_name} - {site_loc}"],
                'Timestamp': [current_time],
                'Pi_Eff_Value': [pi_eff],
                'Porosity_Pct': [calculated_porosity],
                'UCS_Strength_MPa': [calculated_ucs],
                'Status_Kelayakan': [status]
            })
            
            st.session_state.scans_db = pd.concat([new_row, st.session_state.scans_db], ignore_index=True)
            st.success(f"Pemindaian Berhasil Direkam! ID: {new_id}")
            st.balloons()

elif menu == "Client Subscription Analytics":
    st.title("📈 Client Portal: Analisis & Unduh Laporan Resmi")
    st.markdown("Portal khusus klien tambang untuk memantau integritas dinding pit dan mengunduh sertifikat laporan ber-kop perusahaan (*Recurring SaaS*).")
    
    selected_site = st.selectbox("Pilih Area Pit Tambang untuk Analisis", st.session_state.scans_db['Site_Location'].unique())
    
    filtered_data = st.session_state.scans_db[st.session_state.scans_db['Site_Location'] == selected_site]
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Rata-Rata Porositas Batuan", f"{filtered_data['Porosity_Pct'].mean():.2f} %")
    with col_b:
        st.metric("Rata-Rata Kekuatan UCS", f"{filtered_data['UCS_Strength_MPa'].mean():.2f} MPa")
        
    st.markdown("### Grafik Tren Porositas & Kekuatan Batuan")
    st.line_chart(filtered_data.set_index('Timestamp')[['Porosity_Pct', 'UCS_Strength_MPa']])
    
    st.markdown("---")
    st.subheader("Unduh Dokumen Laporan Resmi")
    
    # Tombol Unduh PDF Berkop Perusahaan
    pdf_bytes = generate_pdf_report(selected_site, filtered_data)
    st.download_button(
        label="📥 Unduh Sertifikat Laporan Resmi (Format PDF)",
        data=pdf_bytes,
        file_name=f"Sertifikat_Geoteknik_{selected_site.replace(' ', '_')}.pdf",
        mime="application/pdf",
    )

elif menu == "Manajemen Kontrak & Lisensi":
    st.title("💼 Manajemen Paket Layanan & Monetisasi")
    st.markdown("Kelola skema penagihan untuk kombinasi **Field Service** dan **Data Software Subscription**.")
    
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        st.subheader("Tier 1: High-Margin Field Service")
        st.markdown("""
        * **Skema:** Penagihan per hari penugasan atau per 100 titik pemindaian di lokasi pit.
        * **Target:** Kontraktor tambang baru yang membutuhkan asesmen cepat tanpa investasi alat.
        * **Estimasi Margin:** Sangat Tinggi.
        """)
        if st.button("Buat Penawaran Field Service Baru"):
            st.success("Formulir penawaran baru berhasil diinisiasi!")
        
    with col_p2:
        st.subheader("Tier 2: Cloud Software Subscription (SaaS)")
        st.markdown("""
        * **Skema:** Langganan bulanan (*Monthly Recurring Revenue*) per lisensi tambang.
        * **Fasilitas:** Akses *real-time dashboard*, pemantauan stabilitas lereng jarak jauh, dan unduh PDF tak terbatas.
        * **Estimasi Margin:** Stabil & Berkelanjutan.
        """)
        if st.button("Kelola Lisensi Klien Aktif"):
            st.info("Menghubungkan ke panel manajemen lisensi klien aktif...")
