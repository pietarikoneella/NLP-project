import re
import pke
extractor = pke.unsupervised.TopicRank()
import spacy
nlp = spacy.load('en_core_web_sm')
nlp.max_length = 3000000 



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
file = open("synopsis_no_names.txt", "r", encoding = "ISO-8859-1")
text = file.read()
synopsis_tuples = re.findall(r"(< synopsis ?>|< Pianist \"|< , \"|< 's|< ,)(.+)(<\/synopsis )?> ", text)
synopses = []
for i in synopsis_tuples:
    synopses.append(i[1])
print("getting synopsis")
file.close()

# extract themes
file = open("synopsis_themes.txt", "w")
i = 0
for synopsis in synopses:
    extractor.load_document(synopsis, language='en')
    extractor.candidate_selection()
    extractor.candidate_weighting()
    number_of_themes = 10 #int(input("How many themes would you like? "))
    keyphrases = extractor.get_n_best(n=number_of_themes)
    for theme in keyphrases:
        file.write(str(theme[1]) + " " + theme[0] + "\n")
    file.write("\n")
    i += 1
    print(i, "synopses processed.")
file.close()
