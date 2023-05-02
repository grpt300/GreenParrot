from gensim import corpora, models
from POC.topic_mining import preprocess_corpus
from POC.TopicCatagorizer import get_categories

def perform_topic_extractor(corpus):
    try:
        # Step 1 (preprocess corpus as needed)
        corpus = preprocess_corpus(corpus)

        # Step 2: Create dictionary and bag-of-words representation
        dictionary = corpora.Dictionary(corpus)
        corpus_bow = [dictionary.doc2bow(doc) for doc in corpus]

        # Step 3: Train LDA model
        num_topics = 5  # set number of topics
        lda_model = models.LdaModel(corpus_bow, num_topics=num_topics, id2word=dictionary, passes=10)

        # Step 4: Interpret LDA model output
        topic_categories = []
        for i in range(num_topics):
            topic_words = lda_model.show_topic(i, topn=10)  # get top 10 words for topic i
            topic_words_csv = "|".join([word for word, _ in topic_words])
            category_words_csv = "|".join(['|'.join(get_categories(word)) for word, _ in topic_words])
            prefix_topic_index = f"Topic {i}"
            topic_categories.append(f"Index-{prefix_topic_index}:Topic-{topic_words_csv}:Category-{category_words_csv}")
        topic_categories_csv = ":::".join(topic_categories)


        # Step 5: Get topic distribution for new document
        topic_probs_list = [lda_model.get_document_topics(doc, minimum_probability=0.0) for doc in corpus_bow]
        topic_probs_csv = ":::".join([",".join([f"{topic_id}:{prob}" for topic_id, prob in topic_probs]) for topic_probs in topic_probs_list])

        # Step 6 : Put both topic_probs_csv and topic_categories_csv in a dictionary
        topic_extractor_dict = {
            "Topic_probs_csv": topic_probs_csv,
            "Topic_categories_csv": topic_categories_csv
        }

        return topic_extractor_dict
    except Exception as e:
        print(f"Error in perform_topic_extractor: {e}")
        return {"topic_probs_csv": "", "topic_categories_csv": ""}