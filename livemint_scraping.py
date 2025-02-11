from bs4 import BeautifulSoup
import requests
import streamlit as st

headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

def search_for_stock_news_urls(ticker):

    search_quey=f'livemint {ticker} share'
    
    url='https://www.googleapis.com/customsearch/v1'
    
    params={
    'q':search_quey,
    'key':st.secrets['GOOGLE_API_KEY'],
    'cx':st.secrets['SEARCH_ENGINE_ID']
    }
    respose=requests.get(url,params=params)
    result=respose.json()
    
    if 'items' in result:
        print(result['items'][0]['link'])
        return result['items'][0]['link']
    

def get_news_links(news_page_url):

    r = requests.get(news_page_url,headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    d=soup.find(id='stock_news')
    news_links=[a.get('href') for a in d.find_all('a') ]
    news_links=list(set(news_links))
    
    return news_links

def scrape_and_process(URLs):
    ARTICLES = []
    for url in URLs: 
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text = [paragraph.text for paragraph in paragraphs]
        words = ' '.join(text).split(' ')[:350]
        ARTICLE = ' '.join(words)
        ARTICLES.append(ARTICLE)
    return ARTICLES

def pipeline_mint(monitored_tickers):

    raw_urls = {ticker:search_for_stock_news_urls(ticker) for ticker in monitored_tickers}
    news_urls ={ticker:get_news_links(raw_urls[ticker]) for ticker in monitored_tickers}
    articles = {ticker:scrape_and_process(news_urls[ticker]) for ticker in monitored_tickers}
    return articles,news_urls

