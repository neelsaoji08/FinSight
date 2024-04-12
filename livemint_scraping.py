from bs4 import BeautifulSoup
import requests
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}


def preprocess(url):
    x=url.split('=')[5:]
    new_url=''
    for i in range(0,len(x)):
        new_url+=x[i]
    return new_url

def search_for_stock_news_urls(ticker):
    
    url=f"https://www.google.com/search?q=mint+{ticker}+share+price"
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    news_links=[a.get('href') for a in soup.find_all('a') 
            if f"https://www.livemint.com/market/market-stats/stocks-" in a["href"] ]
    news_page_url=preprocess(news_links[0])

    return news_page_url

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

