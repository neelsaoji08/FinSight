senti={0:'Negative',
       1:'Neutral',
       2:'Postive'}

def create_output_array(summaries, scores, urls,monitored_tickers):
    output = []
    for ticker in monitored_tickers:
        for counter in range(len(summaries[ticker])):
            output_this = [
                ticker,
                summaries[ticker][counter],
                scores[ticker][counter],
                senti[scores[ticker][counter].argmax()],
                urls[ticker][counter]
            ]
            output.append(output_this)
    return output