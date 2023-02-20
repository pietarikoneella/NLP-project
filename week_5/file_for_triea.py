import nltk
from nltk.stem import PorterStemmer
from nltk import word_tokenize
#nltk.download('punkt')
import pke
import re
import numpy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import matplotlib.pyplot as plt

extractor = pke.unsupervised.TopicRank()

def index_documents_from_text_file(filename):
    """ This function first opens a file, reads its contents
        into a string and closes the file. Then it creates and returns a list
        of every item consisiting of an article title and the article text itself
    """
    document_string = ""
    
    # Opening the file, storing the contents of the article into one string, closing the file
    try:
        input_file = open(filename, "r", encoding = 'utf8')    
        for line in input_file:
            line = line.strip()
            document_string += line + " "
        input_file.close()

    except FileNotFoundError:
        print(f"File was not found.")
    except OSError:
        print(f"Something went wrong reading the file.")
    except:
        print("Something went wrong.")
    
    title_list = re.findall(r"\<article name\=\"([\w\s\d\.\,\(\)\?\!]*)\"\>", document_string)
    article_content_string = re.sub(r"\<article name\=\"[\w\s\d\.\,\(\)\?\!]*\"\>", "",  document_string)
    content_list = article_content_string.strip().split("</article>")
    # Combining the article titles and contents into a list 
    # The three stars are added in between to aid in separating the article title from the body text
    article_and_title_list = []
    for i in range(len(title_list)):
        article_and_title_list.append(title_list[i] + " *** " + content_list[i])
    
    return article_and_title_list

def get_all_titles():
    document_string = ""
    
    # Opening the file, storing the contents of the article into one string, closing the file
    try:
        input_file = open("articles.txt", "r", encoding = 'utf8')    
        for line in input_file:
            line = line.strip()
            document_string += line + " "
        input_file.close()

    except FileNotFoundError:
        print(f"File was not found.")
    except OSError:
        print(f"Something went wrong reading the file.")
    except:
        print("Something went wrong.")
    
    title_list = re.findall(r"\<article name\=\"([\w\s\d\.\,\(\)\?\!]*)\"\>", document_string)
    print(title_list)
    return title_list

get_all_titles()
