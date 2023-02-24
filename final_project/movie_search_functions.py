import nltk
from nltk.stem import PorterStemmer
from nltk import word_tokenize
#nltk.download('punkt')
import pke
import numpy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import matplotlib.pyplot as plt

def this_is_movie_search():
    message = "NLP is great!"
    return message