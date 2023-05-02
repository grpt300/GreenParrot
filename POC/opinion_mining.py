import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

def get_sentiment(text):
    try:
        sia = SentimentIntensityAnalyzer()
        sentiment_scores = sia.polarity_scores(text)

        # Convert sentiment_scores to a dictionary with key as "sentiment"
        sentiment_dict = {
            "Sentiment": sentiment_scores['compound']
        }
        return sentiment_dict
    except Exception as e:
        print(f"Error in get_sentiment: {e}")
        return {"sentiment": 0}
