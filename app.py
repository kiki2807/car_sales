import pandas as pd 
import scipy.stats 
import streamlit as st 
import matplotlib.pyplot as plt
import time
import plotly.express as px

df_car_sales = pd.read_csv('/Users/cristinagomez/car_sales/vehicles_us.csv')
st.title('Car Sales')
st.write('This is a simple example of a Streamlit app. The data below is a dataset showing the sales of cars in the US.)')

st.dataframe(df_car_sales)

st.header('Data Visualization')
st.subheader('Price Distribution')
st.write('Below is a histogram showing the distribution of car prices.')

numeric_cols = df_car_sales.select_dtypes(include=['int64', 'float64']).columns

Q1 = df_car_sales[numeric_cols].quantile(0.25)
Q3 = df_car_sales[numeric_cols].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

df_no_outliers = df_car_sales[~((df_car_sales[numeric_cols] < lower_bound) | (df_car_sales[numeric_cols] > upper_bound)).any(axis=1)]
fig, ax = plt.subplots(figsize=(12, 6))
df_no_outliers['price'].plot(kind='hist', bins=50, color='orange', ax=ax)
ax.set_title('Price Distribution')
ax.set_xlabel('Price')
plt.xticks(rotation=90)

st.pyplot(fig)

st.subheader('Model Year vs Price')
st.write('Below is a scatter plot showing the relationship between the model year and the price of the cars.')

fig, ax = plt.subplots()
ax.scatter(df_no_outliers['model_year'], df_no_outliers['price'], c='green', alpha=0.5, s=10)

ax.set_xlabel('Model Year')
ax.set_ylabel('Price')
ax.set_title('Model Year vs Price')
ax.grid(True)

st.pyplot(fig)

st.subheader('Mileage vs Price')
st.write('Below is a scatter plot showing the relationship between the mileage and the price of the cars.')

fig, ax = plt.subplots()
ax.scatter(df_no_outliers['odometer'], df_no_outliers['price'], c='green', alpha=0.5, s=10)

ax.set_xlabel('Mileage')
ax.set_ylabel('Price')
ax.set_title('Mileage vs Price')
ax.grid(True)

st.pyplot(fig)

st.subheader('Model vs Price')
st.write('Below is a bar chart showing the average price of the cars by model.')

df_grouped = df_no_outliers.groupby('model')['price'].mean().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(12, 6))
df_grouped.plot(kind='bar', color='purple', ax=ax)
ax.set_title('Model vs Price')
ax.set_xlabel('Model')
ax.set_ylabel('Average Price')
plt.xticks(rotation=90)

st.plotly_chart(fig)

