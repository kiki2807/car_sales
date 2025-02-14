import pandas as pd 
import scipy.stats 
import streamlit as st 
import matplotlib.pyplot as plt
import plotly.express as px

df_car_sales = pd.read_csv('vehicles_us.csv')




df_car_sales['model_year'] = df_car_sales['model_year'].fillna(df_car_sales['model_year'].median())
df_car_sales['model_year'] = df_car_sales['model_year'].astype('int')

df_car_sales['is_4wd'] = df_car_sales['is_4wd'].fillna(df_car_sales['is_4wd'].median())
df_car_sales['is_4wd'] = df_car_sales['is_4wd'].astype('int')

df_car_sales['cylinders'] = df_car_sales['cylinders'].fillna(df_car_sales['cylinders'].median())
df_car_sales['cylinders'] = df_car_sales['cylinders'].astype('int')

df_car_sales['odometer'] = df_car_sales['odometer'].fillna(df_car_sales['odometer'].median())
df_car_sales['odometer'] = df_car_sales['odometer'].astype('int')

df_car_sales['paint_color'] = df_car_sales['paint_color'].fillna('Unknown')


st.title('Car Sales')
st.write('This is a simple example of a Streamlit app. The data below is a dataset showing the sales of cars in the US.)')

st.dataframe(df_car_sales)

year_checkbox = st.checkbox('Filter by year', value=True)
if year_checkbox:
    model_year = st.slider('Year', min_value=1984, max_value=2021, value=(1984, 2021))
    df_car_sales = df_car_sales[(df_car_sales['model_year'] >= model_year[0]) & (df_car_sales['model_year'] <= model_year[1])]
    st.dataframe(df_car_sales)

price_checkbox = st.checkbox('Filter by price', value=True)
if price_checkbox:
    price = st.slider('Price', min_value=0, max_value=200000, value=(0, 200000))
    df_car_sales = df_car_sales[(df_car_sales['price'] >= price[0]) & (df_car_sales['price'] <= price[1])]
    st.dataframe(df_car_sales)

model_checkbox = st.checkbox('Filter by model', value=True)
if model_checkbox:
    model = st.multiselect('Model', df_car_sales['model'].unique())
    df_car_sales = df_car_sales[df_car_sales['model'].isin(model)]
    st.dataframe(df_car_sales)

condition_checkbox = st.checkbox('Filter by condition', value=True)
if condition_checkbox:
    condition = st.multiselect('Condition', df_car_sales['condition'].unique())
    df_car_sales = df_car_sales[df_car_sales['condition'].isin(condition)]
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


fig = px.histogram(df_no_outliers, x='price', nbins=50, title='Price Distribution')
fig.update_layout(xaxis_title='Price', yaxis_title='Count')
st.plotly_chart(fig)
   
st.subheader('Model Year vs Price')
st.write('Below is a scatter plot showing the relationship between the model year and the price of the cars.')

fig = px.scatter(df_no_outliers, x='model_year', y='price', title='Model Year vs Price', color='price')
fig.update_layout(xaxis_title='Model Year', yaxis_title='Price')
st.plotly_chart(fig)

st.subheader('Mileage vs Price')
st.write('Below is a scatter plot showing the relationship between the mileage and the price of the cars.')

fig= px.scatter(df_no_outliers, x='odometer', y='price', title='Mileage vs Price', color='price')
fig.update_layout(xaxis_title='Mileage', yaxis_title='Price')
st.plotly_chart(fig)

st.subheader('Model vs Price')
st.write('Below is a bar chart showing the average price of the cars by model.')


df_grouped = df_no_outliers.groupby('model')['price'].mean().reset_index()

fig = px.bar(df_grouped, x='model', y='price', color='price', title='Model vs Price', height=600)
fig.update_layout(xaxis_title='Model', yaxis_title='Average Price', xaxis_tickangle=-45)

st.plotly_chart(fig)

