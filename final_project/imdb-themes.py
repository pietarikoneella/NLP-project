import re
import pke
import spacy
nlp = spacy.load('en_core_web_sm')
extractor = pke.unsupervised.TopicRank()



#create file without names
file_no_names = open("synopsis_no_names.txt", "w")
file = open("synopses.txt", "r")
text = file.read()
text = nlp(text)
tag = ["PROPN"]
for token in text:
    if token.pos_  not in tag:
        file_no_names.write(token.text)
        file_no_names.write(" ")
file.close()
file_no_names.close()

# get synopsis
file = open("synopsis_no_names.txt", "r")
text = file.read()
synopses = re.findall(r"< synopsis >(.+)<\/synopsis > ", text)
print("getting synopsis")
file.close()

# extract themes
file = open("synopsis_themes.txt", "w")
for synopsis in synopses:
    extractor.load_document(synopsis, language='en')
    extractor.candidate_selection()
    extractor.candidate_weighting()
    number_of_themes = 10 #int(input("How many themes would you like? "))
    keyphrases = extractor.get_n_best(n=number_of_themes)
    for theme in keyphrases:
        file.write(str(theme[1]) + " " + theme[0] + "\n")
    file.write("\n")
print("themes are extracted")
file.close()
