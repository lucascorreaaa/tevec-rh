import numpy as np
from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Dropout, Embedding, LSTM, Bidirectional
import os
import sys
import pickle

def  main():
    # Reading input text from user and transforming to input into the model
    input_text = list(sys.argv[1])
    tokenizer = Tokenizer(num_words=2000, split=' ')
    input_text = tokenizer.texts_to_sequences(input_text)
    input_text = pad_sequences(input_text, maxlen=100, dtype='int32', value=0)
    print('input_text: ',input_text)
    
    # Loading Bidirectional LSTM Model
    filename = 'lstm_model.sav'
    model = pickle.load(open(filename, 'rb'))
    sentiment = model.predict(input_text, batch_size=1, verbose=2)[0]
    if(np.argmax(sentiment) == 0):
        print("negative")
        print(model.summary())
    elif (np.argmax(sentiment) == 1):
        print("positive")

if __name__ == "__main__":
    main()