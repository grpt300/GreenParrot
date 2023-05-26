import openai
import os

openai.api_key = os.environ.get('OPENAI_API_KEY')

def analyze_sentiment(text):
    # Specify the model and prompt for sentiment analysis
    model = 'gpt-3.5-turbo'
    prompt = 'This is a sentiment analysis task. The sentiment of the following text is:'

    # Create the chat completion prompt
    chat_prompt = f'{prompt}\n{text}\n---\n'

    # Generate a response using the ChatGPT API
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "system", "content": chat_prompt}],
        max_tokens=1,
        temperature=0.0
    )

    # Extract the sentiment from the response
    sentiment = response.choices[0].message.content.strip()

    return sentiment

# Example usage
text_to_analyze = "'A sign of trouble?' Why more Americans are missing their debt payments."
sentiment_result = analyze_sentiment(text_to_analyze)
print(f"The sentiment of the text is: {sentiment_result}")
