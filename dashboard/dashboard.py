import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

data = pd.read_csv('./data/data2.csv')


# melakukan plot terhadap data untuk pertanyaan no 1
st.header('Jumlah Penjualan Mingguan Berdasarkan Metode Pembayaran')
data['order_purchase_timestamp'] = pd.to_datetime(data['order_purchase_timestamp']).sort_values(ascending=True)
order_product_visualization = data[['payment_type', 'order_purchase_timestamp']]
order_product_visualization.set_index('order_purchase_timestamp', inplace=True)
weekly_sale = order_product_visualization.groupby('payment_type').resample('W').size().reset_index()
weekly_sale_reset = weekly_sale.reset_index()
melted_sale = pd.melt(weekly_sale_reset, id_vars=['payment_type'], value_vars=weekly_sale_reset.columns[1:], var_name='date', value_name='count')

# Menggunakan Plotly Express untuk membuat line chart
fig = px.line(melted_sale, x='date', y='count', color='payment_type')
fig.update_layout(xaxis_title='Tanggal', yaxis_title='Jumlah Pembayaran')

# Menampilkan plot di Streamlit
st.write(fig)

# melakukan plot terhadap data untuk pertanyaan no 2
data['is_late'] = data['order_estimated_delivery_date'] <= data['order_delivered_customer_date']
data['is_late'] = data['is_late'].map({True: 'Terlambat', False: 'Tidak Terlambat'})
late_count = data['is_late'].value_counts()

# Membuat countplot dengan plotly express
fig = px.bar(late_count, x=late_count.index, y=late_count.values, color=late_count.index)

# Menampilkan plot di Streamlit dan memberikan header
st.header('Perbandingan Jumlah Pengiriman Tepat Waktu dan Terlambat')
st.write(fig)


# melakukan plot terhadap data untuk pertanyaan no 3
category_sale_six_month = data.loc[(data['order_purchase_timestamp'] > '2018-03-01') & (data['order_purchase_timestamp'] < data['order_purchase_timestamp'].max()), ['product_category_name_english', 'order_purchase_timestamp']].groupby('product_category_name_english').resample('M', on='order_purchase_timestamp').size().reset_index()
category_sale_six_month.columns = ['product_category_name_english', 'order_purchase_timestamp', 'count']
category_sale_six_month = category_sale_six_month.loc[category_sale_six_month['product_category_name_english'].isin(category_sale_six_month.groupby('product_category_name_english').sum().sort_values(by='count', ascending=False).index[:5]), :]


# Membuat line plot chart dengan Plotly Express
fig = px.line(category_sale_six_month, x='order_purchase_timestamp', y='count', color='product_category_name_english')
fig.update_layout(xaxis_title='Tanggal', yaxis_title='Jumlah Penjualan')
# Menampilkan plot di Streamlit dan memberikan header
st.header('Jumlah Penjualan 5 Kategori Produk Terbanyak dalam 6 Bulan Terakhir')
st.write(fig)