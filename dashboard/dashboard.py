import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import os

path_to_file = os.path.join(os.path.dirname(__file__), '../dashboard/all_data.csv')


all_data = pd.read_csv(path_to_file)

all_data['payment_type'] = all_data['payment_type'].astype(str).dropna()
all_data['deliver_time'] = all_data['deliver_time'].astype(str).dropna()
all_data['product_category_name_english'] = all_data['product_category_name_english'].astype(str).dropna()
all_data = all_data.replace('nan', pd.NA).dropna(subset=['payment_type', 'deliver_time', 'product_category_name_english'])

st.title("E-Commerce Data Analysis Dashboard")

st.sidebar.header("Filters")

payment_type_options = sorted(all_data['payment_type'].unique())
selected_payment_types = st.sidebar.multiselect("Select Payment Type(s):", payment_type_options, default=payment_type_options)
filtered_data = all_data[all_data['payment_type'].isin(selected_payment_types)]

deliver_time_options = sorted(all_data['deliver_time'].unique())
selected_deliver_time = st.sidebar.multiselect("Select Delivery Time:", deliver_time_options, default=deliver_time_options)
filtered_data = filtered_data[filtered_data['deliver_time'].isin(selected_deliver_time)]

product_category_options = sorted(all_data['product_category_name_english'].unique())
selected_product_categories = st.sidebar.multiselect("Select Product Category(s):", product_category_options, default=product_category_options)
filtered_data = filtered_data[filtered_data['product_category_name_english'].isin(selected_product_categories)]

st.header("Key Insights")

st.subheader("Payment Type Distribution")
payment_type_counts = filtered_data.groupby('payment_type')['order_id'].count()
fig, ax = plt.subplots()
sns.barplot(x=payment_type_counts.index, y=payment_type_counts.values, ax=ax)
plt.xlabel("Payment Type")
plt.ylabel("Number of Orders")
plt.xticks(rotation=45)
st.pyplot(fig)

st.subheader("Delivery Time Distribution")
delivery_time_counts = filtered_data.groupby('deliver_time')['order_id'].count()
fig, ax = plt.subplots()
sns.barplot(x=delivery_time_counts.index, y=delivery_time_counts.values, ax=ax)
plt.xlabel("Delivery Time")
plt.ylabel("Number of Orders")
plt.xticks(rotation=45)
st.pyplot(fig)

st.subheader("Top Selling Product Categories")
product_category_sales = filtered_data.groupby('product_category_name_english')['order_id'].count().sort_values(ascending=False).head(10)
fig, ax = plt.subplots()
sns.barplot(x=product_category_sales.values, y=product_category_sales.index, ax=ax)
plt.xlabel("Number of Orders")
plt.ylabel("Product Category")
st.pyplot(fig)
