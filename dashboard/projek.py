import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='white')

# Fungsi untuk membuat kategori review
def categori_df(df):
    bystatez_df = df.groupby(by="review_category").order_id.nunique().reset_index()
    return bystatez_df

# Fungsi untuk membuat analisis tipe pembayaran
def type_pembayaran(df):
    bystate_df = df.groupby(by="payment_type").order_id.nunique().reset_index()
    return bystate_df

# Fungsi untuk membuat analisis RFM
def rfm_analisis(df):
    # Mengelompokkan data untuk mendapatkan metrik RFM
    rfm_df = df.groupby(by="customer_id", as_index=False).agg({
        "order_purchase_timestamp": "max",  # Mengambil tanggal order terakhir
        "order_id": "nunique",               # Menghitung jumlah order
        "price": "sum"                       # Menghitung jumlah revenue yang dihasilkan
    })

    # Mengubah nama kolom
    rfm_df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]

    # Menghitung kapan terakhir pelanggan melakukan transaksi (hari)
    rfm_df["max_order_timestamp"] = pd.to_datetime(rfm_df["max_order_timestamp"]).dt.date  # Pastikan ini dalam format tanggal
    recent_date = rfm_df["max_order_timestamp"].max()  # Menggunakan rfm_df untuk mendapatkan tanggal terakhir
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
    
    return rfm_df

# Membaca dataset
main_df = pd.read_csv("D:\My Data ALL\Documents\data\dashboard\main.csv")

# Membuat DataFrame untuk analisis
categori_orders_df = categori_df(main_df)
payment_order_items_df = type_pembayaran(main_df)
rfm_df = rfm_analisis(main_df)

# Streamlit layout
st.header('Projek dicoding E-Commerce Publik Dataset')
st.subheader('Mursawal  ML-08')

# Visualisasi jenis produk yang paling banyak di order
st.subheader("1. Jenis Produk yang paling banyak di order customer")

fig, ax = plt.subplots(figsize=(10, 5)) 
colors_ = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="review_category",
    y="order_id",
    data=categori_orders_df.sort_values(by="order_id", ascending=False),
    palette=colors_
)
plt.title("Penilaian terhadap barang yang di order", loc="center", fontsize=15)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='y', labelsize=12)
st.pyplot(fig)



# Visualisasi jenis pembayaran yang paling sering digunakan
st.subheader("2. Jenis kategori yang paling sering diberikan customer terhadap produk")
fig, ax = plt.subplots(figsize=(10, 5))  # Membuat figure untuk visualisasi
colors_ = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="order_id",
    y="payment_type",
    data=payment_order_items_df.sort_values(by="order_id", ascending=False),
    palette=colors_,
    ax=ax
)
ax.set_title("Jenis Pembayaran yang paling sering dilakukan", loc="center", fontsize=15)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=12)
st.pyplot(fig)

# RFM Analisis
st.subheader("3. RFM Analisis ")
col1, col2, col3 = st.columns(3)

with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)

with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)

with col3:
    avg_frequency = format_currency(rfm_df.monetary.mean(), "AUD", locale='es_CO') 
    st.metric("Average Monetary", value=avg_frequency)

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))
colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]

sns.barplot(y="recency", x="customer_id", data=rfm_df.sort_values(by="recency", ascending=True).head(3), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("customer_id", fontsize=30)
ax[0].set_title("By Recency (days)", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=15)

sns.barplot(y="frequency", x="customer_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(3), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("customer_id", fontsize=30)
ax[1].set_title("By Frequency", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=15)

sns.barplot(y="monetary", x="customer_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(3), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel("customer_id", fontsize=30)
ax[2].set_title("By Monetary", loc="center", fontsize=50)
ax[2].tick_params(axis='y', labelsize=30)
ax[2].tick_params(axis='x', labelsize=15)

st.pyplot(fig)
