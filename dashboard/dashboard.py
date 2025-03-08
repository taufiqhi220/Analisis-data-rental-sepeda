import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
main_df = pd.read_csv("dashboard/main_data.csv")
main_df["dteday"] = pd.to_datetime(main_df["dteday"])

# Batasi rentang tanggal hanya untuk tahun 2011 dan 2012
min_date = main_df[main_df["yr"].isin([0, 1])]["dteday"].min()
max_date = main_df[main_df["yr"].isin([0, 1])]["dteday"].max()

# Sidebar untuk filter tanggal
with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
    # Filter data berdasarkan rentang tanggal
    filtered_df = main_df[(main_df["dteday"] >= pd.to_datetime(start_date)) & (main_df["dteday"] <= pd.to_datetime(end_date))]

# Buat helper function
def calculate_rentals(df):
    return {
        "holiday": df.groupby("holiday")["cnt"].sum(),
        "weekday": df.groupby("weekday")["cnt"].sum(),
        "workingday": df.groupby("workingday")["cnt"].sum(),
        "season": df.groupby("season")["cnt"].sum(),
    }

rental_data = calculate_rentals(filtered_df)

# Ganti indeks dengan label yang sesuai
holiday_labels = ["Bukan Libur", "Libur"]
weekday_labels = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
workingday_labels = ["Akhir Pekan / Libur", "Hari Kerja"]
season_labels = ["Spring", "Summer", "Fall", "Winter"]

st.title("Analisis Data Rental Sepeda 🚲")

# Menampilkan Rental berdasarkan Holiday
st.subheader("Rental Sepeda Berdasarkan Hari Libur")
fig, ax = plt.subplots(figsize=(6, 4))
rental_data["holiday"].plot(kind="bar", color=["blue", "red"], ax=ax)
ax.set_title("Rental pada Hari Libur")
ax.set_ylabel("Jumlah Rental")
ax.set_xlabel("Status Hari Libur")
ax.set_xticks(range(len(holiday_labels)))
ax.set_xticklabels(holiday_labels, rotation=0)
st.pyplot(fig)

# Menampilkan Rental berdasarkan Weekday
st.subheader("Rental Sepeda Berdasarkan Hari dalam Seminggu")
fig, ax = plt.subplots(figsize=(6, 4))
rental_data["weekday"].plot(kind="bar", color="green", ax=ax)
ax.set_title("Rental Berdasarkan Hari dalam Seminggu")
ax.set_ylabel("Jumlah Rental")
ax.set_xlabel("Hari dalam Seminggu")
ax.set_xticks(range(len(weekday_labels)))
ax.set_xticklabels(weekday_labels, rotation=45)
st.pyplot(fig)

# Menampilkan Rental berdasarkan Workingday
st.subheader("Rental Sepeda Berdasarkan Hari Kerja")
fig, ax = plt.subplots(figsize=(6, 4))
rental_data["workingday"].plot(kind="bar", color=["orange", "purple"], ax=ax)
ax.set_title("Rental pada Hari Kerja")
ax.set_ylabel("Jumlah Rental")
ax.set_xlabel("Status Hari Kerja")
ax.set_xticks(range(len(workingday_labels)))
ax.set_xticklabels(workingday_labels, rotation=0)
st.pyplot(fig)

# Menampilkan Rental berdasarkan Musim
st.subheader("Rental Sepeda Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(8, 5))
rental_data["season"].plot(kind="bar", color=["springgreen", "gold", "orange", "lightblue"], ax=ax)
ax.set_title("Jumlah Rental Sepeda Berdasarkan Musim")
ax.set_ylabel("Jumlah Rental")
ax.set_xlabel("Musim")
ax.set_xticks(range(len(season_labels)))
ax.set_xticklabels(season_labels, rotation=0)
st.pyplot(fig)
