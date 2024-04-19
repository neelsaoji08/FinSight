import streamlit as st
import pandas as pd
from stock_preprocessing_and_model import pipeline

df=pd.read_csv('tokens\India_tickers.csv')


st.title('Stock Price Predictions')


stock_name = df['Name'].values
selected_stock = st.selectbox(
    "Type or select a stock from the dropdown",
    stock_name
)

ticker=df[df['Name']==selected_stock]['Ticker']

model=pipeline(ticker)


