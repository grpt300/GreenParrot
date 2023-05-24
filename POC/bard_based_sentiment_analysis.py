from google.cloud import language

def analyze_sentiment(text_content):
    """
    Analyzing Sentiment in a String

    Args:
      text_content The text content to analyze
    """

    client = language.LanguageServiceClient()

    document = language.Document(content=text_content, type_=language.Document.Type.PLAIN_TEXT)

    response = client.analyze_sentiment(document=document)

    # Get overall sentiment of the input document
    print(u"Document sentiment score: {}".format(response.document_sentiment.score))
    print(
        u"Document sentiment magnitude: {}".format(
            response.document_sentiment.magnitude
        )
    )

# The text to analyze
text_content = "C3.ai Stock Rises on Earnings Update. Demand Is ‘Just Exploding’ for Enterprise AI, CEO Says"
analyze_sentiment(text_content)

# [END language_sentiment_text]