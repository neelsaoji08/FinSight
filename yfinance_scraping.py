from bs4 import BeautifulSoup
import requests
import re



def search_for_stock_news_urls(ticker):
    search_url = "https://www.google.com/search?q=yahoo+finance+{}&tbm=nws".format(ticker)
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    r = requests.get(search_url,headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    atags = soup.find_all('a')
    hrefs = [link['href'] for link in atags]
    return hrefs 

def strip_unwanted_urls(urls, exclude_list):
    val = []
    for url in urls: 
        if 'https://' in url and not any(exclude_word in url for exclude_word in exclude_list):
            res = re.findall(r'(https?://\S+)', url)[0].split('&')[0]
            val.append(res)
    return list(set(val))


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



def pipeline_yfinance(monitored_tickers):

    raw_urls = {ticker:search_for_stock_news_urls(ticker) for ticker in monitored_tickers}
    exclude_list = ['maps', 'policies', 'preferences', 'accounts', 'support','google.com']
    cleaned_urls = {ticker:strip_unwanted_urls(raw_urls[ticker], exclude_list) for ticker in monitored_tickers}
    articles = {ticker:scrape_and_process(cleaned_urls[ticker]) for ticker in monitored_tickers}
    return articles,cleaned_urls
