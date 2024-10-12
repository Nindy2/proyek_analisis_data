import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

all_df = pd.read_csv("all_data.csv")
datetime_columns = ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"]
all_df.sort_values(by="order_purchase_timestamp", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])
  
min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()

with st.sidebar:
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) &
                (all_df["order_purchase_timestamp"] <= str(end_date))]

st.header('Proyek Analisis Data Dashboard :sparkles:')

# Grafik Jumlah Pemesanan
monthly_orders_df = main_df.resample(rule='M', on='order_purchase_timestamp').agg({
    "order_id": "nunique",
    "payment_value": "sum"
})

monthly_orders_df = monthly_orders_df.reset_index()
monthly_orders_df.rename(columns={
    "order_id": "order_count",
    "payment_value": "revenue"
}, inplace=True)

st.subheader("Jumlah Pemesanan per Bulan")
fig=plt.figure(figsize=(10, 5))
plt.plot(monthly_orders_df["order_purchase_timestamp"], monthly_orders_df["order_count"], marker='o', linewidth=2, color="#72BCD4")
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
st.pyplot(fig)

# Grafik Keuntungan
st.subheader("Keuntungan per Bulan")
fig = plt.figure(figsize=(10, 5))
plt.plot(monthly_orders_df["order_purchase_timestamp"], monthly_orders_df["revenue"], marker='o', linewidth=2, color="#72BCD4")
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
st.pyplot(fig)

# Grafik Tipe Pembayaran
st.subheader("Jenis Pembayaran yang Digunakan")
fig=plt.figure(figsize=(14,6))
g = sns.countplot(x="payment_type", data=main_df[main_df["payment_type"] != "not_defined"])
g.set_xlabel("Jenis Pembayaran", fontsize=15)
g.set_ylabel("Count", fontsize=15)
st.pyplot(fig)

# Grafik Status Pemesanan Yang Belum Tuntas
st.subheader("Jumlah Status Pemesanan yang Belum Tuntas")
fig=plt.figure(figsize=(14,6))
g = sns.countplot(x="order_status", data=main_df[main_df["order_status"] != "delivered"])
g.set_xlabel("Status Pemesanan", fontsize=15)
g.set_ylabel("Count", fontsize=15)
st.pyplot(fig)
