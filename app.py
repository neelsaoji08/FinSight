import streamlit as st
from livemint_scraping import pipeline_mint
from moneycontrol_scraping import pipeline_moneycontrol
from yfinance_scraping import pipeline_yfinance
from model import pipeline_training
from create_dataframe import create_output_array
import pandas as pd
from anynewsarticle import process_url


def download_button(name, csv, key):
    """
    Creates a Streamlit download button for a CSV file.

    Args:
        name: The name of the button.
        csv: The CSV data to download.
        key: A unique key for the button.
    """
    st.download_button(
        "Press to Download",
        csv,
        f"{name}.csv",
        "text/csv",
        key=f'{key}-csv'
    )

st.title('Financial News Summary And Sentiment Analysis')
st.sidebar.title('To get Analysis of any news Article')
st.sidebar.header("News Article URLs")

urls = []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i+1}")
    if len(url) != 0:
        urls.append(url)

process_url_clicked = st.sidebar.button("Process URLs")

if process_url_clicked:
    df = process_url(urls)  # Assuming 'process_url' is a defined function
    st.sidebar.dataframe(df)
    csv = df.to_csv(index=False)
    st.sidebar.download_button(
        "Press to Download",
        csv,
        "links.csv",
        "text/csv",
        key='download-csv'
    )

ticks = st.text_input(label='Stocks to Monitor')
mint = st.checkbox(label='Scrape News from LiveMint', value=False)
money = st.checkbox(label='Scrape News from MoneyControl', value=False)

tickers = []
if st.button('Process Stocks'):
    if ticks:
        tickers = ticks.split(' ')
    if mint:
        articles_mint, news_urls_mint = pipeline_mint(tickers)  # Assuming 'pipeline_mint' is defined
        scores_mint, summaries_mint = pipeline_training(tickers, articles_mint)  # Assuming 'pipeline_training' is defined
        output = create_output_array(summaries_mint, scores_mint, news_urls_mint, tickers)  # Assuming 'create_output_array' is defined
        df = pd.DataFrame(output)
        df.columns = ['Stock', 'Summary', 'Scores', 'Sentiment', 'link', 'max_score']
        st.header('LiveMint Articles')
        st.dataframe(df)
        csv = df.to_csv(index=False)
        download_button('Livemint', csv, 'mint')


    if money:
        articles_money, news_urls_money = pipeline_moneycontrol(tickers)  # Assuming 'pipeline_moneycontrol' is defined
        scores_money, summaries_money = pipeline_training(tickers, articles_money)
        output = create_output_array(summaries_money, scores_money, news_urls_money, tickers)
        df = pd.DataFrame(output)
        df.columns = ['Stock', 'Summary', 'Scores', 'Sentiment', 'link', 'max_score']
        st.header('Moneycontrol Articles')
        st.dataframe(df)
        csv = df.to_csv(index=False)
        download_button('moneycontrol', csv, 'money')

    # if yfin:
    #     articles_yfin,news_urls_yfin=pipeline_yfinance(tickers)
    #     scores_yfin,summaries_yfin=pipeline_training(tickers,articles_yfin)
    #     output=create_output_array(summaries_yfin,scores_yfin,news_urls_yfin,tickers)
    #     df=pd.DataFrame(output)
    #     st.header('Yfinance Articles')
    #     df.columns=['Stock','Summary','Scores','Sentiment','link']
    #     st.dataframe(df)

    #     csv = df.to_csv(index=False)
    #     download_button('yfinance',csv,'yfinance')
