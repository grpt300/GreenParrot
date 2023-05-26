import numpy as np
from keras.layers import Dense, Embedding, LSTM
from keras.models import Sequential
from keras.preprocessing import sequence
from keras.utils import np_utils, pad_sequences
from nltk.corpus import treebank
import nltk
import os
import pickle

# Load the Stanford Sentiment Treebank dataset
os.environ['SSL_CERT_FILE'] = 'cacert.pem'
nltk.download('treebank')
tagged_sents = treebank.tagged_sents(tagset='universal')[:750]
data = []

# implemented the for loop to iterate through the tagged_sents
tagged_index = 0
tagged_length = len(tagged_sents)
while(tagged_length > tagged_index):
    sentence = tagged_sents[tagged_index]
    tokenized_sentence = [word.lower() for word, tag in sentence]
    tags = [tag for word, tag in sentence]
    data.append((tokenized_sentence, tags))
    tagged_index += 1

# Define the vocabulary size and maximum sequence length
vocab_size = 2000
max_len = 100

# Create a dictionary of word frequency counts and use it to generate an index for each word
word_counts = {}
for words,_ in data:
    for word in words:
        if word not in word_counts:
            word_counts[word] = 1
        else:
            word_counts[word] += 1
word_index = {word: i + 1 for i, (word, _) in enumerate(sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:vocab_size])}

X = [[word_index.get(word, 0) for word in words][:92] for words, _ in data]
X = pad_sequences(X, maxlen=92)
Y = [[1 if tag == 'pos' else 0 for tag in tags] for _, tags in data]
max_len = max(len(sublist) for sublist in Y)
Y_padded = pad_sequences(Y, maxlen=max_len, padding='post')
Y_array = np.array(Y_padded)
Y_onehot = np_utils.to_categorical(Y_array, num_classes=2)
Y_onehot = np.reshape(Y_onehot, (-1, 2))

print("X:", X)
print("Y:", Y_onehot)

# Define the LSTM model
model = Sequential()
model.add(Embedding(vocab_size + 1, 128, input_length=max_len))
model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(2, activation='softmax'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X, Y_onehot, epochs=10, batch_size=32, validation_split=0.2)

# Save the model into a pickle file
with open('sentiment_analysis_model_750.pkl', 'wb') as f:
    pickle.dump(model, f)