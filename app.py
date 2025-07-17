import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json

st.set_page_config(layout="wide")
st.title("UAV Performance Dashboard - ARUNA")

# Sidebar Load Config
st.sidebar.header("Load Configuration")
config_file = st.sidebar.file_uploader("Upload JSON Config", type="json")

if config_file is not None:
    config = json.load(config_file)
else:
    config = {}

# Sidebar Inputs
st.sidebar.header("Input Parameters")
uav_name = st.sidebar.text_input("UAV Name", config.get("UAV Name", "ARUNA-X"))
mass = st.sidebar.number_input("UAV Mass (kg)", 1.0, 100.0, config.get("mass", 5.3), step=0.1)
wingspan = st.sidebar.number_input("Wingspan (m)", 0.5, 10.0, config.get("wingspan", 2.1))
wing_area = st.sidebar.number_input("Wing Area (m²)", 0.1, 5.0, config.get("wing_area", 0.4513))
aspect_ratio = st.sidebar.number_input("Aspect Ratio", 2.0, 30.0, config.get("aspect_ratio", round(wingspan**2 / wing_area, 2)))
cl_max = st.sidebar.number_input("CL_max", 0.5, 2.5, config.get("cl_max", 1.5))
cl_cruise = st.sidebar.number_input("Target CL_cruise", 0.4, 1.2, config.get("cl_cruise", 0.65))
cd0 = st.sidebar.number_input("CD₀", 0.010, 0.080, config.get("cd0", 0.022))
efficiency = st.sidebar.number_input("Prop+Motor Efficiency", 0.2, 1.0, config.get("efficiency", 0.65))
battery_capacity = st.sidebar.number_input("Battery Capacity (Wh)", 100, 5000, config.get("battery_capacity", 600))

# Save config JSON
st.sidebar.markdown("---")
if st.sidebar.button("💾 Save Current Config"):
    save_config = {
        "UAV Name": uav_name,
        "mass": mass,
        "wingspan": wingspan,
        "wing_area": wing_area,
        "aspect_ratio": aspect_ratio,
        "cl_max": cl_max,
        "cl_cruise": cl_cruise,
        "cd0": cd0,
        "efficiency": efficiency,
        "battery_capacity": battery_capacity
    }
    config_json = json.dumps(save_config, indent=2)
    st.sidebar.download_button("Download Config JSON", config_json, file_name="uav_config.json")

# Constants & Calculation
rho = 1.225
g = 9.81
W = mass * g
e = 0.85
V = np.linspace(10, 45, 100)

CL = W / (0.5 * rho * wing_area * V**2)
CD = cd0 + CL**2 / (np.pi * e * aspect_ratio)
D = 0.5 * rho * wing_area * V**2 * CD
P = D * V / efficiency
endurance_hr = battery_capacity / P
range_km = endurance_hr * V * 3.6
endurance_min = endurance_hr * 60
eff_whkm = (P * 3.6) / V
climb_rate = (2000 - P) / W
climb_rate = np.maximum(climb_rate, 0)

# Revised AoA estimation
CL_0 = 0.2
CL_alpha_deg = 0.11  # per degree
aoa = (CL - CL_0) / CL_alpha_deg

ld_ratio = CL / CD

# Characteristic speeds
stall_speed = np.sqrt((2 * W) / (rho * wing_area * cl_max))
cruise_speed = np.sqrt((2 * W) / (rho * wing_area * cl_cruise))
k = 1 / (np.pi * e * aspect_ratio)
loiter_speed = np.sqrt((2 * W) / (rho * wing_area)) * np.sqrt(k / cd0)

# General Stats
st.subheader("General Stats")
col1, col2, col3 = st.columns(3)
col1.metric("AUW", f"{mass:.2f} kg")
col1.metric("Wing Loading", f"{(mass * g / wing_area):.1f} N/m²")
col1.metric("Stall Speed", f"{stall_speed:.2f} m/s")
col2.metric("Cruise Speed", f"{cruise_speed:.2f} m/s")
col2.metric("Loiter Speed", f"{loiter_speed:.2f} m/s")
col2.metric("Max Climb", f"{np.max(climb_rate):.1f} m/s")
col3.metric("Battery", f"{battery_capacity} Wh")
col3.metric("Efficiency", f"{efficiency:.2f}")
col3.metric("CL_max", f"{cl_max}")

# DataFrame
df = pd.DataFrame({
    "Airspeed (m/s)": V,
    "Lift/Drag": ld_ratio,
    "Range (km)": range_km,
    "Endurance (min)": endurance_min,
    "Climb Rate (m/s)": climb_rate,
    "Drag (N)": D,
    "Efficiency (Wh/km)": eff_whkm,
    "Power (W)": P,
    "Fuselage AoA (deg)": aoa
})

# 8 Plot Layout (2 rows x 4 columns)
metrics = [
    "Lift/Drag", "Range (km)", "Endurance (min)", "Climb Rate (m/s)",
    "Drag (N)", "Efficiency (Wh/km)", "Power (W)", "Fuselage AoA (deg)"
]

figs = []
for metric in metrics:
    fig, ax = plt.subplots()
    ax.plot(V, df[metric], color='orange')
    ax.axvline(stall_speed, color='blue', linestyle='--', label='Stall')
    ax.axvline(cruise_speed, color='green', linestyle='--', label='Cruise')
    ax.axvline(loiter_speed, color='red', linestyle='--', label='Loiter')
    ax.set_title(f"{metric} vs Airspeed")
    ax.set_xlabel("Airspeed (m/s)")
    ax.set_ylabel(metric)
    ax.grid(True)
    figs.append(fig)

# Display in grid 2x4
st.subheader("Performance Charts")
row1 = st.columns(4)
row2 = st.columns(4)
for i in range(4):
    row1[i].pyplot(figs[i])
    row2[i].pyplot(figs[i+4])

# Download CSV
st.subheader("Export")
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("📥 Download All Performance Data", csv, file_name=f"{uav_name}_performance.csv", mime="text/csv")

