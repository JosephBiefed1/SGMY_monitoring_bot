import pandas as pd
#import joblib
#from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.linear_model import LogisticRegression
import nltk
from nltk.corpus import stopwords
import os
import spacy
# Load stop words
stop_words = set(stopwords.words('english'))




# Download necessary NLTK data (only required once)
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
from transformers import pipeline

import re

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

def contains_around_specific_range(sentence):
    # Matches "around" followed by a number between 1 and 20
    pattern = r"\b(around|about|abt|than|then)\s([1-9]|1[0-4]|15)\b"  # Matches "around" + 1 to 20
    return bool(re.search(pattern, sentence))

def remove_words(message):
    words = ['wah', 'sia', 'loh', 'lorh', 'omg', 'chey','leh', 'la','lah','damn','ah']
    for word in words:
        message = message.replace(word, '')
    return message

nlp = spacy.load("en_core_web_sm")

def is_question_nlp(text):
    doc = nlp(text)
    for token in doc:
        if token.dep_ == "aux" and token.head.pos_ == "VERB":
            return True
    return text.endswith("?")

# Load zero-shot classification model
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
def split_words(lst):
    output = []
    for word in lst:
        output.extend(word.split())
    
    return list(map(lambda x: x.lower(), output))

needed_locations = ['sg', 'traffic', 'bus', 'car', 'taxi', 'taxis', 'grab', 'checkpoint', 'custom','ica', 'checkpoint', 'egate', 'immigration','imigration', 'queue', 'road','gate']

def extract_nouns_and_phrases(sentence):
    # Tokenize and tag parts of speech
    words = nltk.word_tokenize(sentence)
    pos_tags = nltk.pos_tag(words)

    # Define grammar for noun phrases
    grammar = r"""
        NP: {<DT>?<JJ>*<NN.*>}  # Noun phrase with optional determiner and adjectives
        N: {<NN.*>}             # Standalone nouns
    """

    # Use chunk parser
    chunk_parser = nltk.RegexpParser(grammar)
    tree = chunk_parser.parse(pos_tags)

    # Extract nouns and noun phrases
    nouns_and_phrases = []
    for subtree in tree:
        if isinstance(subtree, nltk.Tree):  # If it's a noun phrase
            phrase = " ".join(word for word, tag in subtree.leaves())
            nouns_and_phrases.append(phrase)
        else:  # Standalone nouns
            word, tag = subtree
            if tag.startswith('NN'):  # Filter for noun tags
                nouns_and_phrases.append(word)
    
    return split_words(nouns_and_phrases)
def classify_message(text):
    text = remove_words(text)
    noun_phrases = extract_nouns_and_phrases(text)
    if not is_question_nlp(text):
        labels = [2, 1]

        # Classify
        result = classifier(text, candidate_labels=labels) if text else {'labels': [0]}
        return(1 if contains_around_specific_range(text) else result['labels'][0])
    else:
        return 0

