# UAV Performance Dashboard (ARUNA)


## 🎯 Fitur:
- Input parameter: massa UAV, luas sayap, CL_max, CD₀, efisiensi, dll
- 8 grafik performa:
  - Lift/Drag vs Airspeed
  - Range (km) vs Airspeed
  - Endurance (min) vs Airspeed
  - Climb Rate (m/s) vs Airspeed
  - Drag (N) vs Airspeed
  - Efficiency (Wh/km) vs Airspeed
  - Power (W) vs Airspeed
  - Fuselage AoA (deg) vs Airspeed
- Panel General Stats (AUW, CL_max, Wing Loading, dll)
- Garis vertikal: Stall, Cruise, Loiter speed
- Tombol download semua data performa ke CSV

## 🚀 Cara Menjalankan
1. Install Streamlit dan dependensi:
```bash
pip install -r requirements.txt
```

2. Jalankan dashboard:
```bash
app.py
```

3. Akses di browser (default: http://localhost:8501)

## 🛫 Cocok untuk
- Perancang UAV / pesawat ringan
- Evaluasi efisiensi sistem propulsi
- Analisis misi: endurance, cruise, climb
