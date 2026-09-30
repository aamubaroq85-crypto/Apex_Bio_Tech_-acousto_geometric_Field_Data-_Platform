import streamlit as st
import pandas as pd
import numpy as np
import datetime

# Konfigurasi Halaman
st.set_page_config(
    page_title="Apex Bio Tech | Acousto-Geometric Platform",
    page_icon="⛏️",
    layout="wide"
)

# Sidebar Navigasi & Status Langganan
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
    
    # Menampilkan tabel data pemindaian
    st.dataframe(st.session_state.scans_db, use_container_width=True)
    
    st.info("💡 **Tips Bisnis:** Gunakan modul *Field Service* untuk memasukkan data baru saat melakukan audit di lokasi klien, dan berikan akses *Client Subscription* bagi manajemen tambang untuk memantau data secara real-time.")

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
            pi_eff = st.number_input("Nilai Kalibrasi $\pi_{\text{eff}}$", value=1.618033, format="%.6f")
            acoustic_freq = st.number_input("Frekuensi Resonansi Akustik (kHz)", value=45.5)
            raw_attenuation = st.number_input("Atenuasi Gelombang (dB/m)", value=2.15)
        
        submitted = st.form_submit_button("Proses Pemindaian & Hitung Parameter")
        
        if submitted:
            # Algoritma simulasi turunan konstanta Zuhri untuk porositas dan UCS
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
    st.title("📈 Client Portal: Analisis & Unduh Laporan Berlangganan")
    st.markdown("Portal khusus klien tambang untuk memantau integritas dinding pit dan data pori batuan secara berkelanjutan (*Recurring SaaS*).")
    
    # Filter berdasarkan lokasi
    selected_site = st.selectbox("Pilih Area Pit Tambang untuk Analisis", st.session_state.scans_db['Site_Location'].unique())
    
    filtered_data = st.session_state.scans_db[st.session_state.scans_db['Site_Location'] == selected_site]
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Rata-Rata Porositas Batuan", f"{filtered_data['Porosity_Pct'].mean():.2f} %")
    with col_b:
        st.metric("Rata-Rata Kekuatan UCS", f"{filtered_data['UCS_Strength_MPa'].mean():.2f} MPa")
        
    st.markdown("### Grafik Tren Porositas & Kekuatan Batuan")
    st.line_chart(filtered_data.set_index('Timestamp')[['Porosity_Pct', 'UCS_Strength_MPa']])
    
    # Tombol Ekspor Laporan berbayar/langganan
    csv_data = filtered_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Unduh Sertifikat Laporan Geoteknik Resmi (.CSV / PDF)",
        data=csv_data,
        file_name=f"Laporan_Porositas_{selected_site.replace(' ', '_')}.csv",
        mime="text/csv",
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
        * **Estimasi Margin:** Sangat Tinggi (Biaya variabel alat rendah, nilai jasa konsultasi ahli berdasarkan risiko keselamatan).
        """)
        st.button("Buat Penawaran Field Service Baru")
        
    with col_p2:
        st.subheader("Tier 2: Cloud Software Subscription (SaaS)")
        st.markdown("""
        * **Skema:** Langganan bulanan (*Monthly Recurring Revenue*) per lisensi tambang.
        * **Fasilitas:** Akses *real-time dashboard*, pemantauan stabilitas lereng jarak jauh, dan unduh laporan tak terbatas.
        * **Estimasi Margin:** Stabil & Berkelanjutan (Pendapatan pasif bulanan dari infrastruktur cloud).
        """)
        st.button("Kelola Lisensi Klien Aktif")
