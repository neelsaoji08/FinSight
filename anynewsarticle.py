from transformers import PegasusTokenizer, PegasusForConditionalGeneration
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import requests
from bs4 import BeautifulSoup
from scipy.special import softmax
import pandas as pd

senti={0:'Negative',
       1:'Neutral',
       2:'Postive'}


model_name = "human-centered-summarization/financial-summarization-pegasus"
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name)

tokenizer_sentiment = AutoTokenizer.from_pretrained(
    "cardiffnlp/twitter-roberta-base-sentiment-latest")
model_sentiment = AutoModelForSequenceClassification.from_pretrained(
    "cardiffnlp/twitter-roberta-base-sentiment-latest")

headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}


def scrape_and_process(URLs):
    ARTICLES = []
    for url in URLs: 
        r = requests.get(url,headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text = [paragraph.text for paragraph in paragraphs]
        words = ' '.join(text).split(' ')[:350]
        ARTICLE = ' '.join(words)
        ARTICLES.append(ARTICLE)
    return ARTICLES


def summarize(articles):
    summaries = []
    for article in articles:
        input_ids = tokenizer.encode(article, return_tensors='pt')
        output = model.generate(input_ids, max_length=55,
                                num_beams=5, early_stopping=True)
        summary = tokenizer.decode(output[0], skip_special_tokens=True)
        summaries.append(summary)
    return summaries

def find_sentiment(summaries):
    final_scores=[]
    for summary in summaries:
        encoded_input = tokenizer_sentiment(summary,padding=True,truncation=True ,return_tensors='pt')
        output = model_sentiment(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        final_scores.append(scores)
    return final_scores

def process_url(urls):
    ARTICLES=scrape_and_process(urls)
    summaries=summarize(ARTICLES)
    scores=find_sentiment(summaries)
    sentiment=[]
    for s in scores:
        sentiment.append(senti[s.argmax()])
    
    df = pd.DataFrame({'URLs': urls, 'Summary': summaries, 'Score': scores, 'Sentiment': sentiment})
    return df

