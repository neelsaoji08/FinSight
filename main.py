import streamlit as st
# from livemint_scraping import pipeline_mint
# from moneycontrol_scraping import pipeline_moneycontrol
# from yfinance_scraping import pipeline_yfinance
# from model import pipeline_training


st.title('Financial News Summary And Sentiment Analysis')
st.sidebar.title('To get Analysis of any news Article')
st.sidebar.header("News Article URLs")
urls = []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i+1}")
    urls.append(url)

process_url_clicked = st.sidebar.button("Process URLs")


if  process_url_clicked:
    pass 


ticks=st.text_input(label='Stocks to Monitior')

mint=st.checkbox(label='Scrape News from LiveMint',value=False,)
money=st.checkbox(label='Scrape News from MoneyControl',value=False)
yfin=st.checkbox(label='Scrape News from Yfinance',value=False)

if st.button('Process Stocks'):

    if ticks:
        tickers=ticks.split(' ')

    if mint:
        pass
    if money:
        pass
    if yfin:
        pass



