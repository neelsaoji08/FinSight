
from transformers import PegasusTokenizer, PegasusForConditionalGeneration
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
from transformers import AutoTokenizer,AutoModelForSequenceClassification
from peft import get_peft_model, LoraConfig
import numpy as np

model_name = "human-centered-summarization/financial-summarization-pegasus"
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name)


tokenizer_sentiment = AutoTokenizer.from_pretrained("ahmedrachid/FinancialBERT-Sentiment-Analysis")
model_sentiment = AutoModelForSequenceClassification.from_pretrained("ahmedrachid/FinancialBERT-Sentiment-Analysis", num_labels=3)
lora_config = LoraConfig.from_pretrained('models/FinancialBert')
model_sentiment = get_peft_model(model_sentiment, lora_config)





def summarize(articles):
    summaries = []
    for article in articles:
        input_ids = tokenizer.encode(article, return_tensors='pt')
        output = model.generate(input_ids, max_length=100,
                                num_beams=5, early_stopping=True)
        summary = tokenizer.decode(output[0], skip_special_tokens=True)
        summaries.append(summary)
    return summaries


def find_sentiment(text):
    encoded_input = tokenizer_sentiment(text,padding=True,truncation=True ,return_tensors='pt')
    output = model_sentiment(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    return scores


def pipeline_training(monitored_tickers, articles):
    summaries = {ticker: summarize(articles[ticker]) for ticker in monitored_tickers}
    scores = {ticker: [] for ticker in monitored_tickers}

    for ticker, ticker_summaries in summaries.items():
        for summary in ticker_summaries:
            score = find_sentiment(summary)
            scores[ticker].append(np.array(score))

    return scores,summaries
