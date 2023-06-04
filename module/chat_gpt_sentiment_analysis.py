import openai
import os

openai.api_key = os.environ.get('OPENAI_API_KEY')

def analyze_sentiment(text):
    """
    Analyze the sentiment of a text using the ChatGPT API
    """
    # Specify the model and prompt for sentiment analysis
    model = 'gpt-3.5-turbo'
    prompt = 'This is a sentiment analysis task. The sentiment of the following text is:'

    # Create the chat completion prompt
    chat_prompt = f'{prompt}\n{text}\n---\n'

    # Generate a response using the ChatGPT API
    # implement 5 retries
    i_index = 0
    while i_index < 5:
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "system", "content": chat_prompt}],
                max_tokens=1,
                temperature=0.0
            )
            break
        except Exception as e:
            print(f"Error in analyze_sentiment: {e}")
            i_index += 1
            continue

    # Extract the sentiment from the response
    sentiment = response.choices[0].message.content.strip()

    return sentiment

def get_sentiment(text):
    """
    Get the sentiment of a text using the ChatGPT API
    """
    sentiment_result = analyze_sentiment(text)
    sentiment_result = sentiment_result.upper()
    if sentiment_result == "POSITIVE":
        return {
            "Sentiment": 1.0
        }
    elif sentiment_result == "NEUTRAL":
        return {
            "Sentiment": 0.0
        }
    elif sentiment_result == "NEGATIVE":
        return {
            "Sentiment": -1.0
        }
    else:
        return {
            "Sentiment": 0.0
        }
